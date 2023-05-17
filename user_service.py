"""Module that provides user-related services."""

from middleware import UserData

class UserService:
    """Class that provides user-related services."""

    def __init__(self):
        self.user = UserData()

    def login(self):
        """Perform user login."""
        return self.user.login()

    def create_user(self):
        """Create user."""
        return self.user.create_user()

    def logout(self):
        """Perform user logout."""
        return self.user.logout()
