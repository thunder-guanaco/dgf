$(window).on("load", function() {
    $("#search-friend-input").on("keyup", function() {
        searchFriends($(this).val())
    });
});

function searchFriends(name) {
    if (name.length > 0) {
        $(".all-friends .friend-wrapper").hide();
        $(`.all-friends .friend-wrapper[data-search*="${name.toLowerCase()}"]`).show();
    }
    else {
        $(".all-friends .friend-wrapper").show();
    }
}
