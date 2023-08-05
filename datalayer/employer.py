from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from model.employer import Base, User
from typing import List, Optional
from datalayer.mysql_connect import MySqlConnect


class Employer(MySqlConnect):

    def add(self, user: str) -> None:
        self.session.add(user)
        self.session.commit()

    def get_by_id(self, id: int) -> Optional[User]:
        employer = self.session.query(User).filter(User.id == id).first()
        return employer

    def remove(self, id: str) -> None:
        self.session.delete(id)
        self.session.commit()

    def get(self) -> List[User]:
        users = self.session.query(User).all()
        return users

    def update_user_info(self, user: User, new_info: dict):
        for key, value in new_info.items():
            setattr(user, key, value)

        self.session.commit()
