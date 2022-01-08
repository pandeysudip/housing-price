//function for dropdown menu and initial graphs 
function init() {
    d3.json('/data/predict').then((data) => {
        //select the dropdown.
        var menu = d3.select("#selDataset");
        console.log(data)

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
        var initSample = uniqueCity[1002]
        createMap(initSample);
    })
};

function createMap(city) {
    //removing map if already exist
    var container = L.DomUtil.get('map1');
    if (container != null) {
        container._leaflet_id = null;
    }

    // Create a map object.
    var myMap = L.map("map1", {
        center: [37.09, -95.71],
        zoom: 4
    });
    // Define a markerSize() function that will give each city a different radius based on its population.
    function markerSize(value) {
        return Math.sqrt(value) * 200;
    }

    // Add a tile layer.
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(myMap);

    d3.json('/data/predict').then((data) => {
        console.log(data)

        for (var i = 0; i < data.length; i++) {
            var d = data[i]
            console.log(d)
            //console.log(d);

            if (d.City == city) {

                // Setting the marker 
                L.circle([d.Lat, d.Lng], {
                    color: "blue",
                    fillColor: "black",
                    fillOpacity: 0.75,
                    radius: markerSize(d.RandomForestPredictedHouseValue)

                }).bindPopup(`<h1>${d.City}</h1>  <hr> <h3>Predicted House Value:$ ${d.RandomForestPredictedHouseValue.toLocaleString()}</h3>`)
                    .addTo(myMap);
            }

        }
    });

}


function optionChanged(newSample) {
    createMap(newSample);
    graphs(newSample)
};
init();