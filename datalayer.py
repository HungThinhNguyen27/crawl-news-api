
import time
import hashlib
import newspaper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,func
from config import Config
from model import Base, news, Category
from math import ceil
from flask import jsonify, request, url_for
from datetime import datetime, time , timedelta
from flask_apscheduler import APScheduler

SECRET_KEY = Config.SECRET_KEY
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB

class ArticleMysql:
    
    def __init__(self):
        self.engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_all_articles(self):

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
            total_count = self.session.query(func.count(news.id)).filter(news.title.contains(query)).scalar()
        else:
            articles = self.session.query(news)\
                .limit(limit)\
                .offset(offset)\
                .all()
            total_count = self.session.query(func.count(news.id)).scalar()

        total_pages = int(ceil(total_count / limit))

        if page <= 0:
            return jsonify({"message": "Invalid page number"}), 400
        elif page > total_pages: 
            return jsonify({"message": "This page does not exist"}), 400
        elif limit < 1 or limit > 100:
            return jsonify({"message": "Invalid limit number"}), 400

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
            next_page_url = url_for('article.get_all_articles', limit=limit, page=next_page, key=query ) if next_page else None
        else:
            next_page_url = url_for('article.get_all_articles', limit=limit, page=next_page ) if next_page else None

        metadata = {
            'page_number': page,
            'items_per_page': limit,
            'total_count': total_count,
            'total_pages': total_pages,
            'current_url': request.url,
            'next_page_url': next_page_url
        }

        if not articles_dict:
            return jsonify({'message': 'No articles found'}), 404

        return jsonify({'articles': articles_dict, 'metadata': metadata})


    def search_article_by_id(self, id):

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
            return jsonify({'article': article_dict}),200
        else:
            return jsonify({"message": "Article with id {} not found".format(id)}), 404
        
    def delete_article_by_id(self, id):

        article = self.session.query(news).filter_by(id=id).first()
        if article:
            self.session.delete(article)
            self.session.commit()
            return jsonify({"message": "Article with id {} has been deleted".format(id)})
        else:
            return jsonify({"message": "Article with id {} not found".format(id)}), 404
        
class CrawlData:

    def __init__(self):
        self.database = ArticleMysql()

    def calculate_hash(self, text):
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8', 'ignore'))
        return md5.hexdigest()

    def detect_duplicate(self, hash):
        count = self.database.session.query(func.count(news.id)).filter(news.hash == hash).scalar()
        return count > 0
    
    def add_news(self, url, category):
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
        cats = self.database.session.query(Category).all()
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
        self.scheduler = APScheduler()
        start_time = datetime.utcnow()
        run_time = time(hour=21, minute=26)
        end_time = start_time + timedelta(minutes=5)
        self.scheduler.add_job(
            id='Scheduled task', 
            func = self.crawl_all_news(),
            trigger='cron', 
            day_of_week='mon-sun',
            start_date=run_time, 
            end_date=end_time, 
            hour=run_time.hour,
            minute=run_time.minute,
            )
        
        self.scheduler.start()