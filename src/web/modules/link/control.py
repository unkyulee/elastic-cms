import importlib
import web.util.tools as tools

# dispatcher
def get(p):
    # replace {{login}}
    p['navigation']['url'] = p['navigation']['url'].replace('{{login}}', p['login'])

    # read the navigation information and redirect
    return tools.redirect(p['navigation']['url'])


def authorize(p):
    return True
