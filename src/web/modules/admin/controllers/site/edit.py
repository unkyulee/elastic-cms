from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load site
    site_id = p['nav'][-1]
    p['site'] = es.get(p['host'], 'core_nav', 'site', site_id)
    if not p['site']:
        return tools.alert('not valid site id - {}'.format(site_id))

    # update site
    doc = {
        'name': tools.get('name'),
        'display_name': tools.get('display_name'),
        'description': tools.get('description'),
        'is_displayed': tools.get('is_displayed'),
        'order_key': tools.get('order_key')
    }
    es.update(p['host'], 'core_nav', 'site', site_id, doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
