import os
import requests
import urlparse
from flask import request, Response
import lib.es as es

def is_reverse_proxy(host, url):
    option = "size=10000"
    proxy_list = es.list(host, 'core_proxy', 'rev_proxy', '*', option)

    # check if any rules match
    for proxy in proxy_list:
        if url.startswith(proxy['inc_url']):
            return proxy

    return False


def rev_proxy(host, url, rev_proxy_rule):
    # get raw url
    url = urlparse.unquote(url)

    # get remaining url
    pass_url = url.replace(rev_proxy_rule['inc_url'], '')

    # get destination url
    dest_url = "".join([rev_proxy_rule['out_url'], pass_url])

    # destination url should not match the inc_url rules
    if dest_url.startswith(rev_proxy_rule['inc_url']):
        return "infinite loop detected {} -> {}".format(url, dest_url)

    # replace /? -> ?
    dest_url = dest_url.replace("/?v", "?").strip("/")

    # remove cache header
    req_header = {}
    for h, v in request.headers:
        if "if" in h.lower(): continue
        if "cache" in h.lower(): continue
        req_header[h] = v

    # disable cache
    req_header["Cache-Control"] = "no-cache"
    req_header["Pragma"] = "no-cache"

    # Make Http Request
    resp = requests.request(method=request.method, url=dest_url,
                            #headers=req_header,
                            #data=request.get_data(),
                            #cookies=request.cookies,
                            #stream=True
                            )

    # Response
    headers = {}

    # remove content encoding header in response
    for h, v in resp.headers.items():
        if h.lower() == "content-encoding": continue
        if h.lower() == "transfer-encoding": continue
        if h.lower() == "content-length": continue
        headers[h] = v
    def generate():
        for chunk in resp.iter_content(1000):
            yield chunk

    return Response(generate(), status=resp.status_code, headers=headers)
