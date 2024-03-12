from flask import jsonify


def error_message(msg='', err=''):
    return jsonify("{'success':false, 'message':'%s', 'error':'%s'}" % (msg, err))


def success_message(msg=''):
    return jsonify("{'success':true, 'message':'%s'}" % msg)


def warning_message(msg='', warn=''):
    return jsonify("{'success':warning, 'message':'%s', 'warning':'%s'}" % (msg, warn))
