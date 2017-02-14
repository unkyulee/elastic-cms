import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools

import web.modules.install.modules.people.install as people
import web.modules.install.modules.schedule.install as schedule
import web.modules.install.modules.document.install as document
import web.modules.install.modules.dashboard.install as dashboard
import web.modules.install.modules.search.install as search

def install(host, form, base_dir):

    # check if core_nav already exists
    if not es.index_exists(host, "core_nav"):
        # create core_nav
        schema = tools.read_file(
            "web/templates/install/schema/core_nav.json", base_dir)
        es.create_index(host, "core_nav", schema)
        es.flush(host, "core_nav")
        # set default title
        tools.set_conf(host, '-1', 'title', 'Portal')
        # create defailt role
        doc = {
            'site_id': 0,
            'users': ['EVERYONE'],
            'name': 'Users',
            'description': 'users'
        }
        es.create(host, 'core_nav', 'role', 'Users', doc)

        doc = {
            'site_id': 0,
            'users': ['EVERYONE'],
            'name': 'Admins',
            'description': 'site administrator'
        }
        es.create(host, 'core_nav', 'role', 'Admins', doc)
        es.flush(host, "core_nav")

    # check if core_data already exists
    if not es.index_exists(host, "core_data"):
        # create core_data
        schema = tools.read_file(
            "web/templates/install/schema/core_data.json", base_dir)
        es.create_index(host, "core_data", schema)
        es.flush(host, "core_data")

    # check if core_proxy already exists
    if not es.index_exists(host, "core_proxy"):
        # create core_proxy
        schema = tools.read_file(
            "web/templates/install/schema/core_proxy.json", base_dir)
        es.create_index(host, "core_proxy", schema)
        es.flush(host, "core_proxy")

    # check if core_task already exists
    if not es.index_exists(host, "core_task"):
        # create core_task
        schema = tools.read_file(
            "web/templates/install/schema/core_task.json", base_dir)
        es.create_index(host, "core_task", schema)
        es.flush(host, "core_task")

    # insert data
    install_data(host, base_dir)

    # install people
    people.install(host, base_dir)

    # install schedule
    schedule.install(host, base_dir)

    # install document
    document.install(host, base_dir)

    # install dashboard
    dashboard.install(host, base_dir)

    # install search
    search.install(host, base_dir)


    # create config
    config.create(base_dir, **form)

    return True



def install_data(host, base_dir):
    # delete module, operation
    try:
        es.delete_query(host, "core_nav", "module", {"query":{"match_all":{}}} )
        es.delete_query(host, "core_nav", "operation", {"query":{"match_all":{}}} )
    except:
        pass

    # bulk insert data
    bulk_install = tools.read_file(
        "web/templates/install/schema/core_nav_bulk.json", base_dir)
    es.bulk(host, bulk_install)

    # task module definition
    os.chdir("{}/web/templates/install/task_module".format(base_dir))
    for file in glob.glob("*.xml"):
        id = file.split("_")[0]
        definition = readfile(file)
        es.update(host, "core_task", "module", id, {
            "definition": definition
        })

    # install root site
    if not es.get(host, "core_nav", "site", 0):
        es.create(host, "core_nav", "site", 0,
            {"name": "",
             "display_name":"Root",
             "description":"Root site"})

    # install default navigation - dashboard
    if not es.get(host, "core_nav", "navigation", 0):
        es.create(host, "core_nav", "navigation", 0,
            {"name": "", "display_name":"Home",
             "site_id":0, "module_id":"4", "is_displayed":"1", "order_key": 0})

    # install default navigation - install
    if not es.get(host, "core_nav", "navigation", 1):
        es.create(host, "core_nav", "navigation", 1,
            {"name": "install", "display_name":"install",
             "site_id":0, "module_id":"1", "is_displayed":"0"})

    # install default navigation - auth
    if not es.get(host, "core_nav", "navigation", 2):
        es.create(host, "core_nav", "navigation", 2,
            {"name": "auth", "display_name": "Authentication",
             "site_id":0, "module_id": "2", "is_displayed":"0"})

    # install default navigation - admin
    if not es.get(host, "core_nav", "navigation", 3):
        es.create(host, "core_nav", "navigation", 3,
            {"name": "admin", "display_name":"admin",
             "site_id":0, "module_id":"3", "is_displayed":"0"})

    # install default navigation - people
    if not es.get(host, "core_nav", "navigation", 4):
        es.create(host, "core_nav", "navigation", 4,
            {"name": "people", "display_name":"People",
             "site_id":0, "module_id":"7", "is_displayed":"1", "order_key": 4})

    # install default navigation - people
    if not es.get(host, "core_nav", "navigation", 5):
        es.create(host, "core_nav", "navigation", 5,
            {"name": "schedule", "display_name":"Schedule",
             "site_id":0, "module_id":"7", "is_displayed":"1", "order_key": 5})

    # install default navigation - people
    if not es.get(host, "core_nav", "navigation", 6):
        es.create(host, "core_nav", "navigation", 6,
            {"name": "doc", "display_name":"Document",
             "site_id":0, "module_id":"7", "is_displayed":"1", "order_key": 6})
