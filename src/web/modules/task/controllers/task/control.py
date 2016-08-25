import importlib

def get(p):
    operation = 'default'
    if len(p['nav']) > 3: operation = p['nav'][3]

    path = "web.modules.task.controllers.task.{}".format(operation)
    control = importlib.import_module(path)
    return control.get(p)
