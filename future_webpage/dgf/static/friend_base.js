$(window).on("load", function() {
    $(".youtube-video").each(function(index) {

        var video = $(this);
        var youtube_id = video.attr("youtubeid");

        img = new Image();
        img.src = "http://img.youtube.com/vi/" + youtube_id + "/mqdefault.jpg";
        img.onload = function () {
            // if the video does not exist(therefore thumbnail don't exist)
            // a default thumbnail of 120 width is returned.
            if (this.width === 120) {
                console.log("Youtube ID " + youtube_id + " is not valid!");
                video.remove();
            }
            else {
                this.width = 192;
                this.height = 108;
                video.append(this)
                video.grtyoutube({
                    autoPlay:true,
                    theme: "dark"
                });
            }
        };
    });
    var count = 0;
    $(".youtube-video").each(function(index) {
        $(this).delay(count*50).show("slow");
        count = count + 1;
    });
});
