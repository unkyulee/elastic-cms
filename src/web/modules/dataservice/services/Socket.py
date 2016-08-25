import socket
import traceback
import json
import json_serialize
import web.util.tools as tools

def execute(p):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Connection = p['ds']['connection'].split(":")
        s.connect((Connection[0], int(Connection[1])))
        s.send(p['ds']['query'])
        documents = s.recv(8000)

        # json
        ret_json = json.dumps(documents, default=json_serialize.json_serial)

        if tools.get("callback"):
            return "{}({})".format(callback, ret_json)
        else:
            return ret_json

    except Exception, e:
        return "{}\n{}".format(e.message, traceback.format_exc())

    return result
