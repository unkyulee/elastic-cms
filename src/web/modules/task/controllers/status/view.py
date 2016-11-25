from flask import render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    # load instance
    instance_id = p['nav'][-1]
    p['instance'] = es.get(p['host'], 'core_task', 'instance', instance_id)
    if not p['instance']:
        return tools.alert('invalid instance id - {}'.format(instance_id))

    # load task
    p['task'] = es.get(p['host'], 'core_task', 'task', p['instance']['task_id'])

    # statistics
    query = "instance_id:{}".format(p['instance']['id'])
    p['total'] = es.count(p['host'], 'core_task', 'log', query)

    query = "instance_id:{} AND status:SUCCESS".format(p['instance']['id'])
    p['success'] = es.count(p['host'], 'core_task', 'log', query)

    query = "instance_id:{} AND status:ERROR".format(p['instance']['id'])
    p['error'] = es.count(p['host'], 'core_task', 'log', query)

    return render_template("task/status/default.html", p=p)
