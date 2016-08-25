import importlib
import web.util.tools as tools

# dispatcher
def get(p):

    # load module
    if not p['operation']: p['operation'] = 'default'
    if p['operation'] == 'config': p['operation'] = 'edit'

    path = "web.modules.dashboard.controllers.{}".format(p['operation'])
    control = importlib.import_module(path)
    return control.get(p)



def authorize(p):
    # check which permission the user has
    if not p['operation']: p['operation'] = 'default'
    if p['operation'] == 'config': p['operation'] = 'edit'

    if p['operation'] in p['allowed_operation']:
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
