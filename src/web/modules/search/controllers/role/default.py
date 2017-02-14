from flask import render_template, request
import web.util.tools as tools
import lib.es as es

def get(p):
    # role list
    query = 'site_id:{}'.format(p['site']['id'])
    option = 'size=1000&sort=name:asc'
    p['role_list'] = es.list(p['host'], 'core_nav', 'role', query, option)

    return render_template("post/role/default.html", p=p)
