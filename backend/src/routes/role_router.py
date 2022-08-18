from flask import Blueprint
from middleware.validate_request import required_params
from middleware.validate_token import token_required
from database.models import Role
from validator.role import RolSchema

instance = Role.Role()
role_router = Blueprint("role_router", __name__)

@role_router.route("/", methods=["POST"])
@required_params(RolSchema())
def createRole():
    return instance.createRole()

@role_router.route("/")
def listRoles():
    return instance.listRoles();

@role_router.route("/schedule", methods=["PUT"])
@token_required
def updateSchedule(_):
    return instance.updateSchedule()

@role_router.route("/schedule")
@role_router.route("/schedule/<role>")
@token_required
def getSchedule(_, role=None):
    return instance.getSchedule(role)

@role_router.route("/schedule/role")
@role_router.route("/schedule/role/<role>/<date>")
@token_required
def getScheduleOfRole(_, role=None, date=None):
    return instance.getScheduleOfRole(role, date) 
