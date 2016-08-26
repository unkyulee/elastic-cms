import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools


def install(host, base_dir):
    # check if people already exists
    if not es.index_exists(host, "people"):
        # create core_proxy
        schema = tools.read_file(
            "web/templates/install/schema/post.json", base_dir)
        es.create_index(host, "people", schema)
        es.flush(host, "people")

        # general configuration
        h = host; n = 4;
        tools.set_conf(h, n, 'name', 'People')
        tools.set_conf(h, n, 'description', 'Members of the organization')
        tools.set_conf(h, n, 'host', 'http://localhost:9200')
        tools.set_conf(h, n, 'index', 'people')
        tools.set_conf(h, n, 'upload_dir', '')
        tools.set_conf(h, n, 'allowed_exts', "jpg, jpeg, gif, png")
        tools.set_conf(h, n, 'page_size', 10)
        tools.set_conf(h, n, 'query', '*')
        tools.set_conf(h, n, 'sort_field', 'created')
        tools.set_conf(h, n, 'sort_dir', 'desc')

        # create fields
        es.create_mapping(host, 'people', 'post', {
            "email": { "type": "string" },
            "office": { "type": "string" },
            "phone": { "type": "string" },
            "photo": { "type": "string" },
            "password": { "type": "string" },
            "new_password": { "type": "string" }
        })
        es.flush(host, 'people')

        # add type field configuration
        doc = {
            "id": 'type',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'type',
            "visible": ['view'],
            "order_key": 5,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')

        # add id field configuration
        doc = {
            "id": 'id',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'id',
            "visible": ['create', 'view'],
            "order_key": 10,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')

        # add password field configuration
        doc = {
            "id": 'password',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'password',
            "visible": ['create'],
            "order_key": 11,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": """
<input type=password class="form-control" name="password">
            """
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')

        # add new_password field configuration
        doc = {
            "id": 'id',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'id',
            "visible": '',
            "order_key": 12,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": """
<input type=password class="form-control" name="new_password">
            """
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')

        # add title field configuration
        doc = {
            "id": 'title',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'full name',
            "visible": ['create', 'view', 'edit'],
            "order_key": 20,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # add office field configuration
        doc = {
            "id": 'office',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'office',
            "visible": ['create', 'view', 'edit'],
            "order_key": 100,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # add photo field configuration
        doc = {
            "id": 'photo',
            "is_filter": '0',
            "filter_field": '',
            "handler": 'file',
            "name": 'photo',
            "visible": ['create', 'view', 'edit'],
            "order_key": 100,
            "list_tpl": '',
            "view_tpl": """
{% if item.photo %}
<a href="{{p.url}}/file/view/{{item.photo}}">
  <img src="{{p.url}}/file/view/{{item.photo}}" width=200>
</a>
{% endif %}
            """,
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # add email field configuration
        doc = {
            "id": 'email',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'email',
            "visible": ['create', 'view', 'edit'],
            "order_key": 100,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # add phone field configuration
        doc = {
            "id": 'phone',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'phone',
            "visible": ['create', 'view', 'edit'],
            "order_key": 100,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # add description field configuration
        doc = {
            "id": 'description',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'description',
            "visible": ['create', 'edit', 'view'],
            "order_key": 200,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": """
<textarea id="description" name="description" class="form-control" rows=5>{{item.description}}</textarea>
            """
        }
        es.update(host, 'people', 'field', doc['id'], doc)
        es.flush(host, 'people')


        # create workflow
        doc = {
            "name" : 'create',
            "description" : '',
            "status" : '',
            "condition" : '',
            "validation" : """
import hashlib

def validation(p):
    if p['post'].get('password'):
        p['post']['password'] = hashlib.sha512(p['post'].get('password')).hexdigest()


            """,
            "postaction" : '',
            "screen" : ''
        }
        es.create(host, 'people', 'workflow', '', doc)


        doc = {
            "name" : 'password',
            "description" : '',
            "status" : '',
            "condition" : '',
            "validation" : """
import hashlib

def validation(p):
    # check if the password matches the orginal
    password = hashlib.sha512(p['post'].get('password')).hexdigest()
    if p['original'].get('password'):
        orig_password = hashlib.sha512(p['original'].get('password')).hexdigest()
    else:
        orig_password = ''

    # update to new password
    if password == orig_password:
        p['post']['password'] = hashlib.sha512(p['post'].get('new_password')).hexdigest()

    else:
        # if the password doesn't match then alert
        raise Exception('password does not match')

            """,
            "postaction" : '',
            "screen" : ['password', 'new_password']
        }
        es.create(host, 'people', 'workflow', '', doc)

        # add default people
        doc = {
            "id": 'EVERYONE',
            "title": 'EVERYONE',
            "description": 'system account representing all authenticated users'
        }
        es.update(host, 'people', 'post', doc['id'], doc)
        es.flush(host, 'people')

        # set permission
        permission_id = 'Admins_4'
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


        permission_id = 'Users_4'
        doc = {
            "operations": [
                'saerch/', 'post/view', 'filter/', 'file/', 'history/list',
                'history/view', 'post/create', 'post/edit'
            ]
        }
        es.create(host, 'core_nav', 'permission', permission_id, doc)


        # side layout
        tools.set_conf(h, n, 'side', """
<button type="button" class="btn btn-danger btn-block"
    onclick="location='{{p.url}}/post/edit/{{p.post.id}}?wf=password'">Change Password</button>
<br>
        """)


        # people item renderer
        tools.set_conf(h, n, 'search_item_template', """
{% extends "post/search/base.html" %}

{% macro default(post) %}
<table class="table">
  <tr>
    <th class="bg-success" colspan="2">
      <span>
        <a href="{{ p.url }}/post/view/{{ post.id }}">
          <b>{{post.highlight.title|first|safe}}</b>
        </a>
      </span>
    </th>
  </tr>

  <tbody>


    <tr>
      <td>
        <!-- photo -->
        {% if post.photo %}
        <a href="{{p.url}}/post/view/{{post.id}}">
          <img src="{{p.url}}/file/view/{{post.photo}}" height=120>
        </a>
        {% endif %}
      </td>
      <td>

        {% if post.email %}
        <div class="col-lg-6 col-md-6">
          <label class="col-lg-4 col-md-4 control-label">email</label>
          <div class="col-lg-8 col-md-8">{{post.email}}</div>
        </div>
        {% endif %}

        {% if post.phone %}
        <div class="col-lg-6 col-md-6">
          <label class="col-lg-4 col-md-4 control-label">phone</label>
          <div class="col-lg-8 col-md-8">{{post.phone}}</div>
          </div>
        </div>
        {% endif %}


        {% if post.office %}
        <div class="col-lg-6 col-md-6">
          <label class="col-lg-4 col-md-4 control-label">office</label>
          <div class="col-lg-8 col-md-8">{{post.office}}</div>
          </div>
        </div>
        {% endif %}

      </td>
    </tr>


  </tbody>
</table>

<br>
{% endmacro %}

{% block search_result %}

{% include "post/search/part/summary.html" %}
{% include "post/search/part/didyoumean.html" %}

{% for post in p.post_list %}
  {{ default(post) }}
{% endfor %}

{% include "post/search/part/pagination.html" %}

{# display create icon when post/create is allowed #}
{% if 'post/create' in p.allowed_operation %}
<div class="col-lg-12 text-right">
  <a href="{{p.url}}/post/create" title="new">
    <button type="button" class="btn btn-xs btn-danger">
      <span class="glyphicon glyphicon-plus"></span> New
    </button>
  </a>
</div>
{% endif %}


{% endblock %}
        """)
