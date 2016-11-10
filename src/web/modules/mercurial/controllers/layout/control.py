from flask import request, render_template
from web.modules.mercurial.services import config
import lib.es as es
import web.util.tools as tools

def get(p):
    # get host and index name
    h = p['host']; n = p['navigation']['id'];
    host = tools.get_conf(h, n, 'host', 'http://localhost:9200')
    index = tools.get_conf(h, n, 'index')

    if request.method == "POST":
        config.set_conf(host, index, 'top', tools.get('top'))
        config.set_conf(host, index, 'footer', tools.get('footer'))
        config.set_conf(host, index, 'side', tools.get('side'))
        config.set_conf(host, index, 'content_header', tools.get('content_header'))
        config.set_conf(host, index, 'content_footer', tools.get('content_footer'))
        config.set_conf(host, index, 'intro', tools.get('intro'))
        config.set_conf(host, index, 'list', tools.get('list'))

    p['top'] = config.get_conf(host, index, 'top' ,'')
    p['footer'] = config.get_conf(host, index, 'footer' ,'')
    p['side'] = config.get_conf(host, index, 'side' ,'')
    p['content_header'] = config.get_conf(host, index, 'content_header' ,'')
    p['content_footer'] = config.get_conf(host, index, 'content_footer' ,'')
    p['intro'] = config.get_conf(host, index, 'intro' ,'')
    p['list'] = config.get_conf(host, index, 'list' ,'')

    return render_template("mercurial/layout/default.html", p=p)
