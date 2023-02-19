async function getData(url = '',  data) {
	const response = await fetch(url, {
		method: 'POST',
		mode: 'cors',
		cache: 'no-cache',
		headers: {
			'Content-Type': 'application/json'
		},
		redirect: 'follow',
		referrerPolicy: 'no-referrer',
		body: JSON.stringify(data)
	});
	return response;
}



async function handleIPmappingSubmit()
{
	document.getElementById('mappingsubmit').disabled = true;
	document.getElementById('mappingsubmitspinner').hidden = false;

	var data = {'name': document.getElementById('nameselect').value,
				'ip': document.getElementById('ipselect').value};

	getData('/addmapping', data).then(resp => resp.text()).then(resp => {
		handleResponseToast('mappingModal', resp);
		refreshMapping();
	})

}

async function handleCreatePasswordSubmit()
{
	var data = {'password': document.getElementById('vpnpassword').value,
				'passwordrepeat': document.getElementById('repeatvpnpassword').value};

	getData('/createpassword', data).then(resp => resp.text()).then(resp => {
		handleResponseToast('createpasswordmodal', resp);
	})
}

function unlockVPNProfiles()
{
	getData('/passwordset', {}).then(resp => resp.text()).then(resp => {
		var res = JSON.parse(resp);
		if (!res['error']) {
			if (res['value']) {
				window.location.href = '/settingsauthenticated';
			} else {
				var createpasswordmodal = new bootstrap.Modal(document.getElementById("createpasswordmodal"), {});
				createpasswordmodal.show();
			}
		}
	})
}

function validatepassword()
{
	var password = document.getElementById('vpnpassword');
	var passwordrepeat = document.getElementById('repeatvpnpassword');
	var valid = password.value === passwordrepeat.value
	if (valid) {
		password.classList.remove('is-invalid');
		password.classList.add('is-valid');
		passwordrepeat.classList.remove('is-invalid');
		passwordrepeat.classList.add('is-valid');
	} else {
		password.classList.remove('is-valid');
		password.classList.add('is-invalid');
		passwordrepeat.classList.remove('is-valid');
		passwordrepeat.classList.add('is-invalid');
	}
	return valid
}

function sumbitVPNPassword(){
	//form = document.getElementById("vpnpasswordform");
	if (validatepassword()) {
		handleCreatePasswordSubmit();
	}
}


async function handleVPNConfigSubmit()
{
	document.getElementById('vpnconfigsubmit').disabled = true;
	document.getElementById('vpnconfigsubmitspinner').hidden = false;

	var inputform = document.getElementById('vpnconfigform');
	var inputs = inputform.getElementsByTagName('input');
	
	var data = {};
	var cmd = '/storeconfig';
	for (i = 0; i < inputs.length; i++) {
		if (inputs[i].id == 'vpnconfigismodification') {
			cmd = '/replaceconfig'
		} else if (inputs[i].type == 'checkbox') {
			data[inputs[i].id] = inputs[i].checked
		} else {
			data[inputs[i].id] = inputs[i].value
		}
	}
	config = document.getElementById('vpnconfig')
	data[config.id] =  config.value

	getData(cmd, data).then(resp => resp.text()).then(resp => {
		handleResponseToast('configurationDataModal', resp);
		refreshVPNSettingData();
	})
}

function sumbitVPNConfig(){
	form = document.getElementById("vpnconfigform")
	if (checkformvalidity(form)) {
		handleVPNConfigSubmit();
		//form.dispatchEvent(new CustomEvent('submit', {cancelable: true}));
	}
}

function sumbitMappingConfig(){
	form = document.getElementById("mappingform")
	if (checkformvalidity(form)) {
		handleIPmappingSubmit();
		//form.dispatchEvent(new CustomEvent('submit', {cancelable: true}));
	}
}

async function deleteVPNConfigConfirmed()
{
	data = {profilename: document.getElementById('deletename').innerHTML}
	getData('/deleteconfig', data).then(resp => resp.text()).then(resp => {
		handleResponseToast('deleteModal', resp);
		refreshVPNSettingData();
	})
}

async function deleteMappingConfirmed()
{
	data = {profilename: document.getElementById('deletename').innerHTML}
	getData('/deletemapping', data).then(resp => resp.text()).then(resp => {
		handleResponseToast('deleteModal', resp);
		refreshMapping();
	})
}

function handleResponseToast(modalname, resp)
{
	var myModalEl = document.getElementById(modalname);
	var toasttext = document.getElementById('alerttoasttext');
	var modal = bootstrap.Modal.getInstance(myModalEl)
	modal.hide();
	var res = JSON.parse(resp);
	toasttext.innerHTML = "<strong>" + res['text'] + "</strong>";
	toastelem = document.getElementById("alerttoast")
	if (res['error']) {
		toastelem.classList.remove('bg-success');
		toastelem.classList.remove('bg-danger');
		toastelem.classList.add('bg-danger');
	} else {
		toastelem.classList.remove('bg-success');
		toastelem.classList.remove('bg-danger');
		toastelem.classList.add('bg-success')
	}
	thetoast = bootstrap.Toast.getOrCreateInstance(toastelem)
	thetoast.style
	thetoast.show()
}

function changeState(id)
{
	getData('/changestate', {ip: id, state: 'toggle'}).then(resp => resp.json()).then(resp => {
		var row = document.getElementById('img-' + resp['ip']);
		row.src = 'static/' + resp['state'] + '.png'
	})
}

function deleteConfigModal(event)
{
	var profilename = event.relatedTarget.getAttribute('data-id');
	var data = JSON.parse(profilename);
	document.getElementById('deletename').innerHTML = data['data'];
	document.getElementById('deletetype').innerHTML = data['type'];

	var deletesubmit = document.getElementById('deletemodalconfirm');
	var type = data['type'].slice(0, 'Mapping'.length)
	if (type == 'Mapping') {
		deletesubmit.onclick = deleteMappingConfirmed;
	} else {
		deletesubmit.onclick = deleteVPNConfigConfirmed;
	}
}

function profiletablehasdefault()
{
	doc = document.getElementById('vpnsettingstablebody');
	defaults = doc.getElementsByClassName('isdefault');
	for (u = 0; u < defaults.length; u++) {
		if (defaults[u].innerHTML == 'yes')
			return true;
	}
	return false;
}

function configModal(event)
{
	document.getElementById('vpnconfigsubmit').disabled = false;
	document.getElementById('vpnconfigsubmitspinner').hidden = true;
	var jsondata = event.relatedTarget.getAttribute('data-id');
	var data = JSON.parse(jsondata);
	var name = data ? data['data'] : null;
	var inputform = document.getElementById('vpnconfigform');
	var defaultisset = profiletablehasdefault(inputform);
	inputform.classList.remove("was-validated");
	// adding new configuration
	if (!name) {
		var inputs = inputform.getElementsByTagName('input');
		var textarea = inputform.getElementsByTagName('textarea');
		data = [].concat(Array.from(inputs)).concat(Array.from(textarea));
		for (i = 0; i < data.length; i++) {
			if (data[i].type == 'checkbox') {
				data[i].checked = false
				if (data[i].id == 'isdefault') {
					if (defaultisset) {
						data[i].checked = false;
						data [i].disabled = true;
					} else {
						data[i].checked = true;
						data [i].disabled = false;
					}
					data[i].checked = !defaultisset
				}
			} else {
				data[i].value = ''
			}
		}
		var el = document.getElementById("vpnconfigismodification");
		if (el)
			el.outerHTML = "";
		return;
	}

	// modifying existing configuration
	data = {profilename: name, completeData: true}
	getData('/getvpnconfigurations', data).then(resp => resp.json()).then(resp => {
		for (const [key, value] of Object.entries(resp['profile0'])) {
			theelement = document.getElementById(key)
			if (theelement.type == 'checkbox') {
				if (value) {
					theelement.checked = true;
				} else {
					if (defaultisset && theelement.id == 'isdefault') {
						theelement.disabled = true;
					}
					theelement.checked = false;
				}
			} else {
				theelement.value = value
			}
		}
		var el = document.getElementById("vpnconfigismodification");
		if (!el) {
			var input = document.createElement('input');
			input.setAttribute('type', 'hidden');
			input.setAttribute('id', 'vpnconfigismodification');
			document.getElementById("vpnconfigform").appendChild(input);
		}
	})
}

function refreshMapping()
{
	tablebody = document.getElementById('vpnmappingtablebody')
	tablebody.innerHTML = `<tr id="vpntableloader">
							<td></td><td></td><td>
							<span class="spinner-border align-middle" role="status" aria-hidden="true">
							</td><td></td><td></td>
							</tr>`;
							data = {}
	getData('/getmappings', data).then(resp => resp.json()).then(resp => {
		newtable = '';
		counter = 0
		iplist = []
		for (const [ip, name] of Object.entries(resp)) {
			newtable += '<tr id="profile' + (counter++) + '">'
			newtable += '<td class="col-3 IPAddress">' + ip + '</td>'
			newtable += '<td class="col-3 VPNProfile">' + name + '</td>'
			newtable += `<td class="col-4"></td><td class="cold-2 modify">
				<a class="btn btn-primary" data-bs-toggle="modal" data-id='{"type": "Mapping for", "data": "`
				+ ip + '", "profile": "' + name + `"}' href="#mappingModal" role="button">edit...</a>`
			newtable += `<a class="btn btn-primary mx-xl-2" data-bs-toggle="modal" data-id='{"type": "Mapping for", "data": "` + ip +'", "profile": "' + name
			newtable += `"}' href="#deleteModal" role="button">delete</a></td></tr>`
			iplist.push(ip)
		}
		ipselect = document.getElementById('ipselect')
		for (i = 0; i < ipselect.length; i++) {
			var currentoption = ipselect.options[i]
			if (iplist.includes(currentoption.value))
				currentoption.hidden = true
			else
				currentoption.hidden = false
		}

		tablebody.innerHTML = newtable;
	})
}

function refreshVPNSettingData()
{
	tablebody = document.getElementById('vpnsettingstablebody');
	tablebody.innerHTML = `<tr id="vpntableloader">
							<td></td><td></td><td>
							<span class="spinner-border align-middle" role="status" aria-hidden="true">
							</td><td></td><td></td>
							</tr>`;
	data = {}
	getData('/getvpnconfigurations', data).then(resp => resp.json()).then(resp => {
		newtable = '';
		counter = 0
		for (const [k, config] of Object.entries(resp)) {
			newtable += '<tr id="profile' + (counter++) + '">'
			currentprofilename = ''
			for ([key, value] of Object.entries(config)) {
				if (key == 'profilename') {
					currentprofilename = value;
				}
				colsize = " col-3"
				if (value == true) {
					value = 'yes';
					colsize = " col-2"
				} else if (value == false) {
					value = 'no';
					colsize = " col-2"
				}
				newtable += '<td class="' + key + colsize+ '">' + value + '</td>';
			}
			newtable += `<td class="col-2 modify">
				<a class="btn btn-primary" data-bs-toggle="modal" data-id='{"type": "VPNProfile", "data": "${currentprofilename}"}' href="#configurationDataModal" role="button">edit...</a>
				<a class="btn btn-primary mx-xl-2" data-bs-toggle="modal" data-id='{"type": "VPNProfile", "data": "${currentprofilename}"}' href="#deleteModal" role="button">delete</a>
		 	 	</td></tr>`
		}
		tablebody.innerHTML = newtable;
	})
}

function mappingModal(event)
{
	document.getElementById('mappingform').classList.remove("was-validated")
	document.getElementById('mappingsubmit').disabled = false;
	document.getElementById('mappingsubmitspinner').hidden = true;
	var nameselect = document.getElementById('nameselect')
	var ipselect = document.getElementById('ipselect')
	ipselect.value = ''
	nameselect.value = ''
	ipselect.disabled = false
	var jsondata = event.relatedTarget.getAttribute('data-id');
	var data = JSON.parse(jsondata);
	if (data) {
		ipselect.value = data['data']
		nameselect.value = data['profile']
		ipselect.disabled = true
	}
}

function modalData()
{
	var configurationDataModal = document.getElementById('configurationDataModal')
	configurationDataModal.addEventListener('show.bs.modal', function(event){ configModal(event); })

	var deleteModal = document.getElementById('deleteModal')
	deleteModal.addEventListener('show.bs.modal',  function(event){ deleteConfigModal(event); })

	var deleteModal = document.getElementById('mappingModal')
	deleteModal.addEventListener('show.bs.modal',  function(event){ mappingModal(event); })

}

function checkformvalidity(from)
{
	result = form.checkValidity()
	form.classList.add('was-validated')
	return result
}
