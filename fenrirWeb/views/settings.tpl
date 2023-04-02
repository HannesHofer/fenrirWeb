<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Fenrir (c)</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
  </head>

  <body onload="modalData();" style="padding-top: 5rem;">
    {%- include "navbar" -%}
    <main role="main">
      <div class="container mt-4">
        <div class="m-4 mx-0"><h4>VPN Profile configuration</h4></div>
        <table class="table">
          <thead>
            <tr>
              {%- set vpncolumns = ['profilename', 'description', 'isdefault', 'ondemand'] -%}
              {%- for col in vpncolumns -%}
                <th>{{col}}</th>
              {%- endfor -%}
              <th>modify</th>
            </tr>
          </thead>
          <tbody id="vpnsettingstablebody">
            {%- for key, config in vpnconfigs.items() -%}
              <tr id="profile{{loop.index}}">
                {%- for col in vpncolumns -%}
                  {%- set colsize="col-3" %}
                  {%- set currentval = config[col] -%}
                  {%- if currentval == true -%}
                    {%- set currentval="yes" -%}
                    {%- set colsize="col-2" %}
                  {%- elif currentval == false -%}
                    {%- set currentval="no" -%}
                    {%- set colsize="col-2" %}
                  {%- endif -%}
                  <td class="{{colsize}} {{col}}">{{currentval}}</td>
                {% endfor %}
                <td class="col-2 modify">
                  <button class="btn btn-primary" data-bs-toggle="modal" data-id='{"type": "VPNProfile", "data": "{{config[vpncolumns[0]]}}"}'  href="#configurationDataModal" role="button" {% if not isauthenticated %} disabled {% endif %}>edit...</button>
                  <button class="btn btn-primary mx-xl-2" data-bs-toggle="modal" data-id='{"type": "VPNProfile", "data": "{{config[vpncolumns[0]]}}"}' href="#deleteModal" role="button" {% if not isauthenticated %} disabled {% endif %} >delete</a>
                </td>
              </tr>
            {%- endfor -%}
            </tr>
          </tbody>
        </table>
        <div class="row mt-4">
          {%- set addclass = "btn btn-success col-2" -%}
          {%- if not isauthenticated -%}
            <div class="offset-8 col-2">
              <a class="btn btn-primary offset-6 col-6" href="javascript:unlockVPNProfiles();" role="button">Unlock</a>
            </div>
          {%- else -%}
            {%- set addclass = addclass + " offset-10" -%}
          {%- endif -%}
          <button class="{{addclass}}" data-bs-toggle="modal" href="#configurationDataModal" role="button" {% if not isauthenticated %} disabled {% endif %} >Add VPN Configuration...</button>
       </div>
      </div>

      <div class="container mt-4 pt-4">
        <div class="m-4 mx-0"><h4>IP/VPNProfile mapping</h4></div>
        <table class="table">
          <thead>
            <tr>
              {%- set mappingcolumns = ['IPAddress', 'VPNProfile'] -%}
              {%- for col in mappingcolumns -%}
                <th>{{col}}</th>
              {%- endfor -%}
              <th></th>
              <th>modify</th>
            </tr>
          </thead>
          <tbody id="vpnmappingtablebody">
            {%- for ip, profile in vpnmappinconfig.items() -%}
              <tr id="mapping{{loop.index}}">
                <td class="col-3 {{mappingcolumns[0]}}">{{ip}}</td>
                <td class="col-3 {{mappingcolumns[1]}}">{{profile}}</td>
                <td class="col-4"></td>
                <td class="col-2 modify">
                  <a class="btn btn-primary" data-bs-toggle="modal" data-id='{"type": "Mapping for", "data": "{{ip}}", "profile": "{{profile}}"}' href="#mappingModal" role="button">edit...</a>
                  <a class="btn btn-primary mx-xl-2" data-bs-toggle="modal" data-id='{"type": "Mapping for", "data": "{{ip}}", "profile": "{{profile}}"}' href="#deleteModal" role="button">delete</a>
                </td>
              </tr>
            {%- endfor -%}
          </tbody>
        </table>
        <a class="btn btn-success offset-10 col-2 mt-4" data-bs-toggle="modal" href="#mappingModal" role="button">Add IP/VPNProfile map...</a>
      </div>

      <div class="container mt-4 pt-4">
        <div class="m-4 mx-0"><h4>Password management</h4></div>
        <button class="btn btn-success row mt-4 offset-10" data-bs-toggle="modal" data-id='{"type": "change"}' href="#changepasswordmodal" role="button" {% if not isauthenticated %} disabled {% endif %} >Change Password...</button>
      </div>
    </main>

    <div class="modal fade" id="configurationDataModal" aria-hidden="true" aria-labelledby="configurationDataModalLabel" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered ">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="configurationDataModal">VPN Configuration Data</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {%- include "vpninput" -%}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-success" id="vpnconfigsubmit" onclick="sumbitVPNConfig();">
              <span class="spinner-border spinner-border-sm mr-2" id="vpnconfigsubmitspinner" hidden role="status" aria-hidden="true"></span>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="mappingModal" aria-hidden="true" aria-labelledby="mappingModalLabel" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered ">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">IP/VPNProfile mapping</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {%- include "mappinginput" -%}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-success" id="mappingsubmit" onclick="sumbitMappingConfig();">
              <span class="spinner-border spinner-border-sm mr-2" id="mappingsubmitspinner" hidden role="status" aria-hidden="true"></span>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" >Delete Profile</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete <span id="deletetype"></span>: <span id="deletename"></span>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" id="deletemodalconfirm" onclick="deleteVPNConfigConfirmed();">Yes</button>
          </div>
        </div>
      </div>
    </div>
    {%- include "changepassword" -%}
    {%- if needscreatepassword -%}
      {%- include "createpassword" -%}
    {%- endif -%}
    <div id="alerttoast" class="toast m-3 border-0 start-50 translate-middle-x fixed-top fade text-white w-50" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div id="alerttoasttext" class="toast-body col-11 text-center"><strong></strong></div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
      <script src="static/fenrir.js"></script>
      <script src="static/bootstrap.min.js"></script>
  </body>
</html>