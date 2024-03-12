"""
Do not use 'object' methods to return shop details. Always use 'data.format' methods instead.
"""
from flask import request
from api import data
from database import key_utils
from utils import messages
from database.models import Shop
from api import db


def get_all():
    return data.format_shops(Shop.query.all())


def get_all_objects():
    return Shop.query.all()


def get_shop_by_id(shop_id):
    return data.format_shop(Shop.query.filter_by(id=shop_id).first())


def get_shop_by_name(shop_name):
    if shop_name == 'unknown':
        key = key_utils.get_key_object_by_hash(request.args.get('api-key'))
        return data.format_shop(get_shop_object_by_id(key.shop_id))
    return data.format_shop(get_shop_object_by_name(shop_name))


def get_shop_object_by_id(shop_id):
    return Shop.query.filter_by(id=shop_id).first()


def get_shop_object_by_name(shop_name):
    return Shop.query.filter_by(shop_name=shop_name).first()


def create_shop(data):
    try:
        new_shop = Shop(
            shop_name=data.get('shop_name'),
            email=data.get('email'),
            contact=data.get('contact'),
            address=data.get('address')
        )
    except Exception as e:
        return messages.error_message('could not create shop object', str(e)), 400
    try:
        db.session.add(new_shop)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not create shop in database', str(e)), 500
    return messages.success_message('shop successfully created'), 201


def delete_shop(shop_id):
    try:
        shop = Shop.query.filter_by(id=shop_id).first()
    except Exception as e:
        return messages.error_message('could not find shop in database', str(e)), 404
    try:
        db.session.delete(shop)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not delete shop from database', str(e)), 500
    return messages.success_message('shop successfully deleted'), 201


def update_shop(shop_id, fields):
    error = None
    try:
        shop = Shop.query.filter_by(id=shop_id).first()
    except Exception as e:
        return messages.error_message('could not find shop in database', str(e)), 404
    for field in fields:
        try:
            globals()['update_' + field](shop, fields[field])
        except Exception as e:
            error += f'field {field} could not be updated (err: {str(e)})\n'
    if error:
        return messages.error_message('could not update shop', error), 403
    try:
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not save shop updates in database', str(e)), 500
    return messages.success_message('shop successfully updated'), 201


def update_shop_name(shop, value):
    shop.shop_name = value


def update_email(shop, value):
    shop.email = value


def update_contact(shop, value):
    shop.contact = value


def update_address(shop, value):
    shop.address = value
