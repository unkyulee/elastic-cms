from flask import request, render_template
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow
import web.modules.post.services.upload as upload
import web.util.jinja as jinja


def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # init workflow
    wf = tools.get("wf", 'comment_edit')
    p['workflow'] = workflow.init(wf, host, index)

    # load comment
    post_id = p['nav'][-1]
    p['post'] = es.get(host, index, 'post', post_id)
    if not p['post']:
        return tools.alert('not valid post id - {}'.format(post_id))

    # comment_id
    comment_id = tools.get("id")
    p['comment'] = next((x for x in p['post']['comment'] if x['id'] == comment_id), None)
    if not p['comment']:
        return tools.alert('not valid comment_id - {}'.format(comment_id))

    # field map
    fields = es.list(host, index, 'field')
    p['field_map'] = {}
    for field in fields:
        p['field_map'][field['name']] = field['id']

    # update comment
    p['comment']['updated'] = es.now()
    p['comment']['updated_by'] = p['login']
    p['comment']['comment'] = tools.get("comment")

    es.update(host, index, 'post', post_id, p['post'])
    es.flush(host, index)

    return tools.redirect(request.referrer)
