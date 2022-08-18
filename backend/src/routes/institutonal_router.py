from flask import Blueprint
from validator.auth import InstitutionalSchema
from middleware.validate_request import required_params
from middleware.validate_token import token_required
from database.models import Institutional

instance_institutional = Institutional.Institutional()

institutional_rest = Blueprint("institutional_rest", __name__)

@institutional_rest.route("/login", methods=["POST"])
@required_params(InstitutionalSchema())
def login():
    return instance_institutional.login()

@institutional_rest.route("/login-google", methods=["POST"])
def loginGoogle():
    return instance_institutional.loginGoogle()

@institutional_rest.route("/update-photo", methods=["PUT"])
@token_required
def updateProfilePhoto(userAuth):
    return instance_institutional.updateProfilePhoto(userAuth)

@institutional_rest.route("/record", methods=["POST"])
@token_required
def saveRecord(_):
    return instance_institutional.saveRecord() 

@institutional_rest.route("/record")
@institutional_rest.route("/record/<code>/<type>")
@token_required
def getRecords(_, code=None, type=None):
    return instance_institutional.getRecords(code, type)






