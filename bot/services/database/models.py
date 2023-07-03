from sqlalchemy import (
    Column,
    BigInteger,
    Text, String,
    Boolean,
    ForeignKey,
    Float
)

from sqlalchemy import select, delete
from sqlalchemy.orm import relationship

from .database import Base
from .entities import UserMixin


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    lang = Column(String(3), default=None, nullable=True)

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
    
    @classmethod
    async def get(cls, s, user_id) -> UserMixin:
        stmt = select(cls).where(cls.id == user_id)
        result = await s.execute(stmt)
        result = result.scalars().one_or_none()

        return result
    
    @classmethod
    async def update(cls, s, user):
        stmt = select(cls).where(cls.id == user.id)
        result = await s.execute(stmt)
        result = result.scalars().one_or_none()
        result.lang = user.lang
        await s.commit()


    @classmethod
    async def delete(cls, s, user_id):
        stmt = delete(cls).where(cls.id == user_id)
        print(stmt, user_id)
        try:
            await s.execute(stmt)

            await s.commit()
        except Exception as e:
            print(e)

class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(BigInteger, ForeignKey("categories.id"), nullable=True)
    
    parent = relationship(
                "Category",
                remote_side=[id],
                back_populates="children",
                passive_deletes="all",
                lazy="joined",
                join_depth=1,
                uselist=False,
            )
    children = relationship(
                "Category",
                remote_side=[parent_id],
                back_populates="parent",
                passive_deletes="all",
                lazy="joined",
                join_depth=1,
                uselist=True,
            )


class DesignTemplate(Base):
    __tablename__ = "design_templates"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    preview_image = Column(Text, nullable=False) # This could be a URL to the image
    is_free = Column(Boolean, nullable=False, default=False) # Indicates if the design is free or paid
    price = Column(Float, nullable=True) # Price for the template, if it's not free
    category_id = Column(BigInteger, ForeignKey("categories.id")) # FK to the Category

