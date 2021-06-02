from flask import redirect, session
from functools import wraps


def check_logged_in_p(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_p' in session:
            return func(*args, **kwargs)
        return redirect('/login_p')
    return wrapper
