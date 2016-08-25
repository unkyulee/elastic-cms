# Run Flask App

# Explicitly set current directory to be compatible when instantiated for WSGI
import os, sys
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

# Import flask app from Web/__init__.py
from web import app as application
application.config['BASE_DIR'] = BASE_DIR

if __name__ == "__main__":
    # Run Web Server
    application.run(host='0.0.0.0',port=8081, debug=True)
