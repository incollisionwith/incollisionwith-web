(function() {
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 19, attribution: osmAttrib});

    var mapElems = document.getElementsByClassName('map');
    for (var i=0; i < mapElems.length; i++) {
        var mapElem = mapElems.item(i);
        var latLng = new L.LatLng(mapElem.dataset.lat, mapElem.dataset.lon);
        map = L.map(mapElem);
        map.setView(latLng, 14);
        map.addLayer(osm);
        var marker = L.marker(latLng).addTo(map);
    }
})();