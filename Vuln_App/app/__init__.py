from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'hi'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import models, views
#db.drop_all()
db.create_all()
