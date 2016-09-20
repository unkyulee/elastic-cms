from flask import render_template, request
import lib.es as es
import web.util.tools as tools


def get(p):
    p['site_id'] = tools.get('site_id')
    if not p['site_id']: return tools.alert('site id is missing')

    # get navigation list
    query = 'site_id:{}'.format(p['site_id'])
    option = 'size=1000&sort=order_key:asc'
    p['nav_list'] = es.list(p['host'], 'core_nav', 'navigation', query, option)


    # role list
    query = 'site_id:{}'.format(p['site_id'])
    option = 'size=1000&sort=name:asc'
    p['role_list'] = es.list(p['host'], 'core_nav', 'role', query, option)

    # module list
    query = "*"
    option = 'size=1000&sort=name:asc'
    p['module_list'] = es.list(p['host'], 'core_nav', 'module', query, option)

    # module list
    for nav in p['nav_list']:
        module = es.get(p['host'], 'core_nav', 'module', nav['module_id'])
        nav['module'] = module

    return render_template("admin/role/default.html", p=p)
