import os
import json
import textract
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, text

def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    SQL_CONNECTION = root.find("SQL_CONNECTION").text
    SQL = root.find("SQL").text
    TABLE = root.find("TABLE").text
    # Create sql engine
    engine = create_engine(SQL_CONNECTION)
    with engine.connect() as conn:
        # read database if there are any task waiting
        SQL_RESULT = None
        try:
            p["log"].info(SQL.strip())
            SQL_RESULT = conn.execute(text(SQL))
            p["log"].success("SQL execution completed")
        except Exception, e:
            AllGood = False
            p["log"].error(SQL, e)

        # Fetch the dataset
        p["log"].info("start extracting text ...")
        row_count = 0
        for r in SQL_RESULT:
            s = None
            try:
                s = os.stat(r.filepath)
                content = textract.process(r.filepath)
                InsertText(conn, TABLE, s.st_ino, s.st_dev, r.filepath, content)
                p["log"].success(
                        "Text extracted from {}\nText length: {}".format(
                                  r.filepath, len(content)))
                row_count += 1
            except Exception, e:
                if r: SetUpdated(conn, TABLE, r.filepath)
                p["log"].error("text extraction failed", e)

    # indexing completed
    p["log"].success("extraction completed: {}".format(row_count))

    return AllGood


def SetUpdated(conn, TABLE, filepath):
    SQL = """
    UPDATE {} SET is_updated = 0 WHERE filepath=:filepath
    """.format(TABLE)
    conn.execute(text(SQL), filepath=filepath)


def InsertText(conn, TABLE, ino, dev, filepath, content):
    SQL = """
    INSERT INTO {} (ino, dev, filepath, content, is_updated)
    VALUES (:ino, :dev, :filepath, :content, 0)
    ON DUPLICATE KEY UPDATE
        ino = :ino, dev = :dev,
        filepath = :filepath,
        content = :content,
        is_updated = 0
    """.format(TABLE)
    conn.execute(text(SQL), ino=ino, dev=dev, filepath=filepath, content=content)
