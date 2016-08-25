import ldap
import web.util.tools as tools

# ldap authenticate
def authenticate(p, username, password):
    ldap_uri = tools.get_conf(p['host'], '-1', 'ldap', '')
    ldap_path = tools.get_conf(p['host'], '-1', 'ldap_path', '')
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
