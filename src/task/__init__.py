import time
import importlib
import traceback
from threading import Thread
import task.services.task as task
from task.services.TaskLog import *
from config import *


def monitor_infinite():
    print("Starting Task Runner ...")
    while True:
        monitor_once()
        time.sleep(5) # loop every 5s


# Monitor Task and run inifitely to process the task
def monitor_once():
    instances = []

    # Any Task waiting?
    import socket
    hostname = socket.gethostname()

    # trigger schedule tasks
    task.trigger_scheduled_tasks()

    # get waiting instances
    instances.extend(task.waiting_tasks(hostname))

    # Run Task
    for instance in instances:
        print("[{}] * New task found [{}]: {}".format(
            now(), instance['id'], instance['task']['name'])
        )
        thread = Thread(target = run_task, args = (instance,))
        thread.start()


# Run Task - this should be thread
def run_task(instance):
    task_successful = True

    # Set instance "RUNNING"
    task.status(instance, "RUNNING")

    # set instance started time
    task.started(instance)

    # Get List of action
    actions = task.actions(instance['task_id'])
    for action in actions:
        print("[{}] Action: {}".format(now(), action['name']))
        log = TaskLog(HOST, task, instance, action)
        # prepare parameters
        p = {
            'instance': instance,
            'action': action,
            'log': log
        }
        # run task
        task_module_path = "task.modules.{}".format(action['module']['name'])
        module = importlib.import_module(task_module_path)
        try:
            task_successful = module.run(p)
            if not task_successful and action['stop'] != "No":
                log.info("stopped - {}".format(action['name']))
                break
        except Exception, e:
            print(e.message)
            print(traceback.format_exc())
            log.error("action failed: {}".format(action['name']), e)


    # Set instance "RUNNING"
    if task_successful:
        task.status(instance, "COMPLETED")
    else:
        task.status(instance, "ERROR")

    # set instance finished time
    task.finished(instance)



# instead of using dateformat thingy all the time
def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')
