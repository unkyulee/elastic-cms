from subprocess import PIPE, Popen
from sqlalchemy import create_engine

def run(p):
    try:
        p["log"].info(p["action"]['query'])
        proc = Popen(p["action"]['query'], shell=True,
                     stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result = proc.communicate()
        message = ''
        for r in result:
            if r: message += r + '\n'
        p["log"].success(message)
    except Exception, e:
        AllGood = False
        p["log"].error("command line execution failed",e)

    return True
