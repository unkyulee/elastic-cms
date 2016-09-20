import importlib
import web.util.tools as tools

# dispatcher
def get(p):
    # read the navigation information and redirect
    return tools.redirect(p['navigation']['url'])


def authorize(p):
    return True
