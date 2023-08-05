

from datalayer.mysql_connect import MySqlConnect
from model.articles import Category
from typing import Optional, List


class Category_(MySqlConnect):

    def get(self) -> List[Category]:
        category = self.session.query(Category).all()
        return category

    def add(self, new_url_article: Category) -> None:
        self.session.add(new_url_article)
        self.session.commit()

    def get_by_url(self, url: str):
        category_news = self.session.query(
            Category).filter(Category.url == url).first
        return category_news
