from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy()
db.init_app(app)

from app import views
from app.models import create_itself

create_itself()
