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
	return response.json();
}

function changeState(id)
{
	getData("/changestate", {ip: id, state: 'toggle'}).then(resp => {
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
