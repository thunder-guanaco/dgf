$(window).on("load", function() {
    showBestBagTagImprovement();
});

function showBestBagTagImprovement() {
    var min = 0;
    $("#bag-tags .content .news-best").each(function(){
        var bagTagDifference = $(this).data("bag-tag-difference");
        if (bagTagDifference < min) {
            min = bagTagDifference;
        }
    });
    $("#bag-tags .content .news-best[data-bag-tag-difference='" + min + "']").addClass("fire");
}

function claimBagTag(number, url) {

    if (number == ownBagTagNumer) {
        alert(youAlreadyHaveThatBagTag + number);
        return;
    }

    text = bagTagClaimText + number + "?";
    if (!confirm(text)) {
        return;
    }

    $.ajax({
        type: "POST",
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
    $("#select-from-metrix").toggle();

    $("#bag-tags .player").toggleClass("clickable");
    $("#bag-tags .since").toggle();

    $("#admin-bag-tags").toggle();

    if (multipleBagTagMode) {

        $("#bag-tags .friend-ball").each(function() {
            $(this).attr("old-href", $(this).attr("href"));
            $(this).removeAttr("href");
            $("#bag-tags .news").css({"visibility": "hidden"});
            $("#bag-tags .news-best").css({"visibility": "hidden"});
        });
    }
    else {

        $("#bag-tags .friend-ball").each(function() {
            $(this).attr("href", $(this).attr("old-href"));
            $(this).removeAttr("old-href");
            $("#bag-tags .news").css({"visibility": "visible"});
            $("#bag-tags .news-best").css({"visibility": "visible"});
        });

        $("#bag-tags .number").removeClass("selected");
        $("#at-least-2-bag-tags-hint").hide();
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

    $("#multiple-bag-tag-players").sortableLists({
        currElClass: "draggedPlayer",
        listSelector: "ul",
        maxLevels: 1,
        insertZone: 500,
        //insertZonePlus: true,
        scroll: 100,
        placeholderCss: {"background-color": "rgba(143, 25, 80, 0.1)"},
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

    $("#multiple-bag-tag-error span").remove();
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
            $("#multiple-bag-tag-error").append("<span>" + response.statusText + "</span>")
        }
    });
}

function multipleBagTagsCancel() {

    $("#multiple-bag-tag-numbers").remove();
    $("#multiple-bag-tag-players").remove();

    $("#multiple-bag-tag-error span").remove();

    $("#edit-bag-tags").hide();
    $("#bag-tags").show();

}

assignNewBagTagsMode = false;

function assignNewBagTagPopup() {

    assignNewBagTagsMode = !assignNewBagTagsMode;

    if (assignNewBagTagsMode) {

        $("#assign-new-bag-tag-popup .friend-ball").each(function() {
            $(this).attr("old-href", $(this).attr("href"));
            $(this).removeAttr("href");
        });
    }
    else {
        $("#assign-new-bag-tag-popup .friend-ball").each(function() {
            $(this).attr("href", $(this).attr("old-href"));
            $(this).removeAttr("old-href");
        });
    }

    $("#assign-new-bag-tag-button .assign").toggle();
    $("#assign-new-bag-tag-button .cancel").toggle();

    $("#assign-new-bag-tag-popup .player").toggleClass("clickable");
    $("#assign-new-bag-tag-popup").toggle();
}

function emptyBagTagClicked(username) {

    bagTagElement = $("#assign-new-bag-tag-popup .line[data-username='" + username + "'] .number");
    bagTagElement.toggleClass("selected");
}

function assignNewBagTags() {

    $("#assign-new-bag-tag-popup-error span").remove();

    var players = [];
    $("#assign-new-bag-tag-popup .number.selected").each(function(){
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
            $("#assign-new-bag-tag-popup-error").append("<span>" + response.statusText + "</span>")
        }
    });
}

function selectFromMetrix() {

    $("#select-from-metrix .select").toggle();
    $("#select-from-metrix .back").toggle();

    $("#bag-tags-metrix").toggle();
    $("#bag-tags .content").toggle();
}

function tournamentClicked(tournamentId) {
    $.ajax({
        type: "GET",
        url: "https://discgolfmetrix.com/api.php?content=result&id=" + tournamentId,
        success: function(response) {
            handleMetrixResponse(response);
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

function sortBy(results, field, reverse=false) {
    return results.sort(function(a, b) {
        if (reverse) {
            return b[field] - a[field];
        }
        else {
            return a[field] - b[field];
        }
    });
}

function parseTourResults(results) {

    var sortedResults = sortBy(results, "Place");
    var parsedResults = {};

    sortedResults.forEach(result => {
        var userId = result["UserID"];
        if (metrixUserIds.includes(userId)) {
            var username = metrixUserIdToFriend[userId];
            $("#bag-tags .content .number[data-username='" + username + "']").addClass("selected");
            parsedResults[username] = {
                "place": result["Place"],
                "score": result["Total"],
            };
        }
    });
    return parsedResults;
}

function parseSubCompetitions(competitions) {

    var allResults = {};
    competitions.forEach(competition => {
        competition["Results"].forEach(result => {
            var userId = result["UserID"];
            if (metrixUserIds.includes(userId)) {
                var username = metrixUserIdToFriend[userId];
                var score = result["Sum"];
                if (username in allResults) {
                    allResults[username]["score"] += score;
                }
                else {
                    allResults[username] = {
                        "score": score,
                        "username": username,
                    };
                }
            }
        });
    });

    var unsortedResults = Object.keys(allResults).map(function(key){
        return allResults[key];
    });

    var sortedResults = sortBy(unsortedResults, "score");

    var parsedResults = {};
    var i = 1;
    sortedResults.forEach(result => {
        var username = result["username"];
        $("#bag-tags .content .number[data-username='" + username + "']").addClass("selected");
        parsedResults[username] = {
            "place": i,
            "score": result["score"],
        };
        i += 1;
    });
    return parsedResults;
}

metrixResults = {};
function handleMetrixResponse(response) {

    var competition = response["Competition"];
    if (competition["ShowTourView"] == "1") {
        metrixResults = parseTourResults(competition["TourResults"]);
    }
    else {
        metrixResults = parseSubCompetitions(competition["SubCompetitions"]);
    }

    $("#bag-tags .content").show();
    $("#bag-tags-metrix").hide();

    changeMultipleBagTags();
    sortBagTags();
    addScores();
}

function getMetrixPlace(li) {
    return metrixResults[$(li).children("div").first().data("username")]["place"];
}

function sortBagTags() {
    $("#multiple-bag-tag-players li").sort(function(a, b){
        return getMetrixPlace(a) - getMetrixPlace(b);
    }).appendTo("#multiple-bag-tag-players");
}

function addScores() {
    $("#multiple-bag-tag-players .player").each(function(){
        var username = $(this).data("username");
        var score = metrixResults[username]["score"];
        $(this).append("<span class='score'>(" + score + ")</span>");
    });
}
