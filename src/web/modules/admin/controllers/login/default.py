"""
List out defined Login Modules
"""
import os
from flask import request, render_template
import web.util.tools as tools
import lib.es as es


def get(p):
    # get list authentication plugins
    p['login_modules'] = get_login_modules(p)
    p['login_module_types'] = get_login_module_types(p)
    return render_template("admin/login/default.html", p=p)


def get_login_modules(p):
    query = "*"
    option = 'size=1000&sort=priority:desc'
    return es.list(p['host'], 'core_nav', 'login_module', query, option)


def get_login_module_types(p):
    # get list of auth services
    path = os.path.join(p['base_dir'], 'web', 'modules', 'auth', 'services')
    module_types = []
    for (dirpath, dirname, filenames) in os.walk(path):
        module_types = [f.replace('.py', '') for f in filenames if f.endswith('.py') and f != '__init__.py']

    return module_types
