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

@api.route("/", methods=['GET', 'POST'])
def apiIndex():
    return Response("{\"status\" : \"please see the documentation\"}", status=200, mimetype="application/json")

@api.route("/getoken", methods=['GET', 'POST'])
def getToken():
    jsonValues = request.args if request.method == "GET" else request.get_json()
    try:
        username = jsonValues['username']
        password = jsonValues['password']
    except Exception as error:
        return (jsonify(**{"status" : "error", "error" : f"{error.args[0]}"}), 412)

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                return (jsonify({"status" : "success", "token" : returnToken(roles[typeUser][1])}), 200)
            else:
                break
    
    return (jsonify(**{"status":"unsuccess", "log" : "User or password are incorrect"}), 200)


@api.route("/insert", methods=['GET', 'POST'])
@accessLevelToken(function="insert")
def insertAPI():
    receivedJob = checkFromHome()
    checkName = checkCommonRequirements(receivedJob)
    if checkName[0]: return checkName[1]
    createdJobReturn = createJob(receivedJob)
    if createdJobReturn[0]:
        jobInstance = createdJobReturn[1]
    else:
        return (jsonify(**createdJobReturn[1]), createdJobReturn[2])
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
    checkName = checkCommonRequirements(receivedJob)
    if checkName[0]: return checkName[1]

    jobName = receivedJob["job_name_edit"]
    receivedJob.pop("job_name_edit")
    createdJobReturn = createJob(receivedJob)
    if createdJobReturn[0]:
        jobInstance = createdJobReturn[1]
    else:
        return (jsonify(**createdJobReturn[1]), createdJobReturn[2])

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
    checkName = checkCommonRequirements(receivedJob)
    if checkName[0]: return checkName[1]
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
    checkName = checkCommonRequirements(receivedJob)
    if checkName[0]: return checkName[1]
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
    if request.method == "POST":
        jsonObject = request.get_json()
    else:
        jsonObject = request.args
    if "namejob" in jsonObject:
        return parseFormToJob(jsonObject)
    else:
        return jsonObject

def checkCommonRequirements(receivedJob):
    """
    All job need the attributes name
    """
    if receivedJob == None:
        return (True, (jsonify(**{"status":"unsuccess", "log" : "Job data don't passed"}), 200))
    elif "name" not in receivedJob.keys():
        return (True, (jsonify(**{"status":"unsuccess", "log" : "Job-name don't passed"}), 200))
    elif receivedJob["name"] == "":
        return (True, (jsonify(**{"status":"unsuccess", "log" : "Job-name can't null"}), 200))
    else:
        return (False, "")