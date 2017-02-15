import importlib
import web.util.tools as tools
from .services import config

def get(p):
    # load global configuration
    p['c'] = config.get(p)

    if not p['operation']: p['operation'] = 'search'
    if p['operation'] == "admin": p['operation'] = 'config'
    path = "web.modules.search.controllers.{}.control".format(p['operation'])
    control = importlib.import_module(path)
    return control.get(p)



def authorize(p):
    # get operation/mode string
    if not p['operation']:
        auth_key = 'search/'
    else:
        auth_key = p['operation'] + '/'

    if len(p['nav']) > 3 and p['nav'][3] \
            and p['operation'] != "permission" \
            and p['operation'] != "search" \
            and p['operation'] != "filter" \
            and p['operation'] != "file":
        auth_key += p['nav'][3]

    if auth_key in p['allowed_operation']:
        return True

    # if auth method is none then show
    auth = tools.get_conf(p['host'], '-1', 'auth', '')
    if auth == 'None' or not auth:
        return True

    # super user can have access
    admins = tools.get_conf(p['host'], '-1', 'admins', '')
    if p['login'] in admins:
        return True

    return False
