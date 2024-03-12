"""
Do not use 'object' methods to return user details. Always use 'data.format' methods instead.
"""
import smtplib
import hashlib
from werkzeug.security import generate_password_hash
from api import data, auth
from utils import messages
from utils.email import Email
from . import shop_utils
from .models import User, db, Sale


def get_all():
    return data.format_users(get_all_objects())


def get_all_objects():
    return User.query.all()


def get_users_by_shop(shop_id):
    return data.format_users(get_users_object_by_shop(shop_id))


def get_users_object_by_shop(shop_id):
    shop = shop_utils.get_shop_object_by_id(shop_id)
    return User.query.filter_by(shop_id=shop.id).all()


def get_user_object_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_object_by_email(email, shop_id=None):
    if shop_id:
        return User.query.filter_by(email=email, shop_id=shop_id).first()
    return User.query.filter_by(email=email).first()


def get_user_object_by_token(token):
    return User.query.filter_by(current_token=token).first()


def get_user_object_by_reset_hash(hash):
    return User.query.filter_by(reset_hash=hash).first()


def get_user_by_id(user_id):
    return data.format_user(User.query.filter_by(id=user_id).first())


def get_user_by_email(email):
    return data.format_user(User.query.filter_by(email=email).first())


def get_user_by_token(token):
    return data.format_user(User.query.filter_by(current_token=token).first())


def create_user(data, commit=True):
    try:
        shop_id = data.get('shop_id')
        if not shop_id:
            shop = shop_utils.get_shop_object_by_name(data.get('shop'))
            shop_id = shop.id
        new_user = User(
            email=data.get('email'),
            contact=data.get('contact'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=generate_password_hash(data.get('password'), method='pbkdf2'),
            role=data.get('role'),
            shop_id=shop_id
        )
    except Exception as e:
        return messages.error_message('could not create user object', str(e)), 400
    try:
        db.session.add(new_user)
        if commit:
            db.session.commit()
    except Exception as e:
        return messages.error_message('could not create user in database', str(e)), 500
    return messages.success_message('user successfully created'), 201


def delete_user(user_id):
    try:
        user = get_user_object_by_id(user_id)
    except Exception as e:
        return messages.error_message('could not find user in database', str(e)), 404
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not delete user from database', str(e)), 500
    return messages.success_message('user successfully deleted'), 201


def update_user(user_id=None, fields=None):
    error = ''
    try:
        user = get_user_object_by_id(user_id)
    except Exception as e:
        return messages.error_message('could not find user in database', str(e)), 404
    for field in fields:
        try:
            globals()['update_' + field](user, fields[field])
        except Exception as e:
            error += f'field {field} could not be updated (err: {str(e)})\n'
    if error:
        return messages.error_message('could not update user', error), 403
    try:
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not save user updates in database', str(e)), 500
    return messages.success_message('user successfully updated'), 201


def update_type(user, value):
    pass


def update_first_name(user, value):
    user.first_name = value


def update_last_name(user, value):
    user.last_name = value


def update_email(user, value):
    user.email = value


def update_contact(user, value):
    user.contact = value


def update_password(user, value):
    user.password = generate_password_hash(value, method='pbkdf2')


def update_role(user, value):
    user.role = value


def update_shop(user, value):
    try:
        shop_id = int(value)
    except Exception as e:
        shop = shop_utils.get_shop_object_by_name(value)
        shop_id = shop.id
    user.shop_id = shop_id


def update_shop_id(user, value):
    update_shop(user, value)


def create_admin_instance():
    from .models import Shop
    from .models import ApiKey
    if not Shop.query.filter_by(shop_name='admin_local').first():
        create_admin_shop(Shop)
        create_admin_user(User, Shop)
        create_mgr_emp_sale(User, Shop, Sale)
    if not User.query.filter_by(email='admin@local').first():
        create_admin_user(User, Shop)
    if not ApiKey.query.filter_by(shop_id=Shop.query.filter_by(shop_name='admin_local').first().id).first():
        create_admin_api_key(ApiKey, Shop)


def create_admin_shop(shop):
    from api import db
    s = shop(
        shop_name='admin_local',
        email='admin@local',
        contact='0000000000',
        address='local_admin_shop'
    )
    db.session.add(s)
    db.session.commit()


def create_admin_user(user, shop):
    u = user(
        email='admin@local',
        contact='00000000',
        first_name='admin',
        last_name='local',
        password=generate_password_hash('localadministrator', method='pbkdf2'),
        role='admin',
        shop_id=(shop.query.filter_by(shop_name='admin_local').first()).id
    )
    db.session.add(u)
    db.session.commit()


def create_admin_api_key(apikey, shop):
    k = apikey(
        shop_id=shop.query.filter_by(shop_name='admin_local').first().id,
        hash=hashlib.md5('admin_api_key_for_test'.encode()).hexdigest()
    )
    db.session.add(k)
    db.session.commit()


# to be deleted - just a test
def create_mgr_emp_sale(user, shop, sale):
    mgr = user(
        email='mgr@local',
        contact='00000000',
        first_name='mgr',
        last_name='local',
        password=generate_password_hash('12345678', method='pbkdf2'),
        role='mgr',
        shop_id=(shop.query.filter_by(shop_name='admin_local').first()).id
    )
    read = user(
        email='read@local',
        contact='00000000',
        first_name='read',
        last_name='local',
        password=generate_password_hash('12345678', method='pbkdf2'),
        role='read',
        shop_id=(shop.query.filter_by(shop_name='admin_local').first()).id
    )
    emp = user(
        email='emp@local',
        contact='00000000',
        first_name='emp',
        last_name='local',
        password=generate_password_hash('12345678', method='pbkdf2'),
        role='emp',
        shop_id=(shop.query.filter_by(shop_name='admin_local').first()).id
    )
    db.session.add(mgr)
    db.session.add(read)
    db.session.add(emp)
    sale = sale(
        user_id=(user.query.filter_by(first_name='emp').first()).id,
        value='100',
        rate='10',
        commission='10',
        status='paid',
    )
    db.session.add(sale)
    db.session.commit()


def send_user_reset_password_email(user_data):
    user_ = get_user_object_by_email(user_data.get('email'))
    auth.create_reset_hash(user_)
    email = Email()
    try:
        email.subject('Generic Shop: Reset Password')\
            .sender('<your_email>')\
            .recipients([user_.email])\
            .password('<email_password>')\
            .body(data.format_reset_password_email(user_))\
            .send()
        return messages.success_message('reset password email successfully sent'), 201
    except smtplib.SMTPException as e:
        return messages.error_message('could not perform your reset password request', str(e)), 500


def set_new_user_password(request_=None):
    user = get_user_object_by_reset_hash(request_.args.get('h'))
    return update_user(user_id=user.id, fields=request_.form)
