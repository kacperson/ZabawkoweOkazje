from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from stronka.ceneo import my_ceneo

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ACompl1cat3dText.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WWWW.db'
app.config['SQLITE_DATABASE_CHARSET'] = 'cp1252'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from stronka import routes