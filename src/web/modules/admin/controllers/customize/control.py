import importlib

def get(p):
    operation = 'edit'
    if len(p['nav']) > 3: operation = p['nav'][3]

    path = "web.modules.admin.controllers.customize.{}".format(operation)
    control = importlib.import_module(path)

    return control.get(p)
