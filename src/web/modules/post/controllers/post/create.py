from flask import request, render_template
import json
import traceback
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow
import web.modules.post.services.upload as upload
import web.util.jinja as jinja
import web.modules.admin.services.notification as notification


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
            raise
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
    p['post'] = {}
    p['original'] = {}
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
            ret = validation(p)
            if ret != True and ret: return ret
        except SystemExit: pass
        except Exception, e:
            raise
    ######################################################

    # create post
    p['post']['created'] = es.now()
    p['post']['created_by'] = p['login']
    response = es.create(host, index, 'post', p['post'].get('id'), p["post"])

    # get created id
    p["post"]["id"] = response["_id"]

    # handle attachment
    #try:
    for f in request.files:
        if request.files[f]:
            p["post"][f] = \
                upload.save(request.files[f], p['c']['allowed_exts'],
                            p["post"]["id"], p['c']['upload_dir'])
    #except Exception, e:
    #    es.delete(host, index, 'post', p['post'].get('id'))
    #    return tools.alert(str(e))

    es.update(host, index, 'post', p["post"]["id"], p["post"])
    es.flush(host, index)

    ######################################################
    # Record History
    if p['c']['keep_history'] == "Yes":
        for k, v in p['post'].items():
            if k in ["updated", "viewed"]: continue
            if p['original'].get(k) != p['post'].get(k):
                # write history
                doc = {
                    "id": p["post"]["id"],
                    "field": k,
                    "previous": unicode(p['original'].get(k)),
                    "current": unicode(p['post'].get(k)),
                    "login": p['login'],
                    "created": es.now()
                }
                es.create(host, index, 'log', '', doc)


    ######################################################
    # Post action
    p['post'] = es.get(host, index, 'post', p["post"]["id"])
    if p['workflow'] and p['workflow'].get('postaction'):
        try:
            exec (p['workflow']['postaction'], globals())
            ret = postaction(p)
            if ret != True and ret: return ret
        except SystemExit: pass
        except Exception, e:
            raise
    ######################################################


    ######################################################
    # notification
    if p['workflow']:
        notifications = es.list(host, index, 'notification', 'workflow:{}'.format(p['workflow'].get('name')))
        for p['notification'] in notifications:
            p['notification']['recipients'] = jinja.getlist(p['notification'].get('recipients'))

            if p['notification'] and p['notification'].get('condition'):
                try:
                    exec (p['notification'].get('condition'), globals())
                    ret = condition(p)
                    if ret != True and ret: return ret
                except SystemExit: pass
                except Exception, e:
                    raise

                # send notification
                notification.send(p,
                    p['notification'].get('header'),
                    p['notification'].get('message'),
                    p['notification'].get('recipients')
                )
    ######################################################


    # redirect to view
    return tools.redirect("{}/post/view/{}".format(p['url'], p["post"]["id"]))
