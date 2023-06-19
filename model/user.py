import sqlalchemy

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    """Class representing user table."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )
