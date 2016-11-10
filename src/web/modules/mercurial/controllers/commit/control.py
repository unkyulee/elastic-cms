from flask import render_template
from web import app
import importlib
import web.util.tools as tools

def get(p):
    # load post module
    operation = 'default'
    path = "web.modules.mercurial.controllers.commit.{}".format(operation)
    control = importlib.import_module(path)

    return control.get(p)
