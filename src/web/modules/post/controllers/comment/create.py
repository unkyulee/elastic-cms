from flask import request, render_template
import time
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow
import web.modules.post.services.upload as upload
import web.util.jinja as jinja
import traceback
import web.modules.admin.services.notification as notification


def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # init workflow
    wf = tools.get("wf", 'comment')
    p['workflow'] = workflow.init(wf, host, index)

    # for workflow actions
    p["post"] = es.get(host, index, 'post', tools.get("post_id"))
    if not p["post"]:
        return tools.alert('post id is not valid- {}'.format(tools.get("post_id")))

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

    # create comment
    id = str(time.time()).replace(".", "")
    p['comment'] = {
        "id": id,
        "comment": tools.get("comment"),
        "created": es.now(),
        "created_by": p['login']
    }
    comments = p["post"].get("comment") \
        if p["post"].get("comment") \
        else []
    comments.append(p['comment'])

    ######################################################
    # validate
    if p['workflow'] and p['workflow'].get('validation'):
        try:
            exec (p['workflow']['validation'], globals())
            ret = validation(p)
            if ret != True and ret: return ret
        except SystemExit: pass
        except Exception, e:
            return "{}\n{}".format(e.message, traceback.format_exc())
    ######################################################

    es.update(host, index, 'post', p["post"]['id'], p['post'])
    es.update(host, index, 'post', p["post"]['id'], {"comment": comments})
    es.flush(host, index)

    ######################################################
    # Post action
    if p['workflow'] and p['workflow'].get('postaction'):
        try:
            exec (p['workflow']['postaction'], globals())
            postaction(p)
        except SystemExit: pass
        except Exception, e:
            return "{}\n{}".format(e.message, traceback.format_exc())
    ######################################################

    ######################################################
    # notification
    if p['workflow']:
        notifications = es.list(host, index,
            'notification', 'workflow:{}'.format(p['workflow'].get('name')))
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

    return tools.redirect(request.referrer)
