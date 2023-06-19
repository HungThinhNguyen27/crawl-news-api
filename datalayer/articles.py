# export PYTHONPATH=$PYTHONPATH:/Users/macos/Downloads/WORKSPACE/NewsCrawlerAPI/model

from config import Config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.articles import Base, News, Category
from typing import List, Optional, Tuple
from elasticsearch import Elasticsearch
from datalayer.database import Database


class Article(Database):

    def search(self, query: Optional[str], limit: int, offset: int) -> Tuple[List[News], int]:
        articles_query = self.session.query(News)
        total_count = self.get_total_count()

        if query:
            articles_query = articles_query.filter(News.title.contains(query))
            total_count = self.get_total_count(query)

        articles = articles_query.limit(limit).offset(offset).all()
        return articles, total_count

    def get_total_count(self, query: Optional[str] = None) -> int:
        if query:
            total_count_query = self.session.query(func.count(News.id)).filter(
                News.title.contains(query))

        else:
            total_count_query = self.session.query(func.count(News.id))
        total_count = total_count_query.scalar()
        return total_count

    def get(self, id: int) -> Optional[News]:
        id_articles = self.session.query(News).filter(News.id == id).first()
        return id_articles

    def delete(self, id: int) -> None:
        self.session.delete(id)
        self.commit()

    def add(self, news: News) -> None:
        article_new = self.session.add(news)
        self.session.commit()
        return article_new

    def commit(self) -> None:
        self.session.commit()

    def get_hash(self, hash: str) -> bool:
        count = self.session.query(func.count(News.id)).filter(
            News.hash == hash).scalar()

        return count > 0
