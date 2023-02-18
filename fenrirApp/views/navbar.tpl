<header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top bg-dark bg-primary">
      <div class="container-fluid">
          <a class="navbar-brand col-1" href="index.html">
              <img src="static/favicon.ico" width="48" height="48" class="d-inline-block align-center" style="filter: invert(100%);" alt="Fenrir Home">
              Fenrir Home
          </a>
          <ul class="nav navbar-nav mr-auto offset-7 col-1">
            <li class="nav-item">
              {%- if isauthenticated -%} {%- set href="settingsauthenticated" -%} {%- else -%} {%- set href="settings" -%} {%- endif -%}
              <a class="nav-link d-inline-block align-center" href="{{href}}">
                <img src="static/settings.png" width="32" height="32" class="d-inline-block align-center" style="filter: invert(100%);" alt="Seetings">
                Settings</a>
            </li>
          </ul>
      </div>
    </nav>
</header>