$(function () {
    $('#quizContainer').fullpage({
        sectionsColor: getBackColor(),
        'navigation': true
    })
});
function getBackColor() {
    var colorList = [];
    var colorCount = {{ quiz|count }};
    var colorDivide = 360 / colorCount;
    for (var i = 0; i < colorCount; i++) {
        var backColor = 'hsl(' + Math.floor(i * colorDivide + Math.random() * (colorDivide + 1) / 2).toString() + ', 15%, 10%)';
        colorList.push(backColor);
    }
    var colorListSort = [];
    for (var i = colorList.length - 1; i >= 0; i--) {
    	var j = Math.floor(Math.random() * colorList.length);
    	colorListSort[i] = colorList[j];
    	colorList.splice(j, 1);
    }
    return colorListSort;
}
function nextView() {
    $.fn.fullpage.moveSectionDown();
}

function checkOption(this) {
    var input = document.getElementById(this.id.slice(0, this.id.length - 1));
    input.value = this.innerHTML;
}