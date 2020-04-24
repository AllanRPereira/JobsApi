from flask import Flask, render_template, url_for, request, session, redirect
from docs.frontend.auth import checkPermissionToOperation
from docs.frontend import roles
import docs.frontend.api as apiFunctions
from docs.frontend.api import api
from docs.frontend.api import returnToken
from docs.frontend import secret_key
from docs.frontend import databaseConn
from docs.frontend import createJob
import json

frontEnd = Flask(__name__)
frontEnd.config["SECRET_KEY"] = secret_key
frontEnd.register_blueprint(api)

@frontEnd.route("/")
def index():
    if "USER" not in session.keys():
        return render_template("login.html", alert=False, contentAlert=None)
    else:
        return render_template("operation.html")

@frontEnd.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                session["USER"] = typeUser
                session["TOKEN"] = returnToken(json.loads(str(roles[typeUser][1]).replace("\'", "\"")))
                session["PERMISSIONS"] = roles[typeUser][1]["privilege"]
                return redirect(url_for("operations", _method="POST", user=username))
            else:
                break
    return render_template("login.html", alert=True, contentAlert="Usuário ou senha digitados estão incorretos")

@frontEnd.route("/operations/<user>", methods=["GET", "POST"])
def operations(user="public"):
    if "USER" not in session:
        return redirect(url_for("login"))
    else:
        permissions = session["PERMISSIONS"]
        return render_template("operation.html", permissions=permissions, tokenAccess=session["TOKEN"])

@frontEnd.route("/consultHome", methods=["POST"])
@checkPermissionToOperation("consult")
def consultHome():
    return apiFunctions.consultAPI()

@frontEnd.route("/insertHome", methods=["POST"])
def insertHome():
    pass

@frontEnd.route("/deleteHome", methods=["POST"])
@checkPermissionToOperation("delete")
def deleteHome():
    pass

@frontEnd.route("/editHome", methods=["POST"])
@checkPermissionToOperation("edit")
def editHome():
    pass

def parseFormToJob(formRequest):
    if formRequest["tasksJobOption"] == "not":
        taskInformation = []
    else:
        attributes = ("taskName", "weightTask", "completedTask")
        correlationAttributes = ("name", "weight", "completed")
        propertyTasks = []
        for attribute in attributes:
            propertyTasks.append([value for key, value in formRequest.items() if key.find(attribute) != -1])
        tasks = zip(propertyTasks[0], propertyTasks[1], propertyTasks[2])
        taskInformation = [ {
            correlationAttributes[0] : task[0],
            correlationAttributes[1] : task[1],
            correlationAttributes[2] : True if task[2] == "yes" else False
         } for task in tasks
        ]
        
    jobValues = {
        "name" : formRequest["namejob"],
        "active" : True if formRequest["jobActiveOption"] == "yes" else False,
        "parentJob" : formRequest["parentJob"],
        "tasks" : taskInformation

    }
    return jobValues

if __name__ == "__main__":
    frontEnd.run(host="127.0.0.1", debug=True, port=5000)