var statuRowHeight = document.getElementById('statuRow').offsetHeight;
var quoteHeight = document.getElementById('quote').offsetHeight;
var quoteDivElement = document.getElementById('quoteDiv');
quoteDivElement.style.height = statuRowHeight - quoteHeight - 55 + 'px';
var quoteDivOptiscroll = new Optiscroll(quoteDivElement);

var chartDivHeight = document.getElementById('chartDiv').offsetHeight;
var chartDivElement = document.getElementById('quizChart');
chartDivElement.style.minHeight = chartDivHeight + 'px';

function upDivide(char) {
	var charUp = '';
	for (var i = 0; i < char.length; i++) {
		charUp += '[' + char[i] + ']';
	}
	return charUp;
}
document.getElementById('charDivide').innerHTML = upDivide('{{ user.char_res }}')

function datetimeTransform(dateInt) {
	var quiztime = new Date(dateInt * 1000);
	var qY = quiztime.getFullYear().toString();
	var qM = (quiztime.getMonth() + 1 < 10 ? '0' + (quiztime.getMonth() + 1) : quiztime.getMonth() + 1).toString();
	var qD = (quiztime.getDate() < 10 ? '0' + quiztime.getDate() : quiztime.getDate()).toString();
	var qh = (quiztime.getHours() < 10 ? '0' + quiztime.getHours() : quiztime.getHours()).toString();
	var qm = (quiztime.getMinutes() < 10 ? '0' + quiztime.getMinutes() : quiztime.getMinutes()).toString();
	var qs = (quiztime.getSeconds() < 10 ? '0' + quiztime.getSeconds() : quiztime.getSeconds()).toString();
	var qtime = qY + '-' + qM + '-' + qD + ' ' + qh + ':' + qm + ':' + qs;
	return qtime;
}
