import json
import urllib2
import contextlib

# http request wrapper
def http_req_json(url, method="GET", data=None):
    # convert body to json format
    if data and type(data) is dict:
        data = json.dumps(data)
    # build up the request
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data.encode('utf-8') if data else None)
    request.get_method = lambda: method
    # send request
    with contextlib.closing(opener.open(request)) as url:
        response = url.read()

    return json.loads(response) if response else ""
