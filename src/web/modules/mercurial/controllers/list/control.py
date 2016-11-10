from flask import render_template
from web import app
import importlib
import web.util.tools as tools

def get(p):
    # load post module
    operation = 'default'
    if len(p['nav']) > 3 and p['nav'][3]: operation = p['nav'][3]

    path = "web.modules.mercurial.controllers.list.{}".format(operation)
    control = importlib.import_module(path)

    return control.get(p)
