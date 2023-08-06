
"""
Module: middleware

This module provides the UserData class, which handles user-related operations.
"""
from datetime import datetime, timedelta
import jwt
from flask import jsonify, request, session
from model import user
from config import Config
from datalayer import ArticleMysql
from article_handler import Response

class UserData:
    """
    Middleware class for user-related operations.
    """

    def __init__(self):
        self.database = ArticleMysql()

    def create_table_user(self):
        """
        Create user table in the database.
        """
        self.database.execute_query("""
            CREATE TABLE user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                role VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.database.commit()
        self.database.disconnect()

    def login(self):
        """
        User login functionality.
        """
        username = request.json.get('username')
        password = request.json.get('password')

        # Check user login information
        user_obj = self.database.session.query(user).filter_by(
            username=username, password=password).first()
        self.database.session.commit()

        if user_obj:
            payload = {
                'sub': username,
                'exp': datetime.utcnow() + timedelta(minutes=15)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

            return jsonify({'token': token})
        else:
            return Response.invalid_username_or_password()


    def create_user(self):
        """
        Create a new user.
        """
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        role = request.json.get('role')

        existing_user = self.database.session.query(user).filter_by(
            username=username).first()

        if existing_user:
            return Response.username_already_exists()
        if role not in ['user', 'manager']:
            return Response.invalid_role()

        new_user = user(
            username=username,
            password=password,
            email=email,
            role=role
        )
        self.database.session.add(new_user)
        self.database.session.commit()
        return Response.user_created()
    