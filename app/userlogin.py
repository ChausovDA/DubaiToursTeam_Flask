"""Модуль для хранения информации о пользователе"""
from flask_login import UserMixin


class UserLogin(UserMixin):
    """Класс представления пользователя"""
    def __init__(self):
        self.__user = None

    def from_db(self, user_id, d_base):
        """Выполняет загрузку пользовательских данных из БД"""
        self.__user = d_base.getUser(user_id)
        return self

    def create(self, user):
        """Записывает информацию о пользователе, и возвращает её"""
        self.__user = user
        return self

    def get_id(self):
        """Возвращает id текущего пользователя"""
        return str(self.__user['id'])
