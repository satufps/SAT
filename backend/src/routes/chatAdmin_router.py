from flask import Blueprint
from database.models import ChatAdmin
from middleware.validate_token import token_required
from middleware.validate_request import required_params
from validator.chat import ChatSchema, UsersChat

instance = ChatAdmin.ChatAdmin()
chat_admin_rest = Blueprint("chat_admin_rest", __name__)

@chat_admin_rest.route("/")
@chat_admin_rest.route("/<role>")
@token_required
def getAdminsByRole(_, role=None):
    return instance.getAdminsByRole(role);

@chat_admin_rest.route("/admin/")
@chat_admin_rest.route("/admin/<document>")
@token_required
def getAdminByDocument(_, document=None):
    return instance.getAdminByDocument(document);

@chat_admin_rest.route("/", methods=["POST"])
@token_required
@required_params(ChatSchema())
def sendMessage(_):
    return instance.sendMessage();

@chat_admin_rest.route("/list", methods=["POST"])
@token_required
@required_params(UsersChat())
def listChat(_):
    return instance.listChat();

