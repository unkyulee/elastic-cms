"""
Create Login Module Process
"""
from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # create new login module
    doc = {
        "type": tools.get('type'),
        "name": tools.get('name'),
        "description": tools.get('description'),
        "priority": tools.get('priority'),
        "configuration": tools.get('configuration')
    }
    es.create(p['host'], 'core_nav', 'login_module', '', doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
