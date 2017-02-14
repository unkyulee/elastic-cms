from flask import request, render_template
from web.modules.post.services import notification
import web.util.tools as tools

def get(p):
    h = p['host']; n = p['navigation']['id'];

    # Post Module Description
    if request.method == "POST":
        conf = {
            'gmail_id': tools.get('gmail_id'),
            'gmail_pw': tools.get('gmail_pw')
        }
        notification.set_conf(p['c']['host'], p['c']['index'], conf)

    return tools.redirect("{}/notification".format(p['url']))
