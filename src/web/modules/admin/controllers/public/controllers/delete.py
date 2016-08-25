from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load public url
    public_id = p['nav'][-1]
    public = es.get(p['host'], 'core_proxy', 'public', public_id)
    if not public:
        return tools.alert('not valid public url id - {}'.format(public_id))

    # delete
    es.delete(p['host'], 'core_proxy', 'public', public_id)
    es.flush(p['host'], 'core_proxy')

    return tools.redirect(request.referrer)
