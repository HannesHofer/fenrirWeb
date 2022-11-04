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

function changeState(id)
{
	getData("/changestate", {ip: id, state: 'toggle'}).then(resp => resp.json()).then(resp => {
		var row = document.getElementById('img-' + resp['ip']);
		row.src = 'static/' + resp['state'] + '.png'
	})
}

function replaceHREFS() 
{
	items = document.getElementsByClassName('list-group-item')
	Array.from(items).forEach((element) => {
		element.href = 'javascript:void(0);'
	});
}

async function sendConfig(data, ) {
	data = {vpnconfig: document.getElementById("vpnconfig").value,
	        vpnauth: document.getElementById("vpnauth").value}
	getData("/storeconfig", data).then(resp => resp.text()).then(resp => {
		document.getElementById("header").innerHTML += resp
	})
}
