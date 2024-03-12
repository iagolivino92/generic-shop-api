from api import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.String(13))
    address = db.Column(db.String(240))
    users = db.relationship('User')
    join_requests = db.relationship('JoinRequest')
    api_keys = db.relationship('ApiKey')


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    join_request_id = db.Column(db.Integer)
    hash = db.Column(db.String(256))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    contact = db.Column(db.String(13))
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    role = db.Column(db.String(5))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    current_token = db.Column(db.String(256), unique=True)
    token_time = db.Column(db.DateTime(timezone=True))
    reset_hash = db.Column(db.String(256), unique=True)
    reset_hash_expiration = db.Column(db.DateTime(timezone=True))
    sales = db.relationship('Sale')


class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(1500))
    status = db.Column(db.String(100))


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_update_date = db.Column(db.DateTime(timezone=True), default=func.now())
    value = db.Column(db.String(100))
    rate = db.Column(db.String(100))
    commission = db.Column(db.String(100))
    status = db.Column(db.String(100))
