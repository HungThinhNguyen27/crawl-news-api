from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.user import Base, User
from typing import List, Optional
from datalayer.database import Database



class UserMysql(Database):

    def get_by_username_password(self, username: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter_by(
            username=username, password=password).first()

        return user

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.session.query(
            User).filter_by(username=username).first()
        return user

    def add(self, user):
        self.session.add(user)
        self.session.commit()

    def user_check_role(self, current_user: str) -> Optional[User]: # xoa

        user_check = self.session.query(User).filter_by(
            username=current_user).first()

        if user_check and user_check.role:
            return user_check
        else:
            return None
