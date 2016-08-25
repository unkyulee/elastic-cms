
# Statement for enabling the development environment
DEBUG = True

# Elasticsearch host
HOST = "http://localhost:9200"

# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "some random string for encryption"

# Secret key for signing cookies
SECRET_KEY = "some random string for encryption"

# Session configuration
SESSION_TYPE = 'redis'
    