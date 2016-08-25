import json
import xml.etree.ElementTree as ET
# Import SQL Alchemy
from sqlalchemy import create_engine, text
import lib.es as es

def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    SOURCE_SQL_CONNECTION = root.find("SOURCE_SQL_CONNECTION").text.strip()
    SOURCE_SQL = root.find("SOURCE_SQL").text.strip()
    ELASTIC_SEARCH_HOST = root.find("ELASTIC_SEARCH_HOST").text
    INDEX = root.find("INDEX").text
    DOC_TYPE = root.find("DOC_TYPE").text
    # Data Body
    SQL_RESULT = None
    # Create sql engine
    engine = create_engine(SOURCE_SQL_CONNECTION)
    # Get SQL connection
    with engine.connect() as conn:
        try:
            p["log"].info(SOURCE_SQL)
            SQL_RESULT = conn.execute(text(SOURCE_SQL))
            p["log"].success("SQL execution success.")
        except Exception, e:
            AllGood = False
            p["log"].error("SQL execution failed.", e)


        # Fetch the dataset
        p["log"].info("start indexing ...")
        row_count = 0
        for r in SQL_RESULT:
            body = {}; id = None; updated = None;
            for column, value in r.items():
                if column == "id": id = value; continue;
                if column == "updated": updated = value;
                body[column] = value
            # Check if the document has id
            if not id:
                AllGood = False
                p["log"].log("ERROR", "id doesn't exist\nid: {}\n{}".format(id, str(body)))
                break
            # Check if the document has updated field
            if not updated or updated[0] == "0":
                AllGood = False
                p["log"].log("ERROR", "update field should not be NULL or 0")
                break
            # Create Index
            try:
                es.create(ELASTIC_SEARCH_HOST, INDEX, DOC_TYPE, id, body)
            except Exception,e:
                AllGood = False
                p["log"].error("id: {}\n{}".format(id, str(body)), e)

            # total indexed document count
            row_count += 1
        # indexing completed
        p["log"].success("Indexing completed: {}".format(row_count))

    return AllGood
