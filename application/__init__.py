from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask import flash
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from application import routes