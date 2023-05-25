"""
Module: middleware

This module provides the UserData class, which handles user-related operations.
"""
import jwt
from model import User
from config import Config
from datalayer import UserMysql
from datetime import datetime, timedelta
from flask import jsonify, request, session


class UserService:
    """
    Middleware class for user-related operations.
    """

    def __init__(self):
        self.datalayer = UserMysql()

    def login(self, username, password):
        """
        User login functionality.
        """
        # Check user login information
        user_obj = self.datalayer.user_check_login(username, password)
        if user_obj:
            payload = {
                "sub": username,
                "exp": datetime.utcnow() + timedelta(minutes=20),
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            return token, user_obj
        return user_obj

    def create_user(self, username, password, email, role):
        exis_user = self.datalayer.existing_user(username)

        if exis_user:
            return exis_user

        new_user = User(username=username, password=password, email=email, role=role)

        add_user = self.datalayer.add_user(new_user)

        return add_user

    def user_check_role(self, current_user):
        user_check_role = self.datalayer.user_check_role(current_user)
        return user_check_role
