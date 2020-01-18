from flask import abort
from flaskcarleasing.models import User
from functools import wraps
from flask_login import current_user


def check_rights(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.superuser:
            abort(403)
        return func(*args, **kwargs)
    return wrapper