from flask import render_template, request
import lib.es as es
import web.util.tools as tools


def get(p):
    p['site_id'] = tools.get('site_id')
    if not p['site_id']: return tools.alert('site id is missing')

    # get navigation list
    query = 'site_id:{} AND -module_id:1 AND -module_id:2 AND -module_id:3'.format(p['site_id'])
    option = 'size=1000&sort=order_key:asc'
    p['nav_list'] = es.list(p['host'], 'core_nav', 'navigation', query, option)

    # module list
    query = "* AND -name:admin AND -name:auth AND -name:install"
    option = 'size=1000&sort=name:asc'
    p['module_list'] = es.list(p['host'], 'core_nav', 'module', query, option)

    # module list
    for nav in p['nav_list']:
        module = es.get(p['host'], 'core_nav', 'module', nav['module_id'])
        nav['module'] = module

    return render_template("admin/nav/default.html", p=p)
