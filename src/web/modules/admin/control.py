import importlib
import web.util.tools as tools

# dispatcher
def get(p):
    # load module
    if not p['operation']: p['operation'] = 'config'
    path = "web.modules.admin.controllers.{}.control".format(p['operation'])
    control = importlib.import_module(path)
    return control.get(p)


def authorize(p):
    # if auth method is none then show
    auth = tools.get_conf(p['host'], '-1', 'auth', '')
    if auth == 'None' or not auth:
        return True

    # only super user can have access
    admins = tools.get_conf(p['host'], '-1', 'admins', '')
    if p['login'] in admins:
        return True

    return False
