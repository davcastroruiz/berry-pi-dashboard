import os

class Config:
    SECRET_KEY = os.urandom(24)  # Clave secreta para manejar sesiones
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'  # Base de datos SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False