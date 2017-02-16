import urlparse
from flask import request
import lib.es as es
import web.util.tools as tools

def get(p):
    index = tools.get('index')
    id = tools.get('id')
    if not index or not id:
        return tools.alert('invalid id or index')

    # find config with matching index
    configs = es.list(p['host'], 'core_nav', 'config',
        "name:'index' AND value:'{}'".format(index))
    if not len(configs) > 0:
        return tools.alert('site not found')

    # get site id
    navigation_id = configs[0]['id'].split('_')[0]
    navigation = es.get(p['host'], 'core_nav', 'navigation', navigation_id)
    site = es.get(p['host'], 'core_nav', 'site', navigation['site_id'])

    # form url
    url = urlparse.urljoin(request.url_root, site.get('name'))
    url = urlparse.urljoin(url, navigation.get('name'))

    # add id at the end of the url
    url = "{}/post/view/{}".format(url, id)

    return tools.redirect(url)
