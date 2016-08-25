from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # url shall exist
    if not tools.get('url'): return tools.alert("url is missing")

    # create new reverse proxy rule
    doc = {
        'url': tools.get('url')
    }
    es.create(p['host'], 'core_proxy', 'public', '', doc)
    es.flush(p['host'], 'core_proxy')

    return tools.redirect(request.referrer)
