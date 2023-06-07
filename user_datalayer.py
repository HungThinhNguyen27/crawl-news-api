from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model import Base, User
from typing import List, Optional


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


class UserMysql(Database):
    def get_username_password(self, username: str, password: str) -> Optional[User]:
        get_username_password = (
            self.session.query(User)
            .filter_by(username=username, password=password)
            .first()
        )
        return get_username_password

    def get_username(self, username: str) -> Optional[User]:
        get_username = self.session.query(User).filter_by(username=username).first()
        return get_username

    def add_user(self, user):
        user_add = self.session.add(user)
        self.session.commit()

        return user_add

    def user_check_role(self, current_user: str) -> Optional[User]:
        user_check = self.session.query(User).filter_by(username=current_user).first()

        if user_check and user_check.role:
            return user_check
        else:
            return None
