from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load rule
    rev_proxy_id = p['nav'][-1]
    rev_proxy = es.get(p['host'], 'core_proxy', 'rev_proxy', rev_proxy_id)
    if not rev_proxy:
        return tools.alert('not valid rev_proxy id - {}'.format(rev_proxy_id))


    # edit role
    doc = {
        'inc_url': tools.get('inc_url'),
        'out_url': tools.get('out_url'),
        'auth_method': tools.get('auth_method'),
        'header': tools.get('header')
    }
    es.update(p['host'], 'core_proxy', 'rev_proxy', rev_proxy_id, doc)
    es.flush(p['host'], 'core_proxy')

    return tools.redirect(request.referrer)
