<div id="next-tournaments"></div>
<script>
    $.ajax({
        url: "https://discgolffriends.de/friends/tremonia-series/future-dates",
        success: function(response) {
            $("#next-tournaments").html(response);
        }
    });
</script>
