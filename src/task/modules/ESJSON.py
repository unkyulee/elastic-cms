import json
import urllib2
from dateutil.parser import parse
import xml.etree.ElementTree as ET
# Import SQL Alchemy
from sqlalchemy import create_engine, text
import lib.es as es
import lib.http as http

def run(p):
    AllGood = True

    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    ELASTIC_SEARCH_HOST = root.find("ELASTIC_SEARCH_HOST").text
    INDEX = root.find("INDEX").text
    DOC_TYPE = root.find("DOC_TYPE").text
    JSON_URL = root.find("JSON_URL").text.strip()
    LOOP_PATH = root.find("LOOP_PATH").text
    MAP = {} # table_field:ldap_field
    for m in root.findall("MAP"):
        PATH = None; CONST = None; STRINGFORMAT = None; DATEFORMAT = None;
        if m.find("CONST") is not None: CONST = m.find("CONST").text
        if m.find("PATH") is not None: PATH = m.find("PATH").text
        if m.find("STRINGFORMAT") is not None: STRINGFORMAT = m.find("STRINGFORMAT").text
        if m.find("DATEFORMAT") is not None: DATEFORMAT = m.find("DATEFORMAT").text
        ES_FIELD = m.find("ES_FIELD").text
        MAP[ES_FIELD] = {
            "PATH":PATH,
            "CONST":CONST,
            "STRINGFORMAT":STRINGFORMAT,
            "DATEFORMAT":DATEFORMAT
        }


    # Read json from source url
    p["log"].info(JSON_URL)
    try:
        response = http.http_req_json(JSON_URL)
    except urllib2.HTTPError, e:
        AllGood = False
        p["log"].error(e.read(), e)
    except Exception, e:
        AllGood = False
        p["log"].error("", e)


    # convert to json format
    json_data = response
    # go to iterate point
    json_data = JsonPath(LOOP_PATH.split("."), json_data)
    # loop in to data
    row_count = 0
    for d in json_data:
        doc = {}
        # mapping
        for field, map in MAP.items():
            value = None
            # value from json path
            if map["PATH"]: value = JsonPath(map["PATH"].split("."), d)
            # is it const value?
            if map["CONST"]: value = map["CONST"]
            # does it have string format?
            if map["STRINGFORMAT"] and value: value = str(map["STRINGFORMAT"]).format(value) if value else None
            if map["DATEFORMAT"] and value: value = parse(value).strftime(map["DATEFORMAT"])
            # value should be ready now
            doc[field] = value

        # Create Index
        try:
            es.create(ELASTIC_SEARCH_HOST, INDEX, DOC_TYPE, doc["id"], doc)
        except Exception,e:
            AllGood = False
            p["log"].error("id: {}\n{}".format(doc["id"], str(doc)), e)

        # total indexed document count
        row_count += 1

    # indexing completed
    p["log"].success("Indexing completed: {}".format(row_count))

    return AllGood


def JsonPath(path, data):
    pathed = data
    try:
        for p in path: pathed = pathed[p]
    except Exception, e:
        pathed = None
    return pathed
