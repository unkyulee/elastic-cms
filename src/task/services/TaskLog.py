import traceback
import lib.es as es

# Make a log into TaskLog
class TaskLog():
    def __init__(self, host, task, instance, action):
        self.host = host
        self.task = task
        self.instance = instance
        self.action = action

    def log(self, status, message):
        es.create(self.host, 'core_task', 'log', '', {
            "instance_id": self.instance['id'],
            "action": self.action['name'],
            "status": status,
            "message": message,
            "created": es.now()
        })

    def info(self, message):
        self.log("INFO", message)

    def success(self, message):
        self.log("SUCCESS", message)

    def error(self, message, e):
        m = "{}\n{}\n{}".format(message, e.message, traceback.format_exc())
        self.log("ERROR", m)
