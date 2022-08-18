from flask import Blueprint
from middleware.validate_token import token_required
from middleware.validate_request import required_params
from database.models import Suggestion
from validator.suggestion import SuggestionSchema, ResponseSuggestion,FilterSuggestion

instance = Suggestion.Suggestion()
suggestion_router = Blueprint("suggestion_router", __name__)

@suggestion_router.route("/", methods=["POST"])
@token_required
@required_params(SuggestionSchema())
def createSuggestion(user):
    return instance.createSuggestion(user)

@suggestion_router.route("/paginate")
@token_required
def paginateSuggestion(_):
    return instance.paginateSuggestion()

@suggestion_router.route("/filter", methods=["POST"])
@token_required
@required_params(FilterSuggestion())
def filterSuggestion(_):
    return instance.filterSuggestion()

@suggestion_router.route("/response", methods=["PUT"])
@token_required
@required_params(ResponseSuggestion())
def responseSuggestion(_):
    return instance.responseSuggestion()

