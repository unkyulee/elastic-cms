from flask import request, render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    # Load Action
    action_id = p['nav'][-1]
    p['action'] = es.get(p['host'], 'core_task', 'action', action_id)
    if not p['action']:
        return tools.alert('not valid action id - {}'.format(action_id))

    if request.method == "POST":
        es.update(p['host'], 'core_task', 'action', tools.get('action_id'), {
            'task_id': tools.get('task_id'),
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

    # load module
    p['action']['module'] = es.get(p['host'], 'core_task',
                                   'module', p['action']['module_id'])

    # load task
    p['task'] = es.get(p['host'], 'core_task',
                       'task', tools.get('task_id'))

    # task module list
    option = 'size=10000&sort=description:asc'
    p['task_module_list'] = es.list(p['host'], 'core_task',
                                      'module', '*', option)

    return render_template("task/action/edit.html", p=p)
