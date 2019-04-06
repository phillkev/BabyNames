function handleClick() {

    // Prevent the form from refreshing the page
    d3.event.preventDefault();

    // Grab the name from the filter
    var name = d3.select("#name").property("value");
    
    // Build the chart with the selected name
    buildChart(name)
}

// Attach an event to listen for the form button
d3.selectAll("#filter-btn").on("click", handleClick);

function buildChart(userSelection) {
    // // Grab json and populate chart
    console.log(userSelection);
    var url = `/linechart/${userSelection}`;
    d3.json(url).then(function (response) {
        if (userSelection) {
            if(isEmpty(userSelection)) {
                // Object is empty (Would return true in this example)
                return "Name not found."
            } else {
                // Object is NOT empty and build chart
                var trace = [{
                    x: response.Year,
                    y: response.total_count,
                    // hovertext: response.total_count,
                    type: "scatter"
                }];
        
                var layout = {
                    title: name,
                    xaxis: { title: 'Year' },
                    yaxis: { title: 'Number of Instances' }
                };
                var chart = document.getElementById('line');
                Plotly.newPlot(chart, trace, layout);
            }
        }  
        
    })
}

function init() {
    // Use sample text to build the initial plot
    const firstName = "michael";
    buildChart(firstName);
}


function optionChanged(newName) {
    // Fetch new data each time a new name is selected
    buildCharts(newName);
}

// Initialize 
init();  