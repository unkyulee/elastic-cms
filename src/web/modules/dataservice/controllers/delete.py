# delete data source
from flask import request
import lib.es as es
import web.util.tools as tools

def get(p):
    id = tools.get('id')
    # delete
    es.delete(p['host'], 'core_data', 'datasource', id)
    es.flush(p['host'], 'core_data')

    return tools.redirect(request.referrer)
