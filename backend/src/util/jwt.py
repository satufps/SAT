import datetime
from flask import jsonify
import jwt
from util import environment, response

def generateToken(payload, expireIn):
    token = jwt.encode({'payload': payload, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=expireIn)}, environment.SECRET_JWT)  
    return token


def renewToken(current_user):
        token = generateToken(current_user, 60)
        return response.success("Identificado!!", current_user, token)
    
def validateUserAuth(current_user, role):
    res = True
    if role:
        roleAuth = current_user["rol"]
        if role == "administrativo":
            res = roleAuth in ["psicologo", "medico", "odontologo", "vicerrector"]
        elif role == "institucional":
            res = roleAuth in ["estudiante", "docente", "jefe"]
        elif role == "docente":
            res = roleAuth in ["docente", "jefe"]
        else:
            res = roleAuth == role
    return jsonify(res)
    