from flask import Blueprint, request
from middleware.validate_token import token_required
from middleware.validate_request import required_params
from validator.postulation import FilterPostulation, PostulationSchema, PostulateSchema
from database.models import Institutional
from database.models import Postulation

instance_institutional = Institutional.Institutional()
instance_postulation = Postulation.Postulation()

student_rest = Blueprint("student_rest", __name__)

@student_rest.route("/")
@student_rest.route("/<code>")
@token_required
def getStudent(_, code = None):
    return instance_institutional.getByCode(code, "student")

@student_rest.route("/course/")
@student_rest.route("/course/<code>")
@token_required
def getCourses(_,code = None):
    return instance_institutional.getMyCoursesStudent(code)

@student_rest.route("/postulate", methods=["POST"])
@token_required
@required_params(PostulationSchema())
def postulateStudent(_):
    return instance_postulation.generatePostulation()

@student_rest.route("/postulate/validate", methods=["POST"])
@token_required
@required_params(PostulateSchema())
def validatePostulation(_):
    return instance_postulation.validatePostulation()

@student_rest.route("/profits/")
@student_rest.route("/profits/<code>/<risk>")
@token_required
def getProfits(_, code=None, risk=None):
    return instance_institutional.getProfits(code, risk)

@student_rest.route("/profits/risk")
@token_required
def adminProfits(_):
    return instance_institutional.adminProfits()

@student_rest.route("/postulate")
@token_required
def paginatePostulation(userAuth):
    return instance_postulation.paginatePostulations(userAuth)

@student_rest.route("/postulate/filter", methods=["POST"])
@token_required
@required_params(FilterPostulation())
def filterPostulation(_):
    return instance_postulation.filterPostulations()

@student_rest.route("/postulate/counter")
@token_required
def countPostulation(userAuth):
    return instance_postulation.countPostulation(userAuth["rol"])

@student_rest.route("/semesters")
@student_rest.route("/semesters/<code>")
@token_required
def getSemesters(_, code=None):
    return instance_institutional.getSemesters(code)