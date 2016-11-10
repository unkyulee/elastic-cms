# mercury web management

import importlib
import web.util.tools as tools
from .services import config

def get(p):
    # load global configuration
    p['c'] = config.get(p)

    # default operation is 'list'
    if not p['operation']: p['operation'] = 'list'

    # alias for admin -> config
    if p['operation'] == "admin": p['operation'] = 'config'

    # load controller
    path = "web.modules.mercurial.controllers.{}.control".format(p['operation'])
    control = importlib.import_module(path)

    # process the request
    return control.get(p)



def authorize(p):
    # get operation/mode string
    if not p['operation']:
        auth_key = 'list/'
    else:
        auth_key = p['operation'] + '/'

    if len(p['nav']) > 3 and p['nav'][3] \
            and p['operation'] != "list":
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
