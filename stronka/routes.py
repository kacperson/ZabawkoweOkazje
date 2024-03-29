import os
import secrets

import flask
import flask_login
from werkzeug.security import safe_join
from sqlalchemy import text

from stronka.sendmail import send_verification_email
from flask import render_template, redirect, url_for, flash, request, abort, send_file, send_from_directory, session
from flask_login import login_user, logout_user, current_user, login_required
from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User, SearchHistory
from stronka import db
from stronka.ceneo.main import ceneo_scrapper
import stronka.algorithmSort as alg
import json

UPLOAD_FOLDER = "stronka/static/uploads"
EXPORT_FOLDER = "stronka/static/exports"
ALLOWED_EXTENSIONS = set(["txt"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["EXPORT_FOLDER"] = EXPORT_FOLDER

# The UPLOAD_FOLDER variable is used to specify the directory where uploaded files will be stored.
# The EXPORT_FOLDER variable is used to specify the directory where exported files will be stored.
# The ALLOWED_EXTENSIONS variable is used to specify the file extensions that are allowed to be uploaded.
# The app.config["UPLOAD_FOLDER"] and app.config["EXPORT_FOLDER"] lines set the previously defined variables as
# configurations for the app.

# The home_page() function renders the home page of the website when the "/" or "/home" route is accessed.
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

# The list_page() function renders the list page of the website when the "/list" route is accessed.
@app.route("/list", methods=["POST", "GET"])
def list_page():
    return render_template("list.html")


# The login_page() function handles the form submission for logging in and verifies the entered username and password
# against the database. If the login is successful, the user is logged in and redirected to the home page.
# If it fails, an error message is displayed.
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
            f"http://10.160.73.90:5000/verify?token={user_to_create.verification_token}",
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


#  verify() -  verifies the user's email address
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
        if 'logged_in' in session:
            obj = SearchHistory(user_id=current_user.id, items=params)
            db.session.add(obj)
            db.session.commit()
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


@app.route("/profile", methods=["GET"])
def show_history():
    query0 = text(f'SELECT * FROM history  WHERE user_id={current_user.id} ORDER BY id')
    all_items = db.session.execute(query0)
    items_list = []
    for row in all_items:
        items_dict = {'id': row.id, 'user_id': row.user_id, 'items': row.items, 'search_date': row.search_date}
        items_list.append(items_dict)

    return render_template("profile.html", history=items_list)


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
        products = data.get('products')
        data = {}
        data["TLP"] = alg.ProductsWithLowestPrice(products).get_products()
        data["TFS"] = alg.ProductsWithFewestShops(products).get_products()
        if 'logged_in' in session:
            with open(os.path.join(app.config['EXPORT_FOLDER'], f'{current_user.username}TLP'), "w") as file:
                json.dump(data["TLP"], file, indent=4)
            with open(os.path.join(app.config['EXPORT_FOLDER'], f'{current_user.username}TFS'), "w") as file:
                json.dump(data["TFS"], file, indent=4)
    return data


@app.route("/getfileTLP")
def getfileTLP():
    return send_file(
        f'static/exports/{current_user.username}TLP',
        download_name=f'ListaZakupow{current_user.username}TLP.txt',
        as_attachment=True
    )

@app.route("/getfileTFS")
def getfileTFS():
    return send_file(
        f'static/exports/{current_user.username}TFS',
        download_name=f'ListaZakupow{current_user.username}TFS.txt',
        as_attachment=True
    )
