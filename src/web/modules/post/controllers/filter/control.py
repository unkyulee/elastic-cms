from flask import render_template, request, jsonify
import web.util.tools as tools
import lib.http as http
import lib.es as es
import urllib2


def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # search keyword
    p["q"] = tools.get('q', '*')
    p["fq"] = tools.get('fq', '*')

    # load field
    field_id = p['nav'][-1]
    p['field'] = es.list(host, index, 'field', '_id:{}'.format(field_id))
    if not p['field']:
        return 'not valid field id - {}'.format(field_id)
    p['field'] = p['field'][0]

    # selected filters
    p['field_list'] = es.list(host, index, 'field')
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
    search_query = render_template("post/filter/filter_query.json", p=p)
    try:
        search_url = "{}/{}/post/_search".format(host, index)
        response = http.http_req_json(search_url, "POST", search_query)

    except urllib2.HTTPError, e:
        raise Exception("url: {}\nquery: {}\{}".format(
                search_url, search_query, e.read()))

    if tools.get("debug"):
        import json
        return u"{}\n{}".format(search_query,
                               json.dumps(response, indent=4))

    if tools.get("callback"):
        return u"{}({})".format(tools.get("callback"), jsonify(**response))

    return jsonify(**response)
