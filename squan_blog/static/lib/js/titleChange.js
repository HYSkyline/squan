var visibilityChange;
if (typeof document.hidden !== "undefined") {
	visibilityChange = "visibilitychange";
} else if (typeof document.mozHidden !== "undefined") {
	visibilityChange = "movisibilitychange";
} else if (typeof document.msHidden !== "undefined") {
	visibilityChange = "msvisibilitychange";
} else if (typeof document.webkitHidden !== "undefined") {
	visibilityChange = "webkitvisibilitychange";
}
document.addEventListener(visibilityChange, function() {
	if (document.hidden) {
		document.title = '双犬·平闇';
	} else {
		document.title = '双犬·持灯';
	}
}, false);