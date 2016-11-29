from flask import render_template, request
import json
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # keep pagination
    p["q"] = tools.get('q', '*')
    # pagination
    p["from"] = int(tools.get('from', 0))
    p["size"] = int(tools.get('size', p['c']['page_size']))
    # sort
    p['sort_field'] = tools.get('sort_field', p['c']['sort_field'])
    p['sort_dir'] = tools.get('sort_field', p['c']['sort_dir'])

    # load post
    post_id = p['nav'][-1]
    p['post'] = es.get(host, index, 'post', post_id)
    if not p['post']:
        return tools.alert('not valid post id - {}'.format(post_id))

    # check ACL
    valid_acl = False
    if p['login'] == p['post'].get('created_by'): valid_acl = True
    if p['post'].get('acl_readonly') and p['login'] in p['post'].get('acl_readonly'): valid_acl = True
    if p['post'].get('acl_edit') and p['login'] in p['post'].get('acl_edit'): valid_acl = True
    if not valid_acl:
        return tools.alert('permission not granted')

    # return json format
    if tools.get("json"):
        callback = tools.get("callback")
        if not callback:
            return json.dumps(p['post'])
        else:
            return "{}({})".format(callback, json.dumps(p['post']))

    # get comment list
    query = "post_id:{}".format(post_id)
    option = "size=100&sort=created:desc"
    p['comment_list'] = es.list(host, index, 'comment', query, option)

    # increase visit count
    if not p['post'].get("viewed"): p['post']["viewed"] = 0
    p['post']["viewed"] += 1
    es.update(host, index, 'post', post_id, p['post'])

    # field_list
    p['field_list'] = es.list(host, index, 'field', "visible:view", "size=1000&sort=order_key:asc")

    return render_template("post/post/view.html", p=p)
