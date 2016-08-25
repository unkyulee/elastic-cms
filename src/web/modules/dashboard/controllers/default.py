from flask import request, render_template
from web import app
import web.util.tools as tools

def get(p):
    # Load Dashboard from the configuration
    dashboard = tools.get_conf(p["host"], p["navigation"]["id"], "dashboard")
    if dashboard:
        return render_template(app.jinja_env.from_string(dashboard), p=p)
    return render_template("dashboard/empty.html", p=p)
