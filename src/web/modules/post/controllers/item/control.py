from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.util.tools as tools
from lib.read import readfile

def get(p):
    h = p['host']; n = p['navigation']['id'];

    if request.method == "POST":
        tools.set_conf(h, n, 'search_item_template', tools.get('search_item_template'))
        return tools.redirect(request.referrer)

    default = readfile("{}/web/templates/post/search/default.html".format(p['base_dir']))
    p['search_item_template'] = tools.get_conf(h, n, 'search_item_template', default)
    return render_template("post/item/default.html", p=p)
