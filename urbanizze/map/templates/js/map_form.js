var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib}),

    x = '{{ x|safe }}',
    y = '{{ y|safe }}',
    zoom_init = '{{zoom_init}}',

    map_center = new L.LatLng(y, x),

    map = new L.Map('map', {center: map_center, zoom: zoom_init}),
    drawnItems = L.featureGroup().addTo(map);

var google_satellite = L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    attribution: 'google'
});

var google_streets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

var dataurl = "{% url 'home:geojson_zonas' %}";
var setorurl = "{% url 'home:geojson_setor' %}";

function getColor(n) {
    switch (n) {
        case 'ZA-3':
            return '#c2e5ef';
            break;
        case 'ZR-1':
			return '#e8eacc';
            break;
        case 'ZT-2':
			return '#c5efc2';
            break;
        default:
            return '#aaa';
    }
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.nome),
        weight: 1,
        opacity: 0.4,
        color: 'white',
        fillOpacity: 0.5
    };
}

var zonas = L.geoJson([], {
    style: style,
    maxZoom: 20
});

var setor = L.geoJson([], {
    style: {
			fillColor: 'orange',
			weight: 3,
			opacity: 0.2,
			color: 'blue',
			fillOpacity: 0.3
		},
    maxZoom: 20
});


// Download GeoJSON via Ajax
$.getJSON(dataurl, function (data) {
    // Add GeoJSON layer
    zonas.addData(data);
});

// Download GeoJSON via Ajax
$.getJSON(setorurl, function (data) {
    // Add GeoJSON layer
    setor.addData(data);
});

var baseLayers = {
    "Google Satellite": google_satellite.addTo(map),
    "Google Roads": google_streets,
    'OSM': osm,
};

var overlays = {
    "geom": drawnItems,
    "Zonas": zonas,
		"Macrozoneamento": setor,
};

L.control.layers(
    baseLayers, overlays
).addTo(map);


map.addControl(new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        poly: {
            allowIntersection: false
        }
    },
    draw: {
        polygon: {
            allowIntersection: false,
            showArea: false,
        },
        polyline: false,
        rectangle: false,
        circle: false,
        circlemarker: false,
        marker: false,
    }
}));

// Truncate value based on number of decimals
var _round = function (num, len) {
    return Math.round(num * (Math.pow(10, len))) / (Math.pow(10, len));
};
// Helper method to format LatLng object (x.xxxxxx, y.yyyyyy)
var strLatLng = function (latlng) {
    return "(" + _round(latlng.lat, 6) + ", " + _round(latlng.lng, 6) + ")";
};

// Generate popup content based on layer type
// - Returns HTML string, or null if unknown object
var getPopupContent = function (layer) {
    // Marker - add lat/long
    if (layer instanceof L.Marker || layer instanceof L.CircleMarker) {
        return strLatLng(layer.getLatLng());
        // Circle - lat/long, radius
    } else if (layer instanceof L.Circle) {
        var center = layer.getLatLng(),
            radius = layer.getRadius();
        return "Center: " + strLatLng(center) + "<br />"
            + "Radius: " + _round(radius, 2) + " m";
        // Rectangle/Polygon - area
    } else if (layer instanceof L.Polygon) {
        var latlngs = layer._defaultShape ? layer._defaultShape() : layer.getLatLngs(),
            area = L.GeometryUtil.geodesicArea(latlngs);
        return "Area: " + L.GeometryUtil.readableArea(area, true);
        // Polyline - distance
    } else if (layer instanceof L.Polyline) {
        var latlngs = layer._defaultShape ? layer._defaultShape() : layer.getLatLngs(),
            distance = 0;
        if (latlngs.length < 2) {
            return "Distance: N/A";
        } else {
            for (var i = 0; i < latlngs.length - 1; i++) {
                distance += latlngs[i].distanceTo(latlngs[i + 1]);
            }
            return "Distance: " + _round(distance, 2) + " m";
        }
    }
    return null;
};

// Object created - bind popup to layer, add to feature group
map.on(L.Draw.Event.CREATED, function (event) {
    var layer = event.layer;
    var point_geojson = (layer.toGeoJSON());
    $("#id_geom").val(JSON.stringify(point_geojson["geometry"]));
    var content = getPopupContent(layer);
    if (content !== null) {
        layer.bindPopup(content);
    }
    drawnItems.addLayer(layer);
});

// Object(s) edited - update popups
map.on(L.Draw.Event.EDITED, function (event) {
    var layers = event.layers,
        content = null;
    layers.eachLayer(function (layer) {
        content = getPopupContent(layer);
        if (content !== null) {
            layer.setPopupContent(content);
        }
    });
});
