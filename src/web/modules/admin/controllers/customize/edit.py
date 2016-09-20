from flask import render_template, request
from lib import es
import web.util.tools as tools

def get(p):
    # check if site_id is passed
    p['site_id'] = tools.get('site_id')
    if not p['site_id']: return tools.alert('site id is missing')

    if request.method == "POST":
        # save custom navigation
        p['site'] = {
            'navigation': tools.get('navigation')
        }
        es.update(p['host'], 'core_nav', 'site', p['site_id'], p['site'])
        es.flush(p['host'], 'core_nav')

    # load site
    p['site'] = es.get(p['host'], 'core_nav', 'site', p['site_id'])
    if not p['site']: return tools.alert('site id is not valid')

    return render_template("admin/customize/default.html", p=p)
