<script>
    $.ajax({
        url: "https://discgolffriends.de/static/js/discgolfmetrix.js",
        success: function(response) {
            $("body").append("<script>" + response); // yes, the ending "script" tag is missing
        }
    });
</script>