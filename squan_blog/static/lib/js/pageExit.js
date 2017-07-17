function page_exit() {
	var containerDiv = document.getElementById('container');
	containerDiv.style.animation = "pageDisappear 1s";
	containerDiv.style.webkitanimation = "pageDisappear 1s";
	containerDiv.style.mozanimation = "pageDisappear 1s";
	containerDiv.style.oanimation = "pageDisappear 1s";
	setTimeout('redirectHome()', 1000);
}
function redirectHome() {
	var containerDiv = document.getElementById('container');
	containerDiv.style.visibility = 'hidden';
	window.location.href='https://github.com/HYSkyline';
}