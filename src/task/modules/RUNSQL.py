from sqlalchemy import create_engine
from sqlalchemy.sql import text

def run(p):
    AllGood = True
    # Create sql engine
    engine = create_engine(p["action"]["connection"])
    # Get SQL connection
    with engine.connect() as conn:
        # read database if there are any task waiting
        QueryList = p["action"]['query'].split(";")
        for q in QueryList:
            if q == "" or q.isspace(): continue
            try:
                conn.execute(text(q))
                p["log"].success(q)
            except Exception, e:
                AllGood = False
                p["log"].error("", e)
        # close connection
        conn.close()
    return AllGood
