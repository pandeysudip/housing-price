//function for dropdown menu and initial graphs 
function init() {
    d3.json('/data/predict').then((data) => {
        //select the dropdown.
        var menu = d3.select("#selDataset");

        //states.filter(onlyUnique)
        var cities = []
        for (let i = 0; i < data.length; i++) {
            c = data[i].City
            cities.push(c);
        }
        var uniqueCity = cities
        uniqueCity.forEach((city) => {
            menu.append("option").text(city).property("value", city);
        });
        //creating function for initial plots 
        var initSample = uniqueCity[1]
        createMap(initSample);
    })
};

function createMap() {
    //removing map if already exist
    var container = L.DomUtil.get('map');
    if (container != null) {
        container._leaflet_id = null;
    }

    // Define a markerSize() function that will give each city a different radius based on its population.
    function markerSize(value) {
        return Math.sqrt(value) * 20;
    }

    d3.json('/data/predict').then((data) => {
        var cMarkers = []
        for (var i = 0; i < data.length; i++) {
            var d = data[i]
            console.log(d);


            console.log(d.Lat);
            console.log(d.Commodity)

            // Setting the marker 
            cMarkers.push(
                L.circle([d.Lat, d.Lng], {
                    color: "blue",
                    fillColor: "green",
                    fillOpacity: 0.75,
                    radius: markerSize(d.RandomForestPredictedHouseValue)

                }).bindPopup(`<h1>${d.City}</h1>  <hr> <h3>Predicted House value:$ ${d.RandomForestPredictedHouseValue.toLocaleString()}</h3>`)
            )


        }
        var citydata = L.layerGroup(cMarkers);

        // Create the tile layer that will be the background of our map.
        var streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });
        // water color 
        var watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            subdomains: 'abcd',
            minZoom: 1,
            maxZoom: 16,
            ext: 'jpg'
        });

        // dark map 
        var dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        });

        // google street 
        googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        });

        //google satellite
        googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        });

        // Create a baseMaps object to hold the streetmap layer.
        var baseMaps = {
            "Street Map": streetmap,
            "Water Color": watercolor,
            "Dark": dark,
            "Google Street": googleStreets,
            "Google Sat": googleSat
        };

        // Create an overlay object to hold our overlay.
        var overlayMaps = {
            City: citydata
        };

        // Create our map, giving it the streetmap and earthquakes layers to display on load.
        var myMap = L.map("map", {
            center: [
                37.09, -95.71
            ],
            zoom: 5,
            layers: [googleStreets, citydata]
        });

        // Add the layer control to the map.
        L.control.layers(baseMaps, overlayMaps, {
            collapsed: false
        }).addTo(myMap);

    })

};


function optionChanged(newSample) {
    createMap(newSample);
};

init();