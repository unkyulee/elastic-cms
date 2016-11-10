import importlib

def get(p):
    p['mode'] = 'default'
    if len(p['nav']) > 3: p['mode'] = p['nav'][3]

    if not p['operation']: p['operation'] = 'post'
    path = "web.modules.mercurial.controllers.workflow.{}".format(p['mode'])
    control = importlib.import_module(path)
    return control.get(p)
