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

    # load field list
    p['field_list'] = es.list(host, index, 'field', '*', 'size=1000&sort=name:asc')

    # save workflow
    if request.method == "POST":
        return post(p, host, index, p['workflow'])
    # display workflow edit page
    return render_template("post/workflow/edit.html", p=p)


def post(p, host, index, workflow):
    host = p['c']['host']; index = p['c']['index'];

    doc = {
        "name" : tools.get("name"),
        "description" : tools.get("description"),
        "status" : tools.get("status"),
        "condition" : tools.get("condition"),
        "validation" : tools.get('validation'),
        "postaction" : tools.get('postaction'),
        "screen" : tools.get('screen')
    }
    es.update(host, index, 'workflow', workflow["id"], doc)
    es.flush(host, index)

    return tools.redirect(request.referrer)
