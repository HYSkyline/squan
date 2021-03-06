var map = L.map('map').setView([30.24105142736931, 120.14077259673466], 12);
var streetMap = L.layerGroup([L.tileLayer('http://tile-{s}.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
})]);
var googleMap = L.layerGroup([L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&x={x}&y={y}&z={z}', {
    attribution: 'Map data &copy; 2017 <a href="https://www.google.com/permissions/geoguidelines.html">Google</a>'
})]);
var esriMap = L.layerGroup([L.esri.basemapLayer('Imagery')]);
var mapBase = {
    '街道地图': streetMap,
    '卫星影像': googleMap,
    'ESRI HD': esriMap
};
// map.addLayer(streetMap);
drawnItems = L.featureGroup();
L.control.layers(
	{
        '矢量地图': streetMap,
        '卫星影像': googleMap,
        'ESRI HD': esriMap
    },
    {
    	'绘制图层': drawnItems
    },
    {
    	position: 'topright',
    	collapsed: true
    }
).addTo(map);