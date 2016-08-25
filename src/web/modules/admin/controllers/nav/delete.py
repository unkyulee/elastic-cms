from flask import request
from lib import es
import web.util.tools as tools

def get(p):

    # load navigation
    navigation_id = p['nav'][-1]
    navigation = es.get(p['host'], 'core_nav', 'navigation', navigation_id)
    if not navigation:
        return tools.alert('not valid navigation id - {}'.format(navigation_id))

    # root site can't be edited
    if navigation_id in ["0", "1", "2", "3"]:
        return tools.alert("can't delete system navigation")


    # delete
    es.delete(p['host'], 'core_nav', 'navigation', navigation_id)
    es.flush(p['host'], 'core_nav')

    return tools.redirect(request.referrer)
