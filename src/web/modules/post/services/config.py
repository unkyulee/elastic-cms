import web.util.tools as tools
import os
from web import app
import lib.es as es

def get(p):
    # get host and index from the global config
    h = tools.get_conf(p['host'], p['navigation']['id'], 'host', 'http://localhost:9200')
    n = tools.get_conf(p['host'], p['navigation']['id'], 'index', '')

    return {
        'name': get_conf(h, n, 'name', ''),
        'description': get_conf(h, n, 'description', ''),
        'host': h,
        'index': n,
        'upload_dir':
            get_conf(h, n, 'upload_dir',
                os.path.join( app.config.get('BASE_DIR'), 'uploads' )
            ),
        'allowed_exts': get_conf(h, n, 'allowed_exts',''),
        'page_size': get_conf(h, n, 'page_size', '10'),
        'query': get_conf(h, n, 'query', '*'),
        'sort_field': get_conf(h, n, 'sort_field', '_score'),
        'sort_dir': get_conf(h, n, 'sort_dir', 'desc'),
        'top': get_conf(h, n, 'top', ''),
        'footer': get_conf(h, n, 'footer', ''),
        'side': get_conf(h, n, 'side', ''),
        'content_header': get_conf(h, n, 'content_header', ''),
        'content_footer': get_conf(h, n, 'content_footer', ''),
        'intro': get_conf(h, n, 'intro', ''),
        'search_query': get_conf(h, n, 'intro', ''),
    }

def set(p):
    # get host and index from the global config
    h = tools.get_conf(p['host'], p['navigation']['id'], 'host', 'http://localhost:9200')
    n = tools.get_conf(p['host'], p['navigation']['id'], 'index', '')

    set_conf(h, n, 'name', tools.get('name'))
    set_conf(h, n, 'description', tools.get('description'))
    set_conf(h, n, 'upload_dir', tools.get('upload_dir'))
    set_conf(h, n, 'allowed_exts', tools.get('allowed_exts'))
    set_conf(h, n, 'page_size', tools.get('page_size'))
    set_conf(h, n, 'query', tools.get('query'))
    set_conf(h, n, 'sort_field', tools.get('sort_field'))
    set_conf(h, n, 'sort_dir', tools.get('sort_dir'))


def get_conf(host, index, name, default):
    ret = es.get(host, index, "config", name)
    return ret.get('value') if ret and ret.get('value') else default


def set_conf(host, index, name, value):
    config = {
        'name': name,
        'value': value
    }
    es.update(host, index, "config", name, config)
    es.flush(host, index)
