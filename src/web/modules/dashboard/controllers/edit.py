# edit dashboard
from flask import request, render_template
import web.util.tools as tools

def get(p):
    if request.method == "POST":
        # save dashboard
        tools.set_conf(p['host'], p['navigation']['id'], "dashboard",
                       request.form["dashboard"])

    # get dashboard template from the configuration
    p['dashboard'] = tools.get_conf(
        p["host"], p["navigation"]["id"], "dashboard")
    
    if not p['dashboard']:
        # use default template when nothing is configured
        p['dashboard'] = tools.read_file(
            "web/templates/dashboard/empty.html", p['base_dir'])

    return render_template("dashboard/edit.html", p=p)
