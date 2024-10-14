function extractTournamentId(url) {
    let pattern = /id=(\d+)/;
    return pattern.exec(url)[1];
}

function generateResultsUrl(tournamentId) {
    return "https://turniere.discgolf.de/index.php?p=events&sp=list-results&id=" + tournamentId;
}

function generateLiveScoresUrl(tournamentId) {
    return "https://turniere.discgolf.de/index.php?p=events&sp=live&id=" + tournamentId;
}

function dfvTournamentUrlEntered(urlInput) {
    try{
        $("#invalid-dfv-tournament-url").hide();
        let parsedUrl = new URL(urlInput);
        let tournamentId = extractTournamentId(parsedUrl);
        console.log('tournamentId');
        console.log(tournamentId);
        let resultsUrl = generateResultsUrl(tournamentId);
        $.ajax({
            type: "GET",
            url: resultsUrl,
            success: function(response) {
                handleDfvResultsResponse(response);
            },
            error: function(response, e) {
                console.log('dfvTournamentUrlEntered response');
                console.log(response);
                console.log(e);
                handleDfvResultsError(tournamentId);
            }
        });
    } catch (error){
        $("#invalid-dfv-tournament-url").show();
    }

}

function handleDfvResultsError(tournamentId) {
//     Try results page failed, try livescore
    $.ajax({
            type: "GET",
            url: generateLiveScoresUrl(tournamentId),
            success: function(response) {
                handleDfvLivescoreResponse(response);
            },
            error: function(response, e) {
                console.log(response);
                console.log(e);
                $("#invalid-dfv-tournament-url").show();
            }
        });
}


function parseTourResults(results) {

    let parsedResults = {};
    results.forEach(result => {
        let userId = result["UserID"];
        let username = metrixUserIdToFriend[userId];
        if (username) {
            let previousResult = parsedResults[username] || 0;
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

let dfvScores = {};
function handleDfvResultsResponse(response) {
    console.log('handleDfvResultsResponse');
    console.log(response);
    var competition = response["Competition"];
    if (competition === null) {
        $("#invalid-dfv-tournament-url").show();
        return;
    }

    // if (competition["ShowTourView"] == "1") {
    //     dfvScores = parseTourResults(competition["TourResults"]);
    // }
    // else {
    //     dfvScores = parseSubCompetitions(competition["SubCompetitions"]);
    // }
    //
    // $("#select-bag-tags .content .number").removeClass("selected");
    // Object.keys(dfvScores).forEach(username => {
    //     $("#select-bag-tags .content .number[data-username='" + username + "']").addClass("selected");
    // });

    goToSelectTodaysBagTags();
}

function handleDfvLivescoreResponse(response) {
    console.log('handleDfvLivescoreResponse');
    console.log(response);
    var competition = response["Competition"];
    if (competition === null) {
        $("#invalid-dfv-tournament-url").show();
        return;
    }

    // if (competition["ShowTourView"] == "1") {
    //     dfvScores = parseTourResults(competition["TourResults"]);
    // }
    // else {
    //     dfvScores = parseSubCompetitions(competition["SubCompetitions"]);
    // }
    //
    // $("#select-bag-tags .content .number").removeClass("selected");
    // Object.keys(dfvScores).forEach(username => {
    //     $("#select-bag-tags .content .number[data-username='" + username + "']").addClass("selected");
    // });

    goToSelectTodaysBagTags();
}

function getDfvOrder(li) {
    let player = $(li).children("div").first();
    let username = $(player).data("username");
    let bagTag = $(player).data("bag-tag");

    let score = dfvScores[username] || Number. MAX_VALUE;
    return score * 100 + bagTag;
}

function sortDfvBagTags() {
    $("#multiple-bag-tag-players li").sort(function(a, b){
        return getOrder(a) - getOrder(b);
    }).appendTo("#multiple-bag-tag-players");
}

function addDfvPlayerInfo() {
    $("#multiple-bag-tag-players .player").each(function(){
        let username = $(this).data("username");
        let score = dfvScores[username];
        if (score) {
            $(this).find(".info").append("<div>(" + score + ")</div>");
        }
    });
}
