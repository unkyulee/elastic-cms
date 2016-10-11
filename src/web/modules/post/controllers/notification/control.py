from flask import render_template
from web import app
import importlib
import web.util.tools as tools

def get(p):
    # load notification module
    operation = 'default'
    if len(p['nav']) > 3 and p['nav'][3]: operation = p['nav'][3]

    path = "web.modules.post.controllers.notification.{}".format(operation)
    control = importlib.import_module(path)

    return control.get(p)
