from flask import Blueprint
from middleware.validate_token import token_required
from database.models import Institutional

instance = Institutional.Institutional()
teacher_rest = Blueprint("teacher_rest", __name__)

@teacher_rest.route("/")
@teacher_rest.route("/<code>")
@token_required
def getTeacher(_,code = None):
    return instance.getByCode(code, "teacher")

@teacher_rest.route("/course/")
@teacher_rest.route("/course/<code>")
@token_required
def getCourses(_,code = None):
    return instance.getMyCoursesTeacher(code)

@teacher_rest.route("/course/students/")
@teacher_rest.route("/course/students/<code>/<group>")
@token_required
def getStudentsOfCourse(_, code=None, group=None):
    return instance.getStudentsOfCourse(code, group)

@teacher_rest.route("/course/notes", methods=["POST"])
@token_required
def getNotesOfCourse(_):
    return instance.getNotesOfCourse()

