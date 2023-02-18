<div class="container">
    <form class="needs-validation" id="vpnconfigform" onsubmit="handleVPNConfigSubmit();" novalidate>
        <div class="row">
            <div class="col-12 mb-3 form-floating has-validation">
                <input type="text" class="form-control" id="profilename" placeholder="Profile Name" required>
                <label for="profileName" class="form-label mx-2">Profilename</label>
                <div class="invalid-feedback">Please choose a Profilename.</div>
            </div>
            <div class="col-12 mb-3 form-floating">
                <input type="text" class="form-control" id="description" placeholder="Description">
                <label for="description" class="form-label mx-2">Description</label>
            </div>
            <div class="col-12 mb-3 form-floating has-validation">
                <textarea class="form-control" id="vpnconfig" rows="5" placeholder="ConfigText" style="min-height: 12rem;" required></textarea>
                <label for="vpnconfig" class="form-label mx-2">OpenVPN Config Data</label>
                <div class="invalid-feedback">Please add a OpenVPN Configuration Data.</div>
            </div>
            <div class="col-6 mb-3 form-floating">
                <input type="text" class="form-control" id="username" placeholder="Username">
                <label for="userNameInput" class="form-label mx-2">VPN username</label>
            </div>
            <div class="col-6 mb-3 form-floating">
                <input type="password" class="form-control" id="password" placeholder="Password">
                <label for="passwordInput" class="form-label mx-2">VPN Password</label>
            </div>
        </div>
        <div class="row">
            <div class="form-check col-12 m-3 form-switch">
                <input class="form-check-input" style="transform: scale(1.3);" type="checkbox" role="switch"  id="isdefault" checked>
                <label class="form-check-label mx-2" for="isdefault">Default profile</label>
              </div>
        </div>
        <div class="row">
            <div class="form-check col-12 m-3 form-switch">
                <input class="form-check-input" style="transform: scale(1.3);" type="checkbox" role="switch" value="" id="ondemand">
                <label class="form-check-label mx-2" for="ondemand">On demand connection</label>
              </div>
        </div>
        <input type="text" class="form-control" id="vpnprofileid" hidden>
    </form>
</div>
