from flask import render_template
from web import app
import importlib
import web.util.tools as tools

def get(p):
    h = p['host']; n = p['navigation']['id'];

    # load post module
    operation = 'default'
    if len(p['nav']) > 3 and p['nav'][3]: operation = p['nav'][3]

    path = "web.modules.post.controllers.post.{}".format(operation)
    control = importlib.import_module(path)

    # load top, footer, left
    p['top'] = tools.get_conf(h, n, 'top', '')
    p['footer'] = tools.get_conf(h, n, 'footer', '')
    p['side'] = tools.get_conf(h, n, 'side', '')
    p['content_header'] = tools.get_conf(h, n, 'content_header', '')
    p['content_footer'] = tools.get_conf(h, n, 'content_footer', '')
    p['intro'] = tools.get_conf(h, n, 'intro', '')

    return control.get(p)
