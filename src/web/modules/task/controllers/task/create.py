from flask import request
import web.util.tools as tools
import lib.es as es

def get(p):

    es.create(p['host'], 'core_task', 'task', '', {
        'navigation_id': p['navigation']['id'],
        'name': tools.get('name'),
        'runat': tools.get('runat', 'anywhere'),
        'description': tools.get('description')
    })
    es.flush(p['host'], 'core_task')

    return tools.redirect(request.referrer)
