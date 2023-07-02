import asyncio, os
import logging

from pathlib import Path

from sqlalchemy.engine import URL

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import DialogRegistry

# Middlewares
from bot.middlewares.repo import RepoMiddleware
from bot.middlewares.user import RegisterMiddleware
from bot.middlewares.locale import LocaleMiddleware

# Routers
from bot.handlers.user import router as user_router

# Dialogs
from bot.dialogs.user import dialog as user_dialog

# Config
from bot.config import BotConfig

# Services
from bot.services.locale import (
    Localizator,
    LocaleLoader
)
from bot.services.database import create_pool

from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

BOTFOLDER = Path(__file__).parent


def _configure_fluent(locales_path):
    locales_map = {
        "ru": ("ru",),
    }
    loader = LocaleLoader(
        Path(locales_path),
    )
    return Localizator(loader, locales_map)


async def main():
    logger.warning("Starting bot")

    # print all env variables
    config = BotConfig(
        _env_file=BOTFOLDER / Path(".env")
    )

    storage = MemoryStorage()

    if config.redis_storage:
        print("Using redis storage")
        from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
        storage = RedisStorage.from_url(
            "redis://localhost",
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )


    bot = Bot(token=config.token)
    dp = Dispatcher(storage=storage)
    dsn = URL(
        drivername="mysql+aiomysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    database = await create_pool(db_url=dsn, echo=config.echo)

    # Router
    reg = DialogRegistry(dp)
    reg.register(user_dialog)

    dp.include_router(user_router)

    fluent = _configure_fluent(
        BOTFOLDER / Path("locales/")
    )

    # Middleware
    dp.update.outer_middleware.register(
        RepoMiddleware(db=database)
    )
    dp.callback_query.outer_middleware.register(
        RepoMiddleware(db=database)
    )
    dp.message.outer_middleware.register(
        RegisterMiddleware()
    )
    dp.callback_query.outer_middleware.register(
        RegisterMiddleware()
    )
    dp.message.outer_middleware.register(
        LocaleMiddleware(localizator=fluent)
    )
    dp.callback_query.outer_middleware.register(
        LocaleMiddleware(localizator=fluent)
    )

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli():
    """Wrapper for command line, app's entry point"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
