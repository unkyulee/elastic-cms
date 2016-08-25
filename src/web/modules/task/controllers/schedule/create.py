from flask import request
import web.util.tools as tools
import lib.es as es

def get(p):
    # load task
    task_id = p['nav'][-1]
    p['task'] = es.get(p['host'], 'core_task', 'task', task_id)
    if not p['task']:
        return tools.alert('task not found - {}'.format(task_id))

    # Create Schedule
    doc = {
        "task_id": task_id,
        "dayofmonth": tools.get("dayofmonth", 'None'),
        "dayofweek": tools.get("dayofweek", 'None'),
        "hour": tools.get("hour", 'None'),
        "minute": tools.get("minute", 'None')
    }
    es.create(p['host'], 'core_task', 'schedule', '', doc)
    es.flush(p['host'], 'core_task')


    return tools.redirect(request.referrer)
