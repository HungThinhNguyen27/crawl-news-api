

import threading
from flask import Flask
from config import Config
from article_handler import article
from article_service import ArticleService
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(article)

if __name__ == '__main__':
    # article_service = ArticleService()
    # everyday_thread = threading.Thread(target=article_service.article_crawling)
    # everyday_thread.start()
    app.run(debug=True)







# {
#   "username": "admin",
#   "password": "admin"
# }


# {
#   "username": "meo12",
#   "password": "thinh123",
#   "email": "meo@gmail.com",
#   "role": "user"
# }