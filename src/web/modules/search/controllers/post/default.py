# post list
from flask import render_template
import json
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # return search results in jsonp format
    if tools.get("json"):
        callback = tools.get("callback")
        if not callback:
            return json.dumps(p["post_list"])
        else:
            return "{}({})".format(callback, json.dumps(p["post_list"]))

    # Get Visible Fields of List
    option = "size=1000&sort=order_key:asc"
    p['field_list'] = es.list(host, index, 'field', 'visible:list', option)

    # if list exists then load list
    #ListCustom = LoadConfiguration(p["SiteId"], p["NavigationId"], "list")
    #if ListCustom: return render_template(app.jinja_env.from_string(ListCustom), p=p)
    return render_template("post/post/default.html", p=p)
