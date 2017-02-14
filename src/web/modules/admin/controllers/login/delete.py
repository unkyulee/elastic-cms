"""
Delete Login Module
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

    # deletelogin module
    es.delete(p['host'], 'core_nav', 'login_module', login_module_id)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
