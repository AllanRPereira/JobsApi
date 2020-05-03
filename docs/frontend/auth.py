import jwt
import functools
from flask import session, request, Response, render_template, redirect, url_for, jsonify
from docs.frontend import secret_key

def checkIfUserInSession(view):
    @functools.wraps(view)
    def decoratorView(*args, **kwargs):
        if "USER" not in session.keys():
            return redirect(url_for("index"))
        return view(*args, **kwargs)

    return decoratorView

def accessLevelToken(function):
    def decoratorFunctionPrincipal(view):
        @functools.wraps(view)
        def decoratorLevelToken(*args, **kwargs):
            if request.method == "POST" or request.mimetype == "application/json":
                jsonObject = request.get_json()
            else:
                jsonObject = request.args

            if jsonObject == None or "token" not in jsonObject:
                return Response("{\"status\": \"unauthorized\"}", status=404, mimetype="application/json")
            token = jsonObject["token"]
            try:
                tokenDecoded = jwt.decode(token, secret_key, algorithms="HS256")
            except Exception as error:
                return (jsonify(**{"status" : "error", "log" : f"{error.args[0]}"}), 412)
            if function in tokenDecoded["privilege"]:
                return view(**kwargs)
            else:
                return Response("{\"status\": \"unauthorized\"}", status=401, mimetype="application/json")
        return decoratorLevelToken
    return decoratorFunctionPrincipal
