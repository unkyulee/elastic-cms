# Initialize web application and setup routing
from flask import Flask, request, session, render_template, send_from_directory
app = Flask(__name__) # Define the WSGI application object
# very first run will not have config.py
try: app.config.from_object('config')
except: pass

import os

import web.util.jinja # Initialize jinja custom filters
import web.util.bootstrap as boot # Initialize web
import web.util.web_mod as mod # Module locator
import web.util.rev_proxy as rev # Reverse Proxy
import web.util.tools as tools


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
# Setup Routing - catch all
@app.route('/', defaults={'path':''}, methods=['GET','POST','PUT','DELETE','HEAD'])
@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','HEAD'])
@boot.require_install
def index(path):
    # capture all the exceptions and send email
    try:
        # split navigation
        nav = path.split("/")

        # determine the navigation with given url
        navigation = mod.define(app.config.get("HOST"), nav)
        if not navigation['module']:
            return "page not found", 404

        # authenticate
        req_auth = boot.requires_authentication(navigation)
        authenticated = boot.is_authenticated()

        if req_auth and not authenticated:
            # build payload for the navigation
            navigation = mod.build_payload(app.config, request, navigation)
            navigation['operation'] = None
            import web.modules.auth.control as default
            return default.get(navigation)

        # build payload for the navigation
        navigation = mod.build_payload(app.config, request, navigation)

        # check for rev_proxy
        rev_proxy_rule = rev.is_reverse_proxy(app.config.get("HOST"), request.path)
        if rev_proxy_rule:
            return rev.rev_proxy(app.config.get("HOST"), request.path, rev_proxy_rule)

        # get module
        response = mod.get_module(navigation)

        # check for Authorization
        if req_auth and not response.authorize(navigation):
            return render_template("error/401.html", p=navigation), 401

        # render based on the navigation info
        return response.get(navigation)
    except:
        # internal server error
        return mod.handle_exception(app.config.get("HOST"))
