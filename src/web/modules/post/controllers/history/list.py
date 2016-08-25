from flask import render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load history list
    item_id = p['nav'][-1]
    query =  "id:{}".format(item_id)
    option = "size=100&sort=created:desc"
    p['history_list'] = es.list(host, 'core_history', 'log', query, option)
    if not p['history_list']:
        return tools.alert('not valid id - {}'.format(item_id))

    return render_template("post/history/list.html", p=p)
