from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load navigation
    navigation_id = p['nav'][-1]
    navigation = es.get(p['host'], 'core_nav', 'navigation', navigation_id)
    if not navigation:
        return tools.alert('not valid navigation id - {}'.format(navigation_id))

    if not tools.get('site_id'): return tools.alert("site id missing")
    if not tools.get('module_id'): return tools.alert("module id missing")

    # edit role
    doc = {
        'site_id': tools.get('site_id'),
        'parent_id': tools.get('parent_id'),
        'module_id': tools.get('module_id'),
        'order_key': int(tools.get('order_key')),
        'is_displayed': tools.get('is_displayed'),
        'name': tools.get('name'),
        'display_name': tools.get('display_name'),
        'url': tools.get('url'),
        'new_window': tools.get('new_window'),
        'description': tools.get('description')
    }
    es.update(p['host'], 'core_nav', 'navigation', navigation_id, doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
