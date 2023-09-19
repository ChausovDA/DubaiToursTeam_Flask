"""Модуль для проверки введенных данных"""
from werkzeug.security import check_password_hash


def validate_user(user, name, password):
    """Проверка пользователя"""
    if check_password_hash(user["password"], password) and user["name"] == name:
        return True
    return False


def validate_password(user, old_psw, new_psw, repeat_psw):
    """Проверка пароля"""
    if check_password_hash(user["password"], old_psw) and new_psw == repeat_psw:
        return True
    return False
