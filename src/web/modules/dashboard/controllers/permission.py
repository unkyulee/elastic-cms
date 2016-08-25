# edit dashboard
from flask import request, render_template
import web.util.tools as tools
import lib.es as es

def get(p):
    # get list of roles
    query = "site_id:{}".format(p['site']['id'])
    p['role_list'] = es.list(p['host'], 'core_nav', 'role', query)

    # selected role
    role_id = p['nav'][-1]
    p['role'] = es.get(p['host'], 'core_nav', 'role', role_id)
    if not p['role']:
        p['role'] = p['role_list'][0]

    # get permission
    permission_id = "{}_{}".format(p['role']['id'], p['navigation']['id'])
    p['permission'] = es.get(p['host'], 'core_nav', 'permission', permission_id)

    if request.method == "POST":
        doc = { "operations": [x for x in tools.get('operations', []) if x] }

        if not p['permission']:
            # create permission
            es.create(p['host'], 'core_nav', 'permission', permission_id, doc)
        else:
            # edit permission
            es.update(p['host'], 'core_nav', 'permission', permission_id, doc)
        es.flush(p['host'], 'core_nav')

        return tools.redirect(request.referrer)


    return render_template("dashboard/permission.html", p=p)
