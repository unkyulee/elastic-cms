from flask import render_template, request
import lib.es as es
import web.util.tools as tools

def get(p):
    # load task
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('task not found - {}'.format(task_id))

    es.delete(p['host'], 'core_task', 'task', task_id)
    es.flush(p['host'], 'core_task')

    return tools.redirect(request.referrer)
