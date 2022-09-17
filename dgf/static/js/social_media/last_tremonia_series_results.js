$(window).on("load", function() {

    // remove "No" (Number) from every table
    $("th:contains('No')").text("");

    // remove Disc Golf Metrix icons
    $("svg").hide();

    // remove Disc Golf Metrix links
    $(".last-tremonia-series-results-wrapper a").removeAttr("href");

});
