import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "flask_login_sample/db/flask_login_sample.db"))

class Config():
    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')