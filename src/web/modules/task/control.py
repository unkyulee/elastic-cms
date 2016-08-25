import importlib
import web.util.tools as tools

def get(p):
    # load module
    if not p['operation']: p['operation'] = 'task'
    if p['operation'] == 'config': p['operation'] = 'permission'
    path = "web.modules.task.controllers.{}.control".format(p['operation'])
    control = importlib.import_module(path)

    return control.get(p)



def authorize(p):
    # get operation/mode string
    if not p['operation']:
        auth_key = 'task/default'
    else:
        auth_key = p['operation'] + '/'

    if len(p['nav']) > 3 and p['nav'][3]:
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
