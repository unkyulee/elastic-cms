from flask import session, request
import web.util.tools as tools

def get(p):
    session['user'] = None
    return tools.redirect('/auth?url={}'.format(tools.get('url')))
