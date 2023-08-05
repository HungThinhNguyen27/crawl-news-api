import threading
from flask import Flask
from config import Config
from handler.article import article_handler
from handler.emloyer import user_handler
from handler.es import es
from flask_jwt_extended import JWTManager
from service.crawl_article import CrawlNewsService

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(user_handler)
app.register_blueprint(article_handler)
app.register_blueprint(es)

if __name__ == "__main__":

    # article_service = CrawlNewsService()
    # everyday_thread = threading.Thread(target=article_service.run_everyday())
    # everyday_thread.start()
    from collections.abc import MutableMapping

# 👇️ <class 'collections.abc.MutableMapping'>
    print(MutableMapping)
    app.run(
        # host='0.0.0.0',
        # port=9090,
        debug=True
    )
