import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, text
import lib.es as es

# Run Module
def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    SQL_CONNECTION = root.find("SQL_CONNECTION").text
    SQL = root.find("SQL").text.strip()
    ELASTIC_SEARCH_HOST = root.find("ELASTIC_SEARCH_HOST").text
    INDEX = root.find("INDEX").text
    DOC_TYPE = root.find("DOC_TYPE").text
    # Data Body
    SQL_RESULT = None
    # Create sql engine
    engine = create_engine(SQL_CONNECTION)
    # Get SQL connection
    with engine.connect() as conn:
        try:
            p["log"].info(SQL)
            SQL_RESULT = conn.execute(text(SQL))
            p["log"].success("SQL excuted successfully.")
        except Exception, e:
            AllGood = False
            p["log"].error("SQL execution failed",e)


        p["log"].info("start updating document ...")
        row_count = 0; curr_id = None; prev_id = None; body = {} ;
        for r in SQL_RESULT: # check if id exists
            if not "id" in r:
                AllGood = False
                p["log"].log("ERROR", "id doesn't exist\nid: {}\n{}".format(id, str(body)))
                break

            # save current id
            curr_id = r["id"]

            # try to detect when id is changed - means new document
            if curr_id != prev_id and prev_id:
                try:
                    es.update(ELASTIC_SEARCH_HOST, INDEX, DOC_TYPE, prev_id, body)
                    row_count += 1
                except Exception,e:
                    p["log"].error("id: {}\n{}".format(curr_id, str(body)), e)
                    return False

                finally:
                    # reset body content for the next document
                    body = {}

            # Loop each column
            for column, value in r.items():
                # save id field and continue
                if column == "id": continue;
                # create column if doesn't exist
                if not body.get(column): body[column] = []
                # form body content
                body[column].append(value)

            # Save the current id
            prev_id = curr_id

        # index the last record
        if prev_id:
            es.update(ELASTIC_SEARCH_HOST, INDEX, DOC_TYPE, prev_id, body)
            row_count += 1

        # indexing completed
        p["log"].success("Update index completed: {}".format(row_count))

    return AllGood
