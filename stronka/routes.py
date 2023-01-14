import os
import secrets

import flask
import flask_login
from werkzeug.security import safe_join

from stronka.sendmail import send_verification_email
from flask import render_template, redirect, url_for, flash, request, abort, send_file, send_from_directory, session
from flask_login import login_user, logout_user, current_user, login_required
from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User, SearchHistory
from stronka import db
from stronka.ceneo.main import ceneo_scrapper
from stronka.algorithmSort import SortingAlgorithm
import json


UPLOAD_FOLDER = "stronka/static/uploads"
EXPORT_FOLDER = "stronka/static/exports"
ALLOWED_EXTENSIONS = set(["txt"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["EXPORT_FOLDER"] = EXPORT_FOLDER

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/list", methods=["POST", "GET"])
def list_page():
    return render_template("list.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if (
            attempted_user
            and attempted_user.check_password_correction(
                attempted_password=form.password.data
            )
            and attempted_user.active
        ):
            login_user(attempted_user)
            session['logged_in'] = True
            flash(
                f"Success! You are logged in as: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("home_page"))
        else:
            flash(
                "Username and password are not match! Please try again",
                category="danger",
            )
    return render_template("login.html", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
            active=False,
            verification_token=secrets.token_hex(16),
        )
        db.session.add(user_to_create)
        db.session.commit()
        send_verification_email(
            user_to_create.email_address,
            f"http://localhost:5000/verify?token={user_to_create.verification_token}",
        )
        session['logged_in'] = True
        flash(
            f"Account created successfully! We've send e-mail with verification code. {user_to_create.username}",
            category="success",
        )
        return redirect(url_for("home_page"))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )
    return render_template("signin.html", form=form)


@app.route("/verify")
def verify():
    token = request.args.get("token")
    user = User.query.filter_by(verification_token=token).first()
    if user:
        user.active = True
        user.verification_token = None
        db.session.commit()
        flash("Your email address has been verified. You can now log in.", "success")
    else:
        flash("Invalid verification token", "danger")
    return redirect(url_for("login_page"))


@app.route("/logout")
def logout_page():
    logout_user()
    session.pop('logged_in', None)
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))


@app.route("/ceneo", methods=["POST"])
def get_ceneo():
    params = request.get_json()["params"]
    zwrot = {}
    if params != None:
        lista = params.split(",")
    else:
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        user_filenames = [f for f in filenames if f.startswith('lista')]
        if len(user_filenames) == 0:
            abort(404)
        else:
            max_num = max([int(f.split(".")[0].split("_")[-1]) for f in user_filenames])
        filename = f'lista_{max_num}.txt'
        my_file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r")
        data = my_file.read()
        lista = data.split("\n")
        my_file.close()
    zwrot["nazwy"] = lista
    x, propozycje = ceneo_scrapper(lista)
    zwrot["znalezione"] = x
    zwrot["nieznalezione"] = propozycje

    return zwrot


@app.route("/profile", methods=["GET", "POST"])
def show_history():
    history = SearchHistory.query.filter_by(user_id=current_user.id)
    tempDict = {record.search_date: record.items.split(sep=",") for record in history}

    return render_template("profile.html", history=tempDict)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def file_exist(filename):
    return os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename))


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        user_filenames = [f for f in filenames if f.startswith('lista')]
        if len(user_filenames) == 0:
            max_num = 0
        else:
            max_num = max([int(f.split(".")[0].split("_")[-1]) for f in user_filenames])
        filename = f'lista_{max_num + 1}.txt'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('list.html')

@app.route("/algorithm", methods=["POST"])
def algo():
    data = {}
    if request.method == "POST":
        
        data = json.loads(request.get_data().decode())
        #print(json.dump(data, indent=2))
        #print(data)
        products = data.get('products')
        #print(products)
        sortowanie = SortingAlgorithm(products)
        data = sortowanie.dataIntoSets()
        # print(json.dumps(data[0], indent=2))
        # print(data[1])
        if 'logged_in' in session:
            with open(os.path.join(app.config['EXPORT_FOLDER'], current_user.username), "w") as file:
                json.dump(data, file, indent=4)
    return data

@app.route("/getfile")
def getfile():
    return send_file(
        f'static/exports/{current_user.username}',
        download_name=f'ListaZakupow{current_user.username}.txt',
        as_attachment=True
    )