import jwt
from flask import request, jsonify
from functools import wraps
from util import response, environment

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-token" in request.headers:
            token = request.headers["x-token"]
            
        if not token:
            return response.reject("a valid token is missing")
        
        try:
          data = jwt.decode(token, environment.SECRET_JWT, algorithms=["HS256"])
          current_user = data["payload"] 
        except:
            return response.reject("token is invalid")
        return f(current_user, *args, **kwargs)
    return decorator

def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-token" in request.headers:
            token = request.headers["x-token"]
        if not token:
            return jsonify(False)
        try:
          data = jwt.decode(token, environment.SECRET_JWT, algorithms=["HS256"])
          current_user = data["payload"] 
        except:
            return jsonify(False)
        return f(current_user, *args, **kwargs)
    return decorator
          