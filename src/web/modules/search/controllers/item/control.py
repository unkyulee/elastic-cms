from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.util.tools as tools
from lib.read import readfile

def get(p):
    h = p['host']; n = p['navigation']['id'];

    if request.method == "POST":
        config.set_conf(h, n, 'search_item_template', tools.get('search_item_template'))
        return tools.redirect(request.referrer)

    if not p['c'].get('search_item_template'):
        # set default
        p['c']['search_item_template'] = readfile("{}/web/templates/post/search/default.html".format(p['base_dir']))

    return render_template("post/item/default.html", p=p)
