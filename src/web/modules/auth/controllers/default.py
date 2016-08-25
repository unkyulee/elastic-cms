import importlib
from flask import render_template, session, request
import web.util.tools as tools

def get(p):
    if request.method == "POST":
        # find which auth module to use
        path = "web.modules.auth.services.{}".format(
            tools.get_conf(p['host'], '-1', 'auth', 'LDAP'))
        mod = importlib.import_module(path)

        if mod.authenticate(p, tools.get('login'), tools.get('password')):
            # when authentication is successful
            # save user_id in session
            session['user'] = tools.get('login')

            # then redirect to the previous page
            return_url = tools.get('url')
            if not return_url: return_url = request.referrer
            if not return_url: return_url = '/'

            return tools.redirect(return_url)
        else:
            # otherwise when login fails then reset the session
            session['user'] = None
            p['message'] = "Wrong id or password"

    # Form welcome message if user is already logged in
    if session.get("user"):
        p['message'] = "Welcome, {}".format(session.get('user'))

    # render custom login page
    p['login_html'] = tools.get_conf(
        p['host'], p['navigation']['id'], 'login_html', '')

    # redirect url
    p['ret_url'] = tools.get('url')

    return render_template("auth/default.html", p=p)
