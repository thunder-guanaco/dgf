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
    $("#bag-tags").toggleClass("multiple-mode");
    $("#bag-tags .number").toggleClass("gray");

    $("#toggle-mode").toggleClass("negative");
    $("#toggle-mode .update").toggle();
    $("#toggle-mode .cancel").toggle();

    $("#show-bag-tags-hint").toggle();
    $("#select-bag-tags-hint").toggle();
    $("#change-multiple-bag-tags").toggle();

    $("#bag-tags .player").toggleClass("clickable");
    $("#bag-tags .since").toggle();

    if (multipleBagTagMode) {

        console.log("enter multipleBagTagMode");

        $("#bag-tags .friend-ball").each(function() {
            $(this).attr("old-href", $(this).attr("href"));
            $(this).removeAttr("href");
        });
    }
    else {
        console.log("exiting multipleBagTagMode");

        $("#bag-tags .friend-ball").each(function() {
            $(this).attr("href", $(this).attr("old-href"));
            $(this).removeAttr("old-href");
        });

        $("#bag-tags .number").removeClass("selected");
//        $("#bag-tags .number").css("background-color", "#8d1950");
//        $("#bag-tags .number").css("border-color", "#8d1950");
    }

}

function bagTagClicked(bagTag) {

    bagTagElement = $("#bag-tags .number[data-bag-tag='" + bagTag + "']");

    if (multipleBagTagMode) {
        bagTagElement.toggleClass("selected");
        if (bagTagElement.hasClass("selected")) {
//            bagTagElement.css("background-color", "#212529");
//            bagTagElement.css("border-color", "#212529");
        }
        else {
//            bagTagElement.css("background-color", "#999999");
//            bagTagElement.css("border-color", "#999999");
        }
    }
    else {
        claimBagTag(bagTag, bagTagElement.data("url"));
    }
}

function changeMultipleBagTags() {

    amountOfSelectedBagTags = $("#bag-tags .content .number.selected").length;
    if (amountOfSelectedBagTags < 2) {
        $("#at-least-2-bag-tags-hint").show();
        return;
    }
    else {
        $("#at-least-2-bag-tags-hint").hide();
    }

    $("#multiple-bag-tag-lists").append("<ul id='multiple-bag-tag-numbers'></ul>");
    $("#multiple-bag-tag-lists").append("<ul id='multiple-bag-tag-players'></ul>");

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

    $("#bag-tags").hide();
    $("#edit-bag-tags").show();

    $('#multiple-bag-tag-players').sortableLists({
        currElClass: 'draggedPlayer',
        listSelector: 'ul',
        maxLevels: 1,
        insertZone: 500,
        //insertZonePlus: true,
        scroll: 100,
        placeholderCss: {'background-color': 'rgba(143, 25, 80, 0.1)'},
    });
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

function multipleBagTagsCancel() {

    $("#multiple-bag-tag-numbers").remove();
    $("#multiple-bag-tag-players").remove();

    $("#edit-bag-tags").hide();
    $("#bag-tags").show();

}
