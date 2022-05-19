var tianditu_vec = L.tileLayer.chinaProvider('TianDiTu.Normal.Map', {
    maxZoom: 18,
    minZoom: 1
});
var tianditu_cva = L.tileLayer.chinaProvider('TianDiTu.Normal.Annotion', {
    maxZoom: 18,
    minZoom: 1
});
var tianditu = L.layerGroup([tianditu_vec, tianditu_cva])
var osm = L.tileLayer.chinaProvider('OSM.Normal.Map', {
    maxZoom: 18,
    minZoom: 1
});

// judge the map loaded first
var lang = navigator.language;
console.log("language is " + lang);
var zhs = ["zh-cn", "zh-tw", "zh-hk", "zh-om", "zh-cht", "zh-chs"];
if (zhs.indexOf(lang.toLowerCase()) > -1) {
    default_map = tianditu;
    default_name = "TianDiTu(default)"
    other_map = osm;
    other_name = "OSM"
}
else {
    default_map = osm;
    default_name = "OSM(default)"
    other_map = tianditu;
    other_name = "TianDiTu"
}

// display maps
var map = L.map("mapDiv", {
    center: [34.3227, 108.5525],
    zoom: 4,
    layers: default_map,
    zoomControl: false
});
L.control.layers({
    [default_name]: default_map,
    [other_name]: other_map
}).addTo(map);
L.control.zoom({
    zoomInTitle: 'Zoom in',
    zoomOutTitle: 'Zoom out'
}).addTo(map);

// add test
L.marker([41, 123]).addTo(map)
        .bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();
// add a polygon
L.polygon([
        [41, 123],
        [39, 121],
        [41, 126]
]).addTo(map).bindPopup("I am a polygon.");
// add a event about create popup
var popup = L.popup();
function onMapClick(e) {
        popup
            .setLatLng(e.latlng)
            .setContent("You clicked the map at " + e.latlng.toString())
            .openOn(map);
}
map.on('click', onMapClick);
