# jinja custom filters
import json
from datetime import datetime
from dateutil.parser import *

from flask import render_template
from web import app
import lib.es as es


@app.template_filter("get")
def get(id, host, index, type_):
    ret = ''
    try:
        ret = es.get(host, index, type_, id)
    except Exception, e:
        ret = str(e)
    return ret


@app.template_filter("es_list")
def es_list(host, index, type_, query, option):
    return es.list(host, index, type_, query, option)


@app.template_filter("split")
def split(value, token):
    return value.split(token)


@app.template_filter("replace")
def replace(value, orig, new):
    return value.replace(orig, new)


@app.template_filter("filename")
def filename(value, id):
    return value[value.find('{}_'.format(id))+len(id)+1:]


@app.template_filter("strip")
def strip(value):
    return value.strip()


@app.template_filter("prettyjson")
def prettyjson(value):
    if type(value) is unicode:
        value = json.loads(value)
    return json.dumps(value, indent=4, sort_keys=True)


@app.template_filter("json_to_dict")
def json_to_dict(value):
    if value:
        return json.loads(value)
    return {}


@app.template_filter("render")
def render(value, p, item = None):
    return render_template(
        app.jinja_env.from_string(value),
        p=p, item=item)


@app.template_filter("first")
def first(value):
    if type(value) is list and len(value) > 0:
        return value[0]
    elif value:
        return value
    else:
        return ''


@app.template_filter("getlist")
def getlist(value):
    if type(value) is list:
        return value
    elif value:
        return [value]
    else:
        return []

@app.template_filter("formgetlist")
def formgetlist(value, name):
    return value.getlist(name)


@app.template_filter("is_list")
def is_list(value):
    return isinstance(value, list)


@app.template_filter("dt")
def dt(date, fmt=None):
    if not date: return ""

    date = parse(date)
    if fmt: return date.strftime(fmt)

    return date.strftime("%d %b %Y - %H:%M")

@app.template_filter("pretty_date")
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    time = parse(time, ignoretz=True)
    now = datetime.now()
    
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"
