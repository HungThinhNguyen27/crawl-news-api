from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.articles_model import Base, News, Category
from typing import List, Optional
from elasticsearch import Elasticsearch
import uuid

SECRET_KEY = Config.SECRET_KEY
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB


class Database:
    def __init__(self) -> None:
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}",
            echo=False,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])


class CrawlDataMysql(Database):
    def query_hash(self, hash: str) -> bool:
        count = (
            self.session.query(func.count(News.id)).filter(
                News.hash == hash).scalar()
        )
        return count > 0

    # def add_new_post(self, new_post_template: News) -> None:
    #     new_post = self.session.add(new_post_template)
    #     self.session.commit()
    #     return new_post

    def query_all_src_news(self) -> List[Category]:
        cats = self.session.query(Category).all()
        return cats

    def query_url_src_news(self, url) -> Optional[Category]:
        url_src = self.session.query(Category).filter_by(url=url).first()
        return url_src

    def commit(self) -> None:
        commit = self.session.commit()
        return commit

    def add_new_post(self, news: News) -> None:
        body = {
            "id": id,
            "title": news.title,
            "content": news.content,
            "img_links": news.img_links,
            "original_url": news.original_url,
        }
        self.es.index(index="articles", body=body)
