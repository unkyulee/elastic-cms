from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load role
    role_id = p['nav'][-1]
    p['role'] = es.get(p['host'], 'core_nav', 'role', role_id)
    if not p['role']:
        return tools.alert('not valid role id - {}'.format(role_id))

    # edit role
    doc = {}    
    if tools.get('users'): doc['users'] = tools.get('users')
    if tools.get('name'): doc['name'] = tools.get('name')
    if tools.get('description'): doc['description'] = tools.get('description')

    es.update(p['host'], 'core_nav', 'role', role_id, doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
