import time
import urllib2
from datetime import datetime
from dateutil.tz import *
from lib.http import *


def update(host, index, type_, id, doc):
    # document
    document = {"doc":doc, "doc_as_upsert": True}
    try:
        url = "{}/{}/{}/{}/_update".format(host, index, type_, id)
        http_req_json(url, "POST", document)
        return True
    except urllib2.HTTPError, e:
        raise Exception("url: {}\ndoc: {}\n{}".format(url, doc, e.read()))


def delete_query(host, index, type_, query):
    try:
        search_url = "{}/{}/{}/_query".format(host, index, type_)
        return http_req_json(search_url, "DELETE", query)
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nquery: {}\n{}".format(
            search_url, query, e.read()))


def delete(host, index, type_, id):
    try:
        search_url = "{}/{}/{}/{}".format(host, index, type_, id)
        return http_req_json(search_url, "DELETE")
    except urllib2.HTTPError, e:
        raise Exception("url: {}\n{}".format(
            search_url, e.read()))


def count(host, index, type_, query="*"):
    try:
        query = query_builder(query)
        search_url = "{}/{}/{}/_count".format(host, index, type_)
        response = http_req_json(search_url, "POST", query)
        return response['count']
    except urllib2.HTTPError, e:
        raise Exception("url: {}\n{}".format(search_url, e.read()))


# get record by field
def list(host, index, type_, query="*", option="size=10000", debug=False):
    try:
        query = query_builder(query)
        search_url = "{}/{}/{}/_search?{}".format(host, index, type_, option)
        response = http_req_json(search_url,"POST", query)

        if debug:
            print query
            print search_url
            print response

        docs = []
        for doc in response['hits']['hits']:
            doc['_source']['id'] = doc['_id']
            doc['_source']['index'] = doc['_index']
            docs.append(doc['_source'])
        return docs
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nquery: {}\noption: {}\n{}".format(
            search_url, query, option, e.read()))


def query_builder(query):
    query_json = {
        "query":{
            "query_string":{
                "query": u"{}".format(query)
            }
        }
    }

    return query_json


# get record
def get(host, index, type_, id, default=None):
    try:
        search_url = "{}/{}/{}/{}".format(host, index, type_, id)
        doc = http_req_json(search_url)
        doc['_source']['id'] = doc['_id']
        return doc['_source']
    except urllib2.HTTPError, e:
        return default


# create record
# returns json object when success
def create(host, index, type_, id='', doc=None, debug=False):
    if id is None: id = ''
    try:
        search_url = "{}/{}/{}/{}".format(host, index, type_, id)
        if debug:
            print search_url
        return http_req_json(search_url, "POST", doc)
    except urllib2.HTTPError, e:
        raise Exception("url: {}\id: {}\doc: {}\n{}".format(
            search_url, id, doc, e.read()))


# index list
def index_list(host):
    try:
        response = http_req_json("{}/_cat/indices".format(host))
        return response
    except urllib2.HTTPError, e:
        return e.read()


# download backup
def backup(host, index, dump=True):
    docs = []

    try:
        url = '{}/{}/_search?scroll=1m'.format(host, index)
        response = http_req_json(url)
        scroll_id = response["_scroll_id"]

        # break if the return doesn't have any documents
        if len(response["hits"]["hits"]) == 0: return []
        for d in response["hits"]["hits"]: docs.append(d)

        # Export document until there are no items left
        loop_limit = 100000
        for i in range(loop_limit):
            url = '{}/_search/scroll?scroll=1m&scroll_id={}'.format(host, scroll_id)
            response = http_req_json(url, "GET")

            # break if the return doesn't have any documents
            if len(response["hits"]["hits"]) == 0: break
            for d in response["hits"]["hits"]: docs.append(d)
        if dump:
            return json.dumps(docs, indent=4, ensure_ascii=False, encoding='utf8')
        else:
            return docs

    except urllib2.HTTPError, e:
        raise Exception("url: {}\n{}".format(url, e.read()))


# def restore
def restore(host, index, docs):
    # restore
    record_cnt = 0
    for d in docs:
        document = {u"doc":d["_source"], u"doc_as_upsert": True}
        record_cnt += 1
        try:
            url = "{}/{}/{}/{}/_update".format(host, index, d["_type"], d["_id"])
            response = http_req_json(url, "POST", document)
        except urllib2.HTTPError, e:
            raise Exception("url: {}\n{}".format(url, e.read()))

    return record_cnt


# bulk operation
def bulk(host, bulk_data):
    try:
        url = "{}/_bulk".format(host)
        http_req_json(url, "POST", bulk_data)
        return True
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nbulk: {}\n{}".format(
            url, bulk_data, e.read()))


# create mapping
def create_mapping(host, index, type, mapping):
    try:
        properties = {"properties": mapping}
        url = "{}/{}/_mapping/{}".format(host, index, type)
        return http_req_json(url, "PUT", properties)
    except urllib2.HTTPError, e:
        raise Exception("url: {}\nproperties: {}\n{}".format(
            url, properties, e.read() ))


# mapping
def mapping(host, index, type):
    try:
        url = "{}/{}/{}/_mapping".format(host, index, type)
        return http_req_json(url, "GET")
    except urllib2.HTTPError, e:
        raise Exception("url: {}\n{}".format( url, e.read() ))


# create index
def create_index(host, index, schema):
    try:
        url = "{}/{}".format(host, index)
        return http_req_json(url, "PUT", schema)
    except urllib2.HTTPError, e:
        return (
            "url: {}\nschema: {}\n{}".format(url, schema, e.read())
        )


# check if the index exists
def index_exists(host, index):
    try:
        http_req_json("{}/{}".format(host, index), "HEAD")
        return True
    except urllib2.HTTPError, e:
        return False


# any transaction queue shall be flushed
def flush(host, index):
    try:
        return http_req_json("{}/{}/_flush/synced".format(host, index), "POST")
    except urllib2.HTTPError, e:
        return e.read()


# produces eligible date formate for elasticsearch
def now():
    return datetime.now(tzlocal()).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
