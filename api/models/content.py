import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from database import Base


class Content(Base):
    __tablename__ = "contents"
    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=256), unique=True, nullable=False)


class ContentDependencies(Base):
    __tablename__ = "contents_dependencies"
    content_uuid = Column(UUIDType(binary=False), ForeignKey("contents.uuid"), primary_key=True, nullable=False)
    dependencies_uuid = Column(UUIDType(binary=False), ForeignKey("contents.uuid"), primary_key=True, nullable=False)