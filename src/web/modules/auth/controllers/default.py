import importlib
from flask import render_template, session, request
import web.util.tools as tools
from web.modules.admin.controllers.login.default import get_login_modules

def get(p):
    if request.method == "POST":
        return post(p)

    # Form welcome message if user is already logged in
    if session.get("user"):
        p['message'] = "Welcome, {}".format(session.get('user'))

    # render custom login page
    p['login_html'] = tools.get_conf(
        p['host'], p['navigation']['id'], 'login_html', '')

    # redirect url
    p['return_url'] = tools.get('url')

    return render_template("auth/default.html", p=p)



def post(p):

    # get login Process
    login_modules = get_login_modules(p)

    # try all login process until succeeds
    for login in login_modules:
        # find which auth module to use
        path = "web.modules.auth.services.{}".format(
            tools.get_conf(p['host'], '-1', 'auth', 'LDAP'))
        mod = importlib.import_module(path)
        if mod.authenticate(
            login['configuration'],
            tools.get('login'),
            tools.get('password')):

            # when authentication is successful

            # remember me
            if tools.get('remember'):
                # session will live for 31 days
                session.permanent = True
            else:
                session.permanent = False

            # save user_id in session
            session['user'] = tools.get('login')

            return tools.redirect(get_return_url())

    # ending up here means login failed
    p['message'] = "Login Failed. Check your login name and password."
    return render_template("auth/default.html", p=p)


def get_return_url():
    url = tools.get('url')
    # try to go to the previous page
    if not url: url = request.referrer
    # if the previous page is auth then go to root
    if url and url.endswith('/auth'): url = '/'
    # if there is no previous page then go to root site
    if not url: url = '/'

    return url
