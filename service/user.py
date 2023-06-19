"""
Module: middleware

This module provides the UserData class, which handles user-related operations.
"""
import jwt
from model.user import User
from config import Config
from datalayer.user import UserMysql
from datetime import datetime, timedelta
from typing import Optional, Tuple


class UserService:
    """
    Middleware class for user-related operations.
    """

    def __init__(self):
        self.datalayer = UserMysql()

    def login(self, username: str, password: str) -> Optional[Tuple[str, User]]:
        """
        User login functionality.
        """
        # Check user login information
        user_obj = self.datalayer.get_by_username_password(username, password)
        if user_obj:
            payload = {
                "sub": username,
                "exp": datetime.utcnow() + timedelta(minutes=60),
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            return token, user_obj
        return None

    def create_user(
        self, username: str, password: str, email: str, role: str
    ) -> Optional[User]:
        exis_user = self.datalayer.get_by_username(username)

        if exis_user:
            return exis_user

        new_user = User(username=username, password=password,
                        email=email, role=role)

        add_user = self.datalayer.add(new_user)

        return add_user

    def user_check_role(self, current_user: str) -> Optional[str]:
        user_check_role = self.datalayer.user_check_role(current_user)
        return user_check_role
