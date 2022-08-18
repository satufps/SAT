from flask import request, Response
from pymongo import DESCENDING
from database import config
from bson import json_util
from util import environment, response
import datetime

from util.request_api import request_ufps 

mongo = config.mongo

class Report:
    
    def generateReportSuggestion(self):
        start = request.json["startDate"]
        end = request.json["endDate"]
        action = request.json["action"]
        res = True if action == "accepted" else False
        suggestions = []
        output = []
        for suggestion in mongo.db.suggestion.find({
            "state":False,
            "response":res,
            "date": {'$lte': end, '$gte': start}
        }).sort("date", DESCENDING):
            suggestions.append( (suggestion['profit'], suggestion['admin'], suggestion["codeStudent"], suggestion['date'], suggestion['_id'])) 
        for idProfit, idAdmin, codeStudent, date, id in suggestions:
            req = request_ufps().get(f"{environment.API_URL}/estudiante_{codeStudent}").json()
            user = req["data"]
            student = {
                "nombre": f'{user["nombre"]} {user["apellido"]}',
                "programa": user["programa"],
                "correo": user["correo"],
                "codigo": codeStudent
            }
            profit = mongo.db.profit.find_one({"_id": idProfit}, {"_id": False})
            infoAdmin = mongo.db.administrative.find_one({"_id": idAdmin}, {"nombre":1,"apellido":1,"rol":1, "_id": False})  
            role = mongo.db.role.find_one({"_id":infoAdmin["rol"]}, {"_id":False})["role"]
            infoAdmin = {
                **infoAdmin,
                "rol": role
            }
            output.append({"student":student, "date":date, "_id": str(id),"profit": {**profit}, "admin":{**infoAdmin}})
        if len(output) == 0:
            return response.reject("No se encontrarón resultados para mostrar")
        dataReport = {
                **request.get_json(),
                "date": datetime.datetime.utcnow().isoformat(),
                "type" : "Sugerencias atendidas"
        }
        report = self.createReport(dataReport)
        res = json_util.dumps({"ok":True, "suggestions": output, "report": report})
        return Response(res, mimetype="applicaton/json") 
    
    def createReport(self, report):
        id = mongo.db.report.insert(report)
        return { **report, "_id": str(id) }
    
    def getLastReport(self):
        report = mongo.db.report.find().sort("date", DESCENDING).limit(1)
        last = json_util.dumps(report)
        return Response(last, mimetype="applicaton/json") 