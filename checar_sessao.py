from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from functools import wraps
import db


def checar_sessao_aluno(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_a' in session:
            return func(*args, **kwargs)
        return redirect('/login_a')

    return wrapper


def checar_sessao_direcao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_d' in session:
            return func(*args, **kwargs)
        return redirect('/login_d')

    return wrapper


def checar_sessao_professor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_p' in session:
            return func(*args, **kwargs)
        return redirect('/login_p')

    return wrapper


def checar_sessao_responsavel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_r' in session:
            return func(*args, **kwargs)
        return redirect('/login_r')

    return wrapper
