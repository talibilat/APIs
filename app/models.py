from turtle import title
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(String, server_default="True", nullable=True)
    created_at= Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))