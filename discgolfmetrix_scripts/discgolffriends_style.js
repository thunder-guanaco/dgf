<script>
    // only needed if you only want to show future subcompetitions (not all) like in Tremonia Series
    showOnlyFutureSubcompetitions = false;

    // only needed if you want to have a banner
    image = "https://discgolffriends.de/media/filer_public_thumbnails/filer_public/94/f6/94f61e02-abbd-426a-8f20-66268590e222/1200x300_series_103.png__1200.0x300.0_subsampling-2.png"

    $.ajax({
        url: "https://discgolffriends.de/static/js/discgolfmetrix.js",
        success: function(response) {
            $("body").append("<script>" + response); // yes, the ending "script" tag is missing
        }
    });
</script>