$(window).on("load", function() {

    $("#picture-width").change(function() {
        $("#all-friends").css("width", $(this).val());
        $("#generated-content").css("width", $(this).val());
        $("#generated-content").css("height", $(this).val());
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
        $("#dgf-banner").css("margin-left", `${$(this).val()}px`);
    }).change();


    $("#text-color").change(function() {
        $('#all-friends .text').css('color', $(this).val());
    }).change();

    $("#overlay-color").change(function() {
        var backgroundColor = $(this).val();
        var transparent = "rgba(255, 255, 255, 0)";
        $(".mini-overlay").css("background-image", `linear-gradient(270deg, ${backgroundColor} 33%, ${transparent} 66%)`);
    }).change();

    $(".move-picture input").change(function() {
        username = $(this).parent().parent().data("friend-username");
        $(`#all-friends img[data-friend-username="${username}"]`).css("left", `${$(this).val()}px`);
    }).change();
});