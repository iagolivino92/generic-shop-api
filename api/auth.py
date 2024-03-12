import hashlib
from flask import jsonify, request
from werkzeug.security import check_password_hash
from api import db
from database.user_utils import get_user_object_by_token
from utils import messages
from database import user_utils, shop_utils, join_request_utils, key_utils
from datetime import datetime


def credentials_login(request):
    email = request.form.get('email')
    password = request.form.get('password')
    shop_name = request.args.get('shop')
    if not shop_name:
        return messages.error_message('shop filed is mandatory'), 403
    try:
        shop = shop_utils.get_shop_object_by_id(int(shop_name))
    except Exception as e:
        print(e)
        shop = shop_utils.get_shop_object_by_name(shop_name)
    try:
        db_user = user_utils.get_user_object_by_email(email, shop_id=shop.id)
        if check_password_hash(db_user.password, password):
            refresh_token(db_user)
            return jsonify('{"access_token":"%s"}' % db_user.current_token), 201
        else:
            return messages.error_message('login failed', 'credentials not match'), 401
    except AttributeError as e:
        return messages.error_message('could not complete login', 'user does not exist in the selected shop'), 403


def token_login(token):
    user = user_utils.get_user_object_by_token(token)
    if user:
        return is_token_valid(user, token)
    return messages.error_message('invalid user'), 401


def generate_token_hash(user):
    return hashlib.md5((user.email + user.password + str(datetime.utcnow())).encode()).hexdigest()


def refresh_token(user):
    create_token(user)
    user.token_time = datetime.utcnow()
    db.session.commit()


def create_token(user):
    user.current_token = generate_token_hash(user)


def is_token_valid(user, token):
    user_token = user.current_token
    if user_token == token:
        time_left = get_token_left_time(user.token_time)
        if time_left:
            return messages.warning_message(f'token={token}',
                                            f'token is valid for the next {int(time_left)} minute(s)'), 200
    return messages.error_message('invalid or expired token'), 401


def get_token_left_time(token_creation_time=None, maximum_time=30):
    difference = datetime.utcnow() - token_creation_time
    passed_minutes = difference.total_seconds() / 60
    return maximum_time - passed_minutes if passed_minutes < maximum_time else None


def clear_token(token):
    try:
        user = get_user_object_by_token(token)
        user.current_token = None
        db.session.commit()
        return messages.success_message('token cleared'), 200
    except Exception as e:
        return messages.error_message('could not clear the token', str(e)), 500


def create_reset_hash(user):
    user.reset_hash = generate_token_hash(user)
    user.reset_hash_expiration = datetime.utcnow()
    db.session.commit()


def clear_reset_hash(reset_hash=None):
    try:
        user_ = user_utils.get_user_object_by_reset_hash(reset_hash)
        user_.reset_hash = None
        db.session.commit()
        return messages.success_message('reset hash cleared'), 200
    except Exception as e:
        return messages.error_message('could not clear the reset hash', str(e)), 500


def is_reset_hash_valid(user=None):
    time_left = get_token_left_time(user.reset_hash_expiration, maximum_time=60)  # valid for 60 minutes
    if time_left:
        return messages.warning_message(f'reset_hash={user.reset_hash_expiration}',
                                            f'token is valid for the next {int(time_left)} minute(s)'), 200
    return messages.error_message('invalid or expired token'), 401


def _token_required(f, role='read'):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = user_utils.get_user_object_by_token(request.headers['authorization'])
            is_valid = is_token_valid(user, request.headers['authorization'])
            if is_valid[1] != 200:
                return is_valid
            allow = (user.role == 'admin') or \
                    (user.role == 'mgr' and (role == 'read' or role == 'emp')) or \
                    (user.role == 'read' and role == 'emp') or \
                    (user.role == role)
        except Exception as e:
            print(e)
            allow = False
        return f(*args, **kwargs) if allow else (messages.error_message('user not authorized'), 401)

    return decorated_function


def admin_token_required(f):
    return _token_required(f, role='admin')


def mgr_token_required(f):
    return _token_required(f, role='mgr')


def read_token_required(f):
    return _token_required(f)


def emp_token_required(f):
    return _token_required(f, role='emp')


def api_key_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            header = request.headers['authorization']
            if header:
                emp_token_required(f)
                return f(*args, **kwargs)
        except Exception as e:
            print(e)
        try:
            key = key_utils.get_key_object_by_hash(request.args.get('api-key'))
            # check if the api-key is for the selected shop
            # if not key.shop_id == shop_utils.get_shop_object_by_name(kwargs.get('name')).id:
            # return messages.error_message('api key not valid for the selected shop'), 403
        except Exception as e:
            print(e)
            return messages.error_message('could not find api key'), 403
        if not key:
            return messages.error_message('api key does not exist'), 404
        return f(*args, **kwargs)

    return decorated_function


def reset_hash_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = user_utils.get_user_object_by_reset_hash(request.args.get('h'))
            # check if the api-key is for the selected shop
            # if not key.shop_id == shop_utils.get_shop_object_by_name(kwargs.get('name')).id:
            # return messages.error_message('api key not valid for the selected shop'), 403
        except Exception as e:
            print(e)
            return messages.error_message('could not process your reset password request'), 403
        if not user:
            return messages.error_message('this link is not valid!'), 404
        else:
            is_reset_valid = is_reset_hash_valid(user)
            if not is_reset_valid[1] == 200:
                return messages.error_message('this link is not valid anymore. please create a new reset password request.'), 401
        return f(*args, **kwargs)

    return decorated_function
