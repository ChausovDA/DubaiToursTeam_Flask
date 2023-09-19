"""Маршруты и функции представления"""
import sqlite3

from flask import render_template, request, redirect, url_for, g
from flask_login import login_user, login_required, logout_user

from fdatabase import FDataBase
from app import app, login_manager
from app.validators import validate_password, validate_user
from app.forms import AdminLoginForm, ChangePasswordForm, AddTourForm
from app.userlogin import UserLogin


@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html",
                           about=dbase.get_icons("about"),
                           for_guests=dbase.get_icons("for_guests"),
                           contacts=dbase.get_icons("contacts"),
                           tours=dbase.show_index_tours())


@app.route("/tours")
def tours():
    """Страница с экскурсиями"""
    return render_template("tours.html",
                           safari=dbase.show_tours("safari"),
                           traveling=dbase.show_tours("traveling"),
                           water_walks=dbase.show_tours("water_walks"),
                           air_adventures=dbase.show_tours("air_adventures"),
                           attractions=dbase.show_tours("attractions"),
                           parks=dbase.show_tours("parks"))


@app.route("/login", methods=["POST", "GET"])
def login():
    """Вход в админ панель"""
    form = AdminLoginForm()
    if request.method == "POST":
        user = dbase.get_user(1)
        if user and validate_user(user, request.form["login"], request.form["psw"]):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for("admin_panel"))
        return redirect("login")

    return render_template("login.html", form=form)


@app.route("/admin-panel", methods=["POST", "GET"])
@login_required
def admin_panel():
    """Админ панель"""
    return render_template("panel.html", tours=dbase.show_tours())


@app.route("/logout")
@login_required
def logout():
    """Вход из админ панели"""
    logout_user()
    return redirect(url_for("login"))


@app.route("/change_password", methods=["POST", "GET"])
@login_required
def change():
    """Смена пароля администратора"""
    form = ChangePasswordForm()
    admin = dbase.get_user(1)
    if request.method == "POST" and validate_password(admin, request.form["old_password"],
                                                      request.form["new_password"],
                                                      request.form["repeat_password"]):
        dbase.change_admin_password(request.form["new_password"])
        return redirect(url_for("login"))

    return render_template("change_password.html", form=form)


@app.route("/add_tour", methods=["POST", "GET"])
@login_required
def add_tour():
    """Добавление экскурсии в БД"""
    form = AddTourForm()
    if form.validate_on_submit() and request.method == "POST":
        dbase.add_tour(form.title.data, form.description.data, form.img.data, form.index.data,
                       form.category.data, form.bs_id.data)
        return redirect(url_for("admin_panel"))

    return render_template("add_tours.html", form=form)


@app.route("/delete_tour/<int:tour_id>", methods=["POST", "GET"])
@login_required
def delete(tour_id):
    """Удаление экскурсии из БД"""
    if request.method == "GET":
        dbase.delete_tour(tour_id)
    return render_template("delete_tours.html")


@app.errorhandler(404)
def error_page(error):
    """Страница 404"""
    return render_template("error_page.html"), 404


def connect_db():
    """Соединение с БД"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Получение соединения с БД"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользовательской информации в сессию"""
    return UserLogin().from_db(user_id, dbase)


@app.before_request
def before_first_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    d_base = get_db()
    dbase = FDataBase(d_base)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()
