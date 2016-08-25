
g = None
def run(p):
    ProceedWorkflow = False
    try:
        # Save parameter to global g
        global g; g = p["g"];
        exec (p["action"]['query'], globals())
        ProceedWorkflow = IsReady()
        p["log"].info("Is Ready: {}".format(ProceedWorkflow))
    except Exception, e:
        p["log"].error("init() function failed",e)

    return ProceedWorkflow
