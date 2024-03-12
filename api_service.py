from flask import request
from flask_cors import CORS
from api import *
from api import auth
from api.auth import admin_token_required, mgr_token_required, read_token_required, api_key_required, \
    emp_token_required, reset_hash_required
from database import user_utils, shop_utils, join_request_utils, employee_utils, key_utils, sale_utils

app = create_app()
CORS(app)


@app.route('/api/v1/token', methods=['POST', 'DELETE'])
def get_token():
    if request.method == 'DELETE':
        return auth.clear_token(request.headers['authorization'])
    try:
        return auth.token_login(request.headers['authorization'])
    except KeyError as e:
        print(e)
    return auth.credentials_login(request)


@app.route('/api/v1/users')
@mgr_token_required
def get_users():
    return user_utils.get_all()


@app.route('/api/v1/user/<id>', methods=['GET', 'DELETE', 'PATCH'])
@mgr_token_required
def get_user_by_id(id):
    if request.method == 'GET':
        return user_utils.get_user_by_id(id)
    if request.method == 'PATCH':
        return user_utils.update_user(user_id=id, fields=request.form)
    return user_utils.delete_user(id)


@app.route('/api/v1/user', methods=['GET', 'PUT'])
def get_user_by_token():
    if request.method == 'GET':
        if request.args.get('token'):
            return user_utils.get_user_by_token(request.args.get('token'))
        else:
            return user_utils.get_user_by_email(request.args.get('email'))

    mgr_token_required(mgr_token_required)
    return user_utils.create_user(request.form)


@app.route('/api/v1/user/reset-password', methods=['POST'])
def reset_user_password():
    return user_utils.send_user_reset_password_email(request.form)


@app.route('/api/v1/user/set-new-password', methods=['POST', 'DELETE'])
@reset_hash_required
def set_user_new_password():
    if request.method == "DELETE":
        return auth.clear_reset_hash(request.args.get('h'))
    return user_utils.set_new_user_password(request_=request)


@app.route('/api/v1/users/shop/<shop_id>')
@mgr_token_required
def get_users_by_shop(shop_id):
    return user_utils.get_users_by_shop(shop_id)


@app.route('/api/v1/shops', methods=['GET', 'PUT'])
@admin_token_required
def get_shops():
    if request.method == 'GET':
        return shop_utils.get_all()
    return shop_utils.create_shop(request.form)


@app.route('/api/v1/shop/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
@mgr_token_required
def get_shop(id):
    if request.method == 'DELETE':
        return shop_utils.delete_shop(id)
    if request.method == 'PATCH':
        return shop_utils.update_shop(id, request.form)
    return shop_utils.get_shop_by_id(id)


@app.route('/api/v1/shop/<name>')
@api_key_required
def get_shop_by_name(name):
    return shop_utils.get_shop_by_name(name)


@app.route('/api/v1/join-requests')
@mgr_token_required
def get_join_requests():
    return join_request_utils.get_all()


@app.route('/api/v1/join-requests/shop/<shop_id>')
@mgr_token_required
def get_join_requests_by_shop(shop_id):
    return join_request_utils.get_join_requests_by_shop(shop_id)


@app.route('/api/v1/join-request/<id>', methods=['GET', 'PATCH'])
@mgr_token_required
def get_join_request(id):
    if request.method == 'GET':
        return join_request_utils.get_join_request(id)
    return join_request_utils.update_join_request(id, request.form)


@app.route('/api/v1/create-join-request', methods=['PUT'])
@api_key_required
def update_or_create_join_request():
    return join_request_utils.create_join_request(request)


@app.route('/api/v1/shop/keys/<int:shop_id>')
@mgr_token_required
def get_shop_keys(shop_id):
    return key_utils.get_keys_by_shop(shop_id)


@app.route('/api/v1/shop/key/<int:key_id>', methods=['GET', 'DELETE'])
@mgr_token_required
def get_key_by_id(key_id):
    if request.method == 'DELETE':
        return key_utils.remove_key(key_id)
    return key_utils.get_key_by_id(key_id)


@app.route('/api/v1/keys', methods=['GET', 'POST'])
@mgr_token_required
def get_all_keys():
    if request.method == 'POST':
        return key_utils.create_key(request.form)
    return key_utils.get_keys()


@app.route('/api/v1/key/<k_hash>')
def key_exists(k_hash):
    return key_utils.get_key_by_hash(k_hash)


@app.route('/api/v1/employees', methods=['GET', 'PUT'])
@read_token_required
def get_employees():
    if request.method == 'GET':
        return employee_utils.get_all()
    return user_utils.create_user(request.form)


@app.route('/api/v1/employee/<id>', methods=['GET', 'DELETE', 'PATCH'])
@read_token_required
def get_employee_by_id(id):
    if request.method == 'GET':
        return employee_utils.get_employee_by_id(id)
    if request.method == 'PATCH':
        return user_utils.update_user(user_id=id, fields=request.form)
    return user_utils.delete_user(id)


@app.route('/api/v1/employees/shop/<shop_id>')
@read_token_required
def get_employees_by_shop(shop_id):
    return employee_utils.get_employees_by_shop(shop_id)


@app.route('/api/v1/sales', methods=['GET', 'POST'])
@emp_token_required
def get_sales():
    if request.method == 'GET':
        return sale_utils.get_all(start=request.args.get('s'), end=request.args.get('e'))
    return sale_utils.create_sale(request.form)


@app.route('/api/v1/sale/<sale_id>', methods=['GET', 'PATCH', 'DELETE'])
@emp_token_required
def get_sale(sale_id):
    if request.method == 'GET':
        return sale_utils.get_sale_by_id(sale_id)
    if request.method == 'DELETE':
        return sale_utils.delete_sale(sale_id)
    return sale_utils.update_sale(sale_id, request.form)


@app.route('/api/v1/sales/user/<user_id>')
@emp_token_required
def get_sale_by_user_id(user_id):
    # add verification for who is requesting it. if emp, can only see its own sales.
    return sale_utils.get_sales_by_user_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        user_utils.create_admin_instance()
    app.run()
