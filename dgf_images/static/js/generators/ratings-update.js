$(window).on("load", function() {

    $("#friends-per-row").change(function() {
        $("#all-friends").css("grid-template-columns", `repeat(${$(this).val()}, 1fr)`);
    }).change();

    $("#show-first-logo").change(function() {
        showIfChecked("#first-logo", this);
    }).change();

    $("#show-last-logo").change(function() {
        showIfChecked("#last-logo", this);
    }).change();

    $("#show-banner").change(function() {
        showIfChecked("#dgf-banner", this);
    }).change();

    $("#move-banner").change(function() {
        $("#dgf-banner img").css("margin-left", `${$(this).val()}px`);
    }).change();


    $("#text-color").change(function() {
        $('#all-friends .text').css('color', $(this).val());
    }).change();

    $("#overlay-color").change(function() {
        var backgroundColor = $(this).val();
        var transparent = `${backgroundColor}00`;
        $(".mini-overlay").css("background-image", `linear-gradient(270deg, ${backgroundColor} 33%, ${transparent} 66%)`);
        $(".dgf-logo").css("background-color", backgroundColor);
    }).change();

    $(".move-picture input").change(function() {
        username = $(this).parent().parent().data("friend-username");
        $(`#all-friends img[data-friend-username="${username}"]`).css("left", `${$(this).val()}px`);
    }).change();
});