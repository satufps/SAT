from flask import Blueprint
from middleware.validate_token import token_required
from database.models import Risk

instance = Risk.Risk()
risk_router = Blueprint("risk_router", __name__)

@risk_router.route("/")
@risk_router.route("/<code>")
@token_required
def getRisks(_, code=None):
    return instance.getRisks(code)

@risk_router.route("/calulateStatistics", methods=["POST"])
@token_required
def getStatisticsTotal(_):
    return instance.getStatisticsTotal()

@risk_router.route("/courses/ac012/")
@risk_router.route("/courses/ac012/<code>")
@token_required
def coursesAc012(_, code):
    return instance.coursesAc012(code)

