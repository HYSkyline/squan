function coordtrans(lng, lat) {
	wgs84lng = lng;
	wgs84lat = lat;
	var wgs84togcj02 = coordtransform.wgs84togcj02(lng, lat);
	gcj02lng = wgs84togcj02[0];
	gcj02lat = wgs84togcj02[1];
	// console.log('经纬坐标:' + wgs84lng + ',' + wgs84lat);
	// console.log('国测坐标:' + gcj02lng + ',' + gcj02lat);
	// console.log('百度坐标:' + bd09lng + ',' + bd09lat);
}