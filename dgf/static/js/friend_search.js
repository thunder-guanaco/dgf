$(window).on("load", () => {

    $(".friend-search-field").keyup(searchFriends);
    $(".friend-search").submit(submitForm);

});

function searchFriends() {

    $(".all-friends").removeClass("hidden");

    var name = $(this).val();
    if (name.length > 0) {
        $(".all-friends .friend-wrapper").hide();
        $(`.all-friends .friend-wrapper[data-search*="${name.toLowerCase()}"]`).show();
    }
    else {
        $(".all-friends .friend-wrapper").show();
    }
}

function submitForm(e) {

    e.preventDefault();
    var visibleFriends = $(".all-friends .friend-wrapper:visible()");
    var amount = visibleFriends.length;
    if (amount === 1) {
        window.location = visibleFriends.first().children(".friend-ball").first().attr("href");
    }
    else {
        console.log("More than one friend found! Do nothing.");
    }
}