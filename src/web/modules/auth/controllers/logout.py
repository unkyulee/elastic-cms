from flask import session, request
import web.util.tools as tools
from . import default

def get(p):
    session['user'] = None
    return tools.redirect('/auth?url={}'.format(default.get_return_url()))
