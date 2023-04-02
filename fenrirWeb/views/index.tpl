
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Fenrir (c)</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
  </head>

  <body style="padding-top: 5rem;">
    {%- include "navbar.tpl" -%}
    <main role="main">
      <div class="container-fluid">
        {%- if not hasprofiles or needspassword -%}
          <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
            <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
              <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
            </symbol>
          </svg>
          <div class="alert alert-danger text-center" role="alert">
            <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
            {%- if not hasprofiles -%}
            <a>No VPNProfiles configured. Intercept-routing is not possible without valid VPNProfile. Click <a href="/settings" class="alert-link">here</a> to create a VPNProfile </a>
            {%- else -%}
            <a>Password to decrypt VPNProfiles is needed. Click <a href="/authenticated" class="alert-link">here</a> to Enter Password </a>
            {%- endif -%}
            <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
          </div>
        {%- endif -%}
        {% for result in results %}
        <ul class="list-group">
          {%- set iddata = result.get('IP') -%}
          {%- if result['ENABLED'] == 1 -%}
            {%- set link = "disable/" + iddata -%}
            {%- set image = "static/enabled.png" -%}
            {%- set currentstate = "enabled" -%}
          {%- else -%}
            {%- set link = "enable/" + iddata -%}
            {%- set image = "static/disabled.png" -%}
            {%- set currentstate = "disabled"-%}
          {%- endif -%}
          {%- if not hasprofiles or needspassword -%}
            {%- set iddata = '' -%}
          {%- endif -%}
          <a id="{{ iddata }}" href="javascript:void(0);" onclick="changeState('{{ iddata }}');" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
            <div class="flex-column">
              <p><big>{{ result.get('IP') }}</big></p>
              <p>{{ result['VENDOR'] }}</p>
              <p>{{ result['MAC'] }}</p>
            </div>
            <div class="image-parent" >
                <img id="img-{{ iddata }}" src="{{ image }}" width="150" height="150" class="img-fluid" alt="">
            </div>
          </a>
        </ul>
        {% endfor %}
      </div>
    </main>

    <script src="static/fenrir.js"></script>
    <main>
  </body>
</html>
