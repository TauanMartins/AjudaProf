from flask import redirect, session
from functools import wraps


def check_logged_in_d(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_d' in session:
            return func(*args, **kwargs)
        return redirect('/login_d')
    return wrapper
