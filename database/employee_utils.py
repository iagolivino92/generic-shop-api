from api import data
from . import shop_utils, user_utils
from .models import User


def get_all():
    return data.format_users(get_all_objects())


def get_all_objects():
    return User.query.filter_by(role='emp').all()


def get_employees_by_shop(shop_id):
    return data.format_users(get_employees_object_by_shop(shop_id))


def get_employees_object_by_shop(shop_id):
    shop = shop_utils.get_shop_object_by_id(shop_id)
    return User.query.filter_by(role='emp', shop_id=shop.id).all()


def get_employee_object_by_id(employee_id):
    return User.query.filter_by(role='emp', id=employee_id).first()


def get_employee_object_by_email(email, shop_id=None):
    if shop_id:
        return User.query.filter_by(role='emp', email=email, shop_id=shop_id).first()
    return User.query.filter_by(role='emp', email=email).first()


def get_employee_by_id(employee_id):
    return data.format_user(get_employee_object_by_id(employee_id))


def get_employee_by_email(email):
    return data.format_user(get_employee_by_email(email))


def get_employee_by_token(token):
    return user_utils.get_user_by_token(token)
