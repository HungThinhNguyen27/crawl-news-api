
import os
from dotenv import load_dotenv


class Config(object):
    load_dotenv()
    SECRET_KEY = os.environ.get('KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_HEADER_NAME = os.environ.get('JWT_HEADER_NAME')
    JWT_HEADER_TYPE = os.environ.get('JWT_HEADER_TYPE')
    JWT_ACCESS_COOKIE_NAME = os.environ.get('JWT_ACCESS_COOKIE_NAME')
    JWT_REFRESH_COOKIE_NAME = os.environ.get('JWT_REFRESH_COOKIE_NAME')
    JWT_ACCESS_CSRF_HEADER_NAME = os.environ.get('JWT_ACCESS_CSRF_HEADER_NAME')
    JWT_ACCESS_CSRF_FIELD_NAME = os.environ.get('JWT_ACCESS_CSRF_FIELD_NAME')
