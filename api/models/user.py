import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, validates
from sqlalchemy_utils import UUIDType

from database import Base


class User(Base):
    __tablename__ = "users"
    username = Column(String(length=256), primary_key=True)
    hashed_password = Column(String(length=128))
    
    @validates("username")
    def validate_username(self, key, value):
        if value is None:
            raise ValueError("Value must not be None")

        return value