from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # name shall exist
    if not tools.get('inc_url'): return tools.alert("incoming url is missing")
    if not tools.get('out_url'): return tools.alert("outgoing url is missing")

    # create new reverse proxy rule
    doc = {
        'inc_url': tools.get('inc_url'),
        'out_url': tools.get('out_url'),
        'auth_method': tools.get('auth_method'),
        'header': tools.get('header')
    }
    es.create(p['host'], 'core_proxy', 'rev_proxy', '', doc)
    es.flush(p['host'], 'core_proxy')

    return tools.redirect(request.referrer)
