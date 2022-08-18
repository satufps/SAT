from flask import Blueprint
from database.models import Notification
from middleware.validate_request import required_params
from validator.notification import NotificationSchema

from middleware.validate_token import token_required

instance = Notification.Notification()

notification_rest = Blueprint("notification_rest", __name__)

@notification_rest.route("/", methods=["POST"])
@token_required
@required_params(NotificationSchema())
def createNotification(_):
    return instance.sendNotification()

@notification_rest.route("/")
@notification_rest.route("/<code>")
@token_required
def listNotification(_, code=None):
    return instance.getNotifications(code)

@notification_rest.route("/", methods=["PUT"])
@notification_rest.route("/<id>", methods=["PUT"])
@token_required
def updateNotification(_, id=None):
    return instance.updateNotification(id)

@notification_rest.route("/", methods=["DELETE"])
@notification_rest.route("/<id>", methods=["DELETE"])
@token_required
def deleteNotification(_, id=None):
    return instance.deleteNotification(id)