import os
from flask import Response, request
from database import config
from util import response, emails, environment
from bson import json_util

mongo = config.mongo

class ChatAdmin:
    
    def getAdminsByRole(self, role):
        if(not role):
            return response.error("Se necesita un id de 24 caracteres", 400)
        id = mongo.db.role.find_one({"role":role}, {"total": 1, "_id":True})["_id"]
        data = list(mongo.db.administrative.find({"rol": id, "estado":True}, {"nombre": 1,"apellido": 1, "documento": 1, "correo":1, "_id":False}))
        if len(data) > 0:
            data = list(map(self.getPhoto, data))
        admins = json_util.dumps(data)
        return Response(admins, mimetype="applicaton/json")
    
    def getPhoto(self, admin):
        photo = mongo.db.photo.find_one({"user": admin["documento"]})
        filename = photo["filename"] if photo else None
        if filename:
            path = os.path.join(environment.UPLOAD_FOLDER, filename)
            filename = f"{request.host_url}{path[1:]}"
        return { **admin, "foto": filename }       
    
    def getAdminByDocument(self, document):
        if(not document):
            return response.error("Se necesita el documento del administrativo", 400)
        data = mongo.db.administrative.find_one({"documento": document}, {"nombre": 1,"apellido": 1, "documento": 1, "correo":1, "_id":False})
        admin = json_util.dumps(data)
        return Response(admin, mimetype="applicaton/json")
    
    def sendMessage(self):
        message = request.get_json()
        id = mongo.db.chat.insert(message)
        to = message["receiver"]["correo"]
        subject = f'{message["transmitter"]["nombre"]} te ha enviado un mensaje'
        emails.sendEmail(to, message["message"], subject)
        return response.success("Mensaje enviado", {**message, "_id": str(id)},"")
    
    def listChat(self):
        body = request.get_json()
        receiver = body["receiver"]
        transmitter = body["transmitter"]
        data = mongo.db.chat.find({"$or": [{"receiver.documento": receiver, "transmitter.documento": transmitter} , {"receiver.documento": transmitter, "transmitter.documento": receiver}]}).sort("date").limit(30)
        chat = json_util.dumps(data) 
        return Response(chat, mimetype="applicaton/json")
        
        
        