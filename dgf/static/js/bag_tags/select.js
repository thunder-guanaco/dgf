function selectBagTag(bagTag) {
    console.log(`Selected bag tag ${bagTag}`)
    $("#select-bag-tags .number[data-bag-tag='" + bagTag + "']").toggleClass("selected");
    $("#todays-bag-tags .number[data-bag-tag='" + bagTag + "']").toggleClass("selected");
}

function goToEditMultipleBagTags() {

    amountOfSelectedBagTags = $("#select-bag-tags .content .number.selected").length;
    if (amountOfSelectedBagTags < 2) {
        $(".at-least-2-bag-tags-hint").show();
        scrollUp();
        return;
    }
    else {
        $(".at-least-2-bag-tags-hint").hide();
    }

    $("#multiple-bag-tag-error").empty();
    $("#multiple-bag-tag-list").empty();
    $("#multiple-bag-tag-list").append("<ul id='multiple-bag-tag-numbers'></ul>");
    $("#multiple-bag-tag-list").append("<ul id='multiple-bag-tag-players'></ul>");
    $("#multiple-bag-tag-list").append("<ul id='multiple-bag-tag-delete'></ul>");

    $("#select-bag-tags .content .number.selected").each(function(index) {
        var number = $(this).data("bag-tag");

        var numberListItem = $("#multiple-bag-tag-numbers").append("<li data-bag-tag='" + number + "'></li>").children("li:last-child");
        $("#select-bag-tags .content .number[data-bag-tag='" + number + "']").clone().appendTo(numberListItem);

        var playerListItem = $("#multiple-bag-tag-players").append("<li data-bag-tag='" + number + "'></li>").children("li:last-child");
        var playerDiv = $("#select-bag-tags .content .player[data-bag-tag='" + number + "']").clone().appendTo(playerListItem);
        $("#select-bag-tags .content .number[data-bag-tag='" + number + "']").clone().prependTo(playerDiv);
        $(playerDiv).append("<div class='info'>");

        var playerListItem = $("#multiple-bag-tag-delete").append("<li></li>").children("li:last-child");
        $(playerListItem).append("<span class='delete' onclick='deleteFriend(" + index + ")'>❌</span>");
    });

    $("#multiple-bag-tag-players").sortableLists({
        currElClass: "draggedPlayer",
        listSelector: "ul",
        maxLevels: 1,
        insertZone: 500,
        scroll: 100,
        placeholderCss: {"background-color": "rgba(143, 25, 80, 0.1)"},
    });

    showPage('#edit-bag-tags');

    if (Object.keys(metrixScores).length) {
        sortBagTags();
        addPlayerInfo();
    }
    else {
        $("#edit-bag-tags .only-metrix").hide();
    }

}
