"""
Module that provides database models for articles, categories, and users.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Index,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


import sqlalchemy

Base = sqlalchemy.orm.declarative_base()


class News(Base):
    """Class representing news table."""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    img_links = Column(String, nullable=False)
    content = Column(Text)
    original_url = Column(String(255))
    category_id = Column(Integer, ForeignKey("category_news.id"))
    hash = Column(Text)
    category = relationship("Category", back_populates="articles")

    __table_args__ = (
        Index("category_idx", category_id),
        Index("title", "content", mysql_length={"title": 255, "content": "longtext"}),
        {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_general_ci",
        },
    )


class Category(Base):
    """Class representing category_news table."""

    __tablename__ = "category_news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    articles = relationship("News", back_populates="category")


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


class ArticleOutput:
    def __init__(self, article):
        self.article = article

    def output(self):
        return {
            "id": self.article.id,
            "title": self.article.title,
            "img_links": self.article.img_links,
            "content": self.article.content,
            "original_url": self.article.original_url,
        }
