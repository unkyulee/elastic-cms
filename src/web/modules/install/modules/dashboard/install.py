# -*- coding: utf-8 -*-
import glob, os
from lib import config # config.py
import lib.es as es
from lib.read import readfile
import web.util.tools as tools


def install(host, base_dir):
    tools.set_conf(host, 0, "dashboard","""

{% extends "base.html" %}
{% block head %}
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.css" />
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"></script>
{% endblock %}
{% block content %}
<!-- CONTENT HEADER -->
<div class="page-header">
  <h2>Portal - <small><b>your company name here</b></small></h2>
  integrate information, people and processes across the organization
</div>

<div class="row">
  <div class="col-lg-3 col-md-3">

    <p class="bg-primary">  <b>Portal Features</b></p>
    <table class="table table-hover table-responsive">
        <tr><td>
            <a href="/people">People</a>
        </td></tr>
        <tr><td>
            <a href="/schedule">Schedule</a>
        </td></tr>
        <tr><td>
            <a href="/doc">Document</a>
        </td></tr>
    </table>

  </div> <!-- col-lg-3 -->

  <div class="col-lg-9 col-md-9">

   <!-- schedule -->
   <div class="row">
     <div class="col-lg-12 col-md-12">

       <a href="/schedule">
           <p class="bg-primary"> <b>Meetings & schedules</b></p>
       </a>
       <div id="News" class="timeline-tgt"></div>
       <script type="text/javascript">
       function LoadTimeline(items) {
           timeline = new vis.Timeline(
               document.getElementById('News'),
               items, { minHeight: '300px', maxHeight: '300px', clickToUse: true }
           );
           timeline.on('select', function (properties) {
               if( properties.items.length > 0 )
                   location = '/schedule/post/view/'+String(properties.items[0])
           });
           return timeline
       }

       function Loadschedule(items) {
           $.ajax({
               url: '/schedule?q=start:[now/d TO now%2B15d]&json=1',
               async: true, dataType: "jsonp",
               success: function(res) {
                   var schedules = []
                   res.hits.hits.forEach(function(entry) {
                     schedule = {
                         id: entry._id,
                         content: entry._source.title,
                         start: entry._source.start
                     }
                     schedules.push(schedule);
                   });
                   // Add to timeline
                   items.add(schedules); timeline.fit();
               },
           });
       }

       var items = new vis.DataSet();
       var timeline = null;
       $(document).ready(function(){
           timeline = LoadTimeline(items);
           Loadschedule(items);
       });

       </script>
     </div>
   </div> <!-- schedule -->
   <br>

    <!-- Documents -->
    <div class="row">
      <div class="col-lg-12 col-md-12">
        <a href="/doc">
            <p class="bg-primary"> <b>Documents</b></p>
        </a>
        <table id="Documents" class="table table-striped table-hover table-responsive"></table>
        <script>
        $.ajax({
          url: '/doc?json=1&size=10',
          async: true, dataType: "jsonp" ,
          success: function(res) {
            var html = ""
            res.hits.hits.forEach(function(entry) {
              author = entry._source.created_by
              if ( Array.isArray(author) ) author = author[0]

              html += "<tr>"
              html += '<td><a href=/doc/post/view/'+entry._id+'><b>'+entry._source.title+'</b></a></td>'
              html += '<td><a href="/search?q='+author+'">'+author+'</a></td>'
              html += "</tr>"
            });
            $("#Documents").html(html);
          } ,
        });
        </script>
      </div>
    </div> <!-- document -->


  </div> <!-- col-lg-9 -->

</div> <!-- row -->

{% endblock %}

    """)
