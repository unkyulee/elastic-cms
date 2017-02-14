# post list
from flask import render_template
import json
import lib.es as es
import web.util.tools as tools
from web.modules.post.services import notification

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # notification config
    h = p['host']; n = p['navigation']['id'];
    p['conf'] = notification.get_conf(h, n)

    # Get notification list
    option = "size=1000&sort=id:asc"
    p['notification_list'] = es.list(host, index, 'notification', '*', option)

    return render_template("post/notification/default.html", p=p)
