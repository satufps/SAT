from flask import request
from flask.wrappers import Response
from bson import json_util
from pymongo import DESCENDING
from util import response
from database import config

mongo = config.mongo

class Binnacle:
    
    def toWriter(self):
        data = request.get_json()
        id = mongo.db.binnacle.insert(data)
        data = {
            **data,
            "_id": str(id)
        }
        return response.success("Todo ok!", data, "")
    
    
    def getBinnacle(self, code):
        if(not code or not code.isdigit() or len(code) < 7):
            return response.error("Se necesita un código de 7 caracteres", 400)
        data = mongo.db.binnacle.find({"student":code}).sort("date", DESCENDING)
        binnacle = json_util.dumps(data)
        return Response(binnacle, mimetype="applicaton/json")