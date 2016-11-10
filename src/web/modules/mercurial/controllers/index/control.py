from flask import request, render_template
from web.modules.mercurial.services import config
import lib.es as es
import web.util.tools as tools

def get(p):
    # Post Module Description
    if request.method == "POST":
        # save to global configuration
        h = p['host']; n = p['navigation']['id'];
        tools.set_conf(h, n, 'host', tools.get('host'))
        tools.set_conf(h, n, 'index', tools.get('index'))

        # create index
        schema = render_template('install/schema/post.json')
        p['message'] = es.create_index(tools.get('host'), tools.get('index'), schema)

    return render_template("mercurial/index/default.html", p=p)
