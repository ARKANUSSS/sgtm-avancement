import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-tres-forte'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite (local)
    SQLALCHEMY_TRACK_MODIFICATIONS = False