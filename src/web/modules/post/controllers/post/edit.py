from flask import render_template, request
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

    # load post
    post_id = p['nav'][-1]
    p['post'] = es.get(host, index, 'post', post_id)
    p['original'] = es.get(host, index, 'post', post_id)
    if not p['post']:
        return tools.alert('not valid post id - {}'.format(post_id))

    # init workflow
    wf = tools.get('wf', 'edit')
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
    else:
        # check ACL
        valid_acl = False
        if p['login'] == p['post'].get('created_by'): valid_acl = True
        if p['post'].get('acl_edit'):
            if p['login'] in p['post'].get('acl_edit'): valid_acl = True
            if 'EVERYONE' in p['post'].get('acl_edit'): valid_acl = True
        if not valid_acl:
            return tools.alert('permission not granted')
    ######################################################

    if request.method == "POST":
        return post(p)

    # get list of field
    if p['workflow'] and p['workflow'].get('screen'):
        p['field_list'] = []
        for field in jinja.getlist(p['workflow'].get('screen')):
            f = es.get(host, index, 'field', field)
            p['field_list'].append(f)
    else:
        query = "visible:edit"
        option = "size=10000&sort=order_key:asc"
        p['field_list'] = es.list(host, index, 'field', query, option)

    return render_template("post/post/edit.html",p=p)


def post(p):
    host = p['c']['host']; index = p['c']['index'];

    # get all submitted fields
    p["post"] = {"id": p['nav'][-1]}
    for field in request.form:
        field_info = p['field_map'][field]
        value = tools.get(field)
        print field_info['id'], value

        # if object then convert to json object
        if field_info.get('handler') == "object":
            if value:
                p["post"][field_info['id']] = json.loads(value)

        # save the value when it's different than the previous value
        elif value:
            p["post"][field_info['id']] = value

        # if the value is emptied
        elif not value and p['original'].get(field_info['id']):
            p["post"][field_info['id']] = value


    ######################################################
    # if acl_edit is set then acl_readonly MUST not be empty
    if p['post'].get('acl_edit') and not p['post'].get('acl_readonly'):
         p['post']['acl_readonly'] = p['post'].get('acl_edit')


    ######################################################
    # validate
    if p['workflow'] and p['workflow'].get('validation'):
        try:
            exec (p['workflow']['validation'], globals())
            validation(p)
        except SystemExit: pass
        except Exception, e:
            return "{}\n{}".format(e.message, traceback.format_exc())
    ######################################################

    # handle attachment
    try:
        for f in request.files:
            if request.files[f]:
                p["post"][f] = \
                    upload.save(request.files[f], p['c']['allowed_exts'],
                                p["post"]["id"], p['c']['upload_dir'])
    except Exception, e:
        return tools.alert(str(e))

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

    # update post
    p['post']['updated'] = es.now()
    p['post']['updated_by'] = p['login']
    es.update(host, index, 'post', p["post"]["id"], p["post"])
    es.flush(host, index)


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
            return "{}\n{}".format(e.message, traceback.format_exc())
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
                    return "{}\n{}".format(e.message, traceback.format_exc())

                # send notification
                notification.send(p,
                    p['notification'].get('header'),
                    p['notification'].get('message'),
                    p['notification'].get('recipients')
                )
    ######################################################

    # redirect to view
    if tools.get("redirect"):
        return tools.redirect(tools.get("redirect"))
    return tools.redirect("{}/post/view/{}".format(p['url'], p["post"]["id"]))
