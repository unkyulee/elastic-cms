import lib.es as es
import web.util.tools as tools

def get(p):
    # load task
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('task not found - {}'.format(task_id))

    response = es.create(p['host'], 'core_task', 'instance', '', {
        'task_id': task_id,
        'status': 'WAITING',
        'login': p['login'],
        'created': es.now()
    })
    es.flush(p['host'], 'core_task')

    # redirect to status
    return tools.redirect("{}/status/view/{}".format(p['url'], response['_id']))
