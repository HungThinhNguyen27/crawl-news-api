
"""
Module for interacting with the data layer.
Provides functions for fetching, inserting, updating, and deleting data from the database.
"""
import time
import hashlib
import newspaper
import time
import schedule
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import Config
from model import Base, news, category
from math import ceil
from flask import jsonify, request, url_for
from urllib.parse import urlparse
from article_handler import Response

SECRET_KEY = Config.SECRET_KEY
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB

class ArticleMysql:
    """
    Class to interact with MySQL database and perform operations related to news articles.
    """

    def __init__(self):
        self.engine = create_engine(
            f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}',
            echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def get_all_articles(self):
        """
        Retrieves all articles from the MySQL database.

        Supports pagination and searching by keyword.

        Returns:
            A JSON response containing a list of articles and metadata
        """
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        query = str(request.args.get('key', ''))
        if query:
            articles = self.session.query(news)\
                .filter(news.title.contains(query))\
                .limit(limit)\
                .offset(offset)\
                .all()
            total_count = self.session.query(func.count(news.id)).filter(
                news.title.contains(query)).scalar()
        else:
            articles = self.session.query(news)\
                .limit(limit)\
                .offset(offset)\
                .all()
            total_count = self.session.query(func.count(news.id)).scalar()

        total_pages = int(ceil(total_count / limit))

        if page <= 0:
            return Response.invalid_page_number()
        elif page > total_pages:
            return Response.page_doesnt_exist()
        elif limit < 1 or limit > 100:
            return Response.invalid_limit_number()

        articles_dict = []

        for article in articles:
            article_dict = {
                'id': article.id,
                'title': article.title,
                'img_links': article.img_links,
                'content': article.content,
                'original_url': article.original_url,
                'category_id': article.category_id,
                'hash': article.hash,
            }
            articles_dict.append(article_dict)

        next_page = page + 1 if page < total_pages else None
        if query:
            next_page_url = url_for(
                'article.get_all_articles',
                limit=limit,
                page=next_page,
                key=query) if next_page else None
        else:
            next_page_url = url_for(
                'article.get_all_articles',
                limit=limit,
                page=next_page) if next_page else None

        metadata = {
            'page_number': page,
            'items_per_page': limit,
            'total_count': total_count,
            'total_pages': total_pages,
            'current_url': request.url,
            'next_page_url': next_page_url
        }

        if not articles_dict:
            return Response.article_not_found()

        return jsonify({'articles': articles_dict, 'metadata': metadata})


    def search_article_by_id(self, id):
        """
        Retrieves an article from the MySQL database by ID.

        """
        article = self.session.query(news)\
            .filter_by(id=id)\
            .first()
        if article:
            article_dict = {
                'id': article.id,
                'title': article.title,
                'img_links': article.img_links,
                'content': article.content,
                'original_url': article.original_url,

            }
            return jsonify({'article': article_dict}), 200
        else:
            return jsonify(
                {"message": "Article with id {} not found".format(id)}), 404


    def delete_article_by_id(self, id):
        """
        Delete an article from the MySQL database by ID.

        """

        article = self.session.query(news).filter_by(id=id).first()
        if article:
            self.session.delete(article)
            self.session.commit()
            return jsonify(
                {"message": "Article with id {} has been deleted".format(id)})
        else:
            return jsonify(
                {"message": "Article with id {} not found".format(id)}), 404


class crawl_data:
    """
    A class for crawling news and adding them to a MySQL database.
    """

    def __init__(self):
        """
        Initializes a new instance of the CrawlData class.
        """
        self.database = ArticleMysql()


    def calculate_hash(self, text):
        """
        Calculates the MD5 hash of a given text string.

        Args:
            text: A string containing the text to hash.

        Returns:
            The MD5 hash of the text as a string.
        """

        md5 = hashlib.md5()
        md5.update(text.encode('utf-8', 'ignore'))
        return md5.hexdigest()


    def detect_duplicate(self, hash):
        """
        Checks whether an article with the given hash already exists in the database.

        Args:
            hash: A string containing the hash to check.

        Returns:
            True if an article with the given hash exists in the database, False otherwise.
        """
        count = self.database.session.query(func.count(
            news.id)).filter(news.hash == hash).scalar()
        return count > 0


    def add_news(self, url, category):
        """
        Crawls a news article from the given URL and adds it to the database.

        Args:
            url: A string containing the URL of the article.
            category: An integer specifying the ID of the category to add the article to.
        """
        article = newspaper.Article(url)
        article.download()
        article.parse()
        hash = self.calculate_hash(article.text)
        if not self.detect_duplicate(hash):
            new_article = news(title=article.title,
                               img_links=article.top_image,
                               content=article.text,
                               original_url=article.url,
                               category_id=category,
                               hash=hash)
            self.database.session.add(new_article)
            self.database.session.commit()
        else:
            print("Duplicated!")


    def crawl_all_news(self):
        """
        Crawls news articles from a list of RSS feeds and adds them to the database.
        """
        cats = self.database.session.query(category).all()
        for cat in cats:
            cat_id = cat.id
            cat_url = cat.url
            source = newspaper.build(cat_url)
            for subcat_url in source.category_urls():
                subcat_source = newspaper.build(subcat_url)
                for article in subcat_source.articles:
                    try:
                        print("====", article.url)
                        self.add_news(article.url, cat_id)
                    except Exception as ex:
                        print(" Error : " + str(ex))
                        pass
        self.database.session.commit()


    def run_everyday(self):

        self.schedule.every().day.at("11:29").do(self.crawl_all_news)
        allow_crawling = True
        start_time = time.time()

        while allow_crawling:
            self.schedule.run_pending()
            elapsed_time = time.time() - start_time
            if elapsed_time == 120:  
                break


    def create_article(self):
            """
            Create a new article for crawling
            """
            name_article = request.json.get('name_article')
            url = request.json.get('url')

            # Kiểm tra xem url có đúng định dạng hay không
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return Response.Invalid_URL_format()

            existing_article= self.database.session.query(category).filter_by(
                url=url).first()

            if existing_article:
                return Response.existing_article()
            
            new_article = category(
                name=name_article,
                url=url
            )
            self.database.session.add(new_article)
            self.database.session.commit()
            return jsonify({'message': 'created article successfully',
                            'new_article': {
                            'name': new_article.name,
                            'url': new_article.url }}), 201


    def crawl_article(self):
            """
            Crawl an article 
            """
            id_article = request.json.get('id_article')

            existing_article= self.database.session.query(category).filter_by(
                id=id_article).first()

            if  not existing_article:
                return Response.article_not_found()
            
            source = newspaper.build(existing_article.url)
            for subcat_url in source.category_urls():
                subcat_source = newspaper.build(subcat_url)
                for article in subcat_source.articles:
                    try:
                        print("Article crawled===", article.url)
                        self.add_news(article.url, id_article)
                    except Exception as ex:
                        print(" Error : " + str(ex))
                        pass
            self.database.session.commit()
            return Response.article_crawling()