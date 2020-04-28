from flask import Flask, render_template, url_for, request, session, redirect
from docs.frontend.auth import checkIfUserInSession
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
        return redirect(url_for("operations", _method="POST", user=session["USER"]))

@frontEnd.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@frontEnd.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                session["USER"] = username
                session["TOKEN"] = returnToken(json.loads(str(roles[typeUser][1]).replace("\'", "\"")))
                session["PERMISSIONS"] = roles[typeUser][1]["privilege"]
                return redirect(url_for("operations", _method="POST", user=username))
            else:
                break
    return render_template("login.html", alert=True, contentAlert="Usuário ou senha digitados estão incorretos")

@frontEnd.route("/operations/<user>", methods=["GET", "POST"])
def operations(user):
    if "USER" not in session:
        return redirect(url_for("login"))
    else:
        if user != session["USER"]:
            return redirect(url_for("operations", _method="POST", user=session["USER"]))
        else:
            permissions = session["PERMISSIONS"]
            return render_template("operation.html", permissions=permissions, tokenAccess=session["TOKEN"])

@frontEnd.route("/consultHome", methods=["GET", "POST"])
@checkIfUserInSession
def consultHome():
    return apiFunctions.consultAPI()

@frontEnd.route("/insertHome", methods=["POST"])
@checkIfUserInSession
def insertHome():
    return apiFunctions.insertAPI()

@frontEnd.route("/deleteHome", methods=["POST"])
@checkIfUserInSession
def deleteHome():
    return apiFunctions.deleteAPI()

@frontEnd.route("/editHome", methods=["POST"])
@checkIfUserInSession
def editHome():
    jsonEdit = request.get_json()
    if "consultToEdit" in jsonEdit.keys():
        return apiFunctions.consultAPI()
    else:
        return apiFunctions.editAPI()


if __name__ == "__main__":
    frontEnd.run(host="127.0.0.1", debug=True, port=5000)