<script>
    // only needed if you only want to show future subcompetitions (not all) like in Tremonia Series
    showOnlyFutureSubcompetitions = false;

    $.ajax({
        url: "https://discgolffriends.de/static/js/discgolfmetrix.js",
        success: function(response) {
            $("body").append("<script>" + response); // yes, the ending "script" tag is missing
        }
    });
</script>