from flask import render_template
import lib.es as es

def get(p):
    # proxy list
    option = 'size=10000'
    p['public_list'] = es.list(p['host'], 'core_proxy', 'public', '*', option)

    return render_template("admin/public/default.html", p=p)
