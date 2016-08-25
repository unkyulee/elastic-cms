from datetime import datetime
import lib.es as es
from config import * # get all configuration


# Get Waiting Task
def waiting_tasks(hostname):
    # get list of tasks that should run under this host
    query = "runat:{} OR runat:anywhere".format(hostname)
    option = "size=10000"
    task_list = es.list(HOST, 'core_task', 'task', query, option)

    # get list of waiting instances
    instances = []
    for task in task_list:
        query = "status:WAITING AND task_id:{}".format(task['id'])
        option = "size=10000"
        instance_list = es.list(HOST, 'core_task', 'instance', query, option)
        for instance in instance_list:
            instance['task'] = task
            instances.append(instance)

    return instances





# Get list of scheduled tasks
def trigger_scheduled_tasks():
    # today
    dayofmonth = datetime.today().day
    dayofweek = datetime.today().weekday()
    hour = datetime.today().hour
    minute = datetime.today().minute

    # get list of tasks that should run under this host
    query = """
        (dayofmonth:{} OR dayofmonth:None) AND
        (dayofweek:{} OR dayofweek:None) AND
        (hour:{} OR hour:None) AND
        (minute:{} OR minute:None)
    """.format( dayofmonth, dayofweek, hour, minute )
    ret = es.list(HOST, 'core_task', 'schedule', query)
    
    for schedule in ret:
        # check if instance exists
        query = """
            task_id:{} AND
            created:[now-1m TO now+1m]
        """.format(schedule['task_id'])
        instance = es.list(HOST, 'core_task', 'instance', query)
        if len(instance) > 0:
            continue # task already triggered
        # create instance
        es.create(HOST, 'core_task', 'instance', '', {
            "task_id": schedule['task_id'],
            "status": "WAITING",
            "login": "agent",
            "created": es.now()
        })
        es.flush(HOST, 'core_task')



# Get list of action to run through
def actions(task_id):
    query = "task_id:{} AND enabled:Yes".format(task_id)
    option = "size=10000&sort=order_key:asc"
    actions = es.list(HOST, 'core_task', 'action', query, option)
    for action in actions:
        action['module'] = es.get(HOST, 'core_task',
                                  'module', action['module_id'])

    return actions











# set instance status
def status(instance, status):
    es.update(HOST, 'core_task', 'instance', instance['id'], {
        "status": status
    })
    es.flush(HOST, 'core_task')


# Set Task Started
def started(instance):
    es.update(HOST, 'core_task', 'instance', instance['id'], {
        "started": es.now()
    })
    es.flush(HOST, 'core_task')


# Set Task Finished
def finished(instance):
    es.update(HOST, 'core_task', 'instance', instance['id'], {
        "finished": es.now()
    })
    es.flush(HOST, 'core_task')
