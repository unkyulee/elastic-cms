"""
Admin Menu
 - Global Configuration
  - Title
  - Global Script
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
    return render_template("admin/config/default.html", p=p)


def get_all_conf(host):
    conf = {}
    conf['title'] = tools.get_conf(host, '-1', 'title', '')
    conf['script'] = tools.get_conf(host, '-1', 'script', '')

    return conf


def set_all_conf(host):
    tools.set_conf(host, '-1', 'title', tools.get('title'))
    tools.set_conf(host, '-1', 'script', tools.get('script'))
