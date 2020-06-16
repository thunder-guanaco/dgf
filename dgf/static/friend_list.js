$(window).on("load", function() {
    hideAllFromRankingsExceptTop();
    loadFriendsRankings();
});

function hideAllFromRankingsExceptTop() {
    $(".friends-ranking .hidden").hide();
    $(".friends-ranking .hidden").removeClass("hidden");
}

function loadFriendsRankings(){
    $(".friends-ranking .show-all").each(function() {
        $(this).click(function(){
        paco=$(this);
            $(this).parent().parent().find(".top").fadeOut();
            $(this).parent().parent().find(".all").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-less").delay(400).fadeIn();
        });
    });

    $(".friends-ranking .show-less").each(function() {
        $(this).click(function(){
            $(this).parent().parent().find(".all").fadeOut();
            $(this).parent().parent().find(".top").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-all").delay(400).fadeIn();
        });
    });
}