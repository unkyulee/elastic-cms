import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools


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

        # general configuration
        tools.set_conf(h, n, 'name', 'Document')
        tools.set_conf(h, n, 'description', 'Document Management')
        tools.set_conf(h, n, 'host', 'http://localhost:9200')
        tools.set_conf(h, n, 'index', index)
        tools.set_conf(h, n, 'upload_dir', '')
        tools.set_conf(h, n, 'allowed_exts', "jpg, jpeg, gif, png, doc, docx, pdf, ppt, pptx, txt, xls, xlsx, rtf, odp, mp4, avi, ogg")
        tools.set_conf(h, n, 'page_size', 30)
        tools.set_conf(h, n, 'query', '*')
        tools.set_conf(h, n, 'sort_field', 'created')
        tools.set_conf(h, n, 'sort_dir', 'desc')

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
            "created_by": "EVERYONE"
        }
        es.update(host, index, 'post', doc['id'], doc)
        es.flush(host, index)
