from flask import Blueprint
from validator.auth import AdministrativeSchema, LoginSchema, ChangePasswordSchema, EmailRecoverySchema, RecoveryPasswordSchema
from middleware.validate_token import token_required
from middleware.validate_request import required_params
from database.models import Administrative

instance = Administrative.Administrative()

administrative_rest = Blueprint("administrative_rest", __name__)    

@administrative_rest.route("/login", methods=["POST"])
@required_params(LoginSchema())
def login():
    return instance.login()

@administrative_rest.route("/register", methods=["POST"])
@token_required
@required_params(AdministrativeSchema())
def register(_):
    return instance.register()
  
@administrative_rest.route("/change-password", methods=["PUT"])
@token_required
@required_params(ChangePasswordSchema())
def changePassword(_):
    return instance.changePassword()

@administrative_rest.route("/recovery-password", methods=["POST"])
@required_params(EmailRecoverySchema())
def sendMailRecoveryPassword():
    return instance.sendMailRecoveryPassword()

@administrative_rest.route("/recovery-password", methods=["PUT"])
@token_required
@required_params(RecoveryPasswordSchema())
def recoveryPassword(email):
    return instance.recoveryPassword(email["email"])

@administrative_rest.route("/change-phone", methods=["PUT"])
@token_required
def updatePhone(user):
    return instance.updatePhone(user)
