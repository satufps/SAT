from flask import request, Response
from bson import json_util
from util import response, emails
from database import config

mongo = config.mongo 

class Chat:
    
    def sendMessage(self, userAuth):
        message = request.get_json(force=True)
        message = {
            **message,
            "transmitter": {
                "code": userAuth["codigo"],
                "email":userAuth["correo"],
                "name":f'{userAuth["nombre"]} {userAuth["apellido"]}',
            }
        }
        id = mongo.db.chat.insert(message)
        to = message["receiver"]["email"]
        subject = f'{message["transmitter"]["name"]} te ha enviado un mensaje'
        emails.sendEmail(to, message["message"], subject)
        return response.success("Mensaje enviado", {**message, "_id": str(id)},"") 
    
    def listChat(self, userAuth):
        receiver = request.get_json(force=True)
        transmitter = {
                "code": userAuth["codigo"],
                "email": userAuth["correo"],
                "name": f'{userAuth["nombre"]} {userAuth["apellido"]}'
        }
        data = mongo.db.chat.find({"$or": [ {"receiver": receiver, "transmitter": transmitter} , {"receiver": transmitter, "transmitter": receiver}]}).sort("date").limit(30)
        chat = json_util.dumps(data)
        return Response(chat, mimetype="applicaton/json")