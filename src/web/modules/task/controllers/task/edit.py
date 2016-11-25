from flask import render_template, request
import lib.es as es
import web.util.tools as tools

def get(p):
    # load task
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('task not found - {}'.format(task_id))

    if request.method == "POST":
        es.update(p['host'], 'core_task', 'task', task_id, {
            'navigation_id': p['navigation']['id'],
            'name': tools.get('name'),
            'runat': tools.get('runat') if tools.get('runat') else 'anywhere' ,
            'description': tools.get('description')
        })
        es.flush(p['host'], 'core_task')

        return tools.redirect(request.referrer)

    # load action list
    # when there are no records then the task fails to run
    option = ''
    if es.count(p['host'], 'core_task', 'action'):
        option = 'size=10000&sort=order_key:asc'

    query = 'task_id:{}'.format(p['task']['id'])
    p['action_list'] = es.list(p['host'], 'core_task', 'action',
                                 query, option)
    for action in p['action_list']:
        action['module'] = es.get(p['host'], 'core_task', 'module', action['module_id'])

    # load schedule list
    query = 'task_id:{}'.format(p['task']['id'])
    p['schedule_list'] = es.list(p['host'], 'core_task', 'schedule', query)

    # load task module List
    option = 'size=10000&sort=description:asc'
    p['task_module_list'] = es.list(p['host'], 'core_task', 'module', '*', option)

    return render_template("task/task/edit.html", p=p)
