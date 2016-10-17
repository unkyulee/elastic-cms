# edit role
from flask import render_template, request
import web.util.tools as tools
import lib.es as es

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load notification
    p['notification'] = None

    # save notification
    if request.method == "POST":
        doc = {
            'header': tools.get('header'),
            'message': tools.get('message'),
            'recipients': tools.get('recipients'),
            'condition': tools.get('condition')
        }
        es.create(host, index, 'notification', None, doc)
        es.flush(host, index)

        return tools.redirect("{}/notification".format(p['url']))

    return render_template("post/notification/create.html", p=p)
