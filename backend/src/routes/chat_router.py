from flask import Blueprint
from database.models import Chat
from middleware.validate_request import required_params
from middleware.validate_token import token_required
from validator.chat import ChatSchema, ReceiverSchema

instance = Chat.Chat()

chat_rest = Blueprint("chat_rest", __name__)


@chat_rest.route("/", methods=["POST"])
@token_required
@required_params(ChatSchema())
def sendMessage(userAuth):
    return instance.sendMessage(userAuth)

@chat_rest.route("/messages", methods=["POST"])
@token_required
@required_params(ReceiverSchema())
def getChat(userAuth):
    return instance.listChat(userAuth)