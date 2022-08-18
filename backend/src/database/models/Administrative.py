import random, os
from pymongo.collection import ReturnDocument
from flask import json, request, jsonify, Response
from util import jwt, response, environment, emails
from database import config
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from bson import json_util
from util import jwt, environment
from util.request_api import request_ufps

mongo = config.mongo

class Administrative:
    
    def register(self): 
        print(request.get_json())
        email = request.json["correo"]
        document = request.json["documento"]
        role = ObjectId(request.json["rol"])
        user = mongo.db.administrative.find_one({"$or":[ {"correo":email}, {"documento":document}]})
        if user:
            return jsonify(False)
        data = request.get_json()
        password = str(random.randrange(1000, 9999))
        data["contrasena"] = generate_password_hash(password)
        data["estado"] = True
        data = {
            **data,
            "rol": role
        }
        mongo.db.administrative.insert(data)
        nombre = f"{request.json['nombre']} {request.json['apellido']}"
        message = f"Hola {nombre}, ha sido creado su cuenta para ingresar en la plataforma SAT, por favor ingrese a su cuenta y cambie la contraseña para mayor seguridad con los siguientes datos:\nCorreo: {email}\nContraseña: {password}"
        subject = f"{nombre} se activó su cuenta en la plataforma SAT"
        emails.sendEmail(email, message, subject)
        return jsonify(True)
    
    def login(self): 
        document = request.json["document"]
        password = request.json["password"]
        user = mongo.db.administrative.find_one({"documento":document})
        if(not user): 
            return response.reject("Revise los datos ingresados")    
        hash = user["contrasena"]
        isValid = check_password_hash(hash, password)
        if not isValid:
            return response.reject("Revise los datos ingresados")   
        id = str(user["_id"])
        del user["_id"]
        del user["contrasena"]
        idRole = ObjectId(user["rol"])
        role = mongo.db.role.find_one({"_id": idRole}, {"_id": False})
        filename = self.getPhoto(document)
        if filename:
            path = os.path.join(environment.UPLOAD_FOLDER, filename)
            path = f"{request.host_url}{path[1:]}" 
        else:  
            path = None
        user = {
            **user,
            "_id": id,
            "rol": role["role"],
            "foto":path
        } 
        token = jwt.generateToken(user, 60)
        return response.success("Bienvenido!!", user, token)
        
    def changePassword(self):
        password = request.json["password"]
        newPassword = request.json["newPassword"]
        id = request.json["id"]
        user = mongo.db.administrative.find_one({"_id":ObjectId(id)})
        if not user:
            return jsonify(False)
        hash = user["contrasena"]
        isValid = check_password_hash(hash, password)
        if not isValid:
            return jsonify(False)
        newPassword = generate_password_hash(newPassword)
        mongo.db.administrative.find_one_and_update({"_id": ObjectId(id)},{"$set":{"contrasena": newPassword}})
        return jsonify(True) 
       
    def sendMailRecoveryPassword(self):
        email = request.json["email"] 
        user = mongo.db.administrative.find_one({"correo":email})
        expireIn = 5
        if not user:
            return jsonify(False)
        token = jwt.generateToken(request.get_json(), expireIn)
        link = f"{environment.FRONTEND_URL}/auth/recovery_password/{token}"
        message = f"Por favor ingrese al siguiente enlace para recuperar su contraseña {link}.\nTenga en cuenta que el enlace caduca en {expireIn} minutos"
        subject = "Recuperar contraseña en la plataforma SAT"
        emails.sendEmail(email, message, subject)
        return jsonify(True)
       
    def recoveryPassword(self, email):
        newPassword = generate_password_hash(request.json["newPassword"])
        user = mongo.db.administrative.find_one_and_update({"correo":email},{"$set":{"contrasena": newPassword}})
        return jsonify(True) if user else jsonify(False)
         
    def getByCode(self, code):
        if(not code or not code.isdigit() or len(code) < 7):
            return response.error("Se necesita un código de 7 caracteres", 400)
        try:
            req = request_ufps().get(f"{environment.API_URL}/vicerrector_{code}")
            data = req.json()
            if(data["ok"]):
                user = data["data"]
                del user["contrasena"]
                return response.success("Todo Ok!", user, "")
            else: 
                return response.error("No se encontraron resultados", 400)
        except:
          return response.success("No se encontraron resultados", None, "")   
        
    def getFaculties(self): 
        req = request_ufps().get(f"{environment.API_URL}/facultades")
        data = req.json()
        return response.success("Todo ok!", data, "")
    
    def validateProgram(self, nameProgram):
        req = request_ufps().get(f"{environment.API_URL}/facultades")
        data = req.json()
        for i in data: 
            for  j in i["programas"]:            
                if j == nameProgram:  
                    return json.dumps(True)
        return json.dumps(False)
    
    def updatePhone(self, user):
        id = user["_id"]
        phone = request.json["phone"]
        data = mongo.db.administrative.find_one_and_update({"_id":ObjectId(id)}, {"$set": {"telefono":phone}}, return_document=ReturnDocument.AFTER)
        userUpdated = json_util.dumps(data)
        return Response(userUpdated, mimetype="applicaton/json")
             
    def getProfits(self):
        data = mongo.db.profit.find(None, {"nombre":1, "_id": False})
        profits = json_util.dumps(data)
        return Response(profits, mimetype="applicaton/json")
        
    def getPhoto(self, code):
        record = mongo.db.photo.find_one({"user": code},{"filename":1, "_id": False,"total":1})  
        return record["filename"] if record else None
         
