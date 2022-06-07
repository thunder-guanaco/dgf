$(window).on("load", function() {

    // remove "No" (Number) from every table
    $("th:contains('No')").text("");

    // remove Disc Golf Metrix icons
    $("svg").hide();

    if (showOnlyFriends) {
        hideNonFriends();
    }

    if (tableType == 'S') {
        hideHoleResults();
    }

    // remove Disc Golf Metrix links
    //$("#tournament-results a").removeAttr("href");

});

function hideNonFriends() {
    $("td.player-cell").each(function(){
        href = $(this).children("a.profile-link").attr("href");
        if (href == undefined) {
            console.log("hiding " + $(this).text() + " - without metrix ID (not a Friend for sure)");
            $(this).parent().hide();
        }
        else {
            metrixId = href.split("/")[2];
            if (!metrixUserIds.includes(metrixId)) {
                console.log("hiding " + $(this).text() + " because the metrix ID indicates that they are not a Friend");
                $(this).parent().hide();
            }
        }
    });
}

function hideHoleResults() {
    $(".table-wrapper th").hide()
    $(".table-wrapper td").hide()

    $(".table-wrapper th:nth-child(1)").show()
    $(".table-wrapper td:nth-child(1)").show()
    $(".table-wrapper th:nth-child(2)").show()
    $(".table-wrapper td:nth-child(2)").show()
    $(".table-wrapper th:last-child").show()
    $(".table-wrapper td:last-child").show()
}