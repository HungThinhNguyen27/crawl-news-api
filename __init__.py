import threading
from flask import Flask
from config import Config
from user_handler import user_handler
from article_hander import article_handler
from flask_jwt_extended import JWTManager
from crawl_article_service import CrawlNewsService

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(user_handler)
app.register_blueprint(article_handler)

if __name__ == "__main__":

    # article_service = CrawlNewsService()
    # everyday_thread = threading.Thread(target=article_service.run_everyday())
    # everyday_thread.start()
    app.run(debug=True)
