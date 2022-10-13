// CSS
$.ajax({
    url: "https://discgolffriends.de/static/css/discgolfmetrix.css",
    success: function(response) {
        $("head").append("<style>" + response + "</style>");
    }
});

// icons
$(".main-header-meta svg").after("<i class='fi-map'></i> ");
$(".main-header-meta svg").remove();

// top part: banner, breadcrumb, title
var tsNumber = $("#competition-submenu .selected b").text().split(' ').pop();
tsNumber = tsNumber[0] === "#" ? tsNumber : "";
if (typeof image !== "undefined") {
    $(".breadcrumbs").after("<div class='discgolffriends-banner desktop'><img src='" + image + "'></img><span>" + tsNumber + "</span></div>");
    $("#content").before("<img class='discgolffriends-banner mobile' src='" + image + "'></img>");
}
$(".breadcrumbs").hide();
//$(".main-header .main-title h1").hide();

