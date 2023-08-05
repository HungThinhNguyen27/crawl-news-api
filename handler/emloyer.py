import jwt
from config import Config
from functools import wraps
from service.employer import Employers
from flask_jwt_extended import jwt_required
from flask import Flask, jsonify, Blueprint, request, session
import time
from handler.response import employer
from middleware.authentication import Authentication
import time
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
user_handler = Blueprint("user", __name__)
middleware = Employers()
authentication = Authentication()
response = employer()


@user_handler.route("/account", methods=["POST"])
def create_user():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    role = request.json.get("role")

    if role not in ["user", "manager"]:
        return response.invalid_role(role)

    employer = middleware.create_employer(username, password, email, role)
    if employer is None:
        return response.username_already_exists(username)

    return response.create_account_success(username)


@user_handler.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    token_user = middleware.login(username, password)

    if token_user is not None:
        access_token, refresh_token, employer_obj = token_user
        if employer_obj:
            return jsonify({"access_token": access_token},
                           {"refresh_token": refresh_token}), 200
    else:
        return response.invalid_username_or_password()


@user_handler.route("/renew-token", methods=["POST"])
def renew_token():
    refresh_token = request.json.get("refresh_token")

    new_access_token = middleware.refresh_token(refresh_token)

    if new_access_token is not None:
        return jsonify({"access_token": new_access_token}), 200
    else:
        return response.invalid_token()


@user_handler.route("/employer/<int:id>", methods=["DELETE"])
@authentication.jwt_required_authentication
@authentication.manager_required
def delete_employer_by_id(id):
    remove_employer = middleware.remove_employer(id)

    if remove_employer:
        return response.employer_deleted(id)
    else:
        return response.employer_not_found(id)


@user_handler.route("/employer", methods=["GET"])
@authentication.jwt_required_authentication
@authentication.manager_required
def Search():
    employer = middleware.get_all_user()
    return jsonify(employer), 200


@user_handler.route("/logout", methods=["POST"])
@authentication.jwt_required_authentication
def logout():
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        return response.invalid_token()
    else:
        return response.no_token_provided()


@user_handler.route("/account-edit/<int:user_id>", methods=["PUT"])
@authentication.jwt_required_authentication
@authentication.manager_required
def edit_user(user_id):
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    role = request.json.get("role")

    if role not in ["user", "manager"]:
        return response.invalid_role(role)

    new_info = {
        "username": username,
        "password": password,
        "email": email,
        "role": role
    }

    employer_edit = middleware.edit_user_info(user_id, new_info)

    if employer_edit:
        return response.update_success(employer_edit)
    else:
        return response.update_failed(employer_edit)
