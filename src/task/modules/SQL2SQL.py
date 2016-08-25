import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, text

def run(p):
    AllGood = True

    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])

    SOURCE_SQL_CONNECTION = root.find("SOURCE_SQL_CONNECTION").text
    SOURCE_SQL = root.find("SOURCE_SQL").text

    TARGET_SQL_CONNECTION = root.find("TARGET_SQL_CONNECTION").text
    TARGET_SQL_TABLE = root.find("TARGET_SQL_TABLE").text

    MAP = {} # target_field:source_field
    for m in root.findall("MAP"):
        SOURCE_COLUMN_NAME = m.find("SOURCE_COLUMN_NAME").text
        TARGET_COLUMN_NAME = m.find("TARGET_COLUMN_NAME").text
        MAP[SOURCE_COLUMN_NAME] = TARGET_COLUMN_NAME

    # Connect to both sql engine
    source_engine = create_engine(SOURCE_SQL_CONNECTION)
    source_conn = source_engine.connect()

    target_engine = create_engine(TARGET_SQL_CONNECTION)
    target_conn = target_engine.connect()

    # Run Source SQL
    p["log"].info(SOURCE_SQL)

    SQL_RESULT = source_conn.execute(text(SOURCE_SQL))
    p["log"].success("SQL execution success.")

    # run insert for each
    row_count = 0
    for r in SQL_RESULT:
        doc = {}
        TARGET_FIELDS = []
        for column, value in r.items():
            target_field = column
            if MAP.get(column): target_field = MAP[column]
            TARGET_FIELDS.append(target_field)
            doc[target_field] = value

        # form INSERT SQL statement
        INSERT = "INSERT INTO {} ({}) VALUES ({})".format(
            TARGET_SQL_TABLE,
            ', '.join(TARGET_FIELDS),
            ', '.join([":{}".format(t) for t in TARGET_FIELDS]))

        target_conn.execute(text(INSERT), **doc)
        row_count += 1

    source_conn.close()
    target_conn.close()

    p["log"].success("Copy table completed: {} rows".format(row_count))

    return AllGood
