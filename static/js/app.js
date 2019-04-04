function init() {

    d3.json(`/cloudchartdata`).then((word) => {
        // Use d3 to select the panel 
        d3.select("#word_cloud");
        const babynames = word.Name;
        const babycount = word.total_count;

        // build word cloud 
        var words = [babynames]
            .map(function (d) {
                return { text: d, size: babycount };
            });

        d3.wordcloud()
            .size([800, 400])
            .selector('#word_cloud')
            .words(words)
            .start();

    })

    .catch((e) => {return console.log(e)})

}

// Initialize 
init();
