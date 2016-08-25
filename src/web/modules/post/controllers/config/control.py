from flask import request, render_template
from web.modules.post.services import config

def get(p):
    # Post Module Description
    if request.method == "POST":
        config.set(p)
        p['c'] = config.get(p)

    return render_template("post/config/default.html", p=p)
