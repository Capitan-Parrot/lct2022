from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default='USER')
    hashed_password = Column(String)
    work_counter = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)


class RegisterRequest(Base):
    __tablename__ = "register_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    email = Column(String, unique=True, index=True)