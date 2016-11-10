from flask import request, render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load workflow
    workflow_id = p['nav'][-1]
    p['workflow'] = es.get(host, index, 'workflow', workflow_id)
    if not p['workflow']:
        return tools.alert('not valid workflow id - {}'.format(workflow_id))

    # delete
    es.delete(host, index, 'workflow', workflow_id)
    es.flush(host, index)

    return tools.redirect(request.referrer)
