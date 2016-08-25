from flask import request
import lib.es as es
import web.util.tools as tools

def get(p):
    if not tools.get('name'): return tools.alert('name is missing')
    if not tools.get('id'): return tools.alert('id is missing')

    # save to configuration
    id = tools.get('id')
    es.update(p['host'], 'core_data', 'datasource', id, {
        'navigation_id': p['navigation']['id'],
        'type': tools.get('type'),
        'name': tools.get('name'),
        'description': tools.get('description'),
        'connection': tools.get('connection'),
        'query': tools.get('query')
    })
    es.flush(p['host'], 'core_data')

    return tools.redirect(request.referrer)
