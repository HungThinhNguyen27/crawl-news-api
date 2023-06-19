

from datalayer.database import Database
from model.articles import Category
from typing import Optional, List


class Category_(Database):

    def get_category(self) -> List[Category]:
        all_src_news = self.session.query(Category).all()
        return all_src_news

    def get_category_url(self, url: str) -> Optional[Category]:
        Category_url_news = self.session.query(
            Category).filter(Category.url == url).first()
        return Category_url_news

    def add(self, new_src_article):
        article_new = self.session.add(new_src_article)
        self.session.commit()
        return article_new
