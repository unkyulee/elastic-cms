from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load role
    role_id = p['nav'][-1]
    p['role'] = es.get(p['host'], 'core_nav', 'role', role_id)
    if not p['role']:
        return tools.alert('not valid role id - {}'.format(role_id))

    # delete
    es.delete(p['host'], 'core_nav', 'role', role_id)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
