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
const tsNumber = $("#competition-submenu .selected b").text().split(' ').pop();
const bannerText = tsNumber[0] === "#" ? tsNumber : "";
const bannerDiv = "<div class='discgolffriends-banner'><img src='" + image + "'></img><span>" + bannerText + "</span></div>";
if (typeof image !== "undefined") {
    $(".breadcrumbs").after("<div class='desktop'>" + bannerDiv + "</div>");
    $("#content").before("<div class='mobile'>" + bannerDiv + "</div>");
}
$(".breadcrumbs").hide();
//$(".main-header .main-title h1").hide();

