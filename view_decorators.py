from flask import redirect, url_for, session
from functools import wraps


def login_required(function):
    """User must login before access page"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        if is_logged():
            return function(*args, **kwargs)
        return redirect(url_for('.login'))
    return wrapper


def deny_logged(function):
    """If user is logged dont allow him to see page"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        if is_logged():
            return redirect(url_for('.display_images'))
        return function(*args, **kwargs)
    return wrapper


def is_logged():
    """Check is user logged"""
    try:
        if session['logged_in']:
            return True
    except KeyError as e:
        pass
    return False
