from flask import render_template
from web import app
import importlib
import web.util.tools as tools

def get(p):
    h = p['host']; n = p['navigation']['id'];

    p['mode'] = 'default'
    if len(p['nav']) > 3 and p['nav'][3]: p['mode'] = p['nav'][3]

    if not p['operation']: p['operation'] = 'post'
    path = "web.modules.post.controllers.search.{}".format(p['mode'])
    control = importlib.import_module(path)

    return control.get(p)
