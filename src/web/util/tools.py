# toolset for web
import os
from flask import request
from lib import es
from web import app


# redirect
def redirect(url):
    return "<script>location='{}'</script>".format(url)


# alert
def alert(message, url=''):
    message = message.replace("\"", "\\\"")
    if not url:
        turn_to = 'history.back();'
    else:
        turn_to = 'location="{}"'.format(url)
    return '<script>alert("{}");{}</script>'.format(message, turn_to)


# safe get
def get(name, default=''):
    if len(request.form.getlist(name)) > 1:
        return request.form.getlist(name)
    elif request.form.get(name):
        return request.form.get(name)
    elif request.args.get(name):
        return request.args.get(name)
    return default


# read configuraiton
def get_conf(host, navigation_id, name, default=None):
    id = "{}_{}".format(navigation_id, name)
    ret = es.get(host, "core_nav", "config", id)
    return ret.get('value') if ret and ret.get('value') else default


# save configuration
def set_conf(host, navigation_id, name, value):
    id = "{}_{}".format(navigation_id, name)
    doc = {
        "navigation_id": navigation_id,
        "name": name,
        "value": value
    }
    es.update(host, "core_nav", "config", id, doc)
    es.flush(host, "core_nav")


# read file
def read_file(path, base_dir):
    filepath = os.path.join(base_dir, path)
    return open(filepath).read()
