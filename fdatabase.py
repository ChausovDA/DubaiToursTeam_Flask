"""Модуль для работы с базой данных"""
import sqlite3

from werkzeug.security import generate_password_hash


class FDataBase:
    """Класс для работы с базой данных"""
    def __init__(self, d_base):
        self.__db = d_base
        self.__cur = d_base.cursor()

    def show_index_tours(self):
        """Отображение экскурсий на главной странице"""
        self.__cur.execute("""SELECT title, description, img, bs_id
                               FROM tours 
                               WHERE index_page == 'Yes'""")
        res = self.__cur.fetchall()
        if res:
            return res
        return False

    def show_tours(self, cat=None):
        """Отображение экскурсий"""
        if cat:
            self.__cur.execute(f"""SELECT title, description, img, bs_id
                                                   FROM tours 
                                                   WHERE category == '{cat}'""")
            res = self.__cur.fetchall()
            if res:
                return res
        else:
            self.__cur.execute("SELECT id, title , description, img, bs_id, FROM tours")
            res = self.__cur.fetchall()
            if res:
                return res
        return False

    def get_icons(self, cat):
        """Отображение иконок"""
        self.__cur.execute(f"SELECT title, img, url FROM icons WHERE category == '{cat}'")
        res = self.__cur.fetchall()
        if res:
            return res
        return False

    def get_user(self, user_id):
        """Получение информации о пользователе по id"""
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as err:
            print("Ошибка получения данных из БД " + str(err))

        return False

    def change_admin_password(self, password):
        """Изменение пароля администратора"""
        hash_psw = generate_password_hash(password)
        try:
            self.__cur.execute(f"UPDATE users SET password = \'{hash_psw}\' WHERE id == 1")
            self.__db.commit()
        except sqlite3.Error as err:
            print("Не удалось сменить пароль " + str(err))
            return False
        return True

    def add_tour(self, title, description, img, index, category, bs_id):
        """Добавление экскурсии в БД"""
        try:
            self.__cur.execute("INSERT INTO tours VALUES(NULL, ?, ?, ?, ?, ?, ?)",
                               (title, description, img, index, category, bs_id))
            self.__db.commit()
        except sqlite3.Error as err:
            print("Не удалось добавить экскурсию " + str(err))
            return False
        return True

    def delete_tour(self, tour_id):
        """Удаление экскурсии из БД"""
        try:
            self.__cur.execute(f"DELETE FROM tours WHERE id == {tour_id}")
            self.__db.commit()
        except sqlite3.Error as err:
            print("Не удалось удалить экскурсию " + str(err))
            return False
        return True
