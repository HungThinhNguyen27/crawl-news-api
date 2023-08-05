"""
Module: middleware

This module provides the UserData class, which handles user-related operations.
"""
import jwt
from model.employer import User, OutputFormat
from config import Config
from datalayer.employer import Employer
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict


class Employers:
    """
    Middleware class for user-related operations.
    """

    def __init__(self):
        self.employer = Employer()

    def login(self, username: str, password: str) -> Optional[Tuple[str, User]]:
        """
        User login functionality.
        """
        employers = self.employer.get()

        employer_obj = None
        for employer in employers:
            if employer.username == username and employer.password == password:
                employer_obj = employer
                break

        if employer_obj:
            access_token_payload = {
                "sub": username,
                "role": employer_obj.role,
                "exp": datetime.utcnow() + timedelta(minutes=3),
            }

            refresh_token_payload = {
                "sub": username,
                "exp": datetime.utcnow() + timedelta(days=2),
            }
            access_token = jwt.encode(
                access_token_payload, Config.SECRET_KEY, algorithm="HS256")
            refresh_token = jwt.encode(
                refresh_token_payload, Config.SECRET_KEY, algorithm="HS256")

            return access_token, refresh_token, employer_obj
        return None

    def refresh_token(self, refresh_token: str) -> Optional[str]:

        refresh_token_payload = jwt.decode(
            refresh_token, Config.SECRET_KEY, algorithms=["HS256"])
        username = refresh_token_payload["sub"]
        employer_obj = None

        employers = self.employer.get()

        for employer in employers:
            if employer.username == username:
                employer_obj = employer
                break

        if employer_obj:
            access_token_payload = {
                "sub": username,
                "role": employer_obj.role,
                "exp": datetime.utcnow() + timedelta(minutes=5),
            }

            access_token = jwt.encode(
                access_token_payload, Config.SECRET_KEY, algorithm="HS256")
            return access_token

    def create_employer(self, username: str, password: str, email: str, role: str) -> Optional[User]:

        employers = self.employer.get()
        employer_name = [employer.username for employer in employers]
        if employer_name == username:
            return None
        new_employer = User(username=username, password=password,
                            email=email, role=role)
        add_employer = self.employer.add(new_employer)
        return add_employer

    def remove_employer(self, id):
        get_employer = self.employer.get_by_id(id)

        if get_employer:
            self.employer.remove(get_employer)
        return get_employer

    def get_all_user(self) -> List[User]:
        employers = self.employer.get()

        employers_dict = []

        for employer in employers:
            employer_output = OutputFormat(employer)
            emp_dict = employer_output.employer_format()
            employers_dict.append(emp_dict)

        return employers_dict

    def edit_user_info(self, user_id: int, new_info: Dict[str, str]):
        user = self.employer.get_by_id(user_id)

        if user:
            user_info = {key: value for key,
                         value in new_info.items() if key in user.__dict__}
            self.employer.update_user_info(user, user_info)

        return user
