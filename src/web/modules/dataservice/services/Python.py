import traceback
import lib.python as py

def execute(p):
    try:
        return py.run_python(p['ds']['query'])        
    except Exception, e:
        return "{}\n{}".format(e.message, traceback.format_exc())
