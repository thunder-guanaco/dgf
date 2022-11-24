$(window).on("load", function() {

    $("#friends-per-row").change(function() {
        $("#all-friends").css("width", $(this).val() + "00");
    }).change();

    $("#show-first-logo").change(function() {
        showIfChecked("#first-logo", this);
    }).change();

    $("#show-last-logo").change(function() {
        showIfChecked("#last-logo", this);
    }).change();

    $("#text").change(function() {
        $("#generated-text").text($(this).val());
    }).change();

    $("#text-size").change(function() {
        $('#generated-text').css('font-size', $(this).val() + 'px');
    }).change();

    $("#text-color").change(function() {
        $('#generated-text').css('color', $(this).val());
    }).change();

    $("#overlay-color").change(function() {
        $('#overlay').css('background-color', $(this).val());
    }).change();
});
