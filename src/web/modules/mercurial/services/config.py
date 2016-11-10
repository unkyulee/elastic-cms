import os
from web import app
import web.util.tools as tools
import lib.es as es

def get(p):
    # get host and index name
    h = p['host']; n = p['navigation']['id'];
    host = tools.get_conf(h, n, 'host', 'http://localhost:9200')
    index = tools.get_conf(h, n, 'index')

    return {
        'name': get_conf(host, index, 'name', ''),
        'description': get_conf(host, index, 'description', ''),
        'mercurial_path': get_conf(host, index, 'mercurial_path', ''),
        'host': host,
        'index': index
    }


def set(p):
    # get host and index name
    h = p['host']; n = p['navigation']['id'];
    host = tools.get_conf(h, n, 'host', 'http://localhost:9200')
    index = tools.get_conf(h, n, 'index')

    # set config in post scheme
    set_conf(host, index, 'name', tools.get('name'))
    set_conf(host, index, 'description', tools.get('description'))
    set_conf(host, index, 'mercurial_path', tools.get('mercurial_path'))


# read configuraiton
def get_conf(host, index, name, default=None):
    ret = es.get(host, index, "config", name)
    return ret.get('value') if ret and ret.get('value') else default


# save configuration
def set_conf(host, index, name, value):
    doc = { "name": name, "value": value }
    es.update(host, index, "config", name, doc)
    es.flush(host, index)
