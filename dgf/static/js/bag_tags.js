function claimBagTag(number, url) {

    text = bagTagClaimText + number + "?";
    if (!confirm(text)) {
        return;
    }

    $.ajax({
        type: 'POST',
        url: url,
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

multipleBagTagMode = false;

function toggleMultipleBagTagMode() {

    multipleBagTagMode = !multipleBagTagMode;
    $("#bag-tags .number").toggleClass("gray");
    $("#toggle-mode .change").toggle();
    $("#toggle-mode .cancel").toggle();
    $("#change-multiple-bag-tags").toggle();

    if (!multipleBagTagMode) {
        $("#bag-tags .number").removeClass("selected");
    }

}

function bagTagClicked(bagTag) {

    bagTagElement = $("#bag-tags .number[data-bag-tag='" + bagTag + "']");

    if (multipleBagTagMode) {
        bagTagElement.toggleClass("selected");
    }
    else {
        claimBagTag(bagTag, bagTagElement.data("url"));
    }
}

function changeMultipleBagTags() {

    $("#multiple-bag-tag-numbers li").remove();
    $("#multiple-bag-tag-players li").remove();

    $("#bag-tags .content .number.selected").each(function(){
        var number = $(this).data("bag-tag");

        var numberListItem = $("#multiple-bag-tag-numbers").append("<li></li>").children("li:last-child");
        $("#bag-tags .content .number[data-bag-tag='" + number + "']").clone().appendTo(numberListItem);

        var numberElement = $(numberListItem).children(".number");
        $(numberElement).find("span").remove();
        $(numberElement).append("<input value='" + number + "'></input>");

        var playerListItem = $("#multiple-bag-tag-players").append("<li></li>").children("li:last-child");
        $("#bag-tags .content .player[data-bag-tag='" + number + "']").clone().appendTo(playerListItem);
    });

    $("#edit-bag-tags").show();
    $("#bag-tags").hide();

    /*
    var options = {
        // Like a css class name. Class will be removed after drop.
        currElClass: 'currElemClass',
        // or like a jQuery css object. Note that css object settings can't be removed
        currElCss: {
            'background-color':'green',
            'color':'#fff',
            'list-style-type': 'none',
            'padding': 0,
            'margin': 0,
        }
    }
    $('#multiple-bag-tag-players').sortableLists(options);
    */
}

function multipleBagTagsSave() {

    var players = [];
    $("#multiple-bag-tag-players li .player").each(function(){
        players.push($(this).data("username"));
    });

    var bagTags = [];
    $("#multiple-bag-tag-numbers li input").each(function(){
        bagTags.push(parseInt(this.value));
    });

    var data = {};
    players.forEach((player, i) => data[player] = bagTags[i]);
    console.log(data)

    $("#multiple-bag-tag-error span").remove();
    $.ajax({
        type: 'POST',
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
            $("#multiple-bag-tag-error").append("<span>" + response.statusText + "</span>")
        }
    });
}
