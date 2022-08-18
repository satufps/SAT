from bson.objectid import ObjectId
from flask import request, Response
from bson import json_util
from util import response
from database import config

mongo = config.mongo

class Notification:
    
    def sendNotification(self):
        data = request.get_json(force=True)
        id = mongo.db.notification.insert(data)
        notification = {
            **data,
            "_id": str(id) 
        }
        return response.success("Notificación enviada", notification, "")
    
    def deleteNotification(self, id):
        if(not id or len(id) != 24):
            return response.error("Se necesita un id de 24 caracteres", 400)
        mongo.db.notification.delete_one({"_id": ObjectId(id)})
        return response.success("Notificación eliminada", None, "")        
    
    def getNotifications(self, code):
        if(not code  or not code.isdigit()):
            return response.error("Se necesita un código válido", 400)
        data = mongo.db.notification.find({"codeReceiver": code}).sort("date").limit(10)
        notifications = json_util.dumps(data)
        return Response(notifications, mimetype="applicaton/json")
        
    def updateNotification(self, id):
        if(not id or len(id) != 24):
            return response.error("Se necesita un id de 24 caracteres", 400)
        mongo.db.notification.update_one({"_id": ObjectId(id)}, {"$set": {
            "isActive": False
        }})
        return response.success("Notificación actualizada",None, "")
        