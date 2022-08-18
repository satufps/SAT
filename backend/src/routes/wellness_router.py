from flask import Blueprint
from middleware.validate_token import token_required
from database.models import Administrative, Postulation

wellness_rest = Blueprint("wellness_rest", __name__)

instanceAdministrativo = Administrative.Administrative()
instancePostulation = Postulation.Postulation()


@wellness_rest.route("/faculties")
@token_required
def getFaculties(_):
    return instanceAdministrativo.getFaculties()


@wellness_rest.route("/")
@wellness_rest.route("/<code>")
@token_required
def getStudent(_, code=None):
    return instanceAdministrativo.getByCode(code)


@wellness_rest.route("/postulations")
@token_required
def paginatePostulationsWellness(_):
    return instancePostulation.paginatePostulationsWellness()

@wellness_rest.route("/postulation/")
@wellness_rest.route("/postulation/<id>")
@token_required
def getPostulationById(_, id=None): 
    return instancePostulation.getPostulationById(id)

@wellness_rest.route("/semester/program")
@wellness_rest.route("/semester/program/<nameProgram>")
@token_required
def validateProgram(_, nameProgram=None):
    return instanceAdministrativo.validateProgram(nameProgram)

@wellness_rest.route("/profits")
@token_required
def getProfits(_):
    return instanceAdministrativo.getProfits()

