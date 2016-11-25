from flask import render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    # load instance
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('invalid task id - {}'.format(task_id))

    # instance list
    query = 'task_id:{}'.format(task_id)
    option = 'size=50'
    if es.count(p['host'], 'core_task', 'instance'):
        option += '&sort=created:desc'
    p['history_list'] = es.list(p['host'], 'core_task', 'instance',
                                  query, option)

    for history in p['history_list']:
        # statistics
        query = "instance_id:{}".format(history['id'])
        history['total'] = es.count(p['host'], 'core_task', 'log', query)
        if not history['total']: history['total'] = ''

        query = "instance_id:{} AND status:SUCCESS".format(history['id'])
        history['success'] = es.count(p['host'], 'core_task', 'log', query)
        if not history['success']: history['success'] = ''

        query = "instance_id:{} AND status:ERROR".format(history['id'])
        history['error'] = es.count(p['host'], 'core_task', 'log', query)
        if not history['error']: history['error'] = ''

    return render_template("task/status/history.html", p=p)
