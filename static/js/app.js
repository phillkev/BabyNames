function init() {
    
    d3.json(`/`).then((wordcloud) => {
        // Use d3 to select the panel 
        d3.select("#word_cloud");
            const babynames = wordcloud.Name;
            const babycount = wordcloud.total_count;
    
            // build word cloud 
            var Canvas = require("canvas");
        
            var cloud = require("../");
        
            var words = [babynames]
            .map(function(d) {
            return {text: d, size: babycount};
            });
        
            cloud().size([960, 500])
                .canvas(function() { return new Canvas(1, 1); })
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", end)
                .start();
        
            // function end(words) { console.log(JSON.stringify(words)); } 
        
    
    });
}

// Initialize 
init();
