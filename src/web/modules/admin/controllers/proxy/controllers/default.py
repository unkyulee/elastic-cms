from flask import render_template
import lib.es as es

def get(p):
    # proxy list
    option = 'size=10000'
    p['proxy_list'] = es.list(p['host'], 'core_proxy', 'rev_proxy', '*', option)

    return render_template("admin/proxy/default.html", p=p)
