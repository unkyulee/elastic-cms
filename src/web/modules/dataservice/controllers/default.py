from flask import render_template
import lib.es as es
import web.util.tools as tools

def get(p):
    # get data source list
    query = 'navigation_id:{}'.format(p['navigation']['id'])
    option = 'size=10000'
    p['ds_list'] = es.list(p['host'], 'core_data', 'datasource', query, option)

    p['ds'] = {}
    if tools.get('id'):
        p['ds'] = es.get(p['host'], 'core_data', 'datasource', tools.get('id'))
    if not p['ds'] and len(p['ds_list']):
        p['ds'] = p['ds_list'][0]

    return render_template("dataservice/default.html",p=p)
