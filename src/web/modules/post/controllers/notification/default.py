# post list
from flask import render_template
import json
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # Get notification list
    option = "size=1000&sort=id:asc"
    p['notification_list'] = es.list(host, index, 'notification', '*', option)
    
    return render_template("post/notification/default.html", p=p)
