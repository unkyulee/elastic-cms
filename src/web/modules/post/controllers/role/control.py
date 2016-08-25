import importlib

def get(p):
    p['mode'] = 'default'
    if len(p['nav']) > 3 and p['nav'][3]: p['mode'] = p['nav'][3]

    path = "web.modules.post.controllers.role.{}".format(p['mode'])
    control = importlib.import_module(path)
    return control.get(p)
