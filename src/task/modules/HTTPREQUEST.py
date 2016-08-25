import urllib2
import xml.etree.ElementTree as ET
import lib.http as http

def run(p):
    AllGood = True
    # Parse connection string and split into URL,METHOD
    ConnectionString = p["action"]["connection"].split(",")
    # Read Query and parse parameters
    DATA = p["action"]["query"]
    URL = ConnectionString[0] if len(ConnectionString) > 0 else ""
    METHOD = ConnectionString[1] if len(ConnectionString) > 1 else "GET"
    p["log"].info("[{}] {}\n{}".format(METHOD, URL, DATA))

    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(URL, (DATA == None) if "" else DATA )
        request.get_method = lambda: METHOD
        url = opener.open(request)

        p["log"].success(url.read())

    except urllib2.HTTPError, e:
        AllGood = False
        p["log"].error("[request]\n{}\n[data]\n{}\n[response]\n{}".format(
            URL, DATA, e.read()), e)
        
    except Exception, e:
        AllGood = False
        p["log"].error("", e)

    return AllGood
