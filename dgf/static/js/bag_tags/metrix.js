function extractTournamentId(url) {
    return url.pathname.split('/')[1].split('?')[0].split('&')[0];
}

function tournamentUrlEntered(url) {

    try{

        $("#invalid-metrix-tournament-url").hide();
        var url = new URL(url);
        tournamentId = extractTournamentId(url);
        tournamentSelected(tournamentId);

    } catch (error){
        $("#invalid-metrix-tournament-url").show();
    }

}

function tournamentSelected(tournamentId) {
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
            previousResult = parsedResults[username] || 0;
            parsedResults[username] = (result["Total"] || result["Sum"]) + previousResult;
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
                if (username in parsedResults) {
                    parsedResults[username] += result["Sum"];
                }
                else {
                    parsedResults[username] = result["Sum"];
                }
            }
        });
    });
    return parsedResults;
}

metrixScores = {};
function handleMetrixResponse(response) {

    var competition = response["Competition"];
    if (competition === null) {
        $("#invalid-metrix-tournament-url").show();
        return;
    }

    if (competition["ShowTourView"] == "1") {
        metrixScores = parseTourResults(competition["TourResults"]);
    }
    else {
        metrixScores = parseSubCompetitions(competition["SubCompetitions"]);
    }

    $("#select-bag-tags .content .number").removeClass("selected");
    console.log("metrixScores", metrixScores)
    Object.keys(metrixScores).forEach(username => {
        $("#select-bag-tags .content .number[data-username='" + username + "']").addClass("selected");
    });

    goToSelectTodaysBagTags();
}

function getOrder(li) {
    var player = $(li).children("div").first();
    var username = $(player).data("username");
    var bagTag = $(player).data("bag-tag");

    var score = metrixScores[username] || Number. MAX_VALUE;
    return score * 100 + bagTag;
}

function sortBagTags() {
    $("#multiple-bag-tag-players li").sort(function(a, b){
        return getOrder(a) - getOrder(b);
    }).appendTo("#multiple-bag-tag-players");
}

function addPlayerInfo() {
    $("#multiple-bag-tag-players .player").each(function(){
        var username = $(this).data("username");
        var score = metrixScores[username];
        if (score) {
            $(this).find(".info").append("<div>(" + score + ")</div>");
        }
    });
}
