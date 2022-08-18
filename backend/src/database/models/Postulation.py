import math
from flask import request, Response
from util import response, emails
from database import config
from bson import json_util
from pymongo import DESCENDING
from bson.objectid import ObjectId


mongo = config.mongo


class Postulation:
    def generatePostulation(self):
        data = request.get_json()
        postulate = self.searchValidation(data["student"], True)
        if postulate:
            return response.error("Ya se encuentra postulado", 401)
        else:
            data["postulator"] = (
                data["postulator"] if data["postulator"] else data["student"]
            )
            data = {**data, "state": "SIN ATENDER", "isActive": True}
            id = mongo.db.postulation.insert(data)
            namePostulator = (
                f'{data["postulator"]["rol"]} {data["postulator"]["nombre"]}'
            )
            program = data["student"]["programa"]
            message = f"Cordial saludo\nSe le informa que ha sido postulado por el {namePostulator} y se ha enviado la solicitud al jefe del programa de {program} para continuar con el proceso de seguimiento.\nEstado de la Postulación: SIN ATENDER"
            subject = "Postulación generada en el sistema de alertas de la UFPS"
            emails.sendEmail(data["student"]["correo"], message, subject)
            return response.success(
                "Estudiante Postulado", {**data, "_id": str(id)}, ""
            )

    def validatePostulation(self):
        data = request.get_json()
        postulation = self.searchValidation(data["student"], data["isActive"])
        res = json_util.dumps(postulation)
        return Response(res, mimetype="applicaton/json")

    def searchValidation(self, student, isActive):
        data = {"student": student, "isActive": isActive}
        postulation = mongo.db.postulation.find_one(data)
        return postulation

    def paginatePostulations(self, userAuth):
        totalPostulations = mongo.db.postulation.count_documents(
            {"state": "SIN ATENDER"}
        )
        page = request.args.get("page", default=1, type=int)
        perPage = request.args.get("perPage", default=5, type=int)
        totalPages = math.ceil(totalPostulations / perPage)
        offset = ((page - 1) * perPage) if page > 0 else 0
        program = userAuth["programa"]
        data = (
            mongo.db.postulation.find(
                {"student.programa": program, "state": "SIN ATENDER"}
            )
            .sort("date", DESCENDING)
            .skip(offset)
            .limit(perPage)
        )
        postulations = json_util.dumps({"totalPages": totalPages, "data": data})
        return Response(postulations, mimetype="applicaton/json")

    def filterPostulations(self):
        code = request.json["code"]
        data = mongo.db.postulation.find_one({"student.codigo": {"$eq": code}})
        postulations = json_util.dumps(data)
        return Response(postulations, mimetype="applicaton/json")

    def countPostulation(self, role):
        state = "SIN ATENDER" if role == "jefe" else "EN REVISIÓN"
        counter = mongo.db.postulation.count_documents({"state": state})
        return response.success("todo ok!", counter, "")

    def updatePostulationByBoss(self):
        id = request.json["id"]
        state = request.json["state"]
        postulation = mongo.db.postulation.find_one({"_id": ObjectId(id)})
        if not postulation:
            return response.error("La postulacion no existe", 400)
        program = postulation["student"]["programa"]
        email = postulation["student"]["correo"]
        self.updateState(id, state)
        message = f"Cordial saludo\nSe le informa que el estado de su postulación ha sido actualizado  por el director(a) del programa de {program} y se ha enviado a bienestar universitario para continuar con su seguimiento.\nNuevo estado de la Postulación: EN REVISIÓN"
        subject = " Se ha actualizado el estado de su postulación en el  sistema de alertas de la UFPS"
        emails.sendEmail(email, message, subject)
        return response.success("Postulación actualizada", None, "")

    def updateState(self, id, state):
        mongo.db.postulation.update_one(
            {"_id": ObjectId(id)}, {"$set": {"state": state}}
        )
        return True

    def paginatePostulationsWellness(self): 
        totalPostulations = mongo.db.postulation.count_documents(
            {"state": "EN REVISIÓN"}
        )
        page = request.args.get("page", default=1, type=int)
        perPage = request.args.get("perPage", default=5, type=int)
        totalPages = math.ceil(totalPostulations / perPage)
        offset = ((page - 1) * perPage) if page > 0 else 0
        data = (
            mongo.db.postulation.find({"state": "EN REVISIÓN"})
            .sort("date", DESCENDING)
            .skip(offset)
            .limit(perPage)
        )
        postulations = json_util.dumps({"totalPages": totalPages, "data": data})
        return Response(postulations, mimetype="applicaton/json")

    def getPostulationById(self, id):
        if(not id or len(id) != 24):
            return response.error("Se necesita un id de 24 caracteres", 400)
        data = mongo.db.postulation.find_one({"_id":ObjectId(id)})
        postulation = json_util.dumps(data)
        return Response(postulation, mimetype="applicaton/json")
