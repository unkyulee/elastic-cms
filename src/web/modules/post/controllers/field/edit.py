from flask import request, render_template
import web.util.tools as tools
import lib.es as es

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load field
    field_id = p['nav'][-1]
    p['field'] = es.get(host, index, 'field', field_id)
    if not p['field']:
        return tools.alert('not valid field id - {}'.format(field_id))

    # save field
    if request.method == "POST":
        return post(p, host, index)

    return render_template('post/field/edit.html', p=p)


# Post handler
def post(p, host, index):
    # save field
    doc = {
        "is_filter": tools.get("is_filter"),
        "filter_field": tools.get("filter_field"),
        "handler": tools.get("handler"),
        "name": tools.get("name"),
        "visible": tools.get("visible"),
        "order_key": int(tools.get("order_key")),
        "list_tpl": tools.get("list_tpl"),
        "view_tpl": tools.get("view_tpl"),
        "edit_tpl": tools.get("edit_tpl")
    }

    es.update(host, index, 'field', p['field']['id'], doc)
    es.flush(host, index)
    return tools.redirect(request.referrer)
