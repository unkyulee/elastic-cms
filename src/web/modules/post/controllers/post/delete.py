from flask import render_template, request
import lib.es as es
import web.util.tools as tools
import web.modules.post.services.workflow as workflow

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load post
    post_id = p['nav'][-1]
    p['post'] = es.get(host, index, 'post', post_id)
    if not p['post']:
        return tools.alert('not valid post id - {}'.format(post_id))

    # init workflow
    wf = tools.get('wf', 'delete')
    p['workflow'] = workflow.init(wf, host, index)

    ######################################################
    # check condition
    if p['workflow'] and p['workflow'].get('condition'):
        try:
            exec (p['workflow']['condition'], globals())
            condition(p)
        except SystemExit: pass
        except Exception, e: return str(e)
    else:
        # default condition is that only author can edit
        if p['post'].get('created_by') != p['login']:
            return tools.alert('only author can delete')
    ######################################################

    es.delete(host, index, 'post', post_id)
    es.flush(host, index)

    return tools.redirect(p['url'])
