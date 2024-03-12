"""
Do not use 'object' methods to return shop details. Always use 'data.format' methods instead.
"""
from sqlalchemy import func

from api import data
from utils import messages
from database.models import Sale
from api import db


def get_all(start=None, end=None):
    if start and end:
        return data.format_sales(Sale.query.filter(func.date(Sale.creation_date) >= start).filter(func.date(Sale.creation_date) <= end).all())
    return data.format_sales(Sale.query.all())


def get_all_objects():
    return Sale.query.all()


def get_sale_by_id(sale_id):
    return data.format_sale(get_sale_object_by_id(sale_id))


def get_sales_by_user_id(user_id):
    return data.format_sales(get_sales_object_by_user_id(user_id))


def get_sale_object_by_id(sale_id):
    return Sale.query.filter_by(id=sale_id).first()


def get_sales_object_by_user_id(user_id):
    return Sale.query.filter_by(user_id=user_id).all()


def create_sale(data):
    try:
        new_sale = Sale(
            user_id=int(data.get('user_id')),
            value=data.get('value'),
            rate=data.get('rate'),
            commission=data.get('commission'),
            status='pending'
        )
    except Exception as e:
        return messages.error_message('could not create sale object', str(e)), 400
    try:
        db.session.add(new_sale)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not add sale in database', str(e)), 500
    return messages.success_message('sale successfully added'), 201


def delete_sale(sale_id):
    try:
        sale = Sale.query.filter_by(id=sale_id).first()
    except Exception as e:
        return messages.error_message('could not find sale in database', str(e)), 404
    try:
        db.session.delete(sale)
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not delete sale from database', str(e)), 500
    return messages.success_message('sale successfully deleted'), 201


def update_sale(sale_id, fields):
    error = ''
    try:
        sale = get_sale_object_by_id(sale_id)
    except Exception as e:
        return messages.error_message('could not find sale in database', str(e)), 404
    for field in fields:
        try:
            globals()['update_' + field](sale, fields[field])
        except Exception as e:
            error += f'field {field} could not be updated (err: {str(e)})\n'
    if error:
        return messages.error_message('could not update sale', error), 403
    try:
        sale.last_update_date = func.now()
        db.session.commit()
    except Exception as e:
        return messages.error_message('could not save sale updates in database', str(e)), 500
    return messages.success_message('sale successfully updated'), 201


def update_status(sale, value):
    sale.status = value


def update_value(sale, value):
    sale.value = value


def update_rate(sale, value):
    sale.rate = value


def update_commission(sale, value):
    sale.commission = value
