<div class="container">
    <form class="form needs-validation" id="mappingform" onsubmit="handleIPmappingSubmit();" novalidate>
        <div class="mb-3 form-floating row">
            <div class="row mx-3">
               <label class="form-label">IPAddress for mapping</label>
            </div>
            <div class="mx-3 row col-11 has-validation">
                <select class="form-select form-control-lg fs-5" id="ipselect" required>
                    <option disabled selected value=""> -- select an IP -- </option>
                {% for row in devices %}
                    {%- set htype="" -%} {%- if row['IP'] in vpnmappinconfig -%}{%- set htype="hidden "-%} {%- endif -%}
                    <option {{htype}}value="{{row['IP']}}">{{row['IP']}}</option>S
                {% endfor %}
                </select>
                <div class="invalid-feedback">Please choose a IPAddress.</div>
            </div>
        </div>
        <div class="mt-4 form-floating row">
            <div class="row mx-3">
               <label class="form-label">VPNProfile for mapping</label>
            </div>
            <div class="mx-3 row col-11 has-validation">
                <select class="form-select form-control-lg fs-5" id="nameselect" required>
                    <option disabled selected value=""> -- select VPNProfile -- </option>
                {% for key, config in vpnconfigs.items() %}
                    <option value="{{config['profilename']}}">{{config['profilename']}}</option>
                {% endfor %}
                </select>
                <div class="invalid-feedback">Please choose a Profilename.</div>
            </div>
        </div>
    </form>
</div>