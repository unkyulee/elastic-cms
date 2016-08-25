from flask import request, render_template

from web import app
from .services.install import install
import web.util.tools as tools

def get(p={}):
    if request.method == "POST":
        # install elasticsearch essential index
        install(request.form['HOST'], request.form, app.config.get("BASE_DIR"))
        # return to the root page
        return tools.redirect("/")

    # display current configuration
    p["HOST"] = app.config.get("HOST") if app.config.get("HOST") else "http://localhost:9200"
    p["DEBUG"] = app.config.get("DEBUG") if app.config.get("DEBUG") else False
    p["KEYSTRING"] = app.config.get("KEYSTRING") if app.config.get("KEYSTRING") else "some random string for encryption"

    return render_template("install/install.html",p=p)


def authorize(p):
    # if auth method is none then show
    auth = tools.get_conf(p['host'], '-1', 'auth', '')
    if auth == 'None' or not auth:
        return True

    # only super user can have access
    admins = tools.get_conf(p['host'], '-1', 'admins', '')
    if p['login'] in admins:
        return True

    return False
