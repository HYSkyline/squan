var width = document.body.clientWidth;
var height = document.body.clientHeight;
var radius = 80;

shuffle(userlist);

var imageList = [];
for (var i = 0; i < userlist.length; i++) {
	imageList.push(addImage(userlist[i]));
}

var canvas = document.getElementById('userCanvas');
canvas.width = width;
canvas.height = height;
var ctx = canvas.getContext('2d');

var cnt = 0;
var ri =0;
var hexCenterList = [];
for (i = 0; i < userlist.length; i++) {
	imageList[i].onload = function () {
		cnt++;
		if (cnt === userlist.length) {
			for (i = 0; i < userlist.length; i++) {
				var hexCenter = getCenterPosition(i);
				hexCenterList.push(hexCenter);
				polygon(ctx, hexCenter[0], hexCenter[1], radius, 6, imageList[i]);
			}
		}
	}
}

canvas.addEventListener('click', function(e){
    for (var i = 0; i < hexCenterList.length; i++) {
    	if (Math.abs(e.offsetX - hexCenterList[i][0]) < radius && Math.abs(e.offsetY - hexCenterList[i][1]) < radius) {
    		console.log(userlist[i].userinfo);
    		window.location.href = userlist[i].userinfo;
    	}
    }
});

function getCenterPosition(i) {
	var attenuationRateX = 450;
	var attenuationRateY = 320;
	var radiusX = radius + Math.min(Math.floor(height / attenuationRateX, width / attenuationRateX));
	var radiusY = radius + Math.min(Math.floor(height / attenuationRateY, width / attenuationRateY));
	if (i === 0) {
		return [width / 2, height / 2];
	} else {
		ri += 1;
		ri += parseInt(3 * i / userlist.length < 2 ? 2.4 * i / userlist.length * Math.random(): 2 * Math.random());
		var cn = parseInt((1 + Math.sqrt(1 - 4 / 3 * (1 - ri))) / 2);
		var pn = parseInt((ri - 3 * cn * (cn - 1) - 1) / cn);
		var rn = ri - (3 * cn * (cn - 1) + 1) - pn * cn;
		var x = width / 2 + Math.cos(pn * Math.PI / 3) * radiusX * cn * 1.732 + Math.cos((pn * Math.PI / 3) + 2 * Math.PI / 3) * radiusX * 1.732 * rn;
		var y = height / 2 + Math.sin(pn * Math.PI / 3) * radiusY * cn * 1.732 + Math.sin((pn * Math.PI / 3) + 2 * Math.PI / 3) * radiusY * 1.732 * rn;
		return [x, y];
	}
}

function addImage(user) {
	var userImage = document.createElement('img');
	userImage.setAttribute('id', user.username);
	userImage.setAttribute('src', '../../static/img/avatar/' + userlist[i].avatar + '');
	return userImage;
}

function polygon(ctx, x, y, radius, sides, img) {
	if (sides < 3) return;
	var a = (Math.PI * 2) / sides;
	ctx.save();
	
	ctx.translate(x, y);
	ctx.beginPath();
	ctx.moveTo(0, radius);
	for (var i = 1; i < sides; i++) {
		ctx.lineTo(radius * Math.sin(a * i), radius * Math.cos(a * i));
	}
	ctx.closePath();

	ctx.lineWidth = 2;
	ctx.strokeStyle = 'white';
	ctx.stroke();

	ctx.clip();

	var imageRate = 1;
	ctx.drawImage(img, -radius * imageRate, -radius * imageRate, 2 * imageRate * radius, 2 * imageRate * radius);
	ctx.restore();
}

function shuffle(arr) {
    let i = arr.length;
    while (i) {
        let j = Math.floor(Math.random() * i--);
        [arr[j], arr[i]] = [arr[i], arr[j]];
    }
}