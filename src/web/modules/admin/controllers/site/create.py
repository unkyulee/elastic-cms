from flask import request
from lib import es
import web.util.tools as tools

def get(p):   

    # create new site
    site = {
        'name': request.form.get('name'),
        'display_name': request.form.get('display_name'),
        'description': request.form.get('description')
    }
    es.create(p['host'], 'core_nav', 'site', '', site)
    es.flush(p['host'], 'core_nav')


    return tools.redirect(request.referrer)
