from flask import Blueprint
from middleware.validate_token import token_required
from database.models import Activity


instance = Activity.Activity()
activity_router = Blueprint("activity_router", __name__)

@activity_router.route("/", methods=["POST"])
def createActivity():
    return instance.createActivity()

@activity_router.route("/")
def listRoles():
    return instance.listActivities();

@activity_router.route("/activities-student")
@token_required
def listActivitiesStundent(student):
    return instance.listActivitiesStudent(student["codigo"]); 

@activity_router.route("/asist", methods=["POST"])
@token_required
def asistActivity(student):
    return instance.asistActivity(student["codigo"])

@activity_router.route("/asist/")
@activity_router.route("/asist/<code>")
@token_required
def getActivitysAsist(_, code=None):
    return instance.getActivitysAsist(code)

@activity_router.route("/desactive/")
@activity_router.route("/desactive/<id>")
@token_required
def desactiveActivity(_, id=None):
    return instance.desactiveActivity(id)

@activity_router.route("/", methods=["PUT"])
@token_required
def updateActivity(_):
    return instance.updateActivity()

@activity_router.route("/download/")
@activity_router.route("/download/<id>")
@token_required
def download(_, id=None):
    return instance.download(id)




