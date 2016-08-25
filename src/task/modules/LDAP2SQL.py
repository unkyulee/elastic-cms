import ldap
import itertools
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
from sqlalchemy.sql import text

def run(p):
    AllGood = True
    # Read Query and parse parameters
    root = ET.fromstring(p["action"]['query'])
    SQL_CONNECTION = root.find("SQL_CONNECTION").text
    LDAP = root.find("LDAP").text
    BASE_DN = root.find("BASE_DN").text
    FILTER = root.find("FILTER").text
    TABLE = root.find("TABLE").text
    MAP = {} # table_field:ldap_field
    for m in root.findall("MAP"):
        ldap_field = m.find("ldap_field").text
        table_field = m.find("table_field").text
        MAP[table_field] = ldap_field
    ## first you must open a connection to LDAP server
    try:
    	l = ldap.initialize(LDAP)
    	## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
    	## and do a bind as shown in the above example.
    	# you can also set this to ldap.VERSION2 if you're using a v2 directory
    	# you should  set the next option to ldap.VERSION2 if you're using a v2 directory
    	l.protocol_version = ldap.VERSION3
    except ldap.LDAPError, e:
    	# handle error
        p["log"].error("Failed to connect {}".format(LDAP), e)
    # Extract data from LDAP
    ldap_result = []
    try:
        p["log"].info("Extracting from LDAP ...\n{}".format(LDAP))
        ldap_result_id = l.search(BASE_DN, ldap.SCOPE_SUBTREE, FILTER, None)
        # extract data
        while 1:
        	result_type, result_data = l.result(ldap_result_id, 0)
        	if (result_data == []):
        		break # last data
        	else:
        		if result_type == ldap.RES_SEARCH_ENTRY:
        			ldap_result.append(result_data)
    except Exception, e:
        # handle error
        p["log"].error("{}\n{}".format(BASE_DN, FILTER), e)

    # Load to SQL
    p["log"].info("Loading to SQL ...\n{}\n{}".format(TABLE, SQL_CONNECTION))
    engine = create_engine(SQL_CONNECTION)
    record_count = 0
    with engine.connect() as conn:
        for ldap_data in ldap_result:
            SQL = ""
            try:
                SQL = InsertLDAP2SQL(ldap_data, TABLE, MAP)
                conn.execute(SQL)
                record_count += 1
            except Exception, e:
                AllGood = False
                p["log"].error(SQL, e)
                break

    p["log"].success("{} records from LDAP to SQL Success!".format(record_count))

    return AllGood


def InsertLDAP2SQL(ldap_data, TABLE, MAP):
    # INSERT TEMPLATE
    SQL = "INSERT INTO {} ({}) VALUES (".format(TABLE, ', '.join(MAP.keys()))
    for m, has_more in lookahead(MAP.keys()):
        value = ""
        try: value = ldap_data[0][1][MAP[m]][0]
        except: pass
        SQL += "\"{}\"".format(value.replace("\"","\\\""))
        if has_more: SQL += ", "
    SQL += ");"

    return SQL


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False
