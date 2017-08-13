function success(position) {
  alert("position: " + position.coords.latitude + ', ' + position.coords.longitude);
}

function error(msg) {
  alert('position error');
}

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(success, error);
} else {
  error('not supported');
}