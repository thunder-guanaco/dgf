$(window).on("load", function() {
    hideAllExceptTop();
    loadFriendsRankings();
});

function hideAllExceptTop() {
    $(".hidden").hide();
    $(".hidden").removeClass("hidden");
}

function loadFriendsRankings(){
    $("#statistics .show-all-less .show-all").each(function() {
        $(this).click(function(){
        paco=$(this);
            $(this).parents(".show-all-less").find(".top").fadeOut();
            $(this).parents(".show-all-less").find(".all").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-less").delay(400).fadeIn();
        });
    });

    $("#statistics .show-all-less .show-less").each(function() {
        $(this).click(function(){
            $(this).parents(".show-all-less").find(".all").fadeOut();
            $(this).parents(".show-all-less").find(".top").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-all").delay(400).fadeIn();
        });
    });
}
