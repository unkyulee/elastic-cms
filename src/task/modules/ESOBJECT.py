import json
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine, text

# Run Module
def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    SQL_CONNECTION = root.find("SQL_CONNECTION").text
    SQL = root.find("SQL").text
    ELASTIC_SEARCH_HOST = root.find("ELASTIC_SEARCH_HOST").text
    INDEX = root.find("INDEX").text
    DOC_TYPE = root.find("DOC_TYPE").text
    TEMPLATE = root.find("TEMPLATE").text
    FIELD = root.find("FIELD").text
    # Data Body
    SQL_RESULT = None
    # Create sql engine
    engine = create_engine(SQL_CONNECTION)
    # Get SQL connection
    with engine.connect() as conn:
        try:
            p["log"].info(SQL)
            SQL_RESULT = conn.execute(text(SQL))
            p["log"].success("SQL execution success.")
            # connect to Elastic Search
            es = Elasticsearch([ELASTIC_SEARCH_HOST])
        except Exception, e:
            AllGood = False
            p["log"].error("SQL execution failed.", e)

        p["log"].info("start adding objects ...")
        row_count = 0; curr_id = None; prev_id = None;
        body = {"doc":{}} ; es_object = TEMPLATE ;
        for r in SQL_RESULT:
            # check if id exists
            if not "id" in r:
                AllGood = False
                p["log"].log("ERROR", "id doesn't exist\nid: {}\n{}".format(id, str(body)))
                break
            # save id
            curr_id = r["id"]
            # try to detect when id is changed - means new document
            if curr_id != prev_id and prev_id:
                try:
                    es.update(index=INDEX, doc_type=DOC_TYPE, id=prev_id,
                              body=json.dumps(body, ensure_ascii=False,
                                              encoding='utf8'))
                    row_count += 1
                except Exception,e:
                    AllGood = False
                    p["log"].error("id: {}\n{}".format(curr_id, str(body)), e)
                    break
                finally:
                    # reset body content for the next document
                    body = {"doc":{}}
            # Loop each column to complete an object
            es_object = TEMPLATE
            for column, value in r.items():
                # save id field and continue
                if column == "id": continue;
                # form template content
                es_object = es_object.replace("[[{}]]".format(column),
                                              str(value))
            # create column if doesn't exist
            if not body["doc"].get(FIELD): body["doc"][FIELD] = []
            # add object to the body
            body["doc"][FIELD].append(json.loads(es_object))
            # Save the current id
            prev_id = curr_id

        # index the last record
        if prev_id:
            es.update(index=INDEX, doc_type=DOC_TYPE, id=prev_id,
                        body=json.dumps(body, ensure_ascii=False, encoding='utf8'))
            row_count += 1

        # indexing completed
        p["log"].success("Adding objects completed: {}".format(row_count))
    return AllGood
