from flask import request, render_template
from web.modules.post.services import config
import web.util.tools as tools
import lib.es as es

def get(p):
    h = p['c']['host']; n = p['c']['index'];

    if request.method == "POST":
        config.set_conf(h, n, 'top', tools.get('top'))
        config.set_conf(h, n, 'footer', tools.get('footer'))
        config.set_conf(h, n, 'side', tools.get('side'))
        config.set_conf(h, n, 'content_header', tools.get('content_header'))
        config.set_conf(h, n, 'content_footer', tools.get('content_footer'))
        config.set_conf(h, n, 'intro', tools.get('intro'))
        es.flush(h, n)

    return render_template("post/layout/default.html", p=p)
