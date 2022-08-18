from flask import Blueprint
from middleware.validate_token import token_required
from database.models import Report

instance = Report.Report()
report_router = Blueprint("report_router", __name__)

@report_router.route("/suggestion", methods=["POST"])
@token_required
def generateReportSuggestion(_):
    return instance.generateReportSuggestion()

@report_router.route("/suggestion/last")
@token_required
def getLastReport(_):
    return instance.getLastReport()