var amap = new AMap.Map('amap', {
    resizeEnable: true,
    zoom: 14,
    center: [120.1632803679, 30.2710905216],
	mapStyle: 'amap://styles/63914602e989a8dd823bf3c843baccea'
});
amap.setMapStyle('amap://styles/grey');
amap.setFeatures('bg,road,building');

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
function showPosition(position) {
	coordtrans(position.coords.longitude, position.coords.latitude);
	var apoint = new AMap.LngLat(gcj02lng, gcj02lat);
	amap.panTo(apoint);
	positionCursor = document.createElement('div');
	positionCursor.setAttribute('id', 'currentPosition');
	container = document.getElementById('container');
	container.appendChild(positionCursor);
}
function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    }
}

