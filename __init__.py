from flask import Flask
from src.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://wine_user:password@localhost/wine_inventory'
    db.init_app(app)
    return app
