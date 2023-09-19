"""Формы"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AdminLoginForm(FlaskForm):
    """Форма входа администратора"""
    login = StringField("Логин: ", validators=[DataRequired()])
    psw = PasswordField("Пароль: ", validators=[DataRequired()])
    submit = SubmitField("Войти")


class ChangePasswordForm(FlaskForm):
    """Форма смены пароля администратора"""
    old_password = PasswordField("Старый пароль: ", validators=[DataRequired()])
    new_password = PasswordField("Новый пароль: ", validators=[DataRequired()])
    repeat_password = StringField("Повторите пароль: ", validators=[DataRequired()])
    submit = SubmitField("Сменить пароль")


class AddTourForm(FlaskForm):
    """Форма добавления экскурсии"""
    title = StringField("Название: ", validators=[DataRequired()])
    description = TextAreaField("Описание: ", validators=[DataRequired()])
    img = StringField("Путь к изображению: ", validators=[DataRequired()])
    index = StringField("Разместить на главной: ", validators=[DataRequired()])
    category = StringField("Категория: ", validators=[DataRequired()])
    bs_id = StringField("Идентификатор bootstrap: ", validators=[DataRequired()])
    submit = SubmitField("Добавить экскурсию")
