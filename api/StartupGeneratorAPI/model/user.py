from flask_login import UserMixin

from StartupGeneratorAPI.configuration import AppVariables, get_variable

_users = {}


class User(UserMixin):
    def __init__(self, user_id: str, password: str):
        self._user_id = user_id
        self._password = password

    def get_id(self):
        return self._user_id

    def is_password(self, password: str):
        return password == self._password

    @staticmethod
    def get(user_id: str):
        return _users.get(user_id, None)

    @staticmethod
    def authenticate(username: str, password: str):
        if not username or not password:
            return None
        user = _users.get(username, None)
        return user if user and user.is_password(password) else None


def _user_factory(users: dict, username: str, password: str):
    users[username] = User(username, password)


if not get_variable(AppVariables.login_disabled, required=False):
    _user_factory(
        _users,
        get_variable(AppVariables.admin_username),
        get_variable(AppVariables.admin_password),
    )
