"""
Admin Menu
 - Security
  - Allow Guest
   - Safe Network as Guest
  - Site Admin Users
"""
from flask import request, render_template
import web.util.tools as tools

def get(p):
    if request.method == "POST":
        # save configuration
        set_all_conf(p['host'])
        return tools.redirect(request.referrer)

    # get configuration
    p['conf'] = get_all_conf(p['host'])
    return render_template("admin/security/default.html", p=p)


def get_all_conf(host):
    conf = {}
    conf['admins'] = tools.get_conf(host, '-1', 'admins', '')
    conf['safe_network'] = tools.get_conf(host, '-1', 'safe_network', '')

    return conf


def set_all_conf(host):
    tools.set_conf(host, '-1', 'admins', tools.get('admins'))
    tools.set_conf(host, '-1', 'safe_network', tools.get('safe_network'))
