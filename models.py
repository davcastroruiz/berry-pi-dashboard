from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask
from config import Config  # 🔹 Importamos la configuración
from app import db

app = Flask(__name__)
app.config.from_object(Config)  # 🔹 Cargamos la configuración desde `config.py`

db.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
