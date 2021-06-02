from flask import redirect, session
from functools import wraps


def check_logged_in_a(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_a' in session:
            return func(*args, **kwargs)
        return redirect('/login_a')
    return wrapper
