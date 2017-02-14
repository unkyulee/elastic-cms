# edit role
from flask import render_template, request
import web.util.tools as tools
import lib.es as es

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load role
    role_id = p['nav'][-1]
    p['role'] = es.get(host, 'core_nav', 'role', role_id)
    if not p['role']:
        return tools.alert('not valid role id - {}'.format(role_id))


    # save role
    if request.method == "POST":
        # edit role
        doc = {}
        if tools.get('users'): doc['users'] = tools.get('users')
        if tools.get('operations'): doc['operations'] = tools.get('operations')

        es.update(p['host'], 'core_nav', 'role', role_id, doc)
        es.flush(p['host'], 'core_nav')

        return tools.redirect(request.referrer)

    return render_template("post/role/edit.html", p=p)
