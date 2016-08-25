from flask import Response
import lib.es as es

def get(p):
    backup = es.backup(p['c']['host'], p['c']['index'])
    return Response(backup, mimetype='application/json',
        headers={'Content-Disposition':'attachment;filename={}.json'.format(p['c']['index'])})
