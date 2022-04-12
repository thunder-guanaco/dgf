$(window).on("load", function() {
    desktopStickyOffset = $('#navigation-bar').offset().top;
    mobileStickyOffset = $('#mobile-navigation-bar').offset().top;

    // Sticky header
    var sticky = false;
    $(window).scroll(function(){

        var scroll = $(window).scrollTop();

        if (mobileNavigationBarIsVisible()) {

            // mobile
            console.log("scroll: " + scroll);
            console.log("mobileStickyOffset: " + mobileStickyOffset);
            if (scroll > mobileStickyOffset) {
                $("#mobile-navigation-bar").addClass("sticky");
                if (!sticky) {
                    $("#mobile-navigation-bar-language-chooser").slideDown("slow");

                    $("#headline img").hide("slow");
                    $("#headline img").clone().appendTo("#mobile-mini-headline");
                    $("#mobile-mini-headline img").slideDown("slow");

                    sticky = true;
                }
            }
            else {
                $("#mobile-navigation-bar").removeClass("sticky");
                if (sticky) {
                    $("#mobile-navigation-bar-language-chooser").hide("slow");

                    $("#headline img").show();
                    $("#mobile-mini-headline img").slideUp("slow");
                    $("#mobile-mini-headline img").remove();

                    sticky = false;
                }
            }
        }
        else {

            // desktop
            if (scroll > desktopStickyOffset) {
                $("#navigation-bar").addClass("sticky");
                if (!sticky) {
                    $("#navigation-bar-header").show("slow");
                    $("#navigation-bar-language-chooser").slideDown("slow");
                    $("#navigation-bar").slideDown("slow");

                    sticky = true;
                }
            }
            else {
                $("#navigation-bar").removeClass("sticky");
                if (sticky) {
                    $("#navigation-bar-header").hide("slow");
                    $("#navigation-bar-language-chooser").hide("slow");

                    sticky = false;
                }
            }
        }
    });

    loadMobileNavigationBarBehaviour();
    loadLoginNextPageBehaviour();
});

function loadMobileNavigationBarBehaviour() {

    $("#mobile-navigation-bar-header a").click(function(e){
        e.preventDefault();
    });

    $(document).click(function(e) {
        if ($.contains($("#mobile-navigation-bar-header")[0], e.target)
            || $.contains($("#mobile-navigation-opener")[0], e.target)) {
            $(".bar-container").toggleClass("change");
            $(".navbar-collapse").toggle();
        }
        else if (!$.contains($("#navbarResponsive")[0], e.target)) {
            $(".navbar-collapse").hide();
            $(".bar-container").removeClass("change");
        }
    });

    $(".dropdown-toggle").click(function(){
        $(this).toggleClass("open");
        $(this).siblings().toggle();
    });
}

function loadLoginNextPageBehaviour() {
    $("#navigation-bar a[href='/login/']").click(function(e){
        e.target.href = e.target.href + "?next=" + window.location.pathname;
    });
}

function mobileNavigationBarIsVisible() {
    return $("#mobile-navigation-bar").is(":visible") && $("#navbarResponsive").is(":hidden");
}
