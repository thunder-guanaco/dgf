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

function parseTourResults(results) {

    var parsedResults = {};
    results.forEach(result => {
        var userId = result["UserID"];
        var username = metrixUserIdToFriend[userId];
        if (username) {
            parsedResults[username] = {
                "position": result["Place"],
                "score": result["Total"] || result["Sum"],
                "all_scores": result["EventResults"],
            };
        }
    });
    return parsedResults;
}

function parseSubCompetitions(competitions) {

    var parsedResults = {};
    competitions.forEach(competition => {
        competition["Results"].forEach(result => {
            var userId = result["UserID"];
            var username = metrixUserIdToFriend[userId];
            if (username) {
                var score = result["Sum"];
                var position = result["Place"];
                var result = parsedResults[username];
                if (result) {
                    result["position"] += position;
                    result["score"] += score;
                    result["all_scores"].push(score);
                }
                else {
                    parsedResults[username] = {
                        "position": position,
                        "score": score,
                        "all_scores": [score],
                    };
                }
            }
        });
    });
    return parsedResults;
}

metrixResults = {};
sortBagTagsBy = "score";
function handleMetrixResponse(response) {

    var competition = response["Competition"];
    if (competition["ShowTourView"] == "1") {
        metrixResults = parseTourResults(competition["TourResults"]);
    }
    else {
        metrixResults = parseSubCompetitions(competition["SubCompetitions"]);
    }

    $("#select-bag-tags .content .number").removeClass("selected");
    Object.keys(metrixResults).forEach(username => {
        $("#select-bag-tags .content .number[data-username='" + username + "']").addClass("selected");
    });

    changeMultipleBagTags();
}

function getOrder(li) {
    var username = $(li).children("div").first().data("username");
    results = metrixResults[username];
    if (results) {
        return results[sortBagTagsBy];
    }
    else {
        return Number. MAX_VALUE;
    }
}

function sortBagTags(field) {
    if (field) {
        sortBagTagsBy = field;
    }
    $("#multiple-bag-tag-players li").sort(function(a, b){
        return getOrder(a) - getOrder(b);
    }).appendTo("#multiple-bag-tag-players");
}

function addPlayerInfo() {
    $("#multiple-bag-tag-players .player").each(function(){
        var username = $(this).data("username");
        var result = metrixResults[username];

        var position = result["position"];
        var score = result["score"];
        var allScores = result["all_scores"];

        var scoreInfo = "<div>(" + score;
        if (allScores) {
            scoreInfo += " = " + prettify(allScores) + "";
        }
        scoreInfo += ")</div>";
        $(this).find(".info").append(scoreInfo);

        if (position) {
            $(this).find(".info").append("<div class='position'>&nbsp;📈 " + position + "</div>");
        }
    });
}

function prettify(all_scores) {

    var scores = all_scores.map(score => {
        if (!score) {
            return "⛔";
        }
        else {
            return score;
        }
    });

    return scores.join(" + ");
}
