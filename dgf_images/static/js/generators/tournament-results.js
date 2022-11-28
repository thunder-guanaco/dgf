$(window).on("load", function() {

    $("#disc-golf-metrix-url").change(function() {
        updateResults();
    }).change();

    $("#disc-golf-metrix-division").change(function() {
        updateResults();
    });

    $("#text-color").change(function() {
        $('#generated-content').css('color', $(this).val());
    }).change();

    $("#background-color").change(function() {
        $('#results-table').css('background-color', `${$(this).val()}80`);
    }).change();

    $("#overlay-color").change(function() {
        changeOverlayColor();
    }).change();

    $("#results-position").change(function() {
        changeAbsolutePosition("#tournament-results", ["bottom", $(this).val()]);
        $("#dgf-logo-position").change();
        changeOverlayColor();
        resetPicturePosition();
        changeHeaderAlignment($(this).val());
    }).change();

    $("#dgf-logo-color").change(function() {
        $(".dgf-logo").hide();
        $($(this).val()).show();
    }).change();

    $("#dgf-logo-position").change(function() {
        var oppositePosition = $("#results-position").val() === "right" ? "left" : "right";
        changeAbsolutePosition(".dgf-logo", [$(this).val(), oppositePosition]);
    }).change();

    $("#background-picture").change(function() {
        var backgroundColor = $("#background-color").val();
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            $("#tournament-picture").attr("src", reader.result);
            resetPicturePosition();
        });
        reader.readAsDataURL(this.files[0]);
    });

    $("#move-picture").change(function() {
        $("#tournament-picture").css("left", `${$(this).val()}px`);
    }).change();

});

function updateResults() {
    var url = $("#disc-golf-metrix-url").val();
    var tournamentId = url.split('/').pop();
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


function handleMetrixResponse(response) {

    var competition = response["Competition"];

    changeTitle(competition);

    var table = $("#results-table");
    table.empty();

    if (competition["ShowTourView"] === 1) {
        appendHeader(competition, table);
        appendTourResults(competition, table);
    }
    else {
        // TODO: #5688 check this type of tournaments
        displaySubCompetitions(competition["SubCompetitions"]);
    }

    changeGeneratedContentHeight();

}

function changeTitle(competition) {

    var name = competition["Name"].split(" &rarr; ").pop();
    var division = $("#disc-golf-metrix-division").val();
    var date = new Date(competition["Date"]).toLocaleDateString('de-de');

    $("#tournament-title").text(name);
    $("#tournament-division").text(`${division} Division`);
    $("#tournament-date").text(date);
}

function appendHeader(competition, table) {
    var headerTr = $("<tr></tr>");
    headerTr.append('<th></th>');
    headerTr.append('<th></th>');
    headerTr.append('<th></th>');
    competition["Events"].forEach((event) => {
        headerTr.append(`<th>${event["Name"]}</th>`);
    })
    headerTr.append('<th>Gesamt</th>');
    table.append(headerTr);
}

function appendTourResults(competition, table) {

    var division = $("#disc-golf-metrix-division").val();
    var sortedResults = getResultsFromDivision(competition["TourResults"], "Place", division);

    sortedResults.forEach(result => {
        var resultTr = $("<tr></tr>");
        resultTr.append(`<td class='position-${result["Place"]}'></td>`);
        resultTr.append(`<td>${result["Place"]}</td>`);
        resultTr.append(`<td class="name">${result["Name"]}</td>`);
        result["EventResults"].forEach(eventResult => {
            $(resultTr).append(`<td>${eventResult ?? ''}</td>`);
        });
        resultTr.append(`<td>${result["Total"]}</td>`);
        table.append(resultTr);
    });
}

function getResultsFromDivision(results, positionField, division) {
    return results.sort((a, b) => a[positionField] - b[positionField])
                  .filter((result) => result["ClassName"] === division)
}

function displaySubCompetitions(competitions) {

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

function changeGeneratedContentHeight() {
    // why twice? no idea... otherwise it does not work because the height changes...
    [0, 1].forEach(() => {
        var sideLength = $("#tournament-results").height() + 100;
        $("#generated-content").css("height", `${sideLength}px`);
        $("#generated-content").css("width", `${sideLength}px`);
    });
    var sideLength = $("#tournament-results").height() + 100;
    $("#tournament-results").css("height", `${sideLength}px`);
}

function changeOverlayColor() {
    var backgroundColor = $("#overlay-color").val();
    var transparent = "rgba(255, 255, 255, 0)";

    var resultsOnTheRightSide = $("#results-position").val() === "right";
    var firstColor = resultsOnTheRightSide ? transparent : backgroundColor;
    var secondColor = resultsOnTheRightSide ? backgroundColor : transparent;
    var firstPercent = resultsOnTheRightSide ? 0 : 50;
    var secondPercent = resultsOnTheRightSide ? 50 : 100;
    $("#overlay").css("background-image", `linear-gradient(90deg, ${firstColor} ${firstPercent}%, ${secondColor} ${secondPercent}%)`);
}

function resetPicturePosition() {
    $("#move-picture").val(0).change();
}

function changeHeaderAlignment(alignment) {
    var flexAlignment = alignment === "right" ? "flex-end" : "flex-start";
    $("#tournament-results").css("align-items", flexAlignment);
    $("#tournament-results > *").css("text-align", alignment);
}
