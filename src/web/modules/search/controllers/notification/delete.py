from flask import render_template, request
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load notification
    notification_id = p['nav'][-1]
    p['notification'] = es.get(host, index, 'notification', notification_id)
    if not p['notification']:
        return tools.alert('not valid notification id - {}'.format(notification_id))

    # delete notification
    es.delete(host, index, 'notification', notification_id)
    es.flush(host, index)

    return tools.redirect(request.referrer)
