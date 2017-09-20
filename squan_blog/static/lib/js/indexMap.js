function initMap() {
	gmap = new google.maps.Map(document.getElementById('gmap'), {
		zoom: 15,
		center: {lat: 30.2710905216, lng: 120.1632803679},
		disableDefaultUI: true,
	    styles:[
	      {
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#212121"
	          }
	        ]
	      },
	      {
	        elementType: "labels.icon",
	        stylers: [
	          {
	            visibility: "off"
	          }
	        ]
	      },
	      {
	        elementType: "labels.text",
	        stylers: [
	          {
	            visibility: "off"
	          }
	        ]
	      },
	      {
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#757575"
	          }
	        ]
	      },
	      {
	        elementType: "labels.text.stroke",
	        stylers: [
	          {
	            color: "#212121"
	          }
	        ]
	      },
	      {
	        "featureType": "administrative",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#2a2a2a"
	          }
	        ]
	      },
	      {
	        "featureType": "administrative.country",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#9e9e9e"
	          }
	        ]
	      },
	      {
	        "featureType": "administrative.land_parcel",
	        stylers: [
	          {
	            visibility: "off"
	          }
	        ]
	      },
	      {
	        "featureType": "administrative.locality",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#bdbdbd"
	          }
	        ]
	      },
	      {
	        "featureType": "poi",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#757575"
	          }
	        ]
	      },
	      {
	        "featureType": "poi.park",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#181818"
	          }
	        ]
	      },
	      {
	        "featureType": "poi.park",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#616161"
	          }
	        ]
	      },
	      {
	        "featureType": "poi.park",
	        elementType: "labels.text.stroke",
	        stylers: [
	          {
	            color: "#1b1b1b"
	          }
	        ]
	      },
	      {
	        "featureType": "road",
	        elementType: "geometry.fill",
	        stylers: [
	          {
	            color: "#2c2c2c"
	          }
	        ]
	      },
	      {
	        "featureType": "road",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#8a8a8a"
	          }
	        ]
	      },
	      {
	        "featureType": "road.arterial",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#373737"
	          }
	        ]
	      },
	      {
	        "featureType": "road.highway",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#3c3c3c"
	          }
	        ]
	      },
	      {
	        "featureType": "road.highway.controlled_access",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#4e4e4e"
	          }
	        ]
	      },
	      {
	        "featureType": "road.local",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#616161"
	          },
	          {
	            visibility: "off"
	          }
	        ]
	      },
	      {
	        "featureType": "transit",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#757575"
	          }
	        ]
	      },
	      {
	        "featureType": "water",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#000000"
	          }
	        ]
	      },
	      {
	        "featureType": "transit.line",
	        elementType: "geometry",
	        stylers: [
	          {
	            color: "#505050"
	          }
	        ]
	      },
	      {
	        "featureType": "water",
	        elementType: "labels.text.fill",
	        stylers: [
	          {
	            color: "#3d3d3d"
	          }
	        ]
	      }
	    ]
	});
	gmap.setOptions({
    	draggableCursor: 'url(../static/img/mouse/Normal.cur), crosshair'
	});
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
function showPosition(position) {
	coordtrans(position.coords.longitude, position.coords.latitude);
	var gpoint = new google.maps.LatLng(gcj02lat, gcj02lng);
	gmap.panTo(gpoint);
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

