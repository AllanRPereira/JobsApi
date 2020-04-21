from flask import Flask, render_template, url_for, request, session
from docs.frontend.auth import authenticationSession
from docs.frontend import roles
from docs.frontend.api import api
from docs.frontend import secret_key
import secrets
"@()"

frontEnd = Flask(__name__)
frontEnd.config["SECRET_KEY"] = secret_key
frontEnd.register_blueprint(api)

"""
@frontEnd.route("/")
def index():
    if "USER" not in session.keys():
        return render_template("login.html", alert=False, contentAlert=None)
    else:
        return render_template("operation.html")
"""

@frontEnd.route("/")
def index():
    return render_template("operation.html", permissions=("consult", "insert"))

@frontEnd.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    for typeUser in roles.keys():
        if username in roles[typeUser][0].keys():
            if roles[typeUser][0][username] == password:
                session["USER"] = typeUser
                return render_template("operation.html")
            else:
                break
    return render_template("login.html", alert=True, contentAlert="Usuário ou senha digitados estão incorretos")


def consultHome():
    pass

def insertHome():
    pass

def deleteHome():
    pass

def editHome():
    pass

if __name__ == "__main__":
    frontEnd.run(host="127.0.0.1", debug=True, port=5000)