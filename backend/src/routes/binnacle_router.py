from flask import Blueprint
from validator.binnacle import BinnacleSchema
from middleware.validate_token import token_required
from middleware.validate_request import required_params
from database.models import Binnacle


binnacle_rest = Blueprint("binnacle_rest", __name__)
instance = Binnacle.Binnacle()

@binnacle_rest.route("/", methods=["POST"])
@token_required
@required_params(BinnacleSchema())
def toWriter(_):
    return instance.toWriter()

@binnacle_rest.route("/")
@binnacle_rest.route("/<code>")
@token_required
def getBinnacle(_, code=None):
    return instance.getBinnacle(code)
