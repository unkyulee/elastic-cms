from flask import request, render_template
import lib.es as es

def get(p):
    host = p['c']['host']; index = p['c']['index'];
    # get list of workflow
    query = "*" ; option = "size=10000&sort=name:asc";
    p['workflow_list'] = es.list(host, index, 'workflow', query, option)

    return render_template("mercurial/workflow/default.html", p=p)
