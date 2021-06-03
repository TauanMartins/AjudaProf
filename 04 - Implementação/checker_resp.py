from flask import redirect, session
from functools import wraps


def check_logged_in_r(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_r' in session:
            return func(*args, **kwargs)
        return redirect('/login_r')
    return wrapper
