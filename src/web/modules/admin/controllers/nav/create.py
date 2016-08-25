from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    if not tools.get('site_id') and tools.get('site_id') != 0:
        return tools.alert("site id is missing")
    if not tools.get('module_id'): return tools.alert("module id is missing")

    # create new site
    doc = {
        'site_id': tools.get('site_id'),
        'parent_id': tools.get('parent_id'),
        'module_id': tools.get('module_id'),
        'order_key': int(tools.get('order_key')),
        'is_displayed': tools.get('is_displayed'),
        'name': tools.get('name'),
        'display_name': tools.get('display_name'),
        'description': tools.get('description')
    }
    es.create(p['host'], 'core_nav', 'navigation', '', doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
