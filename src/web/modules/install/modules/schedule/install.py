import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools


def install(host, base_dir):
    index = 'schedule'
    h = host
    n = 5
    # check if people already exists
    if not es.index_exists(host, index):
        # create core_proxy
        schema = tools.read_file(
            "web/templates/install/schema/post.json", base_dir)
        es.create_index(host, index, schema)
        es.flush(host, index)

        # general configuration
        tools.set_conf(h, n, 'name', 'Schedule')
        tools.set_conf(h, n, 'description', 'News and event of the organization')
        tools.set_conf(h, n, 'host', 'http://localhost:9200')
        tools.set_conf(h, n, 'index', index)
        tools.set_conf(h, n, 'upload_dir', '')
        tools.set_conf(h, n, 'allowed_exts', "jpg, jpeg, gif, png")
        tools.set_conf(h, n, 'page_size', 1000)
        tools.set_conf(h, n, 'query', '*')
        tools.set_conf(h, n, 'sort_field', 'start')
        tools.set_conf(h, n, 'sort_dir', 'desc')

        # create fields
        es.create_mapping(host, index, 'post', {
            "attendee": { "type": "string" },
            "organizer": { "type": "string" },
            "finish": { "type": "date" },
            "start": { "type": "date" }
        })
        es.flush(host, index)

        # add organizer field configuration
        doc = {
            "id": 'organizer',
            "is_filter": '1',
            "filter_field": '',
            "handler": '',
            "name": 'organizer',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 15,
            "list_tpl": '{{ item.organizer | first }}',
            "view_tpl": """
{% for organizer_id in item.organizer|getlist %}
    {% set organizer = organizer_id|get('http://localhost:9200', 'people', 'post') %}
    {% if organizer %}
        <div class="row">
            <div class="col-sm-11">
                <a href="/schedule?organizer={{organizer.id}}">
                    {{ organizer.title }}
                </a>
            </div>
            <div class="col-sm-1">
                <a href="/people/post/view/{{organizer.id}}">
                  <i class="fa fa-external-link" aria-hidden="true"></i>
                </a>
            </div>
        </div>
    {% endif %}
{% endfor %}
            """,
            "edit_tpl": """
<select id="organizer" style="width:100%"></select>
<ul id="organizer_list" class="list-group"></ul>

<script>
$(document).ready(function() {
  $("#organizer").select2({
    placeholder: "search for people",
    ajax: {
      url: '/people?json=1',
      dataType: 'jsonp',
      data: function (params) { return { q: params.term ? params.term + "*" : "*" } },
      processResults: function (data, page) {
        ResultList = { "results" : [] , "more":false }
        data.hits.hits.forEach(function(entry) {
          ResultList.results.push({
            "id": entry._id,
            "text": entry._source.title
          })
        });
        return ResultList;
      }
    }
  });

  $("#organizer").on('select2:select', function (evt) {
    // Do something
    id = evt.params.data.id;
    text = evt.params.data.text;

    add_organizer( id, text );
  });

  $( "#organizer_list" ).sortable();
  $( "#organizer_list" ).disableSelection();

});


</script>

<script id="organizer_item" type="text/html">
<li class="list-group-item" id="$id">
    <div class="container-fluid" >
        <div class="row">
            <div class="col-md-1">
                <a href="javascript:remove_organizer('$id')"><i class="fa fa-minus-circle" aria-hidden="true"></i></a>
            </div>
            <div class="col-md-11">
                $organizer
            </div>
        </div>
    </div>
    <input type="checkbox" checked=1 style="display: none" name="organizer" value="$id">
</li>
</script>

<script>
String.prototype.replaceAll = function(search, replace) {
    if (replace === undefined) {
        return this.toString();
    }
    return this.split(search).join(replace);
}

function add_organizer(id, organizer, affiliation) {
    var organizer_tpl = $("#organizer_item").html()
    organizer_tpl = organizer_tpl.replaceAll("$id", id)
    organizer_tpl = organizer_tpl.replaceAll("$organizer", organizer)

    var organizer_list = document.getElementById('organizer_list');
    organizer_list.insertAdjacentHTML('beforeend', organizer_tpl);
}

function remove_organizer(id) {
    $("#"+id).remove()
}

// add organizers
{% for a in item.organizer|getlist %}
    {% set organizer = a|get('http://localhost:9200', 'people', 'post') %}
    {% if organizer %}
        add_organizer( "{{ organizer.id }}", "{{ organizer.title }}" );
    {% endif %}
{% endfor %}

</script>
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add start field configuration
        doc = {
            "id": 'start',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'start',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 50,
            "list_tpl": '{{item.start|dt}}',
            "view_tpl": '{{item.start|dt}}',
            "edit_tpl": """
<input type="text" id="start" name="start" value="{{item.start}}">
<script>
$(function() {
    $("#start").datepicker({
      dateFormat: "yy-mm-dd"
    });
});
</script>
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add finish field configuration
        doc = {
            "id": 'finish',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'finish',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 55,
            "list_tpl": '{{item.finish|dt}}',
            "view_tpl": '{{item.finish|dt}}',
            "edit_tpl": """
<input type="text" id="finish" name="finish" value="{{item.finish}}">
<script>
$(function() {
    $("#finish").datepicker({
      dateFormat: "yy-mm-dd"
    });
});
</script>
"""
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add attendee field configuration
        doc = {
            "id": 'attendee',
            "is_filter": '1',
            "filter_field": '',
            "handler": 'multiple',
            "name": 'attendee',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 100,
            "list_tpl": '{{ item.attendee | first }}',
            "view_tpl": """
{% for attendee_id in item.attendee|getlist %}
    {% set attendee = attendee_id|get('http://localhost:9200', 'people', 'post') %}
    {% if attendee %}
        <div class="row">
            <div class="col-sm-11">
                <a href="/schedule?attendee={{attendee.id}}">
                    {{ attendee.title }}
                </a>
            </div>
            <div class="col-sm-1">
                <a href="/people/post/view/{{attendee.id}}">
                  <i class="fa fa-external-link" aria-hidden="true"></i>
                </a>
            </div>
        </div>
    {% endif %}
{% endfor %}
            """,
            "edit_tpl": """
<select id="attendee" style="width:100%"></select>
<ul id="attendee_list" class="list-group"></ul>

<script>
$(document).ready(function() {
  $("#attendee").select2({
    placeholder: "search for people",
    ajax: {
      url: '/people?json=1',
      dataType: 'jsonp',
      data: function (params) { return { q: params.term ? params.term + "*" : "*" } },
      processResults: function (data, page) {
        ResultList = { "results" : [] , "more":false }
        data.hits.hits.forEach(function(entry) {
          ResultList.results.push({
            "id": entry._id,
            "text": entry._source.title
          })
        });
        return ResultList;
      }
    }
  });

  $("#attendee").on('select2:select', function (evt) {
    // Do something
    id = evt.params.data.id;
    text = evt.params.data.text;

    add_attendee( id, text );
  });

  $( "#attendee_list" ).sortable();
  $( "#attendee_list" ).disableSelection();

});


</script>

<script id="attendee_item" type="text/html">
<li class="list-group-item" id="$id">
    <div class="container-fluid" >
        <div class="row">
            <div class="col-md-1">
                <a href="javascript:remove_attendee('$id')"><i class="fa fa-minus-circle" aria-hidden="true"></i></a>
            </div>
            <div class="col-md-11">
                $attendee
            </div>
        </div>
    </div>
    <input type="checkbox" checked=1 style="display: none" name="attendee" value="$id">
</li>
</script>

<script>
String.prototype.replaceAll = function(search, replace) {
    if (replace === undefined) {
        return this.toString();
    }
    return this.split(search).join(replace);
}

function add_attendee(id, attendee, affiliation) {
    var attendee_tpl = $("#attendee_item").html()
    attendee_tpl = attendee_tpl.replaceAll("$id", id)
    attendee_tpl = attendee_tpl.replaceAll("$attendee", attendee)

    var attendee_list = document.getElementById('attendee_list');
    attendee_list.insertAdjacentHTML('beforeend', attendee_tpl);
}

function remove_attendee(id) {
    $("#"+id).remove()
}

// add attendees
{% for a in item.attendee|getlist %}
    {% set attendee = a|get('http://localhost:9200', 'people', 'post') %}
    {% if attendee %}
        add_attendee( "{{ attendee.id }}", "{{ attendee.title }}" );
    {% endif %}
{% endfor %}

</script>
            """
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)

        # add title field configuration
        doc = {
            "id": 'title',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'title',
            "visible": ['create', 'view', 'edit', 'list'],
            "order_key": 10,
            "list_tpl": '',
            "view_tpl": '',
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # add description field configuration
        doc = {
            "id": 'description',
            "is_filter": '0',
            "filter_field": '',
            "handler": '',
            "name": 'description',
            "visible": ['view'],
            "order_key": 1000,
            "list_tpl": '',
            "view_tpl": '<pre><code>{{item.description}}</code></pre>',
            "edit_tpl": ''
        }
        es.update(host, index, 'field', doc['id'], doc)
        es.flush(host, index)


        # set permission
        permission_id = 'Admins_5'
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


        permission_id = 'Users_5'
        doc = {
            "operations": [
                'saerch/', 'post/view', 'filter/', 'file/', 'history/list',
                'history/view', 'post/create', 'post/edit'
            ]
        }
        es.create(host, 'core_nav', 'permission', permission_id, doc)


        # add test event
        doc = {
            "id": 'test',
            "title": "You have installed Elastic-CMS today !",
            "organizer": "EVERYONE",
            "attendee": "EVERYONE",
            "start": es.now(),
            "finish": es.now(),
            "description": 'Thanks for installing the system. This is a sample event'
        }
        es.update(host, index, 'post', doc['id'], doc)
        es.flush(host, index)


        # people item renderer
        tools.set_conf(h, n, 'search_item_template', """
{% extends "post/search/base.html" %}

{% block search_result %}
<link rel="stylesheet" type="text/css" href="//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.7.2/fullcalendar.min.css" />
<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/moment.js/2.14.1/moment.min.js"></script>
<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.7.2/fullcalendar.min.js"></script>

<div class="col-lg-12">
  <div id='calendar'></div>
</div>

<script>
$(document).ready(function() {

    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
      eventLimit: true, // allow "more" link when too many events
      events: [
        {% for post in p.post_list %}
        {
            id:'{{post.id}}',
            title: '{{post.title}}',
            tooltip: '{{post.title}}',
            start: '{{post.start}}'
        }
          {% if not loop.last %}, {% endif %}
        {% endfor %}
      ],
      eventClick: function(calEvent, jsEvent, view) {
        location = '{{p.url}}/post/view/' + calEvent.id
      },
      eventRender: function(event, element) {
        element.attr('title', event.tooltip);
      }
    })

});
</script>


{# display create icon when post/create is allowed #}
{% if 'post/create' in p.allowed_operation %}
<div class="col-lg-12 text-right">
  <br>
  <a href="{{p.url}}/post/create" title="new">
    <button type="button" class="btn btn-xs btn-danger">
      <span class="glyphicon glyphicon-plus"></span> New Schedule
    </button>
  </a>
</div>
{% endif %}

{% endblock %}
        """)
