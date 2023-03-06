$(window).on("load", function() {
    checkClickableFriends();

    // TODO: DELETE THIS!!!!!
    showPage('#metrix-bag-tags');

});

function checkClickableFriends() {

    if (disableClickOnFriends) {
        $("#bag-tags .friend-ball").each(function() {
            $(this).attr("old-href", $(this).attr("href"));
            $(this).removeAttr("href");
        });

        $("#bag-tags .friend-ball .tooltip-text").css("display", "none");
    }
}

function showPage(selector) {
    $("#bag-tags .page").hide();
    $(selector).show();
    $("#bag-tags .page .error").hide();
    scrollUp();
}


function scrollUp() {
    window.scrollTo(0, 0);
    window.scrollTo(0, 0);
    window.scrollTo(0, 0);
}