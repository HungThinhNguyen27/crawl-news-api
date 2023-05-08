
import jwt
from model import User
from config import Config
from datalayer import ArticleMysql
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect, url_for
from flask_jwt_extended import get_jwt_identity

class User_login:

    def __init__(self) :
        self.database = ArticleMysql()

    def create_table_user(self):
        self.database.execute_query("""
            CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) NOT NULL UNIQUE,
                            password VARCHAR(255) NOT NULL, 
                            email VARCHAR(100) NOT NULL UNIQUE, 
                            role VARCHAR(50) NOT NULL, 
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                            """)
        self.database.commit()
        self.database.disconnect()


    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')
        
        # Kiểm tra thông tin đăng nhập của người dùng
        user= self.database.session.query(User)\
                                    .filter_by(username=username,password=password)\
                                    .first()
        self.database.session.commit()

        if user:
            payload = {
                'sub': username,
                'exp': datetime.utcnow() + timedelta(minutes=15)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
        
    def create_user(self):

        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        role = request.json.get('role')
        existing_user = self.database.session.query(User)\
            .filter_by(username=username)\
            .first()

        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        if role not in ['user', 'manager']:
            return jsonify({'error': 'Invalid role'}), 400
        
        new_user = User(
            username=username,
            password=password,
            email=email,
            role=role
        )
        self.database.session.add(new_user)
        self.database.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    
class Manager:

    def __init__(self) :
        self.database = ArticleMysql()

    def delete_article_by_id(self,id):
        current_user = get_jwt_identity()
        user= self.database.session.query(User)\
                        .filter_by(username=current_user)\
                        .first()
        self.database.session.commit()
        if user.role == 'manager':
            articles = self.database.delete_article_by_id(id)
            return articles
        else:
            return jsonify({"Message":"You do not have permission to delete posts."}),403