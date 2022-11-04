<!DOCTYPE html>
<html>
<head>
    <title>Fenrir (c)</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
    </head>
<body onload="replaceHREFS();">
<script src="static/script.js"></script>
{% for result in results %}
<ul class="list-group">
  {%- if result['ENABLED'] == 1 -%}
    {%- set link = "disable/" + result['IP'] -%}
    {%- set image = "static/enabled.png" -%}
    {%- set currentstate = "enabled" -%}
  {%- else -%}
    {%- set link = "enable/" + result['IP'] -%}
    {%- set image = "static/disabled.png" -%}
    {%- set currentstate = "disabled"-%}
  {%- endif -%}
  <a id="{{ result['IP'] }}" href="{{ link }}" onclick="changeState('{{ result['IP'] }}');" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
    <div class="flex-column">
      <p><big>{{ result['IP'] }}</big></p>
      <p>{{ result['VENDOR'] }}</p>
      <p>{{ result['MAC'] }}</p>
    </div>
    <div class="image-parent" >
        <img id="img-{{ result['IP'] }}" src="{{ image }}" width="150" height="150" class="img-fluid" alt="">
    </div>
  </a>
</ul>
{% endfor %}
</body>
</html>