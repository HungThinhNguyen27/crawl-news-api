
import jwt
from datalayer import ArticleMysql
from flask import Flask, jsonify, Blueprint, session,  redirect, url_for
from article_service import ArticleService , user
from config import Config
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config.from_object(Config)

article = Blueprint('article',__name__)
article_service = ArticleService() 
user = user()
db = ArticleMysql()

@article.route('/')
def home():
    return jsonify({'Message':"This is Home page"})

@article.route('/articles', methods=['GET'])
@jwt_required()
def get_all_articles():
    articles = article_service.get_all_articles()
    return articles

@article.route('/articles/<int:id>', methods=['GET']) 
@jwt_required()
def get_article_by_id(id):
   return article_service.get_article_by_id(id)

@article.route('/articles/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_article_by_id(id):
    return article_service.delete_article_by_id(id)
   
@article.route('/login', methods=['POST'])
def login():
    return user.login()

@article.route('/logout', methods=['POST'])
def log_out():
    session.pop('user', None)
    return redirect(url_for('article.home'))

@article.route('/create', methods=['POST'])
def create_user():
    return user.create_user()
