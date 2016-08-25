import os, sys
from flask import render_template

# check if config.py exists
def exists(BASE_DIR):
    if os.path.isfile("{}/config.py".format(BASE_DIR)):
        return True
    return False


# create config file
def create(BASE_DIR, HOST, DEBUG, KEYSTRING):
    config_template = """
# Statement for enabling the development environment
DEBUG = {0}

# Elasticsearch host
HOST = "{1}"

# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "{2}"

# Secret key for signing cookies
SECRET_KEY = "{2}"

# Session configuration
SESSION_TYPE = 'redis'
    """.format(DEBUG[0], HOST[0], KEYSTRING[0])

    config_path = '{}/config.py'.format(BASE_DIR)
    with open(config_path, 'w') as f:
        f.write(config_template)
