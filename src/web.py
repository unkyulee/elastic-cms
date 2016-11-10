# -*- coding: utf-8 -*-
""" Run web application instance

Creates web instances for WSGI

Example:
    Creating a standalone instance 

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# Explicitly set current directory to be compatible when instantiated for WSGI
import os
import sys
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

# Import flask app from Web/__init__.py
from web import app as application
application.config['BASE_DIR'] = BASE_DIR

if __name__ == "__main__":
    # Run Web Server
    application.run(host='0.0.0.0', port=8081, debug=True, threaded=True)
