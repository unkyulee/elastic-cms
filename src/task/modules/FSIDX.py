import os
import pwd
import time
from datetime import datetime
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.sql import text

def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]["query"])
    SQL_CONNECTION = root.find("SQL_CONNECTION").text.strip()
    TABLE = root.find("TABLE").text.strip()
    PATHs = [] # table_field:ldap_field
    for path in root.findall("PATH"):
        PATHs.append({"dir":path.find("dir").text.strip(),
                     "idx":path.find("idx").text.strip()})
    # prepare sql engine
    engine = create_engine(SQL_CONNECTION)
    # Loop Through the dir
    for path in PATHs:
        DeleteFiles(TABLE, engine, p["log"], path["idx"])
        AddFiles(TABLE, engine, p["log"], path["idx"], path["dir"])

    p["log"].success("All file indexing finished")
    return AllGood


def DeleteFiles(TABLE, engine, log, idx):
    SQL = """
    SELECT ino, filepath from {} WHERE idx=:idx
    """.format(TABLE)

    DELSQL = """
    DELETE FROM {} WHERE ino=:ino
    """.format(TABLE)

    log.info("scanning for removed files ... {}".format(idx))
    RemovedFile = 0
    with engine.connect() as conn:
        result = conn.execute(text(SQL), idx=idx)
        for r in result:
            try:
                if os.path.isfile(r.filepath):
                    # if file exists then check if it has same id
                    # same name file but could be different file
                    s = os.stat(r.filepath)
                    if s.st_ino != r.ino:
                        # log.info("File removed .. {} - {}\n{}".format(s.st_ino, r.id, r.filepath))
                        conn.execute(text(DELSQL), ino=r.ino)
                        RemovedFile += 1
                else:
                    # if file doesn't exist then also delete
                    # log.info("File removed .. {}\n{}".format(r.id, r.filepath))
                    conn.execute(text(DELSQL), ino=r.ino)
                    RemovedFile += 1

            except Exception, e:
                # log.info("File removed .. {}\n{}".format(r.id, r.filepath))
                conn.execute(text(DELSQL), ino=r.ino)
                RemovedFile += 1

    log.success("{} files removed ... {}".format(RemovedFile, idx))



def AddFiles(TABLE, engine, log, idx, path):
    log.info("Searching .. {}\n{}".format(idx, path))
    # get last update date
    LastUpdated = GetLastUpdate(TABLE, engine, idx)
    # loop recursively through the path
    row_count = 0
    for dirName, subDirName, fileList in os.walk(path):
        for name in fileList:
            try:
                s = os.stat("{}/{}".format(dirName, name))
                # skip those are not changed
                if datetime.fromtimestamp(int(s.st_mtime)) <= LastUpdated:
                    continue
                #
                fileinfo = {
                    "ino": s.st_ino, "dev": s.st_dev, "idx": idx,
                    "filepath": "{}/{}".format(dirName, name),
                    "dir": dirName, "name": name,
                    "ext": os.path.splitext(name)[1],
                    "owner": pwd.getpwuid(s.st_uid).pw_name,
                    "created": time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(s.st_ctime)),
                    "updated": time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(s.st_mtime))
                }
                #
                InsertFileIndex(TABLE, engine, fileinfo)
                row_count += 1
            except Exception, e:
                log.error("{}/{}".format(dirName, name), e)

    log.success("Indexed {} updated files".format(row_count))



# Get last updated timestamp
def GetLastUpdate(TABLE, engine, idx):
    SQL = """
    SELECT updated FROM {} WHERE idx='{}' ORDER BY updated DESC LIMIT 1
    """.format(TABLE, idx)

    LastUpdated = datetime(1970,1,1)
    with engine.connect() as conn:
        sql_result = conn.execute(text(SQL))
        for r in sql_result:
            LastUpdated = r.updated

    return LastUpdated


# Insert if the file doesn't exist
def InsertFileIndex(TABLE, engine, f):
    SQL = """
    INSERT INTO {}
        (ino, dev, idx, filepath, dir, name, ext, owner, created, updated)
    VALUES
        (:ino, :dev, :idx, :filepath, :dir,
         :name, :ext, :owner, :created, :updated)
    ON DUPLICATE KEY UPDATE
        filepath = :filepath, dir = :dir, name = :name,
        ext = :ext, owner = :owner, is_updated = 1,
        created = :created, updated = :updated
    """.format(TABLE)

    with engine.connect() as conn:
        conn.execute(text(SQL), ino=f["ino"],  dev=f["dev"], idx = f["idx"],
                     filepath=f["filepath"], dir=f["dir"], name=f["name"],
                     ext=f["ext"], owner=f["owner"], created=f["created"],
                     updated=f["updated"])
