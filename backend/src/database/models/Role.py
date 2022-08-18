
from bson.objectid import ObjectId
from flask import request, Response
from database import config
from bson import json_util
from util import response

mongo = config.mongo

class Role:
    
    def createRole(self):
        data = request.get_json()
        schedule = data["schedule"]
        role = mongo.db.role.find_one({"role": data["role"]})
        if role:
          return response.reject("El rol ya existe")
        newRole = mongo.db.role.insert_one({"role": data["role"]}).inserted_id
        schedule = {
          "role": ObjectId(newRole),
          **schedule
        }
        mongo.db.schedule.insert(schedule)
        return response.success("todo ok",{"_id":str(newRole), "role":data["role"]},"") 
    
    def listRoles(self):
        roles =mongo.db.role.find()
        res= json_util.dumps(roles)
        return Response(res, mimetype="applicaton/json")
      
    def updateSchedule(self):
      data = request.get_json()
      role = data["role"]
      del data["role"]
      mongo.db.schedule.update_one({"role": ObjectId(role) }, {"$set": data})
      return response.success("Horario actualizado", {}, "")
    
    def getSchedule(self, role):
      schedule = mongo.db.schedule.find_one({"role": ObjectId(role)})
      res= json_util.dumps(schedule)
      return Response(res, mimetype="applicaton/json") 
    
    def getScheduleOfRole(self, role, date):
      id = mongo.db.role.find_one({"role": role}, {"total":1,"_id": True})["_id"]
      schedule = mongo.db.schedule.find_one({"role": id}, {"_id":False, "role": False})
      reservations = list(mongo.db.meet.find({"role":id, "date":date}, {"_id":False, "hour": 1, "total": 1}) )
      reservations = list(map(lambda reservation : reservation["hour"], reservations)) 
      reservations = list(filter(None, reservations))
      res = {
        "schedule" : schedule,
        "reservations":reservations
      }
      if schedule:
        return response.success("Todo ok!", res, "")
      else:
        return response.reject("No hay resultados")
        
      
      
    
