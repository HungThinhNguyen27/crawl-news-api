import os
from dotenv import load_dotenv


class Config(object):
    load_dotenv()
    SECRET_KEY = os.environ.get("KEY")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

    INDEX = os.environ.get("INDEX")
    ES_HOST = os.environ.get("ES_HOST")
