# export PYTHONPATH=$PYTHONPATH:/Users/macos/Downloads/WORKSPACE/NewsCrawlerAPI/model

from config import Config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.articles_model import Base, News, Category
from typing import List, Optional
from elasticsearch import Elasticsearch


SECRET_KEY = Config.SECRET_KEY
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB


class Database:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}",
            echo=False,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])


class ArticleMysql(Database):
    def get_all_articles(self) -> List[News]:
        all_articles = self.session.query(News).all()
        return all_articles

    def get_articles_by_keywords(self, query: str) -> List[News]:
        first_articles = (
            self.session.query(News)
            .filter(News.title.contains(query))
            .all()
        )
        return first_articles

    def get_articles_by_id(self, id: int) -> Optional[News]:
        id_articles = self.session.query(News).filter_by(id=id).first()
        return id_articles

    def get_hash_article(self, hash: str) -> Optional[News]:
        hash_article = self.session.query(News).filter_by(hash=hash).first()
        return hash_article

    def delete_article_by_id(self, id: int) -> None:
        self.session.delete(id)
        self.session.commit()

    def add_news(self, news: News) -> None:
        article_new = self.session.add(news)
        self.session.commit()
        return article_new

    def get_category(self) -> List[Category]:
        all_src_news = self.session.query(Category).all()
        return all_src_news

    def get_category_url(self, url: str) -> Optional[Category]:
        Category_url_news = self.session.query(
            Category).filter_by(url=url).first()
        return Category_url_news

    def add_new_src_articles(self, new_src_article):
        article_new = self.session.add(new_src_article)
        self.session.commit()
        return article_new

    def add_news_to_elasticsearch(self, news: News) -> None:
        body = {
            "title": news.title,
            "content": news.content,
            "img_links": news.img_links,
            "original_url": news.original_url,
        }
        self.es.index(index="news", body=body)
