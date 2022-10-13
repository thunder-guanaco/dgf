$.ajax({
    url: "https://discgolffriends.de/static/css/discgolfmetrix.css",
    success: function(response) {
        $("head").append("<style>" + response + "</style>");
    }
});
$(".main-header-meta svg").after("<i class='fi-map'></i> ")
$(".main-header-meta svg").remove()
$(".breadcrumbs").after("<img src='https://discgolffriends.de/media/filer_public_thumbnails/filer_public/94/f6/94f61e02-abbd-426a-8f20-66268590e222/1200x300_series_103.png__1200.0x300.0_subsampling-2.png'></img>")
$(".breadcrumbs").remove();
$(".main-title h1").remove();