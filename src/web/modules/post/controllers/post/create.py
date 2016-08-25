from flask import request, render_template
import json
import traceback
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow
import web.modules.post.services.upload as upload
import web.util.jinja as jinja


def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # send out empty post to be compatible with edit form
    p['post'] = {}

    # init workflow
    wf = tools.get("wf", 'create')
    p['workflow'] = workflow.init(wf, host, index)

    # field map
    fields = es.list(host, index, 'field')
    p['field_map'] = {}
    for field in fields:
        p['field_map'][field['id']] = field

    ######################################################
    # check condition
    if p['workflow'] and p['workflow'].get('condition'):
        try:
            exec (p['workflow']['condition'], globals())
            ret = condition(p)
            if ret != True and ret: return ret
        except SystemExit: pass
        except Exception, e:
            return "{}\n{}".format(e.message, traceback.format_exc())
    ######################################################

    if request.method == "POST":
        return post(p)

    # get list of field
    if p['workflow'] and p['workflow'].get('screen'):
        p['field_list'] = []
        for field in jinja.getlist(p['workflow'].get('screen')):
            query = "name:{}".format(field)
            ret = es.list(host, index, 'field', field, query)
            if len(ret): p['field_list'].append(ret[0])
    else:
        query = "visible:create"
        option = "size=10000&sort=order_key:asc"
        p['field_list'] = es.list(host, index, 'field', query, option)

    return render_template("post/post/create.html", p=p)


def post(p):
    host = p['c']['host']; index = p['c']['index'];

    # get all submitted fields
    p["post"] = {}
    for field in request.form:
        field_info = p['field_map'][field]
        value = tools.get(field)
        # if object then convert to json object
        if field_info['handler'] == "object":
            if value:
                p["post"][field_info['id']] = json.loads(value)
        elif value:
            p["post"][field_info['id']] = value

    ######################################################
    # validate
    if p['workflow'] and p['workflow'].get('validation'):
        try:
            exec (p['workflow']['validation'], globals())
            validation(p)
        except SystemExit: pass
        except Exception, e: return str(e)
    ######################################################

    # create post
    p['post']['created'] = es.now()
    p['post']['created_by'] = p['login']
    response = es.create(host, index, 'post', p['post'].get('id'), p["post"])

    # get created id
    p["post"]["id"] = response["_id"]

    # handle attachment
    try:
        for f in request.files:
            if request.files[f]:
                p["post"][f] = \
                    upload.save(request.files[f], p['c']['allowed_exts'],
                                p["post"]["id"], p['c']['upload_dir'])
    except Exception, e:
        es.delete(host, index, 'post', p['post'].get('id'))
        return tools.alert(e.message)

    es.update(host, index, 'post', p["post"]["id"], p["post"])
    es.flush(host, index)

    ######################################################
    # Post action
    if p['workflow'] and p['workflow'].get('postaction'):
        try:
            exec (p['workflow']['postaction'], globals())
            postaction(p)
        except SystemExit: pass
        except Exception, e: return str(e)

    ######################################################

    # redirect to view
    return tools.redirect("{}/post/view/{}".format(p['url'], p["post"]["id"]))
