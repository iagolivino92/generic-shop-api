from flask import jsonify
from utils import messages


def format_users(users):
    users_ = []
    for user in users:
        user_data = {'id': user.id,
                     'email': user.email,
                     'contact': user.contact,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'role': user.role,
                     'shop_id': user.shop_id}
        users_.append(user_data)
    return jsonify(users_), 200


def format_user(user):
    try:
        user_data = {'id': user.id,
                     'email': user.email,
                     'contact': user.contact,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'role': user.role,
                     'shop_id': user.shop_id}
    except AttributeError as e:
        return messages.error_message('user does not exist', str(e)), 404
    return jsonify(user_data), 200


def format_shops(shops):
    shops_ = []
    for shop in shops:
        shop_data = {'id': shop.id,
                     'email': shop.email,
                     'contact': shop.contact,
                     'shop_name': shop.shop_name,
                     'address': shop.address}
        shops_.append(shop_data)
    return jsonify(shops_), 200


def format_shop(shop):
    try:
        shop_data = {'id': shop.id,
                     'email': shop.email,
                     'contact': shop.contact,
                     'shop_name': shop.shop_name,
                     'address': shop.address}
    except AttributeError as e:
        return messages.error_message('shop does not exist', str(e)), 204
    return jsonify(shop_data), 200


def format_join_requests(join_requests):
    join_requests_ = []
    for join_request in join_requests:
        join_data = {'id': join_request.id,
                     'shop_id': join_request.shop_id,
                     'creation_date': join_request.creation_date,
                     'processed_by': join_request.processed_by,
                     'data': join_request.data,
                     'status': join_request.status}
        join_requests_.append(join_data)
    return jsonify(join_requests_), 200


def format_join_request(join_request):
    try:
        join_data = {'id': join_request.id,
                     'shop_id': join_request.shop_id,
                     'creation_date': join_request.creation_date,
                     'processed_by': join_request.processed_by,
                     'data': join_request.data,
                     'status': join_request.status}
    except AttributeError as e:
        return messages.error_message('join request does not exist', str(e)), 204
    return jsonify(join_data), 200


def format_keys(keys):
    _keys = []
    for key in keys:
        key_data = {'id': key.id,
                    'shop_id': key.shop_id,
                    'hash': key.hash,
                    'join_id': key.join_request_id}
        _keys.append(key_data)
    return jsonify(_keys), 200


def format_key(key):
    try:
        key_data = {'id': key.id,
                    'shop_id': key.shop_id,
                    'hash': key.hash,
                    'join_id': key.join_request_id}
    except AttributeError as e:
        return messages.error_message('api key does not exist', str(e)), 204
    return jsonify(key_data), 200


def sales_base(sale):
    return {
        'id': sale.id,
        'creation_date': sale.creation_date,
        'last_update_date': sale.last_update_date,
        'value': sale.value,
        'rate': sale.rate,
        'commission': sale.commission,
        'status': sale.status
    }


def format_sales(sales):
    _sales = []
    for sale in sales:
        _sales.append(sales_base(sale))
    return jsonify(_sales), 200


def format_sale(sale):
    try:
        return jsonify(sales_base(sale)), 200
    except AttributeError as e:
        return messages.error_message('api key does not exist', str(e)), 204


def format_reset_password_email(user):
    template = open('email_template.html')
    template_content = template.read()
    template.close()

    return template_content.replace("{userName}", " ".join([user.first_name, user.last_name]))\
        .replace("{hash_}", user.reset_hash)
