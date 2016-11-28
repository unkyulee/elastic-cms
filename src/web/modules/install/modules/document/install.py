import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools
from web.modules.post.services import config

def install(host, base_dir):
    index = 'doc'
    h = host
    n = 6
    # check if people already exists
    if not es.index_exists(host, index):
        # create core_proxy
        schema = tools.read_file(
            "web/templates/install/schema/post.json", base_dir)
        es.create_index(host, index, schema)
        es.flush(host, index)

        # global configuration
        tools.set_conf(h, n, 'host', 'http://localhost:9200')
        tools.set_conf(h, n, 'index', index)

        # local configuration
        config.set_conf(h, 'doc', 'name', 'Document')
        config.set_conf(h, 'doc', 'description', 'Document Management')
        config.set_conf(h, 'doc', 'upload_dir', '')
        config.set_conf(h, 'doc', 'allowed_exts', "jpg, jpeg, gif, png, doc, docx, pdf, ppt, pptx, txt, xls, xlsx, rtf, odp, mp4, avi, ogg")
        config.set_conf(h, 'doc', 'page_size', 30)
        config.set_conf(h, 'doc', 'query', '*')
        config.set_conf(h, 'doc', 'sort_field', 'created')
        config.set_conf(h, 'doc', 'sort_dir', 'desc')

        # create fields
        es.create_mapping(host, index, 'post', {
            "filepath": { "type": "string" }
        })
        es.flush(host, index)

        # add title field configuration
        doc = {
            "id": 'title',
            "name": 'title',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 100,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add description field configuration
        doc = {
            "id": 'description',
            "name": 'description',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "visible": ['create', 'view', 'edit'],
            "order_key": 101,
            "list_tpl": '',
            "view_tpl": '<pre><code>{{ item.description }}</code></pre>',
            "edit_tpl": """
<textarea id="description" name="description" class="form-control" rows=5>{{item.description}}</textarea>
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add filepath field configuration
        doc = {
            "id": 'filepath',
            "name": 'filepath',
            "is_filter": '0',
            "filter_field": '',
            "handler": 'file',
            "visible": ['create', 'view', 'edit'],
            "order_key": 105,
            "list_tpl": '',
            "view_tpl": """
<a href="{{p.url}}/file/view/{{item.filepath}}?id={{item.id}}" class="btn btn-danger btn-xs">download</a>
<a href="{{p.url}}/file/view/{{item.filepath}}?id={{item.id}}" target=_blank>
{{item.filepath|filename(item.id)}}
</a>
            """,
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # add created_by field configuration
        doc = {
            "id": 'created_by',
            "name": 'created_by',
            "is_filter": '1',
            "filter_field": '',
            "handler": '',
            "visible": ['list'],
            "order_key": 102,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add created_by field configuration
        doc = {
            "id": 'created',
            "name": 'created',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "visible": ['list'],
            "order_key": 103,
            "list_tpl": """{{item.created|dt}}""",
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # add acl_readonly field configuration
        doc = {
            "id": 'acl_readonly',
            "name": 'acl_readonly',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "visible": [],
            "order_key": 900,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": """
{% import "widget/select_multi.html" as select_multi %}
{{select_multi.render("acl_readonly", "acl_readonly", item.acl_readonly, ajax="/people?json=1")}}
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # add acl_edit field configuration
        doc = {
            "id": 'acl_edit',
            "name": 'acl_edit',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "visible": [],
            "order_key": 900,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": """
{% import "widget/select_multi.html" as select_multi %}
{{select_multi.render("acl_edit", "acl_edit", item.acl_edit, ajax="/people?json=1")}}
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # add workflow
        doc = {
          "status": "",
          "postaction": "",
          "name": "security",
          "screen": [
            "acl_readonly",
            "acl_edit"
          ],
          "validation": "",
          "condition": """
# p - context of current request
def condition(p):

    # author can edit
    if p['post'].get('created_by') == p['login']:
        return True

    # editors can edit
    if p['login'] in p['post'].get('acl_edit'):
        return True

    # if allowed to everyone then
    if 'EVERYONE' in p['post'].get('acl_edit'):
        return True

    return tools.alert('permission not granted')
    # this message will be displayed in the web browser when condition not met
    # return tools.alert('edit allowed to author only')

          """,
          "description": "Set Security"
        }

        es.create(host, index, 'workflow', '', doc)
        es.flush(host, index)



        # set permission
        permission_id = 'Admins_6'
        doc = {
            "operations": [
                'saerch/', 'post/view', 'filter/', 'file/', 'history/list',
                'history/view', 'post/create', 'post/edit', 'post/delete',
                'config/', 'list_item/', 'layout/', 'field/default', 'field/edit',
                'mapping/default', 'mapping/edit', 'backup/default', 'backup/download',
                'backup/restore', 'role/default', 'role/edit', 'permission/default',
                'permission/edit', 'workflow/default', 'workflow/create', 'workflow/edit',
                'workflow/delete'
            ]
        }
        es.create(host, 'core_nav', 'permission', permission_id, doc)


        permission_id = 'Users_6'
        doc = {
            "operations": [
                'saerch/', 'post/view', 'filter/', 'file/', 'history/list',
                'history/view', 'post/create', 'post/edit'
            ]
        }
        es.create(host, 'core_nav', 'permission', permission_id, doc)


        # add test document
        doc = {
            "id": 'test_doc',
            "title": "You have installed Elastic-CMS today !",
            "description": "This is sample document",
            "created": es.now(),
            "created_by": "EVERYONE",
            "acl_readonly": "EVERYONE",
            "acl_edit": "EVERYONE"
        }
        es.update(host, index, 'post', doc['id'], doc)
        es.flush(host, index)
