# edit role
from flask import render_template, request
import web.util.tools as tools
import lib.es as es

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load notification
    notification_id = p['nav'][-1]
    p['notification'] = es.get(host, index, 'notification', notification_id)
    if not p['notification']:
        return tools.alert('not valid notification id - {}'.format(notification_id))

    # save notification
    if request.method == "POST":
        doc = {
            'header': tools.get('header'),
            'message': tools.get('message'),
            'recipients': tools.get('recipients'),
            'condition': tools.get('condition'),
            'workflow': tools.get('workflow')
        }
        es.update(host, index, 'notification', notification_id, doc)
        es.flush(host, index)

        return tools.redirect("{}/notification/edit/{}".format(p['url'], notification_id))

    return render_template("post/notification/edit.html", p=p)
