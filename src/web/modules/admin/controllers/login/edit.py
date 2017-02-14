"""
Edit Login Module
"""
from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load login module
    login_module_id = p['nav'][-1]
    login_module = es.get(p['host'], 'core_nav', 'login_module', login_module_id)
    if not login_module:
        return tools.alert('not valid login module id - {}'.format(login_module_id))

    # update new login module
    doc = {
        "type": tools.get('type'),
        "name": tools.get('name'),
        "description": tools.get('description'),
        "priority": tools.get('priority'),
        "configuration": tools.get('configuration')
    }
    es.update(p['host'], 'core_nav', 'login_module', login_module_id, doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
