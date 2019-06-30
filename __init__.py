from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import ipytest
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__ ,template_folder='templates/')
#ipytest.config.rewrite_asserts=True
#1ipytest.config.magics=True
app.config['SECRET_KEY'] = 'bfb00a0f9dc312554db4767e51914588'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tushartiwari211998@gmail.com'
app.config['MAIL_PASSWORD'] = 'tushar@1239'
mail = Mail(app)


from flaskblog import routes
