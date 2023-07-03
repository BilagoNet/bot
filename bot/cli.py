import asyncio, os
import logging

from pathlib import Path

from sqlalchemy.engine import URL

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder


from aiogram_dialog import DialogRegistry
from bot.filters.LangFilter import LangFilter

# Middlewares
from bot.middlewares.repo import RepoMiddleware
from bot.middlewares.user import RegisterMiddleware
from bot.middlewares.locale import LocaleMiddleware

# Routers
from bot.handlers.user import router as user_router
from bot.handlers.not_selected_lang import router as lang_router

# Dialogs
from bot.dialogs.user import dialog as user_dialog

# Config
from bot.config import BotConfig

# Services
from bot.services.locale import (
    Localizator,
    LocaleLoader
)
from bot.services.database import create_pool, create_engine

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
        "uz": ("uz",),
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
    
    engine = await create_engine(db_url=dsn, echo=config.echo)
    database = await create_pool(engine)

    dp.include_router(lang_router)
    
    # Router
    reg = DialogRegistry(dp)
    reg.register(user_dialog)
    
    
    user_router.message.filter(LangFilter(lang=True))

    dp.include_router(user_router)


    # Middleware
    dp.message.outer_middleware.register(
        RegisterMiddleware()
    )
    dp.callback_query.outer_middleware.register(
        RegisterMiddleware()
    )
    
    dp.update.outer_middleware.register(
        RepoMiddleware(db=database)
    )
    dp.callback_query.outer_middleware.register(
        RepoMiddleware(db=database)
    )
    
    fluent = _configure_fluent(
        BOTFOLDER / Path("locales/")
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
    except:
        pass
    finally:
        # await storage.redis.flushdb(asynchronous=True)
        await storage.close()
        await bot.session.close()
        await dp.storage.close()
        await engine.dispose()

def cli():
    """Wrapper for command line, app's entry point"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")



if __name__ == '__main__':
    cli()
