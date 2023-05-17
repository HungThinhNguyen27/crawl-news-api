
from flask import Flask, jsonify, Blueprint, request, session
from flask_jwt_extended import jwt_required, unset_jwt_cookies

from article_service import article_service
from user_service import UserService
from config import Config
from functools import wraps
import jwt
from flask import g

app = Flask(__name__)
app.config.from_object(Config)

article = Blueprint('article', __name__)
article_service = article_service()
user_service = UserService()


def jwt_required_with_blacklist(func):
    @wraps(func)
    @jwt_required()
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.split(' ')[1]
            if token in blacklist:
                return jsonify({'message': 'Token revoked'}), 401  # Token đã bị thu hồi
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                # Tiếp tục xử lý tài nguyên được bảo vệ
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 401  # Token hết hạn
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401  # Token không hợp lệ
        else:
            return jsonify({'message': 'No token provided'}), 401  # Không có token
    return decorated



@article.route('/')
def home():
    """
    Home page
    """
    return jsonify({'Message': "This is Home page"})


@article.route('/articles', methods=['GET'])
@jwt_required_with_blacklist
def get_all_articles():
    articles = article_service.get_all_articles()
    return articles

@article.route('/articles/<int:id>', methods=['GET']) 
@jwt_required_with_blacklist
def get_article_by_id(id):
   return article_service.get_article_by_id(id)


@article.route('/articles/<int:id>', methods=['DELETE'])
@jwt_required_with_blacklist
def delete_article_by_id(id):
    return article_service.delete_article_by_id(id)


@article.route('/add-article', methods=['POST'])
@jwt_required_with_blacklist
def create_a_new_article():
    return article_service.create_a_new_article()


@article.route('/crawl-article', methods=['POST'])
@jwt_required_with_blacklist
def craw_an_article():
    return article_service.crawl_an_article()


@article.route('/login', methods=['POST'])
def login():
    return user_service.login()


@article.route('/create-user', methods=['POST'])
def create_user():
    return user_service.create_user()


blacklist = set()
@article.route('/logout', methods=['POST'])
def logout():

    token = request.headers.get('Authorization')
    if token:
        token = token.split(' ')[1]  
        blacklist.add(token)  
        return jsonify({'message': 'Log out success'}), 200
    else:
        return jsonify({'message': 'No token provided'}), 401
    


