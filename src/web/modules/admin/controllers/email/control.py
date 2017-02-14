"""
Email Configuration
"""
from flask import render_template, request
from web.modules.admin.services.notification import *
import web.util.tools as tools

def get(p):
    # Save Email Configuration
    if request.method == "POST":
        set_conf(p['host'], {
            'gmail_id': tools.get('gmail_id'),
            'gmail_pw': tools.get('gmail_pw')
        })
        return tools.redirect(request.referrer)

    # Display Email Configuration
    p['conf'] = get_conf(p['host'])
    return render_template("admin/email/default.html", p=p)
