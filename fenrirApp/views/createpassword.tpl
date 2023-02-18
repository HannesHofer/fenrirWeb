<div class="modal fade" id="createpasswordmodal" tabindex="-1" aria-labelledby="createpasswordmodalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" >Create Password for VPN Profiles</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="container">
            <form class="needs-validation" id="vpnpasswordform" onsubmit="handleCreatePasswordSubmit();" novalidate>
              <div class="col-12 mb-3 form-floating has-validation">
                <input type="password" class="form-control" id="vpnpassword" placeholder="Password" onkeyup="validatepassword();">
                <label for="vpnpassword" class="form-label mx-2">Enter new VPNProfiles password</label>
                <div class="invalid-feedback">Passwords do not match</div>
              </div>
              <div class="col-12 mb-3 form-floating has-validation">
                <input type="password" class="form-control" id="repeatvpnpassword" placeholder="Password" onkeyup="validatepassword();">
                <label for="repeatvpnpassword" class="form-label mx-2">Repeat VPNProfiles password</label>
                <div class="invalid-feedback">Passwords do not match</div>
              </div>
            </form>
          <p class="mt-3 fw-bolder row offset-1 fs-6">Note:</p>
          <p class="row col-10 offset-1 fs-6">Password must be enterd in order to modify, delete and add VPNConfigurations.<br>
                                 This is done to ensure that sensitive data is not shown without authentication.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-success" onclick="sumbitVPNPassword();">Sumbit</button>
        </div>
      </div>
    </div>
  </div>