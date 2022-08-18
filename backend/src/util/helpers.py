import functools

def indexedCourses(data):
        return functools.reduce(lambda acc, curr: {**acc, curr["codigo"] : curr }, data , {})
    
def validateUser(users, document, password, code):
    aux = None
    if code:
        aux = list(filter(lambda user: user["codigo"] == code and user["documento"] == document and user["contrasena"] == password, users))
    else:
        aux = list(filter(lambda user: user["documento"] == document and user["contrasena"] == password, users))
    if aux:
        aux = aux[0]
    return aux

def parseColor(note):
    if not note:
      return "empty"
    color = ""
    if note < 3:
      color = "bad"
    elif note >= 3 and note < 4:
      color = "regular"
    else:
      color = "good"
    return color

def updateSemestersRegistered(semesters):
    return list(map(lambda semester: {**semester, "promedio" : parseColor(semester["promedio"])}, semesters))

def countSemesters(semesters):
    registered = list(filter(lambda semester: semester["promedio"] != "empty", semesters))
    return len(registered)

def convertLevelRisk(value):
   if value <= 1.9:
     return "critico" 
   if value >=  2 and value <= 2.9:
     return "moderado"   
   if value >=  3 and value <= 3.9:
     return "leve"  
   if value >=  4 and value <= 5:
     return "sin riesgo"
     
def allowed_file(filename):
  extensions = {'png', 'jpg', 'jpeg'}
  return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions
            
  