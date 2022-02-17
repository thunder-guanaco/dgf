/**
 * Yes, the content of this file is EXACTLY like the content of show_all_less.js
 * EXCEPT for the fact that all the classes here are called ...-tournaments
 */

$(window).on("load", function() {
    hideAllExceptTopTournaments();
    loadShowAllLessTournaments();
});

function hideAllExceptTopTournaments() {
    $(".show-all-less-tournaments .hidden").hide();
    $(".show-all-less-tournaments .hidden").removeClass("hidden");
}

function loadShowAllLessTournaments(){

    $("#statistics .show-all-less-tournaments .show-all-tournaments").each(function() {
        $(this).click(function(){
            $(this).parents(".show-all-less-tournaments").find(".top-tournaments").fadeOut();
            $(this).parents(".show-all-less-tournaments").find(".all-tournaments").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-less-tournaments").delay(400).fadeIn();
        });
    });

    $("#statistics .show-all-less-tournaments .show-less-tournaments").each(function() {
        $(this).click(function(){
            $(this).parents(".show-all-less-tournaments").find(".all-tournaments").fadeOut();
            $(this).parents(".show-all-less-tournaments").find(".top-tournaments").delay(400).fadeIn();
            $(this).fadeOut();
            $(this).parent().find(".show-all-tournaments").delay(400).fadeIn();
        });
    });
}
