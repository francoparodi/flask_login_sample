from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user

from application import app
from application import db
from application.forms import LoginForm
from application.models import User


@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return render_template("homepage.html", user=current_user)
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username e Password non combaciano')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/users")
def users():
    if not current_user.is_authenticated:
        return render_template("homepage.html")
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/insert", methods=["POST"])
def insert():
    try:
        username = request.form.get("username")        
        password = request.form.get("password")
        role = request.form.get("role")
        email = request.form.get("email")
        user = User(username=username)
        user.set_password_hash(password)
        user.role = role
        user.email = email
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        msg = "Failed to add user {}".format(username)
        flash(msg)
        print(e)
    return redirect("/users")

@app.route("/update", methods=["POST"])
def update():
    try:
        newUsername = request.form.get("newUsername")
        oldUsername = request.form.get("oldUsername")
        newPassword = request.form.get("newPassword")
        newRole = request.form.get("newRole")
        newEmail = request.form.get("newEmail")
        user = User.query.filter_by(username=oldUsername).first()
        user.username = newUsername
        user.set_password_hash(newPassword)
        user.role = newRole
        user.email = newEmail
        db.session.commit()
    except Exception as e:
        msg = "Failed to update user {}".format(oldUsername)
        flash(msg)
        print(e)
    return redirect("/users")

@app.route("/delete", methods=["POST"])
def delete():
    try:
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        msg = "Failed to delete user {}".format(username)
        flash(msg)
        print(e)
    return redirect("/users")