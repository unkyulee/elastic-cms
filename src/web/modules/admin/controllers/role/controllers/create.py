from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    # load site
    site_id = p['nav'][-1]
    p['selected_site'] = es.get(p['host'], 'core_nav', 'site', site_id)
    if not p['selected_site']:
        return tools.alert('not valid site id - {}'.format(site_id))
    # name shall exist
    if not tools.get('name'): return tools.alert("name can't be empty")

    # create new site
    doc = {
        'site_id': p['selected_site']['id'],
        'users': tools.get('users'),
        'name': tools.get('name'),
        'description': tools.get('description')
    }
    es.create(p['host'], 'core_nav', 'role', '', doc)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
