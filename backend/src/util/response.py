from flask import jsonify


def success(msg, data, token):
    response = {
        "ok":True,
        "msg": msg,
        "data":data
    }
    if token:
        response = {
            **response,
            "token":token
        }
    return response
    
def error(msg, status):
    return jsonify({
        "ok":False,
        "msg": msg
        }), status 
    
def reject(msg):
    return jsonify({
        "ok": False,
        "msg": msg
    })