from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.modules.install.modules.document.install as doc_install

def get(p):
    # Post Module Description
    if request.method == "POST":
        if not p['c']['host']: return tools.alert('elasticsearch host is not set')
        if not p['c']['index']: return tools.alert('elasticsearch index is not set')

        # create index
        host = p['c']['host']
        index = p['c']['index']
        schema = render_template('install/schema/post.json')
        p['message'] = es.create_index(host, index, schema)
        es.flush(host, index)

        # create ACL
        doc_install.create_acl(host, index)


    return render_template("post/index/default.html", p=p)
