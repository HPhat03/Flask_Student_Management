from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager, logout_user
app = Flask(__name__)
app.secret_key = "hjasgdikuhqhjkgavsasudmnxbzcjyatwakjhsh"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/student_management?charset=utf8mb4" % quote('PandaPhat2003@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app= app)
login = LoginManager(app)
