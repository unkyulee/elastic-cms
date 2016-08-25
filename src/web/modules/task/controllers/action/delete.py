from flask import render_template, request
import lib.es as es
import web.util.tools as tools

def get(p):
    # Load Action
    action_id = p['nav'][-1]
    p['action'] = es.get(p['host'], 'core_task', 'action', action_id)
    if not p['action']:
        return tools.alert('not valid action id - {}'.format(action_id))

    # delete
    es.delete(p['host'], 'core_task', 'action', p['action']['id'])
    es.flush(p['host'], 'core_task')

    return tools.redirect(request.referrer)
