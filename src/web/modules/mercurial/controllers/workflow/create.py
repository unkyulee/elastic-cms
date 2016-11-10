from flask import request, render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    doc = {
        "name" : tools.get("name"),
        "description" : tools.get("description"),
        "status" : tools.get("status"),
        "condition" : tools.get("condition"),
        "validation" : tools.get('validation'),
        "postaction" : tools.get('postaction'),
        "screen" : tools.get('screen')
    }
    es.create(host, index, 'workflow', '', doc)
    es.flush(host, index)

    return tools.redirect(request.referrer)
