import json
from flask import render_template, request
import web.util.tools as tools
import lib.es as es

def get(p):
    if request.method == "POST":
        # read file
        file_content = request.files["restore"].read()
        # convert to json
        docs = json.loads(file_content)
        # restore
        count = es.restore(p['c']['host'], p['c']['index'], docs)
        p["message"] = "{} records resotred".format(count)

    return render_template("post/backup/default.html", p=p)
