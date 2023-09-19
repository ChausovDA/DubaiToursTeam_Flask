import os

from flask import Flask
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, '../dubaitoursteam.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
