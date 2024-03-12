from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# database object
db = SQLAlchemy()
db_path = "database.db"


def create_app():
    """
    app initialization
    secret_key is a sha256 for 'generic-shop' string
    """
    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'generic-shop.com:5001'
    app.config['SECRET_KEY'] = 'fb857939e24a93872b67c392149b363ca0e988a3c7739325b38c913b234c3cfb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # load user class - mandatory
    from database.models import Shop, User, JoinRequest
    create_start_database(app)

    return app


def create_start_database(app):
    """
    start database
    :param app:
    :return: None
    """
    # create/start database
    db.init_app(app)
    with app.app_context():
        db.create_all()
