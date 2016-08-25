import importlib
from flask import render_template
import lib.es as es

def get(p):
    # get data source definiton
    query = 'name:{}'.format(p['nav'][3])
    p['ds'] = es.list(p['host'], 'core_data', 'datasource', query)[0]

    # load service
    path = "web.modules.dataservice.services.{}".format(p['ds']['type'])    
    mod = importlib.import_module(path)

    return mod.execute(p)
