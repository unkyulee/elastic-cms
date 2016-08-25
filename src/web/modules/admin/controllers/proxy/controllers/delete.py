from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load rule
    rev_proxy_id = p['nav'][-1]
    rev_proxy = es.get(p['host'], 'core_proxy', 'rev_proxy', rev_proxy_id)
    if not rev_proxy:
        return tools.alert('not valid rev_proxy id - {}'.format(rev_proxy_id))

    # delete
    es.delete(p['host'], 'core_proxy', 'rev_proxy', rev_proxy_id)
    es.flush(p['host'], 'core_proxy')

    return tools.redirect(request.referrer)
