function deleteFriend(index) {

    var player = $("#multiple-bag-tag-players li")[index];
    var bagTag = $(player).data("bag-tag");

    $("#multiple-bag-tag-numbers li[data-bag-tag='" + bagTag + "']").remove();
    $(player).remove();
    $("#multiple-bag-tag-delete li:last").remove();
}

function saveMultipleBagTags() {

    var players = [];
    $("#multiple-bag-tag-players li .player").each(function(){
        players.push($(this).data("username"));
    });

    var bagTags = [];
    $("#multiple-bag-tag-numbers li .number").each(function(index){
        if (index < players.length) {
            bagTags.push($(this).data("bag-tag"));
        }
    });

    console.log(`players: ${players}`);
    console.log(`bag tags: ${bagTags}`);

    var data = {};
    players.forEach((player, i) => data[player] = bagTags[i]);

    $("#multiple-bag-tag-error").empty();
    $.ajax({
        type: "POST",
        url: bagTagUpdateUrl,
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
            $("#multiple-bag-tag-error").append("<span>" + response.statusText + "</span>").show();
        }
    });
}