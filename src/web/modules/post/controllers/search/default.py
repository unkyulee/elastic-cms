from flask import render_template, request
import web.util.tools as tools
import lib.http as http
import lib.es as es
import urllib2
from web import app
import json
from lib.read import readfile
import web.modules.post.services.workflow as workflow
import traceback

def get(p):
    if p['c']['intro'] and not tools.get('q'):
        return render_template(app.jinja_env.from_string(p['c']['intro']), p=p)

    host = p['c']['host']; index = p['c']['index'];
    # debug
    p['debug'] = tools.get('debug', '')
    # search keyword
    p["q"] = tools.get('q', p['c']['query'])
    # pagination
    p["from"] = int(tools.get('from', 0))
    p["size"] = int(tools.get('size', p['c']['page_size']))
    # sort
    p['sort_field'] = tools.get('sort_field', p['c']['sort_field'])
    p['sort_dir'] = tools.get('sort_dir', p['c']['sort_dir'])

    # fields
    p['fields'] = tools.get('fields')

    # init workflow
    wf = tools.get('wf', 'search')
    p['workflow'] = workflow.init(wf, host, index)

    ######################################################
    # check condition
    if p['workflow'] and p['workflow'].get('condition'):
        try:
            exec (p['workflow']['condition'], globals())
            ret = condition(p)
            if ret != True and ret: return ret
        except SystemExit: pass
        except Exception, e:
            return "{}\n{}".format(e.message, traceback.format_exc())

    ######################################################

    # selected filters
    field_list = es.list(host, index, 'field')
    # remove duplicates in filter lists
    p['field_list'] = []
    field_id_list = []
    for field in field_list:
        # add id to the field_id_list
        if field['id'] not in field_id_list:
            field_id_list.append(field['id'])
            p['field_list'].append(field)

    p['field_map'] = {}
    for field in p['field_list']:
        filter_field = field['id']
        if field.get('filter_field'):
            filter_field = field['filter_field']
        p['field_map'][field['id']] = filter_field

    p["selected_filter_list"] = {}
    for field in p['field_list']:
        value = tools.get(field['id'])
        if value:
            # filter will come in as ?created_by=lee _or_ cavalier
            values = value.split("_or_")
            p["selected_filter_list"][field['id']] = values

    # search query
    p["q"] = p["q"].replace('"', '\\"')
    if p['c'].get('search_query'):
        p['search_query'] = render_template(app.jinja_env.from_string(p['c']['search_query']), p=p)
    else:
        p['search_query'] = render_template("post/search/part/search_query.html", p=p)
    p["q"] = p["q"].replace('\\"', '"')

    try:
        search_url = "{}/{}/post/_search".format(host, index)
        p['response'] = http.http_req_json(search_url, "POST", p['search_query'])
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nquery: {}\{}".format(
                search_url, p['search_query'], e.read()))

    # debug mode - return search query
    if tools.get('debug'):
        return p['search_query']

    # extract post list
    p['post_list'] = []
    for r in p['response']["hits"]["hits"]:
        item = {}
        # first take items from the fields
        for k, v in r["_source"].items(): item[k] = v
        # fetch highlight
        item["highlight"] = {}
        if "highlight" in r and k != "url":
            for k, v in r["highlight"].items(): item["highlight"][k] = v

        item["id"] = r["_id"]
        item["_index"] = r["_index"]
        item["_type"] = r["_type"]

        # Save to SearchResult
        p['post_list'].append(item)

    # Feed Pagination
    p["total"] = int(p['response']["hits"]["total"])

    # Get available filter list
    p["available_filter_list"] = []
    # aggregations.[Name of the Filter].buckets.[key or doc_count]
    if p['response'].get("aggregations"):
        for field_id, values in p['response']["aggregations"].items():
            # Exclude empty buckets
            if len(values.get("buckets")) > 0:
                p["available_filter_list"].append(
                    [field for field in p['field_list'] if field['id'] == field_id][0]
                )

    # Suggestion
    p["suggestion"] = []; AnySuggestion = False;
    # suggest.didyoumean[].options[].text
    if p['response']["suggest"].get("didyoumean"):
        for idx, term in enumerate(p['response']["suggest"].get("didyoumean")):
            p["suggestion"].append(term["text"])
            for o in term["options"]:
                AnySuggestion = True
                p["suggestion"][idx] = o["text"]
                break # just take the first option
    # if there are no suggestions then don't display
    if not AnySuggestion: p["suggestion"] = []


    # Get Visible Fields of List
    p['field_list'] = es.list(host, index, 'field', 'visible:list',
                              'size=100&sort=order_key:asc')

    # return json format
    if tools.get("json"):
        callback = tools.get("callback")
        if not callback:
            return json.dumps(p['response'])
        else:
            return "{}({})".format(callback, json.dumps(p['response']))

    # render search result
    if p['c'].get('search_item_template'):
        return render_template(app.jinja_env.from_string(
            p['c'].get('search_item_template')), p=p)

    return render_template("post/search/default.html", p=p)
