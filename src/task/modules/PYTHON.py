import lib.python as py

def run(p):
    try:
        ret = py.run_python(p["action"]['query'])
        p["log"].success(ret)
    except SystemExit:
        # ignore exit()
        pass
    except Exception, e:
        p["log"].error("Python code execution failed.", e)
        return False

    return True
