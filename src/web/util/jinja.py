# jinja custom filters
from flask import render_template
from web import app
from dateutil.parser import *
import json
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



@app.template_filter("escape")
def escape(value):
    if value:
        return json.dumps(value)
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
