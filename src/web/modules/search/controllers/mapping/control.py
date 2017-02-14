import json
from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];
    # Post Module Description
    if request.method == "POST":
        mapping = tools.get('mapping')
        if not mapping: return tools.alert('no mapping defnition')
        # create mapping
        mapping = json.loads("{"+mapping+"}")
        es.create_mapping(host, index, 'post', mapping)

        return tools.redirect(request.referrer)

    # get mapping
    p['mapping'] = es.mapping(host, index, 'post')
    p['mapping'] = json.dumps(p['mapping'], indent=4, sort_keys=True)
    return render_template("post/mapping/default.html", p=p)
