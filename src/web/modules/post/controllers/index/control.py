from flask import request, render_template
from web.modules.post.services import config
import lib.es as es

def get(p):
    # Post Module Description
    if request.method == "POST":
        if not p['c']['host']: return tools.alert('elasticsearch host is not set')
        if not p['c']['index']: return tools.alert('elasticsearch index is not set')

        # create index
        schema = render_template('install/schema/post.json')
        p['message'] = es.create_index(p['c']['host'], p['c']['index'], schema)

    return render_template("post/index/default.html", p=p)
