$(window).on("load", function() {
    stickyOffset = $('#navigation-bar').offset().top;
    console.log($('#navigation-bar').offset().top);

    var sticky = false;
    $(window).scroll(function(){

        var scroll = $(window).scrollTop();

        if (scroll >= stickyOffset) {
            $("#navigation-bar").addClass("sticky");
            if (!sticky) {
                $("#navigation-bar ul").first().prepend($("#header").html());
                $("#navigation-bar").slideDown("slow");
                sticky = true;
            }
        }
        else {
            $("#navigation-bar").removeClass("sticky");
            if (sticky) {
                $("#navigation-bar ul").first().children().first().remove();
                sticky = false;
            }
        }
    });
});
