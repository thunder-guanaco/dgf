function emptyBagTagClicked(username) {
    $("#admin-bag-tags .line[data-username='" + username + "'] .number").toggleClass("selected");
}

function assignNewBagTags() {

    $("#admin-bag-tags .dynamic-error").empty();

    var players = [];
    $("#admin-bag-tags .number.selected").each(function(){
        players.push($(this).parent().data("username"));
    });

    if (players.length == 0) {
        $("#at-least-1-friend-hint").show();
        return;
    }
    else {
        $("#at-least-1-friend-hint").hide();
    }

    var data = {
        "players": players,
    };

    $.ajax({
        type: "POST",
        url: assignNewBagTagsUrl,
        data: data,
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
            $("#admin-bag-tags .dynamic-error").append("<span>" + response.statusText + "</span>").show();
        }
    });
}