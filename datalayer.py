from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model import Base, news, category, user


SECRET_KEY = Config.SECRET_KEY
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB


class ArticleMysql:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}",
            echo=False,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_all_articles(self, query, limit, offset):
        if query:
            articles = (
                self.session.query(news)
                .filter(news.title.contains(query))
                .limit(limit)
                .offset(offset)
                .all()
            )
            total_count = (
                self.session.query(func.count(news.id))
                .filter(news.title.contains(query))
                .scalar()
            )
        else:
            articles = self.session.query(news).limit(limit).offset(offset).all()
            total_count = self.session.query(func.count(news.id)).scalar()

        return articles, total_count

    def get_article_by_id(self, id):
        article = self.session.query(news).filter_by(id=id).first()
        return article

    def delete_article_by_id(self, article):
        self.session.delete(article)
        self.session.commit()

    def check_existing_src_article(self, url):
        """
        Create a new article for crawling
        """
        existing_article = self.session.query(category).filter_by(url=url).first()

        self.session.commit()
        return existing_article

    def add_new_src_articles(self, new_src_article):
        article_new = self.session.add(new_src_article)
        self.session.commit()
        return article_new


class UserMysql:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}",
            echo=False,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def user_check_login(self, username, password):
        user_check = (
            self.session.query(user)
            .filter_by(username=username, password=password)
            .first()
        )
        self.session.commit()
        return user_check

    def user_check_role(self, current_user):
        user_check = self.session.query(user).filter_by(username=current_user).first()

        if user_check and user_check.role:
            return user_check
        else:
            return None

    def existing_user(self, username):
        user_check = self.session.query(user).filter_by(username=username).first()
        self.session.commit()
        return user_check

    def add_user(self, new_user):
        user_new = self.session.add(new_user)
        self.session.commit()

        return user_new


class CrawlDataMysql:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}",
            echo=False,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def detect_duplicate(self, hash):
        count = (
            self.session.query(func.count(news.id)).filter(news.hash == hash).scalar()
        )
        return count > 0

    def add_new_post(self, new_post_template):
        new_post = self.session.add(new_post_template)
        self.session.commit()
        return new_post

    def query_all_src_news(self):
        cats = self.session.query(category).all()
        return cats

    def query_url_src_news(self, url):
        url_src = self.session.query(category).filter_by(url=url).first()
        self.session.commit()
        return url_src

    def commit(self):
        commit = self.session.commit()
        return commit
