from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from csi3335F2023 import mysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models