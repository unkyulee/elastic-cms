from flask import request
from lib import es
import web.util.tools as tools

def get(p):

    # create new site
    site = {
        'order_key': tools.get('order_key'),
        'name': tools.get('name'),
        'display_name': tools.get('display_name'),
        'description': tools.get('description')
    }
    es.create(p['host'], 'core_nav', 'site', '', site)
    es.flush(p['host'], 'core_nav')


    return tools.redirect(request.referrer)
