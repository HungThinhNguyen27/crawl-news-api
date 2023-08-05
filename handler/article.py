from config import Config
from urllib.parse import urlparse
from service.employer import Employers
from service.article import ArticleService
from service.crawl_article import CrawlNewsService
from flask import Flask, jsonify, Blueprint, request
from handler.response import articles
from middleware.authentication import Authentication
import flask
from datalayer.es import ElasticSearch_

app = Flask(__name__)
app.config.from_object(Config)
article_handler = Blueprint("article", __name__)

article_service = ArticleService()
middleware = Employers()
crawl_news = CrawlNewsService()
response = articles()
authentication = Authentication()
elsearch = ElasticSearch_()


@article_handler.route("/v1/articles", methods=["GET"])
@authentication.jwt_required_authentication
def get_all_articles():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    query = str(request.args.get("key", ""))

    if page <= 0:
        return response.page_doesnt_exist()

    elif limit < 1 or limit > 100:
        return response.invalid_limit_number()

    result, total_pages = article_service.search(
        page, limit, query)

    if page > int(total_pages):
        return response.page_doesnt_exist()

    return jsonify(result)


@article_handler.route("/v1/articles/<int:id>", methods=["GET"])
@authentication.jwt_required_authentication
def get_article_by_id(id):
    result = article_service.search_by_id(id)
    if result is not None:
        return response.article_format(result)
    else:
        return response.article_not_found(id)


@article_handler.route("/v1/articles/<int:id>", methods=["DELETE"])
@authentication.jwt_required_authentication
@authentication.manager_required
def delete_article_by_id(id):
    search_article = article_service.delete_article_by_id(id)

    if search_article is not None:
        return response.article_deleted(id)
    else:
        return response.article_not_found(id)


@article_handler.route("/v1/articles", methods=["POST"])
@authentication.jwt_required_authentication
@authentication.manager_required
def add_url_news():

    name_article = request.json.get("name_article")
    url = request.json.get("url")
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return response.Invalid_URL_format()

    src_article_create = article_service.add_newspaper_page(
        name_article, url)

    if not src_article_create:
        return response.articles_name_exists(name_article, url)

    return response.created_successfully(name_article, url)


@article_handler.route("/v1/crawl-article", methods=["POST"])
@authentication.jwt_required_authentication
@authentication.manager_required
def craw_an_article():

    url = request.json.get("url")
    if not url:
        return response.url_not_provided()

    existing_url = crawl_news.crawl_one_url_news(url)

    if not existing_url:
        return response.article_not_found(existing_url)

    return response.article_crawling()
