from flask import Flask
from flask_cors import CORS
from middleware.validate_token import token_required, validate_token
from routes.institutonal_router import institutional_rest
from routes.administrative_router import administrative_rest
from routes.notification_router import notification_rest
from routes.boss_router import boss_rest
from routes.student_router import student_rest
from routes.teacher_router import teacher_rest
from routes.chat_router import chat_rest
from routes.chatAdmin_router import chat_admin_rest
from routes.wellness_router  import wellness_rest
from routes.meet_router  import meet_rest
from routes.binnacle_router  import binnacle_rest
from routes.suggestion_router  import suggestion_router
from routes.report_router  import report_router
from routes.role_router  import role_router
from routes.risk_router  import risk_router
from routes.activity_router import activity_router
from util import environment, jwt
from database import config

app = Flask(__name__, static_url_path='/app/backend/src/static')
app.config["MONGO_URI"]= environment.MONGO_URL
app.config['UPLOAD_FOLDER'] = environment.UPLOAD_FOLDER
config.mongo.init_app(app)

CORS(app)

# JWT
app.config["SECRET_KEY"] = environment.SECRET_JWT

# Rutas
app.register_blueprint(institutional_rest, url_prefix='/auth/institutional')
app.register_blueprint(administrative_rest, url_prefix='/auth/administrative')
app.register_blueprint(student_rest, url_prefix='/students')
app.register_blueprint(teacher_rest, url_prefix='/teachers')
app.register_blueprint(boss_rest, url_prefix='/boss')
app.register_blueprint(chat_rest, url_prefix='/chat')
app.register_blueprint(chat_admin_rest, url_prefix='/chatAdmin')
app.register_blueprint(notification_rest, url_prefix='/notification')
app.register_blueprint(wellness_rest, url_prefix='/wellness')
app.register_blueprint(meet_rest, url_prefix='/meet')
app.register_blueprint(binnacle_rest, url_prefix='/binnacle')
app.register_blueprint(suggestion_router, url_prefix='/suggestion')
app.register_blueprint(report_router, url_prefix='/report')
app.register_blueprint(role_router, url_prefix='/role')
app.register_blueprint(risk_router, url_prefix='/risk')
app.register_blueprint(activity_router, url_prefix='/activity')

@app.route("/auth/renew")
@token_required
def renew(current_user):
    return jwt.renewToken(current_user)

@app.route("/auth/validate-token/")
@app.route("/auth/validate-token/<role>")
@validate_token
def validateUserAuth(current_user, role=None):
    return jwt.validateUserAuth(current_user, role)

@app.route("/")
def ping():
    return "Todo ok!"

# Lanzar servidor
if __name__ == "__main__":
    app.run(debug=True, port=environment.PORT, host="0.0.0.0")
