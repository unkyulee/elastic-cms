from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # root site can't be edited
    if request.form["id"] == "0":
        return tools.alert("Root site can't be deleted")
    else:
        es.delete(p['host'], 'core_nav', 'site', request.form['id'])
        es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
