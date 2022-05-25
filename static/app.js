function makeMap() {
    var tianditu_vec = L.tileLayer.chinaProvider("TianDiTu.Normal.Map", {
        maxZoom: 18,
        minZoom: 1
    });
    var tianditu_cva = L.tileLayer.chinaProvider("TianDiTu.Normal.Annotion", {
        maxZoom: 18,
        minZoom: 1
    });
    var tianditu = L.layerGroup([tianditu_vec, tianditu_cva])
    var osm = L.tileLayer.chinaProvider("OSM.Normal.Map", {
        maxZoom: 18,
        minZoom: 1
    });

    // judge the map loaded first
    var lang = navigator.language;
    console.log("language is " + lang);
    var zhs = ["zh-cn", "zh-tw", "zh-hk", "zh-om", "zh-cht", "zh-chs"];
    if (zhs.indexOf(lang.toLowerCase()) > -1) {
        default_map = tianditu;
        default_name = "天地图"
        other_map = osm;
        other_name = "开放街道地图"
    }
    else {
        default_map = osm;
        default_name = "OpenStreetMap"
        other_map = tianditu;
        other_name = "TianDiTu"
    }

    // display maps
    base_map = L.map("mapDiv", {
        center: [34.3227, 108.5525],
        zoom: 4,
        layers: default_map,
        zoomControl: false
    });
    L.control.layers({
        [default_name]: default_map,
        [other_name]: other_map
    }).addTo(base_map);
    L.control.zoom({
        zoomInTitle: "Zoom in",
        zoomOutTitle: "Zoom out"
    }).addTo(base_map);
}

var point_layer = L.layerGroup();
var line_layer = L.layerGroup();

function renderData(dayid) {
    var lines = [];
    $.getJSON("/day/" + dayid, function(obj) {
        var markers = obj.data.map(function(arr) {
            lines.push([arr[0], arr[1]]);
            return L.marker([arr[0], arr[1]]).bindPopup(arr[2]);
        });
        base_map.removeLayer(point_layer);
        base_map.removeLayer(line_layer);
        point_layer = L.layerGroup(markers);
        line_layer = L.polyline(lines, {color: "red"});
        base_map.addLayer(point_layer);
        base_map.addLayer(line_layer);
    });
}

$(function() {
    makeMap();
    renderData("0");
    $("#daysel").change(function() {
        var val = $("#daysel option:selected").val();
        renderData(val);
    });
})
