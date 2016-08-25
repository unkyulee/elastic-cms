from flask import render_template, request
import web.util.tools as tools

def get(p):
    if request.method == "POST":
        # save login html
        tools.set_conf(
            p['host'], p['navigation']['id'],
            'login_html', request.form['login_html'])
        # 
        return tools.redirect(request.referrer)

    # get login html
    p['login_html'] = tools.get_conf(
        p['host'], p['navigation']['id'], 'login_html', '')
    return render_template("auth/admin.html", p=p)
