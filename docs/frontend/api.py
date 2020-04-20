from flask import Blueprint, request, Response
from docs.frontend import secret_key
from docs.frontend.auth import accessLevelToken
from docs.frontend import databaseConn
from docs.frontend import createJob
import json
import jwt
import time

api = Blueprint("api", __name__, url_prefix="/api")
roles = {
    "ADMIN" : [{
            "adm" : "adm"
    }, {
        "privilege" : ("insert", "delete", "consult", "edit")        
    }]
    ,
    "PUBLIC" : [{
            "teste" : "teste"
    },{
        "privilege" : ("consult",)        
    }]
    
}

@api.route("/")
def apiIndex():
    return Response("{\"status\" : \"please see the documentation\"}", status=200, mimetype="application/json")

@api.route("/getoken", methods=['GET', 'POST'])
def getToken():
    global roles
    jsonValues = request.get_json()
    username = jsonValues['username']
    password = jsonValues['password']

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                return returnToken(roles[typeUser][1])
            else:
                return "User or password incorrect"
    else:
        return "This user doesn't exists"


@api.route("/insert", methods=['GET', 'POST'])
@accessLevelToken(function="insert")
def insertAPI():
    receivedJob = request.get_json()
    if receivedJob == None or "name" not in receivedJob.keys():
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")
    jobInstance = createJob(**receivedJob)
    statusCode, response = databaseConn.insert(jobInstance)
    if statusCode:
        return Response("{\"status\" : \"sucess\"}", status=200, mimetype="application/json")
    else:
        jsonResponse = {
            "status" : "unsuccess",
            "log" : response
        }
        return Response(jsonResponse, status=417, mimetype="application/json")

@api.route("/edit", methods=['GET', 'POST'])
@accessLevelToken("edit")
def editAPI():
    receivedJob = request.get_json()
    if receivedJob == None or "job_edit_name" not in receivedJob:
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")

    jobName = receivedJob["job_edit_name"]
    receivedJob.pop("job_name_edit")
    jobInstance = createJob(**receivedJob)
    statusCode, response = databaseConn.edition(jobInstance, jobName=jobName)
    if statusCode:
        return Response("{\"status\" : \"success\"}", status=200, mimetype="application/json")
    else:
        jsonResponse = {
            "status" : "unsuccess",
            "log" : response
        }
        return Response(json, status=417, mimetype="application/json")

@api.route("/delete", methods=['GET', 'POST'])
@accessLevelToken("delete")
def deleteAPI():
    receivedJob = request.get_json()
    jobName = receivedJob["job_name"]
    
    if databaseConn.exclusion(jobName=jobName):
        return Response("{\"status\" : \"success\"}", status=200, mimetype="application/json")
    else:
        return Response("{\"status\" : \"unsuccess\"}", status=400, mimetype="application/json")

@api.route("/consult", methods=['GET', 'POST'])
@accessLevelToken("consult")
def consultAPI():
    receivedJob = request.get_json()
    if receivedJob == None or "job_name" not in receivedJob:
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")
    jobName = receivedJob["job_name"]
    
    if databaseConn.consult(jobName=jobName):
        return Response("{\"status\" : \"success\"}", status=200, mimetype="application/json")
    else:
        return Response("{\"status\" : \"unsuccess\"}", status=400, mimetype="application/json")

def returnToken(privilege):
    token = jwt.encode(privilege, key=secret_key, algorithm="HS256")
    return token.decode()