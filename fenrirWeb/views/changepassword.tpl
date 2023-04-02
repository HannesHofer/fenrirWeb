<div class="modal fade" id="changepasswordmodal" tabindex="-1" aria-labelledby="changepasswordmodalLabel" aria-hidden="true">
    <div class="modal-dialog modal-md">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" >Change Password for VPN Profiles</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="container">
            <form class="needs-validation" id="chvpnpasswordform" onsubmit="handleChangePasswordSubmit();" novalidate>
              <div class="col-12 mb-3 form-floating has-validation">
                <input type="password" class="form-control" id="chcurrentpassword" placeholder="current Password">
                <label for="currentpassword" class="form-label mx-2">Enter current VPNProfiles password</label>
                <div class="invalid-feedback">Passwords do not match</div>
              </div>

              <div class="col-12 mb-3 form-floating has-validation">
                <input type="password" class="form-control" id="chvpnpassword" placeholder="new Password" onkeyup="validatepassword();">
                <label for="vpnpassword" class="form-label mx-2">Enter new VPNProfiles password</label>
                <div class="invalid-feedback">Passwords do not match</div>
              </div>
              <div class="col-12 mb-3 form-floating has-validation">
                <input type="password" class="form-control" id="chrepeatvpnpassword" placeholder="new Password" onkeyup="validatepassword();">
                <label for="repeatvpnpassword" class="form-label mx-2">Repeat new VPNProfiles password</label>
                <div class="invalid-feedback">Passwords do not match</div>
              </div>
              <div class="col-12 mt-3 form-floating">
                <div class="form-check col-12 m-2 form-switch">
                    <input class="form-check-input" style="transform: scale(1.3);" type="checkbox" role="switch" id="chisencryptionpassword">
                    <label class="form-check-label" for="isencryptionpassword">Use password for VPNProfile encryption</label>
                </div>
              </div>
            </form>
            <div class="mt-5 mx-2 col-12 fs-6">
              <p class="fw-bolder ">Note:</p>
              <p>Password must be enterd in order to modify, delete and add VPNConfigurations.
                  This is done to ensure that sensitive data is not shown without authentication.<br><br>
                  When password is used for VPNProfile encryption password must be enterd in order for VPNConnection(s) to work.</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-success" onclick="sumbitVPNPassword(true);">Sumbit</button>
        </div>
      </div>
    </div>
  </div>