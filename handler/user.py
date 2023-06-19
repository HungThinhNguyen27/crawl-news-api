from cachetools import TTLCache
import jwt
from config import Config
from functools import wraps
from service.user import UserService
from flask_jwt_extended import jwt_required
from service.article import ArticleService
from service.crawl_article import CrawlNewsService
from flask import Flask, jsonify, Blueprint, request, session
import time

app = Flask(__name__)
app.config.from_object(Config)
user_handler = Blueprint("user", __name__)
article_service = ArticleService()
middleware = UserService()
CrawlNews = CrawlNewsService()


def jwt_required_authentication(func):
    @wraps(func)
    @jwt_required()
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
            try:
                # Check the validity of the token
                user_obj = token_cache.get(token)
                if user_obj:
                    data = jwt.decode(
                        token, app.config["SECRET_KEY"], algorithms=["HS256"])
                    if data["exp"] < time.time():
                        return Response.token_expired()
                    if data["sub"] == user_obj.username:
                        return func(*args, **kwargs)
                else:
                    return Response.invalid_token()
            except jwt.ExpiredSignatureError:
                return Response.token_expired()
            except jwt.InvalidTokenError:
                return Response.invalid_token()
        else:
            return Response.no_token_provided()

    return decorated


@user_handler.route("/account", methods=["POST"])
def create_user():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    role = request.json.get("role")

    if role not in ["user", "manager"]:
        return Response.invalid_role(role)

    existing_user = middleware.create_user(username, password, email, role)

    if existing_user:
        return Response.username_already_exists(username)

    return Response.create_account_success(username)


token_cache = TTLCache(maxsize=100, ttl=3600)


@user_handler.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    token_user = middleware.login(username, password)

    if token_user is not None:
        token, user_obj = token_user
        if user_obj:
            # Store tokens in cache
            token_cache[token] = user_obj
            session["logged_in"] = True
            session["username"] = username
            return jsonify({"token": token}), 200
    else:
        return Response.invalid_username_or_password()


@user_handler.route("/logout", methods=["POST"])
@jwt_required_authentication
def logout():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        token_cache.pop(token, None)
        session.clear()
        return Response.log_out_success()
    else:
        return Response.no_token_provided()


class Response:
    @staticmethod
    def token_revoked():
        return jsonify({"message": "Token revoked"}), 401

    @staticmethod
    def token_expired():
        return jsonify({"message": "Token expired"}), 401

    @staticmethod
    def invalid_token():
        return jsonify({"message": "Please login again"}), 401

    @staticmethod
    def valid_token():
        return jsonify({"message": "valid token"}), 401

    @staticmethod
    def log_out_success():
        return jsonify({"message": "Log out success"}), 200

    @staticmethod
    def invalid_username_or_password():
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def username_already_exists():
        return jsonify({"error": "Username already exists"}), 400

    @staticmethod
    def invalid_role(role):
        return jsonify({"error": "Invalid {} role ".format(role)}), 400

    @staticmethod
    def create_account_success(username):
        return (
            jsonify({"message": "Account {} created successfully".format(username)}),
            201,
        )

    @staticmethod
    def username_already_exists(username):
        return jsonify({"message": "Username {} already exists".format(username)}), 201

    @staticmethod
    def no_token_provided():
        return jsonify({"error": "No token provided"}), 400
