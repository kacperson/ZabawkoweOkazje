import os

from random import random

import flask_login
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, logout_user
from werkzeug.utils import secure_filename

from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User
from stronka import db
from stronka.ceneo.main import ceneo_scrapper
from stronka.ceneo.my_ceneo import Ceneo
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from multiprocessing import freeze_support


UPLOAD_FOLDER = 'stronka/static/uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/list')
def list_page():
    return render_template('list.html',)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('signin.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/ceneo', methods=['POST'])
def get_ceneo():
    params = request.get_json()["params"]
    if params != None:
        lista = params.split(",")
    else:
        my_file = open("stronka/static/uploads/xd.txt", "r")
        data = my_file.read()
        lista = data.split("\n")
        my_file.close()
    x, propozycje = ceneo_scrapper(lista)
    zwrot = {}
    zwrot['znalezione'] = x
    zwrot['nieznalezione'] = propozycje
    return zwrot

@app.route('/show_choice', methods=['POST'])
def show_choice():
    params = request.get_json()["params"]
    number = request.get_json()["number"]
    lista1 = []
    lista1.append(params)
    print(params)
    print(number)
    freeze_support()
    options = Options()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    bot = Ceneo(driver)
    bot.odpalenie_strony()
    output = bot.wyszukiwanie(lista1, int(number))
    d1={}
    for i in output:
        d1.update(i)
    print(d1)
    return d1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_exist(filename):
    return os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        """while (True):
            if file_exist(filename):
                print(filename)
                filename = f'{flask_login.current_user + xd}.txt'
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                break"""

