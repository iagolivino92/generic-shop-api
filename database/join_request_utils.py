"""
Do not use 'object' methods to return join request details. Always use 'data.format' methods instead.
"""
import json
from api import data
from utils import messages
from database.models import JoinRequest
from . import user_utils, key_utils
from api import db


def get_all():
    return data.format_join_requests(get_all_objects())


def get_all_objects():
    return JoinRequest.query.all()


def get_join_request(join_id):
    return data.format_join_request(get_join_request_object(join_id))


def get_join_requests_by_shop(shop_id):
    return data.format_join_requests(get_join_request_object_by_shop(shop_id))


def get_join_request_object(join_id):
    return JoinRequest.query.filter_by(id=join_id).first()


def get_join_request_object_by_shop(shop_id):
    return JoinRequest.query.filter_by(shop_id=shop_id).all()


def create_join_request(request):
    data = request.form
    try:
        new_join = JoinRequest(
            shop_id=data.get('shop_id'),
            data=str(data.to_dict())
        )
    except Exception as e:
        return messages.error_message('could not create join request object', str(e)), 400
    try:
        db.session.add(new_join)
        db.session.commit()
        # link join request to the api key
        key_update = key_utils.update_key(key_utils.get_key_object_by_hash(request.args.get('api-key')).id, new_join.id)
        if key_update[1] != 201:
            return key_update
    except Exception as e:
        return messages.error_message('could not create join request in database', str(e)), 500
    return messages.success_message('join request successfully created'), 201


def update_join_request(join_id, data):
    email = data.get('email')
    action = data.get('action')
    try:
        join_request = JoinRequest.query.filter_by(id=join_id).first()
    except Exception as e:
        return messages.error_message('could not find join request in database', str(e)), 404
    return accept_join(join_request, email) if action == 'accept' else decline_join(join_request, email)


def accept_join(join_request, email):
    try:
        data = json.loads(join_request.data.replace("'", '"'))
    except Exception as e:
        return messages.error_message('could not load data field for the join request', str(e)), 403
    user_create = user_utils.create_user(data, commit=False)
    if user_create[1] != 201:
        return user_create
    try:
        join_request.processed_by = email
        join_request.status = 'approved'
        # finally delete api key
        key = key_utils.get_key_object_by_join_id(join_request.id)
        db.session.delete(key)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not update join request', str(e)), 500
    return messages.success_message('join request successfully accepted/user created'), 200


def decline_join(join_request, email):
    if join_request.status:
        return messages.error_message('join request already processed'), 403
    try:
        join_request.processed_by = email
        join_request.status = 'declined'
        # finally delete api key
        key = key_utils.get_key_object_by_join_id(join_request.id)
        db.session.delete(key)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not process join request', str(e)), 500
    return messages.success_message('join request successfully declined'), 200
