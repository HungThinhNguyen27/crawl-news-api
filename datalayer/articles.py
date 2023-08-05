# export PYTHONPATH=$PYTHONPATH:/Users/macos/Downloads/WORKSPACE/NewsCrawlerAPI/model

from config import Config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.articles import Base, News, Category
from typing import List, Optional, Tuple
from elasticsearch import Elasticsearch
from datalayer.mysql_connect import MySqlConnect
# cách dặt tên hàm V + O(mô tả động từ )


class Article(MySqlConnect):

    def search(self, query: Optional[str], limit: int, offset: int) -> Tuple[List[News]]:
        articles_query = self.session.query(News)

        if query:
            articles_query = articles_query.filter(News.title.contains(query))

        articles = articles_query.limit(limit).offset(offset).all()
        return articles

    def count(self, query: Optional[str]) -> int:
        if query:
            total_count_query = self.session.query(func.count(News.id)).filter(
                News.title.contains(query))

        else:
            total_count_query = self.session.query(func.count(News.id))
        total_count = total_count_query.scalar()
        return total_count

    def get(self) -> List[News]:
        articles = self.session.query(News).all()
        return articles

    def get_by_id(self, id: int) -> Optional[News]:
        article = self.session.query(News).filter(News.id == id).first()
        return article

    def delete(self, id: int) -> None:
        self.session.delete(id)
        self.commit()

    def add(self, news: News) -> None:
        self.session.add(news)
        self.session.commit()

    def commit(self) -> None:
        self.session.commit()
