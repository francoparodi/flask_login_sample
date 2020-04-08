from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from application import app
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
    return render_template("users.html")