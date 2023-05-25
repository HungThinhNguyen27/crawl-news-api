from config import Config
from functools import wraps
from urllib.parse import urlparse
from user_service import UserService
from article_service import ArticleService
from flask_jwt_extended import get_jwt_identity
from crawl_article_service import CrawlNewsService
from user_handler import jwt_required_with_blacklist
from flask import Flask, jsonify, Blueprint, request, session


app = Flask(__name__)
app.config.from_object(Config)
article_handler = Blueprint("article", __name__)
article_service = ArticleService()
middleware = UserService()
crawl_news = CrawlNewsService()


@article_handler.route("/articles", methods=["GET"])
@jwt_required_with_blacklist
def get_all_articles():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    query = str(request.args.get("key", ""))

    if page <= 0:
        return Response.invalid_page_number()
    elif limit < 1 or limit > 100:
        return Response.invalid_limit_number()

    result, total_pages = article_service.get_all_articles(page, limit, query)
    if page > int(total_pages):
        return Response.page_doesnt_exist()

    return jsonify(result)


@article_handler.route("/articles/<int:id>", methods=["GET"])
@jwt_required_with_blacklist
def get_article_by_id(id):
    result = article_service.search_article_by_id(id)
    if result is not None:
        article_dict, search_article = result
        return Response.article_format(article_dict)
    else:
        return Response.article_not_found(id)


@article_handler.route("/articles/<int:id>", methods=["DELETE"])
@jwt_required_with_blacklist
def delete_article_by_id(id):
    current_user = get_jwt_identity()
    user_check = middleware.user_check_role(current_user)
    if user_check.role == "manager":
        search_article = article_service.delete_article_by_id(id)
        if search_article:
            return Response.article_deleted(id)
        else:
            return Response.article_not_found(id)
    else:
        return Response.unauthorized()


@article_handler.route("/articles", methods=["POST"])
@jwt_required_with_blacklist
def create_a_src_news():
    current_user = get_jwt_identity()
    user_check = middleware.user_check_role(current_user)
    if user_check.role == "manager":
        name_article = request.json.get("name_article")
        url = request.json.get("url")

        # Kiểm tra xem url có đúng định dạng hay không
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return Response.Invalid_URL_format()

        src_article_create = article_service.create_new_src_article(name_article, url)

        if src_article_create:
            return Response.articles_name_exists(name_article)

        return Response.created_successfully()
    else:
        return Response.unauthorized()


@article_handler.route("/crawl-article", methods=["POST"])
@jwt_required_with_blacklist
def craw_an_article():
    current_user = get_jwt_identity()
    user_check = middleware.user_check_role(current_user)
    if user_check.role == "manager":
        url = request.json.get("url")

        if not url:
            return Response.url_not_provided()

        existing_url = crawl_news.crawl_one_news(url)

        if not existing_url:
            return Response.article_not_found(existing_url)

        return Response.article_crawling()
    else:
        return Response.unauthorized()


class Response:
    @staticmethod
    def unauthorized():
        return jsonify({"Message": "you do not have access to this resource."}), 401

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
    def Invalid_URL_format():
        return jsonify({"error": "Invalid URL format"}), 400

    @staticmethod
    def article_deleted(id):
        return jsonify({"message": "Article with id {} has been deleted".format(id)})

    @staticmethod
    def article_not_found(id):
        return jsonify({"message": "Article with {} not found".format(id)}), 404

    @staticmethod
    def created_successfully(name_article, url):
        return (
            jsonify(
                {
                    "message": "created article successfully",
                    "new_article": {"name": name_article, "url": url},
                }
            ),
            201,
        )

    @staticmethod
    def articles_name_exists(name_article):
        return jsonify(
            {"message": "Articles name {} already exists".format(name_article)}
        )

    @staticmethod
    def article_format(article_dict):
        return jsonify({"article": article_dict}), 200

    @staticmethod
    def article_crawling():
        return jsonify({"message": "Article crawling......"}), 200

    @staticmethod
    def url_not_provided(id):
        return jsonify({"error": "URL not provided"}), 400
