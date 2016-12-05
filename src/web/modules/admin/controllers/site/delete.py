from flask import request
from lib import es
import web.util.tools as tools

def get(p):
    site_id = p['nav'][-1]

    # root site can't be deleted
    if site_id == "0":
        return tools.alert("Root site can't be deleted")

    # check if site id is valid
    site = es.get(p['host'], 'core_nav', 'site', site_id)
    if not site:
        return tools.alert("not valid site id: {}".format(site_id))

    es.delete(p['host'], 'core_nav', 'site', site_id)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
