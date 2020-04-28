import jwt
import functools
from flask import session, request, Response, render_template, redirect, url_for
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
            token = request.get_json()["token"]
            tokenDecoded = jwt.decode(token, secret_key, algorithms="HS256")
            if function in tokenDecoded["privilege"]:
                return view(**kwargs)
            else:
                return Response("{\"status\": \"unauthorized\"}", status=401, mimetype="application/json")
        return decoratorLevelToken
    return decoratorFunctionPrincipal
