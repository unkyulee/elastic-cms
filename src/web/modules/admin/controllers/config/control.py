from flask import request, render_template
import web.util.tools as tools

def get(p):
    if request.method == "POST":
        # save configuration
        set_all_conf(p['host'])

    # get configuration
    p['conf'] = get_all_conf(p['host'])
    return render_template("admin/config/default.html", p=p)


def get_all_conf(host):
    conf = {}
    conf['title'] = tools.get_conf(host, '-1', 'title', '')
    conf['auth'] = tools.get_conf(host, '-1', 'auth', '')
    conf['ldap'] = tools.get_conf(host, '-1', 'ldap', '')
    conf['ldap_path'] = tools.get_conf(host, '-1', 'ldap_path', '')
    conf['admins'] = tools.get_conf(host, '-1', 'admins', '')
    conf['safe_network'] = tools.get_conf(host, '-1', 'safe_network', '')
    conf['script'] = tools.get_conf(host, '-1', 'script', '')

    return conf


def set_all_conf(host):
    tools.set_conf(host, '-1', 'title', tools.get('title'))
    tools.set_conf(host, '-1', 'auth', tools.get('auth'))
    tools.set_conf(host, '-1', 'ldap', tools.get('ldap'))
    tools.set_conf(host, '-1', 'ldap_path', tools.get('ldap_path'))
    tools.set_conf(host, '-1', 'admins', tools.get('admins'))
    tools.set_conf(host, '-1', 'safe_network', tools.get('safe_network'))
    tools.set_conf(host, '-1', 'script', tools.get('script'))
