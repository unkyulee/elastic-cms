from flask import request, render_template
import web.util.tools as tools
import lib.es as es

def get(p):
    if request.method == "POST":
        # save configuration
        set_all_conf(p['host'])
        return tools.redirect(request.referrer)

    # get list authentication plugins
    p['login_modules'] = get_login_modules(p)
    return render_template("admin/login/default.html", p=p)


def get_login_modules(p):
    query = "*"
    option = 'size=1000&sort=priority:desc'
    return es.list(p['host'], 'core_nav', 'login_module', query, option)
