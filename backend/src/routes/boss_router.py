from flask import Blueprint
from database.models import Institutional, Postulation
from validator.program import ProgramSchema
from validator.postulation import UpdateSchema
from middleware.validate_token import token_required
from middleware.validate_request import required_params

boss_rest = Blueprint("boss_rest", __name__)
instanceInstitutional = Institutional.Institutional()
instancePostulation = Postulation.Postulation()


@boss_rest.route("/semesters/students", methods=["POST"])
@token_required
@required_params(ProgramSchema())
def studentsOfPeriod(_):
    return instanceInstitutional.studentsOfPeriod()


@boss_rest.route("/postulation/update", methods=["PUT"])
@token_required
def updatePostulation(_):
    return instancePostulation.updatePostulationByBoss()

@boss_rest.route("/semesters/")
@boss_rest.route("/semesters/<program>")
@token_required
def semestersByProgram(_, program=None):
    return instanceInstitutional.getSemestersByProgram(program)

@boss_rest.route("/courses/")
@boss_rest.route("/courses/<semester>/<program>")
@token_required
def coursesBySemester(_, semester=None, program=None):
    return instanceInstitutional.getCoursesBySemester(semester, program)

@boss_rest.route("/courses/groups/")
@boss_rest.route("/courses/groups/<program>/<course>")
@token_required
def groupsOfCourse(_, program=None, course=None):
    return instanceInstitutional.getGroupsOfCourse(course, program)

@boss_rest.route("/courses/group/")
@boss_rest.route("/courses/group/<program>/<course>/<group>")
@token_required
def group(_, program=None, course=None, group=None):
    return instanceInstitutional.getGroup(course, program, group)
