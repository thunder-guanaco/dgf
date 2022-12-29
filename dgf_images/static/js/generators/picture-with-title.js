$(window).on("load", function() {

    $("#text").change(function() {
        $("#generated-text").text($(this).val());
    }).change();

    $("#text-color").change(function() {
        $('#generated-content').css('color', $(this).val());
    }).change();

    $("#overlay-color").change(function() {
        changeOverlayColor();
    }).change();

    $("#dgf-logo-color").change(function() {
        $(".dgf-logo").hide();
        $($(this).val()).show();
    }).change();

    $("#background-picture").change(function() {
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            $("#picture").attr("src", reader.result);
            resetPicturePosition();
        });
        reader.readAsDataURL(this.files[0]);
    });

    $("#move-picture").change(function() {
        $("#picture").css("left", `${$(this).val()}px`);
    }).change();

});

function changeOverlayColor() {
    var backgroundColor = $("#overlay-color").val();
    var transparent = "rgba(255, 255, 255, 0)";
    $("#overlay").css("background-image", `linear-gradient(0deg, ${backgroundColor} 0%, ${transparent} 50%)`);
}

function resetPicturePosition() {
    $("#move-picture").val(0).change();
}
