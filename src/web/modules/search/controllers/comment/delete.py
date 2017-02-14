from flask import render_template, request
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load comment
    post_id = p['nav'][-1]
    p['post'] = es.get(host, index, 'post', post_id)
    if not p['post']:
        return tools.alert('not valid post id - {}'.format(post_id))

    # comment_id
    comment_id = tools.get("id")
    p['comment'] = next((x for x in p['post']['comment'] if x['id'] == comment_id), {})
    if not p['comment']:
        return tools.alert('not valid comment_id - {}'.format(comment_id))

    # init workflow
    wf = tools.get('wf', 'comment_delete')
    p['workflow'] = workflow.init(wf, host, index)

    # remove comment
    p['post']['comment'].remove(p['comment'])

    es.update(host, index, 'post', post_id, p['post'])
    es.flush(host, index)

    return tools.redirect(request.referrer)
