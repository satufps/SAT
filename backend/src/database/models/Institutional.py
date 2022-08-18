import os, uuid
from bson import json_util
from bson.objectid import ObjectId
from flask import request, Response
from util import jwt, response, environment, helpers
from database import config
from util.request_api import request_ufps, request_ufps_token
from werkzeug.utils import secure_filename

mongo = config.mongo


class Institutional:
    
    def login(self):
        info = request.get_json()
        code = info["code"]
        role = info["role"]
        endpoint = f"{role}_{code}"
        try:
            req = request_ufps().get(f"{environment.API_URL}/{endpoint}")
            data = req.json()
            if data["ok"]:
                user = data["data"]
                del user["contrasena"]
                token = jwt.generateToken(user, 60)
                return response.success("Bienvenido!!", user, token)
            else:
                return response.error("Revise los datos ingresados", 401)
        except:
            return response.error("Revise los datos ingresados", 401)
        
    def loginGoogle(self):
        correo = request.json["correo"]
        rol = request.json["rol"]
        endpoint = f"/{rol}/email/{correo}"
        try: 
            req = request_ufps().get(f"{environment.API_UFPS}/{endpoint}")
            data = req.json()
            print(data)
            if data["ok"]: 
                data = data["data"]
                rol = "estudiante" if rol == "student" else "docente"
                if data["rol"] != rol:
                    return response.error(f"No tiene acceso como {rol}", 401)
                code = data["codigo"]
                filename = self.getPhoto(code) 
                if filename:
                    path = os.path.join(environment.UPLOAD_FOLDER, filename)
                    path = f"{request.host_url}{path[1:]}"
                else:
                    path = None
                auxRole = "jefe" if correo == "judithdelpilarrt@ufps.edu.co" else data["rol"]
                user = {
                    **data,
                    "foto": path,
                    "rol": auxRole,
                }
                token = jwt.generateToken(user, 60)
                return response.success("Bienvenido!!", user, token)
            else:
                return response.error("Revise los datos ingresados", 401)
        except:
            return response.error("Revise los datos ingresados", 401)
        
    def updateProfilePhoto(self, userAuth):
        try:
            if 'file' not in request.files:
                return response.error("No se envio un archivo", 401)
            file = request.files['file'] 
            if file.filename == '':
                return response.error("Ningún archivo seleccionado", 401)
            if file and helpers.allowed_file(file.filename):
                ext = file.filename.split(".")[1]
                file.filename = f"{str(uuid.uuid4())}.{ext}"
                filename = secure_filename(file.filename)
                path = os.path.join(environment.UPLOAD_FOLDER, filename)
                file.save(path)  
                user = userAuth["codigo"] if userAuth["rol"]=="estudiante" or userAuth["rol"]=="docente" else userAuth["documento"]
                photo = self.getPhoto(user)
                if photo: 
                    os.remove(os.path.join(environment.UPLOAD_FOLDER, photo))
                    mongo.db.photo.update_one({"user":user}, {"$set": {"filename":filename}}) 
                else:
                    mongo.db.photo.insert_one({"user":user, "filename": filename})
                token = ""
                photo = f"{request.host_url}{path[1:]}"
                if userAuth["rol"]=="estudiante":
                    pass
                else:
                    userAuth = { **userAuth, "foto": photo }
                    token = jwt.generateToken(userAuth, 60)
                return response.success("Todo ok!", photo, token)
        except Exception as e:
            print(e)
            return response.reject("Hable con el Administrador")
    
    def getPhoto(self, code):
        record = mongo.db.photo.find_one({"user": code},{"filename":1, "_id": False,"total":1})  
        return record["filename"] if record else None

    def getByCode(self, code, role): 
        try:
            endpoint = f"/{role}/code/{code}"
            req = request_ufps_token().get(f"{environment.API_UFPS}/{endpoint}")
            data = req.json()
            if data["ok"]:
                filename = self.getPhoto(code)
                if filename:
                    path = os.path.join(environment.UPLOAD_FOLDER, filename)
                    path = f"{request.host_url}{path[1:]}" 
                else:  
                    path = None
                msg = data["msg"]
                data = data["data"] 
                data = { **data, "foto": path } 
                return response.success(msg, data, "")
            else:
                return response.error(data["msg"], 200)
        except:
            return response.reject("Hable con el Administrador")

    def getMyCoursesStudent(self, code):
        if not code or not code.isdigit() or len(code) != 7:
            return response.reject("Se necesita un código de 7 caracteres")
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/student/courses/{code}")  
            res = req.json()
            if res["ok"]:
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")

    def getMyCoursesTeacher(self, code):
        if not code or not code.isdigit() or len(code) != 5:
            return response.reject("Se necesita un código de 5 caracteres")
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/teacher/courses/{code}")  
            res = req.json()
            if res["ok"]:
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")

    def getNotesOfCourse(self):
        course = request.json["code"]
        group = request.json["group"]
        exam = request.json["exam"]
        req = request_ufps().get(f"{environment.API_URL}/nota_{exam}")
        res = req.json()
        return response.success("Todo ok!", res, "")

    def getStudentsOfCourse(self, code, group):
        try:
            page = int(request.args.get("page")) or 1
            limit = int(request.args.get("limit")) or 15
            filter = request.args.get("filter") or ""
            req = request_ufps_token().get(f"{environment.API_UFPS}/teacher/students-course/{code}/{group}", params={"page":page, "limit":limit, "filter":filter})
            res = req.json()
            if res["ok"]: 
                students = res["data"]["students"]
                for student in students:
                    filename = self.getPhoto(code)
                    if filename:
                        path = os.path.join(environment.UPLOAD_FOLDER, filename)
                        path = f"{request.host_url}{path[1:]}"
                    else:
                        path = None
                    student["foto"] = path
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")

    def getProfits(self, code, risk):
        if not code or not code.isdigit() or len(code) != 7:
            return response.error("Se necesita un código de 7 caracteres", 400)
        req = request_ufps().get(f"{environment.API_URL}/beneficios_{code}")
        data = list(req.json())
        profits = list(
            mongo.db.profit.find({"riesgo": risk}, {"nombre": 1, "_id": False})
        )
        array = []
        for key in profits:
            array.append(key["nombre"])
        aux = list(filter(lambda profit: profit["nombre"] in array, data))
        return response.success("todo ok", aux, "")
    
    def adminProfits(self):
        code = request.args.get("code")
        risk = request.args.get("risk")
        req = request_ufps().get(f"{environment.API_URL}/beneficios_{code}")
        dataUFPS = list(req.json())
        profits = list(filter(lambda profit: not profit["fechaFinal"], dataUFPS))
        profits = list(map(lambda profit : profit["nombre"], profits))
        if len(profits) > 0:
            self.updateReviewSuggestion(profits, code)
        profitsDB = list(mongo.db.profit.find({"riesgo": risk}))
        suggestion = list(mongo.db.suggestion.find({"codeStudent":code, "state":True}, {"profit":1, "_id": False})) 
        responseProfit = list(mongo.db.suggestion.find({"codeStudent":code, "state":False, "response": True}, {"profit":1, "_id": False})) 
        responseCurrent = self.getResponse(dataUFPS, responseProfit, code)
        data = list(map(lambda profit : {"nombre": profit["nombre"], "state": profit["nombre"] in profits, "id":str(profit["_id"]), "isSuggested": {"profit":profit["_id"]} in suggestion, "response": {"profit":profit["_id"]} in responseCurrent }, profitsDB))
        return response.success("Todo ok!", data, "")
    
    def updateReviewSuggestion(self, profits, code):
        profits = list(map(lambda profit : mongo.db.profit.find_one({"nombre": profit}, { "total":1, "_id": 1})["_id"], profits))
        try:
            mongo.db.suggestion.update_many(
            {"codeStudent":code, "inReview": True, "profit": {"$in":profits}  }, {"$set": {"inReview":False}})
        except:
            return response.reject("Error al intentar actualizar una sugerencia")
    
    def getResponse(self, data, response, code):
        profits = list(filter(lambda profit: profit["fechaFinal"], data))
        profits = list(set(map(lambda profit : profit["nombre"], profits)))
        profits = list(map(lambda profit : {"profit": mongo.db.profit.find_one({"nombre": profit}, { "total":1, "_id": 1})["_id"]}, profits))
        profits = list(filter(lambda profit: not mongo.db.suggestion.find_one({"codeStudent":code, "profit":profit["profit"], "inReview":True}) , profits))
        response = list(filter(lambda res: res not in profits, response))
        return response 

    def studentsOfPeriod(self):
        program = "sistemas"
        period = "2021-1"
        split = period.split("-")
        year = split[0]
        semester = split[1]
        res = request_ufps().get(f"{environment.API_URL}/{program}_{year}_{semester}") 
        students = res.json() 
        if students:  
            for student in students:
                code = student["codigo"]
                student["riesgo"] = request_ufps().get(f"{environment.API_URL}/riesgo_{code}").json()["riesgoGlobal"]
        return response.success("todo ok!", students, "")

    def getSemesters(self, code):
        if not code or len(code) != 7 or not code.isdigit():
            return response.error("Se necesita un código de 7 caracteres", 400)
        res = request_ufps().get(f"{environment.API_URL}/semestres_{code}")
        data = res.json()
        data = helpers.updateSemestersRegistered(data)
        dataRes = {"data": data, "registered": helpers.countSemesters(data)}
        return response.success("Todo Ok!", dataRes, "")

    def getRecords(self, code, type):
        if not code or len(code) != 7 or not code.isdigit():
            return response.error("Se necesita un código de 7 caracteres", 400)
        records = mongo.db.record.find_one({"student":code})
        res = json_util.dumps(records)
        return Response(res, mimetype="applicaton/json")
    
    def saveRecord(self):
        record = request.json["record"]
        if not "_id" in record:
            id = mongo.db.record.insert(record)
            record = {
                **record, 
                "_id":str(id)
            } 
        else:
            id = record["_id"]
            del record["_id"]
            mongo.db.record.update_one({"_id": ObjectId(id)}, {"$set": record})
            record = {
                **record,  
                "_id": id
            }
        return record
    
    def getSemestersByProgram(self, program):
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/boss/semesters/{program}")
            res = req.json()
            if res["ok"]: 
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")
    
    def getCoursesBySemester(self, semester, program):
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/boss/courses/{semester}/{program}")
            res = req.json()
            if res["ok"]: 
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")
    
    def getGroupsOfCourse(self, course, program): 
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/boss/courses/groups/{program}/{course}")
            res = req.json()
            if res["ok"]: 
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")
    
    def getGroup(self, course, program, group): 
        try:
            req = request_ufps_token().get(f"{environment.API_UFPS}/boss/courses/group/{program}/{course}/{group}")
            res = req.json()
            if res["ok"]: 
                return response.success(res["msg"], res["data"], "")
            else:
                return response.reject(res["msg"])
        except:
            return response.reject("Hable con el administrador")