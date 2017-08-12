function initMap() {
  map= new google.maps.Map(document.getElementById('map'), {
    center:{
      lat: 30.8438174820,
      lng: 120.9395376068
    },
    zoom: 9,
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
  map.setOptions({
    draggableCursor: 'url(../static/img/mouse/Normal.cur), crosshair'
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  }

}
function showPosition(position) {
  // console.log('console-> showing position.')
  myLng = position.coords.longitude;
  myLat = position.coords.latitude;
  console.log('console-> position:' + myLat + ',' + myLng);
  catchPosition(myLat, myLng);

  var cPosition = coordtransform.wgs84togcj02(myLng, myLat);
  var cLng = cPosition[0];
  var cLat = cPosition[1];
  console.log('console-> cposition:' + cPosition);

  map.setCenter(new google.maps.LatLng(cLat, cLng));
}
