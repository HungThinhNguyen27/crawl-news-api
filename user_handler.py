import jwt
from config import Config
from functools import wraps
from user_service import UserService
from flask_jwt_extended import jwt_required
from article_service import ArticleService
from crawl_article_service import CrawlNewsService
from flask import Flask, jsonify, Blueprint, request

app = Flask(__name__)
app.config.from_object(Config)
user_handler = Blueprint("user", __name__)
article_service = ArticleService()
middleware = UserService()
CrawlNews = CrawlNewsService()


def jwt_required_with_blacklist(func):
    @wraps(func)
    @jwt_required()
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
            if token in blacklist:
                return Response.token_revoked()
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return Response.token_expired()
            except jwt.InvalidTokenError:
                return Response.invalid_token()
        else:
            return Response.no_token_provided()

    return decorated


@user_handler.route("/account", methods=["POST"])
@jwt_required_with_blacklist
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


@user_handler.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    token_user = middleware.login(username, password)

    if token_user is not None:
        token, user_obj = token_user
        if user_obj:
            return jsonify({"token": token}), 200
    else:
        return Response.invalid_username_or_password()


blacklist = set()


@user_handler.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        blacklist.add(token)
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
        return jsonify({"message": "Invalid token"}), 401

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
