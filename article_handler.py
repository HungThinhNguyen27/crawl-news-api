
from flask import Flask, jsonify, Blueprint, request, session
from flask_jwt_extended import jwt_required, unset_jwt_cookies

from article_service import article_service
from user_service import UserService
from config import Config
from functools import wraps
import jwt


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
                return Response.token_revoked()
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return Response.token_expired()
            except jwt.InvalidTokenError:
                return Response.invalid_token()
        else:
            return Response.no_token_provided()
    return decorated


@article.route('/')
def home():
    """
    Home page
    """
    return Response.home_page()


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
        return Response.log_out_success()
    else:
        return Response.no_token_provided()
    


class Response:

    @staticmethod
    def token_revoked():
        return jsonify({'message':'Token revoked'}), 401
    
    @staticmethod
    def token_expired():
        return jsonify({'message':'Token expired'}), 401
    
    @staticmethod
    def invalid_token():
        return jsonify({'message':'Invalid token'}), 401
    
    @staticmethod
    def no_token_provided():
        return jsonify({'message':'No token provided'}), 401
    
    @staticmethod
    def log_out_success():
        return jsonify({'message': 'Log out success'}), 200

    @staticmethod
    def home_page():
        return jsonify({'Message': "This is Home page"}), 200
    
    @staticmethod
    def authorization():
        return jsonify({"Message": "you do not have access to this resource."}), 403
    
    @staticmethod
    def invalid_page_number():
        return jsonify({"message": "Invalid page number"}), 400

    @staticmethod
    def page_doesnt_exist():
        return jsonify({"message": "This page does not exist"}), 400
    
    @staticmethod
    def invalid_limit_number():
        return jsonify({"message": "Invalid limit number"}), 400
    
    @staticmethod
    def invalid_username_or_password():
        return jsonify({'error': 'Invalid username or password'}), 401
    
    @staticmethod
    def username_already_exists():
        return jsonify({'error': 'Username already exists'}), 400
    
    @staticmethod
    def invalid_role():
        return jsonify({'error': 'Invalid role'}), 400

    @staticmethod
    def user_created():
        return jsonify({'message': 'User created successfully'}), 201

    @staticmethod
    def article_not_found():
        return jsonify({'message': 'Article not found'}), 404
    
    @staticmethod
    def existing_article():
        return jsonify({'error': 'Articles already exists'}), 400
    
    @staticmethod
    def Invalid_URL_format():
        return jsonify({'error': 'Invalid URL format'}), 400
    
    @staticmethod
    def article_crawling():
        return jsonify({'message': 'Article crawling......'}), 200