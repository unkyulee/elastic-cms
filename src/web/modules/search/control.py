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
    return True
