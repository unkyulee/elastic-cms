import json
from flask import request, render_template
from web.modules.post.services import config
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # Post Module Description
    if request.method == "POST":
        # parameters
        index_bak = "{}_bak".format(index)
        schema = tools.get('schema')

        # delete index_bak if exists
        if es.index_exists(host, index_bak):
            es.delete_index(host, index_bak)
            es.flush(host, index_bak)

        # create mirror with new schema
        es.create_index(host, index_bak, schema)
        es.flush(host, index_bak)

        # copy post to the backup
        es.reindex(host, index, index_bak)
        es.flush(host, index_bak)

        # delete orginal
        if es.index_exists(host, index):
            es.delete_index(host, index)
            es.flush(host, index)

        # make original with post scheme
        es.create_index(host, index, schema)
        es.flush(host, index)

        # copy back the post from backup
        es.reindex(host, index_bak, index)
        es.flush(host, index)

        # delete backup
        es.delete_index(host, index_bak)
        es.flush(host, index_bak)

        return tools.redirect(request.referrer)

    # get mapping
    p['mapping'] = es.schema(host, index)
    p['mapping'] = json.dumps(p['mapping'], indent=2, sort_keys=True)
    return render_template("post/schema/default.html", p=p)
