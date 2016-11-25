from flask import render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    host = p['c']['host']; index = p['c']['index'];

    # load history
    history_id = p['nav'][-1]
    p['history'] = es.get(host, index, 'log', history_id)
    if not p['history']:
        return tools.alert('not valid id - {}'.format(history_id))

    return render_template("post/history/view.html", p=p)
