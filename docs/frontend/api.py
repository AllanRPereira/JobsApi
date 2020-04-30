from flask import Blueprint, request, Response, jsonify
from docs.frontend import secret_key
from docs.frontend.auth import accessLevelToken
from docs.frontend import databaseConn
from docs.frontend import createJob
from docs.frontend import roles
import jwt
import datetime
import time

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/")
def apiIndex():
    return Response("{\"status\" : \"please see the documentation\"}", status=200, mimetype="application/json")

@api.route("/getoken", methods=['GET', 'POST'])
def getToken():
    jsonValues = request.get_json()
    username = jsonValues['username']
    password = jsonValues['password']

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                return returnToken(roles[typeUser][1])
            else:
                break
    
    return Response("{\"status\" : \"User or password are incorrect\"}", status=200, mimetype="application/json")


@api.route("/insert", methods=['GET', 'POST'])
@accessLevelToken(function="insert")
def insertAPI():
    receivedJob = checkFromHome()
    if receivedJob == None or "name" not in receivedJob.keys():
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")
    jobInstance = createJob(**receivedJob)
    statusCode, content = databaseConn.insert(jobInstance)
    if statusCode:
        content = {
            "status" : "success"
        }
        return (jsonify(**content), 200)
    else:
        jsonResponse = {
            "status" : "unsuccess",
            "log" : content
        }
        return (jsonify(**jsonResponse), 417)

@api.route("/edit", methods=['GET', 'POST'])
@accessLevelToken("edit")
def editAPI():
    receivedJob = checkFromHome()
    if receivedJob == None or "name" not in receivedJob:
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")

    jobName = receivedJob["job_name_edit"]
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
        return (jsonify(**jsonResponse), 417)

@api.route("/delete", methods=['GET', 'POST'])
@accessLevelToken("delete")
def deleteAPI():
    receivedJob = checkFromHome()
    jobName = receivedJob["name"]
    
    statusOperation, content = databaseConn.exclusion(jobName=jobName)

    if statusOperation:
        return Response("{\"status\" : \"success\"}", status=200, mimetype="application/json")
    else:
        return Response("{\"status\" : \"unsuccess\"}", status=400, mimetype="application/json")

@api.route("/consult", methods=['GET', 'POST'])
@accessLevelToken("consult")
def consultAPI():
    receivedJob = checkFromHome()
    if receivedJob == None or "name" not in receivedJob:
        return Response("{\"status\" : \"unsuccess\"}", status=412, mimetype="application/json")
    jobName = receivedJob["name"]
    
    statusOperation, content = databaseConn.consult(jobName=jobName)

    if statusOperation:
        content["status"] = "success"
        return (jsonify(**content), 200)
    else:
        jsonResponse = {
            "status" : "unsuccess",
            "log" : content
        }
        return (jsonify(**jsonResponse), 404)

def returnToken(privilege):
    token = jwt.encode(privilege, key=secret_key, algorithm="HS256")
    return token.decode()

def parseFormToJob(formRequestJson):
    if formRequestJson["tasksJobOption"] == "not":
        taskInformation = []
    else:
        createdAt = datetime.date.today()
        createdTask = f"{createdAt.year:04d}-{createdAt.month:02d}-{createdAt.day:02d}"
        attributes = ("taskName", "weightTask", "completedTask")
        correlationAttributes = ("name", "weight", "completed")
        propertyTasks = []
        for attribute in attributes:
            propertyTasks.append([value for key, value in formRequestJson.items() if key.find(attribute) != -1])
        tasks = zip(propertyTasks[0], propertyTasks[1], propertyTasks[2])
        taskInformation = [ {
            correlationAttributes[0] : task[0],
            correlationAttributes[1] : task[1],
            correlationAttributes[2] : True if task[2] == "yes" else False,
            "createdAt" : createdTask
         } for task in tasks
        ]

    jobValues = {
        "name" : formRequestJson["namejob"],
        "active" : True if formRequestJson["jobActiveOption"] == "yes" else False,
        "parentJob" : {
            "name" : formRequestJson["parentJob"],
            "active" : True if formRequestJson["activeParent"] == "yes" and formRequestJson["parentJob"] else False
        },
        "tasks" : taskInformation

    }

    if "job_name_edit" in formRequestJson.keys():
        jobValues["job_name_edit"] = formRequestJson["job_name_edit"]

    return jobValues

def checkFromHome():
    jsonObject = request.get_json()
    if "namejob" in jsonObject:
        return parseFormToJob(jsonObject)
    else:
        return jsonObject