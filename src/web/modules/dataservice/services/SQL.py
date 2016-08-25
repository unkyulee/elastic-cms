import traceback
import json
from flask import request
from sqlalchemy import create_engine
import web.util.tools as tools
import json_serialize

def execute(p):
    try:
        ### SQL
        # Create sql engine
        engine = create_engine(p['ds']['connection'],
                               isolation_level="READ UNCOMMITTED",
                               strategy='threadlocal')

        conn = engine.connect()

        # Escape some characters % -> %%
        Query = p['ds']['query'].replace("%", "%%")

        # Pass get parameters to the query
        param = {}
        for f in request.args:
            param[f] = request.args[f]
        results = conn.execute(str(Query).format(**param))

        documents = []
        for r in results:
            doc = {}
            for column, value in r.items(): doc[column] = value
            documents.append(doc)
        conn.close()

        # json
        ret_json = json.dumps(documents, default=json_serialize.json_serial)

        if tools.get("callback"):
            return "{}({})".format(callback, ret_json)
        else:
            return ret_json

    except Exception, e:
        return "{}\n{}".format(e.message, traceback.format_exc())
