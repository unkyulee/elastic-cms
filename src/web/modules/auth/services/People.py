import hashlib

from web import app
import lib.es as es
import web.util.tools as tools

# ldap authenticate
def authenticate(p, username, password):
    h = app.config.get("HOST")
    i = 'people'
    t = 'post'
    # get people
    people = es.get(h, i, t, username)
    if people:
        password = hashlib.sha512(password).hexdigest()
        # check password match
        if people['password'] == password:
            return True

    return False
