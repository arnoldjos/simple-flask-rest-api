from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, "test", "test")
]

username_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    username = payload["identity"]
    return username_mapping.get(username)
