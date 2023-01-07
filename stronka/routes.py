from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User, SearchHistory
from stronka import db
from stronka.ceneo.main import ceneo_scrapper
from stronka.ceneo.my_ceneo import Ceneo
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from multiprocessing import freeze_support



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/list', methods=['POST'])
def list_page():
    return render_template('list.html')


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
    lista1 = []
    lista1.append(params)
    freeze_support()
    options = Options()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    bot = Ceneo(driver)
    bot.odpalenie_strony()
    output = bot.zwrocenie_listy(lista1)
    lista2 = ["jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć", "dziesięć"]
    zipped = dict(zip(lista2, output))
    print(zipped)

    return jsonify(zipped)

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

@app.route('/profile', methods=["GET","POST"])
def show_history():
    history = SearchHistory.query.filter_by(user_id=current_user.id)

    return render_template('profile.html', history=history)
