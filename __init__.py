

import threading
from flask import Flask
from config import Config
from article_handler import article
from article_service import article_service
from flask_jwt_extended import JWTManager
from datalayer import crawl_data

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(article)

if __name__ == '__main__':

    # article_service = crawl_data()
    # everyday_thread = threading.Thread(target=article_service.run_everyday())
    # everyday_thread.start()
    app.run(debug=True)


