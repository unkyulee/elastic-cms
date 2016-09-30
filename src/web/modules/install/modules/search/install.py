# -*- coding: utf-8 -*-
import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools


def install(host, base_dir):

    # check if search site exists
    sites = es.list(host, 'core_nav', 'site', "name:'search'")
    if not sites:
        # create a site
        site = {
            'name' : 'search',
            'display_name' : 'Search Engine'
        }

        es.create(host, 'core_nav', 'site', 'search', site)

        # create a navigation
        navigation = {
            "site_id":        'search',
            "module_id":      '7',
            "order_key":      100,
            "is_displayed":   '1',
            "name" :          'search',
            "display_name" :  'Search Engine',
            "new_window" :    '0'
        }
        es.create(host, 'core_nav', 'navigation', 'searchnav', navigation)

        # set up the site
        config = {
            'name': 'index',
            'value': 'everything'
        }
        es.create( host, 'core_nav', 'config', 'searchnav_{}'.format(config['name']), config)

        config = {
            'name': 'host',
            'value': 'http://localhost:9200'
        }
        es.create( host, 'core_nav', 'config', 'searchnav_{}'.format(config['name']), config)

        config = {
            'name': 'search_item_template',
            'value': """
{% extends "post/search/base.html" %}


{% macro default(post) %}
<table class="table">
  <tr><th class="bg-success">
    <!-- Type -->
    <span class="label label-info">{{ post._index }}</span>
    <!-- Title -->
    <span>
      {% if post.url %}
          <a href="{{post.url}}" target=_blank>
      {% else %}
          <a href="/search/redirect?index={{post._index}}&id={{post.id}}">
      {% endif %}
        <b>{{post.highlight.title|first|safe}}</b>
      </a>
    </span>
  </th></tr>
  <tbody>

    {% if p.field_list|length > 0 %}
    <tr><td>
    {% for field in p.field_list
        if field.id != "title"
          and field.id != "description"
          and post[field.id] %}

        <div class="col-lg-6 col-md-6">
          <label class="col-lg-4 col-md-4 control-label">{{field.name}}</label>
          <div class="col-lg-8 col-md-8">

            {% if field.list_tpl %}
              {{ field.list_tpl|render(p, post)|safe }}

            {% elif field.handler == "file" %}
              <a href="{{p.url}}/file/view/{{post[field.id]}}?id={{post.id}}" target=_blank>
                download
              </a>

            {% elif field.handler == "multiple" %}
              {% for v in post[field.id]|getlist %}
                {% if field.is_filter == "1" %}<a href="{{p.url}}?{{field.name}}={{v|strip}}">{% endif %}
                  {{v|strip}}
                {% if field.is_filter == "1" %}</a>{% endif %}
                {%- if not loop.last %}, {% endif %}

              {% endfor %}

            {% else %}
              {% if field.is_filter == "1" %}<a href="{{p.url}}?{{field.name}}={{ post[field.id] }}">{% endif %}
                {{ post[field.id] }}
              {% if field.is_filter == "1" %}</a>{% endif %}

            {%endif%}

          </div>
        </div>
    {%endfor%}
    </td></tr>
    {% endif %}

    {% if post.highlight.description or post.highlight.content %}
    <tr><td>
      {{post.highlight.description|first|safe}}
      {{post.highlight.content|first|safe}}
    </td></tr>
    {% endif %}

    <tr><td>
      {% if post.url %}
      <a href="{{post.url}}" target=_blank>{{post.url}}</a> -
      {% endif %}
      <small>{{post.created|dt}}</small>
    </td></tr>

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
      <span class="glyphicon glyphicon-plus"></span> New
    </button>
  </a>
</div>
{% endif %}


{% endblock %}
            """
        }
        es.create( host, 'core_nav', 'config', 'searchnav_{}'.format(config['name']), config)
