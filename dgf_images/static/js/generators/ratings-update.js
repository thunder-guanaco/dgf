$(window).on("load", function() {

    $("#picture-width").change(function() {
        $("#all-friends").css("width", $(this).val());
    }).change();

    $("#show-first-logo").change(function() {
        showIfChecked("#first-logo", this);
    }).change();

    $("#show-last-logo").change(function() {
        showIfChecked("#last-logo", this);
    }).change();

    $("#text-color").change(function() {
        $('#generated-text').css('color', $(this).val());
    }).change();

    $("#overlay-color").change(function() {
        $('#overlay').css('background-color', $(this).val());
    }).change();
});
