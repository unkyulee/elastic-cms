from flask import render_template
import lib.es as es

def get(p):

    # Load Task List
    option = None
    query = 'navigation_id:{}'.format(p['navigation']['id'])
    if es.count(p['host'], 'core_task', 'task'):
        option = 'sort=name:asc'
    p['task_list'] = es.list(p['host'], 'core_task', 'task', query, option)

    # get last instance information
    for task in p['task_list']:
        query = 'task_id:{}'.format(task['id'])
        option = None
        if es.count(p['host'], 'core_task', 'instance'):
            option = 'sort=created:desc'

        ret = es.list(p['host'], 'core_task', 'instance', query, option)
        task['instance'] = {}
        if len(ret):
            task['instance'] = ret[0]    

    return render_template("task/task/default.html", p=p)
