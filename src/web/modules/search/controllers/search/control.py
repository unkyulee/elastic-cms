import json
import urllib2
import traceback
import cgi

from flask import render_template, request
import web.util.tools as tools
import lib.http as http
import lib.es as es
from web import app
from lib.read import readfile


def get(p):
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
    # selected app
    p['selected_app'] = tools.get('app')

    # search query
    p["q"] = p["q"].replace('"', '\\"') # escape some special chars
    p['search_query'] = render_template("search/search_query.html", p=p)
    p["q"] = tools.get('q', p['c']['query']) # restore to what was entered originally

    # send search request
    try:
        search_url = "{}/{}/post/_search".format(host, index)
        p['response'] = http.http_req_json(search_url, "POST", p['search_query'])
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nquery: {}\{}".format(
                search_url, p['search_query'], e.read()))

    # process the search result
    p['post_list'] = []
    for r in p['response']["hits"]["hits"]:
        item = {}
        # first take items from the fields
        for k, v in r["_source"].items():
            item[k] = v

        # fetch highlight
        if r.get('highlight'):
            for k, v in r["highlight"].items():
                if k == "url" or k == "_index" or k == "app":
                    continue
                value = cgi.escape(v[0])
                value = value.replace("::highlight::", "<font color=red>")
                value = value.replace("::highlight_end::", "</font>")
                item[k] = value

                print k, value[0:20]


        # produce standard fields
        if r.get('_index') and not item.get('app'):
            item['app'] = r.get('_index')
        if not item.get('url'):
            item['url'] = '{}/redirect?index={}&id={}'.format(
                p.get('url'),
                r.get('_index'),
                r.get('_id'))

        # Save to SearchResult
        p['post_list'].append(item)

    # Application Lists
    p['applications'] = []
    if p['response'].get('aggregations'):
        internal = p['response']['aggregations']['internal']['buckets']
        p['applications'].extend(
            [item for item in internal if item.get('key') != 'search']
        )

        external = p['response']['aggregations']['external']['buckets']
        p['applications'].extend(external)

        # sort based on the count
        p['applications'] = sorted(p['applications'],
            key=lambda x: x['doc_count'], reverse=True)

    # Feed Pagination
    p["total"] = int(p['response']["hits"]["total"])

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

    # return json format
    if tools.get("json"):
        callback = tools.get("callback")
        if not callback:
            return json.dumps(p['response'])
        else:
            return "{}({})".format(callback, json.dumps(p['response']))

    return render_template("search/default.html", p=p)
