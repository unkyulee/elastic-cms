import traceback
import lib.es as es


def init(wf, host, index):
    # Get Workflow
    query = "name:{}".format(wf); option = "size=1";
    ret = es.list(host, index, 'workflow', query, option)
    if len(ret): return ret[0]

    return None
