import importlib

def get(p):
    p['mode'] = 'view'
    if len(p['nav']) > 3: p['mode'] = p['nav'][3]

    if not p['operation']: p['operation'] = 'post'
    path = "web.modules.post.controllers.file.{}".format(p['mode'])
    control = importlib.import_module(path)
    return control.get(p)
