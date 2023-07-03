from sqlalchemy import (
    Column,
    BigInteger,
    Text
)

from sqlalchemy import select

from .database import Base
from .entities import UserMixin


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=True)
    nickname = Column(Text, nullable=True)
    lang = Column(Text, nullable=False)

    @classmethod
    async def create(cls, s, user):
        s.add(user)
        await s.commit()

    @classmethod
    async def is_exists(cls, s, user):
        stmt = select(cls).where(cls.id == user.id)
        result = await s.execute(stmt)
        result = result.scalars().one_or_none()

        return bool(result)
