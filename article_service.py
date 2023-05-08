
import config
from datalayer import ArticleMysql, CrawlData
from flask import jsonify, request, url_for
from middleware import User_login, Manager

class ArticleService:

    def __init__(self) :
        self.user = ArticleMysql()
        self.crawdata = CrawlData()
        self.manager = Manager()

    def get_all_articles(self):
        return self.user.get_all_articles()

    def get_article_by_id(self, id):
        return self.user.search_article_by_id(id)
    
    def delete_article_by_id(self, id):
        return self.manager.delete_article_by_id(id)
    
    def article_crawling(self):
        return self.crawdata.run_everyday()

class user:

    def __init__(self) :
        self.user = User_login()

    def login(self):
        return self.user.login()
    
    def create_user(self):
        return self.user.create_user()

    def logout(self):
        return self.user.logout()
