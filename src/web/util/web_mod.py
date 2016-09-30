import os
import json
import importlib
from flask import session
import lib.es as es
import web.util.tools as tools

# find navigation structure
def define(host, nav):
    navigation = {
        "site": None,
        "navigation": None,
        "operation": None,
        "module": None
    }

    # look up in site table to see if any match found
    if len(nav) > 0 and nav[0]:
        # search for the site matches the name given nav[0]
        ret = es.list(host, "core_nav", "site", "name:{}".format(nav[0]))
        # first item is what we want
        if len(ret): navigation['site'] = ret[0]

    # if the site has not been identified yet
    # then assign default site
    if not navigation['site']:
        navigation['site'] = es.get(host, "core_nav", "site", 0) # root site id:0
        # if the site was not identified then it maybe that site is omitted from the url
        # and navigation is directly passed
        nav.insert(0, '')

    # find navigation
    if len(nav) > 1 and nav[1]:
        # search for the navigation matches nav[1]
        query = "site_id:{} AND name:{}".format(navigation['site']['id'], nav[1])
        ret = es.list(host, "core_nav", "navigation", query)
        # first navigation is what we want
        if len(ret): navigation['navigation'] = ret[0]

    # if navigation has not been identified yet then
    # assign the first navigation when ordered by order_key
    if not navigation['navigation']:
        query = "site_id:{}".format(navigation['site']['id'])
        option = "sort=order_key:asc&size=1"
        ret = es.list(host, "core_nav", "navigation", query, option)
        # first navigation is what we want
        if len(ret):
            navigation['navigation'] = ret[0]
            # if the navigation is not identified then it maybe that
            # navigation is omitted from the url and operation is directly passed
            nav.insert(1, navigation['navigation']['name'])


    # identify module
    if navigation['navigation'].get('module_id'):
        module_id = navigation['navigation'].get('module_id')
        navigation['module'] = es.get(host, 'core_nav', 'module', module_id)


    # identify operation
    if len(nav) > 2 and nav[2]:
        navigation['operation'] = nav[2]

    # see if the operation id is available
    query = "module_id:{} AND name:{}".format(
        navigation['module']['id'], nav[2] if len(nav) > 2 and nav[2] else 'default')
    ret = es.list(host, "core_nav", "operation", query)

    if len(ret):
        navigation['operation_id'] = ret[0]['id']


    # save determined nav
    navigation['nav'] = nav

    return navigation



def build_payload(conf, request, navigation):
    # navigation_url
    navigation['url'] = os.path.join(
        request.url_root,
        navigation['site']['name'],
        navigation['navigation']['name']).strip("/")

    # recover for windows format
    navigation['url'] = navigation['url'].replace("\\", "/")

    # full url
    navigation['full_url'] = request.url

    # add config.py
    navigation['host'] = conf['HOST']
    navigation['debug'] = conf['DEBUG']
    navigation['session_key'] = conf['CSRF_SESSION_KEY']
    navigation['base_dir'] = conf['BASE_DIR']

    # global title
    navigation['title'] = tools.get_conf(conf['HOST'], "-1", "title")

    # global script
    navigation['script'] = tools.get_conf(conf['HOST'], "-1", "script")

    # site list
    navigation['site_list'] = get_site_list(conf['HOST'], navigation)

    # navigation list
    navigation['nav_list'] = get_nav_list(conf['HOST'], navigation)

    # login
    navigation['login'] = session.get('user')

    # list of roles where user belongs
    query = "site_id:{} AND (users:{} OR users:EVERYONE)".format(
                navigation['site']['id'], navigation['login'])
    navigation['user_roles'] = es.list(conf['HOST'], 'core_nav', 'role', query, [])

    # get list of all permissions
    navigation['allowed_operation'] = []
    for role in navigation['user_roles']:
        permission_id = "{}_{}".format(role['id'], navigation['navigation']['id'])
        permission = es.get(conf['HOST'], 'core_nav', 'permission', permission_id)
        if permission:
            navigation['allowed_operation'].extend(permission['operations'])

    return navigation


def get_module(navigation):
    # Imports from Web folder and looks for a module
    path = "web.modules.{}.control".format(navigation['module']['name'])
    mod = importlib.import_module(path)

    return mod


def get_nav_list(host, navigation):
    query = "site_id:{} AND is_displayed:1".format(navigation['site']['id'])
    option = "size=10000&sort=order_key:asc"
    nav_list = es.list(host, 'core_nav', 'navigation', query, option)
    nav_tree = []

    # sort the nav list according to the hierarchy
    for nav in nav_list:
        # does its id appears as parent_id in others?
        nav['children'] = list(
            child for child in nav_list
            if child.get('parent_id') == nav['id']
        )
        # if it is not root node then do not add to the tree
        if not nav.get('parent_id'):
            nav_tree.append(nav)

    return nav_tree


def get_site_list(host, navigation):
    query = "is_displayed:1"
    option = "size=10&sort=order_key:asc"
    site_list = es.list(host, 'core_nav', 'site', query, option)

    return site_list
