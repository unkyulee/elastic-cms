# create data source
from flask import request
import lib.es as es
import web.util.tools as tools

def get(p):
    if not tools.get('name'): return tools.alert('name is missing')

    # save to configuration    
    es.create(p['host'], 'core_data', 'datasource', '', {
        'navigation_id': p['navigation']['id'],
        'type': tools.get('type'),
        'name': tools.get('name'),
        'description': tools.get('description'),
        'connection': tools.get('connection'),
        'query': tools.get('query')
    })
    es.flush(p['host'], 'core_data')

    return tools.redirect(request.referrer)
