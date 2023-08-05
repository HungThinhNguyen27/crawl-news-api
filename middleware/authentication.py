
from functools import wraps
from flask_jwt_extended import jwt_required
from handler.response import employer
from flask import request, Flask
from config import Config
from service.employer import Employers
import jwt

response = employer()
employser_service = Employers()

app = Flask(__name__)
app.config.from_object(Config)


class Authentication:

    def __init__(self) -> None:
        pass

    @staticmethod
    def jwt_required_authentication(func):
        @wraps(func)
        @jwt_required()
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token:
                token = token.split(" ")[1]
                try:
                    data = jwt.decode(
                        token, app.config["SECRET_KEY"], algorithms=["HS256"])
                    return func(*args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return response.token_expired()
                except jwt.InvalidTokenError:
                    return response.invalid_token()
            else:
                return response.no_token_provided()
        return decorated

    @staticmethod
    def manager_required(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token:
                token = token.split(" ")[1]
                data = jwt.decode(
                    token, app.config["SECRET_KEY"], algorithms=["HS256"])
                if data["role"] == "manager":
                    return func(*args, **kwargs)
                else:
                    return response.unauthorized()
        return decorated
