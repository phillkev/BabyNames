// Creating map object
var myMap = L.map("map", {
  center: [37.8283, -98.5795],
  zoom: 5
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
}).addTo(myMap);

var geojsonLayer;

var geojsonLayer = new L.GeoJSON.AJAX("states_with_names2.geojson")//.on('data:loaded', function () {
//  myMap.fitBounds(geojsonLayer.getBounds());
//}); 
geojsonLayer.addTo(myMap);


//function buildCharts(sample) {

  // d3.json to fetch the data for the plots
//  d3.json("/chorodata").then(function(smplData){
//    smplData = smplData.sort(function(a, b) {
//      return b.sample_values - a.sample_values;
//    });
 
  // @TODO: Build a choropleth using the birth data
  // create arrays for the choropleth
 
//    var birthValues = smplData.map(sample => sample.sample_values);
//    var bithYear = smplData.map(sample => sample.sample_values + 20);
//    var birthState = smplData.map(sample => sample.otu_id );
//    var birthGender = smplData.map(sample => sample.otu_label );
//    var birthCount = smplData.map(sample => sample.otu_label );
//  });

//};

// Grab data with d3
d3.json("/chlorodata", function(Data) {
  
  // create vars
  var birthState = Data.map(sample => sample.otu_id );
  var birthGender = Data.map(sample => sample.otu_label );
  var birthCount = Data.map(sample => sample.otu_label );
  
  // Create a new choropleth layer
  geojson = L.choropleth(data, {

    // Define what  property in the features to use
    valueProperty: "MHI",

    // Set color scale
    scale: ["#fafa6e", "#2A4858"],

    // Number of breaks in step range
    steps: 7,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
    // Border color
      color: "#fff",
      weight: 0.5,
      fillOpacity: 0.8
    },

    // Binding a pop-up to each layer
    onEachFeature: function(feature, layer) {
      layer.bindPopup(feature.properties.LOCALNAME + ", " + feature.properties.State + "<br>Median Household Income:<br>" +
        "$" + feature.properties.MHI);
    }
  }).addTo(myMap);

  // Set up the legend
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h1>Median Income</h1>" +
      "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
      "</div>";

    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
      labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
  };

  // Adding legend to the map
  legend.addTo(myMap);

});
