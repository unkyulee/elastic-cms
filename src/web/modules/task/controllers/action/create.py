from flask import render_template, request
import lib.es as es
import web.util.tools as tools

def get(p):
    # Load task
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('not valid task id - {}'.format(task_id))

    # create action
    es.create(p['host'], 'core_task', 'action', '', {
        'task_id': task_id,
        'module_id': tools.get('module_id'),
        'enabled': tools.get('enabled'),
        'stop': tools.get('stop'),
        'order_key': int(tools.get('order_key')),
        'name': tools.get('name'),
        'description': tools.get('description'),
        'connection': tools.get('connection'),
        'query': tools.get('query')
    })
    es.flush(p['host'], 'core_task')

    return tools.redirect(request.referrer)
