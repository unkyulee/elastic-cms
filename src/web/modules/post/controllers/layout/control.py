from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.util.tools as tools

def get(p):
    h = p['host']; n = p['navigation']['id'];

    if request.method == "POST":
        tools.set_conf(h, n, 'top', tools.get('top'))
        tools.set_conf(h, n, 'footer', tools.get('footer'))
        tools.set_conf(h, n, 'side', tools.get('side'))
        tools.set_conf(h, n, 'content_header', tools.get('content_header'))
        tools.set_conf(h, n, 'content_footer', tools.get('content_footer'))
        tools.set_conf(h, n, 'intro', tools.get('intro'))

    p['top'] = tools.get_conf(h, n, 'top' ,'')
    p['footer'] = tools.get_conf(h, n, 'footer' ,'')
    p['side'] = tools.get_conf(h, n, 'side' ,'')
    p['content_header'] = tools.get_conf(h, n, 'content_header' ,'')
    p['content_footer'] = tools.get_conf(h, n, 'content_footer' ,'')
    p['intro'] = tools.get_conf(h, n, 'intro' ,'')

    return render_template("post/layout/default.html", p=p)
