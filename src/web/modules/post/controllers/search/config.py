from flask import request, render_template
import web.util.tools as tools
from lib.read import readfile

def get(p):
    h = p['host']; n = p['navigation']['id'];

    # Post Module Description
    if request.method == "POST":
        tools.set_conf(h, n, 'search_query', tools.get('search_query'))
        tools.set_conf(h, n, 'search_item', tools.get('search_item'))
        return tools.redirect(request.referrer)

    path = "{}/web/templates/post/search/part/search_query.json".format(p['base_dir'])
    p['search_query'] = tools.get_conf(h, n, 'search_query', readfile(path))

    path = "{}/web/templates/post/search/part/search_item.html".format(p['base_dir'])
    p['search_item'] = tools.get_conf(h, n, 'search_item' ,readfile(path))
    return render_template("post/search/config.html", p=p)
