"""
Do not use 'object' methods to return key details. Always use 'data.format' methods instead.
"""
import hashlib
from datetime import datetime

from api import data, db
from database.models import ApiKey
from utils import messages


def get_all_objects():
    return ApiKey.query.all()


def get_key_objects_by_shop(shop_id):
    return ApiKey.query.filter_by(shop_id=shop_id).all()


def get_key_object_by_id(key_id):
    return ApiKey.query.filter_by(id=key_id).first()


def get_key_object_by_hash(key_hash):
    return ApiKey.query.filter_by(hash=key_hash).first()


def get_key_object_by_join_id(join_id):
    return ApiKey.query.filter_by(join_request_id=join_id).first()


def get_keys():
    return data.format_keys(get_all_objects())


def get_keys_by_shop(shop_id):
    return data.format_keys(get_key_objects_by_shop(shop_id))


def get_key_by_id(key_id):
    return data.format_key(get_key_object_by_id(key_id))


def get_key_by_hash(key_hash):
    return data.format_key(get_key_object_by_hash(key_hash))


def create_key(data):
    try:
        new_key = ApiKey(
            shop_id=data.get('shop_id'),
            hash=hashlib.md5(str(datetime.utcnow()).encode()).hexdigest()
        )
    except Exception as e:
        print(e)
        return messages.error_message('could not create api key object!', str(e)), 403
    try:
        db.session.add(new_key)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not create api key in database', str(e)), 500
    return messages.success_message('api key successfully created'), 201


def update_key(key_id, join_id):
    try:
        key = get_key_object_by_id(key_id)
    except Exception as e:
        return messages.error_message('could not find api key in database', str(e)), 404
    try:
        key.join_request_id = join_id
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not update api key in database', str(e)), 500
    return messages.success_message('api key successfully updated'), 201


def remove_key(key_id):
    try:
        key = get_key_object_by_id(key_id)
    except Exception as e:
        return messages.error_message('could not find api key in database', str(e)), 404
    try:
        db.session.delete(key)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not clear api key from database', str(e)), 500
    return messages.success_message('key successfully cleared'), 201
