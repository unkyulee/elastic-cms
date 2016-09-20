from flask import render_template, request
import lib.es as es
import web.util.tools as tools


def get(p):
    p['site_id'] = tools.get('site_id')
    if not p['site_id']: return tools.alert('site id is missing')

    # role list
    query = 'site_id:{}'.format(p['site_id'])
    option = 'size=1000&sort=name:asc'
    p['role_list'] = es.list(p['host'], 'core_nav', 'role', query, option)

    return render_template("admin/role/default.html", p=p)
