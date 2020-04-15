from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from flaskr import app, db
from flaskr.forms import LoginForm
from flaskr.models import User

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
            msg = "Invalid credentials"
            flash(msg)
            return redirect(url_for('login'))
        elif user.enabled == 0:
            msg = "User disabled"
            flash(msg)
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/users")
@login_required
def users():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/new")
@login_required
def new():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")    
    return render_template('new.html')

@app.route("/edit/<int:id>")
@login_required
def edit(id):
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    user = User.query.filter_by(id=id).first()
    return render_template("edit.html", user=user)

@app.route("/remove/<int:id>")
@login_required
def remove(id):
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    user = User.query.filter_by(id=id).first()
    return render_template("remove.html", user=user)

@app.route("/add", methods=["POST"])
@login_required
def insert():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        username = request.form.get("username")        
        password = request.form.get("password")
        role = request.form.get("role")
        email = request.form.get("email")
        enabled = request.form.get("enabled")
        user = User(username=username)
        user.set_password_hash(password)
        user.role = role
        user.email = email
        user.enabled = 0
        if enabled == 'on':
            user.enabled = 1
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        msg = "Failed to add user {}".format(username)
        flash(msg)
        print(e)
        return redirect("/new")
    return redirect("/users")

@app.route("/update", methods=["POST"])
@login_required
def update():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        newUsername = request.form.get("newUsername")
        oldUsername = request.form.get("oldUsername")
        password = request.form.get("password")
        oldPassword = request.form.get("oldPassword")
        role = request.form.get("role")
        email = request.form.get("email")
        enabled = request.form.get("enabled")
        user = User.query.filter_by(username=oldUsername).first()
        user.username = newUsername
        if oldPassword != password:
            user.set_password_hash(password)
        user.role = role
        user.email = email
        user.enabled = 0
        if enabled == 'on':
            user.enabled = 1
        db.session.commit()
    except Exception as e:
        msg = "Failed to update user {}".format(oldUsername)
        flash(msg)
        print(e)
        return redirect("/edit")
    return redirect("/users")

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
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
