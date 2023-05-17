
import config
from datalayer import ArticleMysql, crawl_data
from flask import jsonify, request, url_for
from flask_jwt_extended import get_jwt_identity
from model import user


class article_service():
    
    def __init__(self):
        self.datalayer = ArticleMysql()
        self.crawdata = crawl_data()

    def get_all_articles(self):
        return self.datalayer.get_all_articles()

    def get_article_by_id(self, id):
        return self.datalayer.search_article_by_id(id)

    def delete_article_by_id(self, id):
        
        current_user = get_jwt_identity()
        user_check = self.datalayer.session.query(user)\
            .filter_by(username=current_user)\
            .first()
        self.datalayer.session.commit()
        if user_check.role == 'manager':
            articles = self.datalayer.delete_article_by_id(id)
            return articles
        else:
            return jsonify(
                {"Message": "you do not have access to this resource."}), 403
        


    def article_crawling(self):
        return self.crawdata.run_everyday()

    def create_a_new_article(self):
        current_user = get_jwt_identity()
        user_check = self.datalayer.session.query(user)\
            .filter_by(username=current_user)\
            .first()
        self.datalayer.session.commit()
        if user_check.role == 'manager':
            articles = self.crawdata.create_article()
            return articles
        else:
            return jsonify(
                {"Message": "you do not have access to this resource."}), 403

    def crawl_an_article(self):
        current_user = get_jwt_identity()
        user_check = self.datalayer.session.query(user)\
            .filter_by(username=current_user)\
            .first()
        self.datalayer.session.commit()
        if user_check.role == 'manager':
            articles = self.crawdata.crawl_article()
            return articles
        else:
            return jsonify(
                {"Message": "you don't have access ."}), 403

    
    
    