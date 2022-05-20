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

function renderData(districtid) {
    $.getJSON("/district/" + districtid, function(obj) {
        console.log("markers is " + markers);
        var markers = obj.data.map(function(arr) {
            console.log("arr is " + arr);
            return L.marker([arr[0], arr[1]]).bindPopup(arr[2]);
        });
        point_layer = L.layerGroup(markers);
        base_map.addLayer(point_layer);
    });
}

makeMap();
renderData("0");
