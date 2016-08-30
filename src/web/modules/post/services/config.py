import web.util.tools as tools
import os
from web import app

def get(p):
    h = p['host']; n = p['navigation']['id'];

    return {
        'name': tools.get_conf(h, n, 'name', ''),
        'description': tools.get_conf(h, n, 'description', ''),
        'host': tools.get_conf(h, n, 'host', ''),
        'index': tools.get_conf(h, n, 'index', ''),
        'upload_dir':
            tools.get_conf(h, n, 'upload_dir',
                os.path.join( app.config.get('BASE_DIR'), 'uploads' )
            ),
        'allowed_exts': tools.get_conf(h, n, 'allowed_exts',''),
        'page_size': tools.get_conf(h, n, 'page_size', '10'),
        'query': tools.get_conf(h, n, 'query', '*'),
        'sort_field': tools.get_conf(h, n, 'sort_field', '_score'),
        'sort_dir': tools.get_conf(h, n, 'sort_dir', 'desc')
    }


def set(p):
    h = p['host']; n = p['navigation']['id'];

    tools.set_conf(h, n, 'name', tools.get('name'))
    tools.set_conf(h, n, 'description', tools.get('description'))
    tools.set_conf(h, n, 'host', tools.get('host'))
    tools.set_conf(h, n, 'index', tools.get('index'))
    tools.set_conf(h, n, 'upload_dir', tools.get('upload_dir'))
    tools.set_conf(h, n, 'allowed_exts', tools.get('allowed_exts'))
    tools.set_conf(h, n, 'page_size', tools.get('page_size'))
    tools.set_conf(h, n, 'query', tools.get('query'))
    tools.set_conf(h, n, 'sort_field', tools.get('sort_field'))
    tools.set_conf(h, n, 'sort_dir', tools.get('sort_dir'))
