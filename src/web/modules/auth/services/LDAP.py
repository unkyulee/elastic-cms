"""
LDAP Login

Configuration comes in as json formatted string

{
    "ldap_uri": "ldaps://ldap",
    "ldap_path": "uid={}, ou=People, dc=compass"
}
"""
import ldap
import json
import web.util.tools as tools

# ldap authenticate
def authenticate(config, username, password):
    # parse config
    if not config:
        return False

    config = json.loads(config)

    ldap_uri = config.get('ldap_uri')
    ldap_path = config.get('ldap_path')
    user_id = ldap_path.format(username)

    try:
        # Turn off certificate checking!
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        con = ldap.initialize(ldap_uri)
        con.bind(user_id, password)
        con.result()
        con.unbind()

        return True
    except:
        pass

    return False
