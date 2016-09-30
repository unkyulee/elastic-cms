from flask import render_template, request
from lib import es

def get(p):
    # get site list
    query = '*'
    option = 'size=1000&sort=display_name:asc'
    p['site_list'] = es.list(p['host'], 'core_nav', 'site', query, option)
    return render_template("admin/site/default.html", p=p)
