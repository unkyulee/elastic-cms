from flask import request, render_template
from web.modules.mercurial.services import config

def get(p):
    # Post Module Description
    if request.method == "POST":
        config.set(p)
        p['c'] = config.get(p)

    return render_template("mercurial/config/default.html", p=p)
