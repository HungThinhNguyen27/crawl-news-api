"""
Module: middleware

This module provides the UserData class, which handles user-related operations.
"""
from datetime import datetime, timedelta
import jwt
from flask import jsonify, request, session
from model import user
from config import Config
from datalayer import UserMysql


class UserData:
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
                "exp": datetime.utcnow() + timedelta(minutes=60),
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            return token, user_obj
        return user_obj

    def create_user1(self, username, password, email, role):
        exis_user = self.datalayer.existing_user(username)

        if exis_user:
            return exis_user

        new_user = user(username=username, password=password, email=email, role=role)

        add_user = self.datalayer.add_user(new_user)

        return add_user
