# init script for web.py/__init__.py
import time
from functools import wraps
from flask import session, request

from web import app
import lib.config as config # check config file
import lib.es as es # elasticsearch api
import web.util.tools as tools
import lib.util as util


# check if the site was installed
def require_install(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        # check config.py exists
        if  not config.exists(app.config.get('BASE_DIR')):
            # if config file doesn't exists then redirect to install page
            import web.modules.install.control as install
            return install.get()

        # call actual function
        return f(*args, **kwds)

    return wrapper


def requires_authentication(navigation):
    # if module is auth then no need authentication
    if navigation['navigation']['module_id'] == "2":
        return False

    # is it public
    if is_public():
        return False

    return True


def is_public():
    host = app.config.get("HOST")
    url = request.url

    public_list = es.list(host, 'core_proxy', 'public')

    # check if any rules match
    for public in public_list:
        if url.startswith(public['url']):
            return True

    return False


def is_authenticated():
    host = app.config.get("HOST")

    # check if session exists
    if session.get("user") and not util.is_ip(session.get("user")):
        return True

    # is allowed network?
    elif is_allowed_network(host, request.remote_addr):
        # set IP address as user
        session['user'] = request.remote_addr
        return True

    # if AUTH_METHOD is none then no need to authenticate
    elif get_auth_method(host) == "None":
        # set IP address as user
        session['user'] = request.remote_addr
        return True

    return False


def get_auth_method(host):
    id = "{}_{}".format("-1", "auth")
    ret = es.get(host, "core_nav", "config", id)
    return ret['value'] if ret else "None"


def is_allowed_network(host, ip):
    id = "{}_{}".format("-1", "safe_network")
    ret = es.get(host, "core_nav", "config", id)
    networks = ret.get('value') if ret else []
    if not isinstance(networks, list): networks = [networks]

    for n in networks:
        if ip.startswith(n):
	    print ip, n, ip.startswith(n)
            return True

    return False
