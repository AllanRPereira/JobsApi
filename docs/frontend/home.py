from flask import Flask, render_template, url_for, request
from docs.frontend.api import api
from docs.frontend import secret_key
import secrets
"@()"

frontEnd = Flask(__name__)
frontEnd.config["SECRET_KEY"] = secret_key
frontEnd.register_blueprint(api)

@frontEnd.route("/")
def index():
    return "Hello Application"

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