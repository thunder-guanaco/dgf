$(window).on("load", function() {

    $("#disc-golf-metrix-url").change(function() {
        updateResults();
    }).change();

    $("#manual-table").change(function() {
        updateResults();
    });

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
        changeOverlay();
    }).change();

    $("#overlay-angle").change(function() {
        changeOverlay();
    }).change();

    $("#overlay-depth").change(function() {
        changeOverlay();
    }).change();

    $("#results-position").change(function() {
        changeAbsolutePosition("#tournament-results", ["bottom", $(this).val()]);
        $("#dgf-logo-position").change();
        changeOverlay();
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

    $("#results-justify-content").change(function() {
       $("#tournament-results").css("justify-content", $(this).val());
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

    $("#picture-zoom").change(function() {
        $("#tournament-picture").css("height", `${$(this).val()}%`);
    }).change();

    $("#move-picture-horizontal").change(function() {
        $("#tournament-picture").css("left", `${$(this).val()}px`);
    }).change();

    $("#move-picture-vertical").change(function() {
        $("#tournament-picture").css("top", `${$(this).val()}px`);
    }).change();

});

function updateResults() {
    var manualTable = $("#manual-table").is(':checked');
    if (manualTable) {
        updateTitlesFromMetrixApi();
        copyManualTableFromMetrixPage();
    }
    else {
        updateResultsFromMetrixApi();
    }
}

const ONLY_TITLES = true;
function updateTitlesFromMetrixApi() {
    updateResultsFromMetrixApi(ONLY_TITLES);
}

function updateResultsFromMetrixApi(onlyTitles=false) {
    var url = $("#disc-golf-metrix-url").val();
    var tournamentId = url.split('/').pop();
    $.ajax({
        type: "GET",
        url: "https://discgolfmetrix.com/api.php?content=result&id=" + tournamentId,
        success: function(response) {
            handleMetrixApiResponse(response, onlyTitles);
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

function handleMetrixApiResponse(response, onlyTitles) {

    var competition = response["Competition"];

    changeTitle(competition);

    if (onlyTitles) {
        return;
    }

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

    var name = competition["Name"].split(" &rarr; ").pop().split(" (")[0];
    var comment = competition["Comment"];
    var division = $("#disc-golf-metrix-division").val();
    var date = new Date(competition["Date"]).toLocaleDateString('de-de');

    $("#tournament-title").text(name);
    $("#tournament-mode").text(comment);
    $("#tournament-division").text(division);
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

function copyManualTableFromMetrixPage() {
    var url = $("#disc-golf-metrix-url").val();
    $.ajax({
        type: "GET",
        url: `${proxyUrl}?url=${encodeURIComponent(url)}`,
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            handleMetrixPageResponse(response);
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

function handleMetrixPageResponse(response) {

    copyTable(response);
    showOnlyOneDivision($("#disc-golf-metrix-division").val());
    showTiesFootnote();
    addMedals();

    changeGeneratedContentHeight();
}

function copyTable(response) {
    var tmpElement = $("<div></div>");
    tmpElement.html(response);
    var metrixManualTable = $("table.data-hover", tmpElement);
    $("#results-table").html(metrixManualTable.html());
    $("#results-table thead th").css("max-width", "10em");
    $("#results-table tbody td[nowrap=nowrap]").addClass("name");
    $("#results-table thead th:contains('No')").before("<th></th>");
    $("#results-table thead th:contains('No')").text("");
    $("#results-table tbody td:first-child()").css("text-align", "left");

}

function showOnlyOneDivision(division) {

    if (division == "Open") {
        $("#results-table tbody tr:has(th:contains('Amateur'))").nextAll("tr").hide();
    }
    else {
        $("#results-table tbody tr:has(th:contains('Open'))").nextAll("tr").hide();
        $("#results-table tbody tr:has(th:contains('Amateur'))").nextAll("tr").show();
    }
    $("#results-table tbody tr:has(th)").hide();

}

function showTiesFootnote() {

    var ties = $("#results-table td:first-child():visible()").filter((index, node) => $(node).text().includes("*"));
    $("#ties-footnote").css('display', ties.length > 0 ? 'unset' : 'none');

}

function addMedals() {
    for (i=1; i<=100; i++) {
        $("#results-table td:first-child()").filter((index, node) => $(node).text().replace("*", "") == i).before(`<td class='position-${i}'></td>`);
    }
}

const pxToInt = (text) => parseInt(text.replace("px", ""));

function changeGeneratedContentHeight() {

    // make it big so that the results fit inside (#tournament-results has the height set to auto)
    $("#generated-content").height(2000);
    $("#generated-content").width(2000);
    $("#tournament-results").css("height", "auto");

    var resultsHeight = pxToInt($("#tournament-results").css("height"));
    var resultsWidth = pxToInt($("#tournament-results").css("width"));
    var sideLength = `${Math.max(resultsHeight, resultsWidth + 125)}px`;

    // and now let's resize it
    $("#generated-content").css("height", sideLength);
    $("#generated-content").css("width", sideLength);
    $("#tournament-results").css("height", sideLength);
}

function changeOverlay() {
    var backgroundColor = $("#overlay-color").val();
    var transparent = `${backgroundColor}00`;

    var overlayAngle = $("#overlay-angle").val();
    var overlayDepth = $("#overlay-depth").val();

    var resultsOnTheRightSide = $("#results-position").val() === "right";
    var firstColor = resultsOnTheRightSide ? transparent : backgroundColor;
    var secondColor = resultsOnTheRightSide ? backgroundColor : transparent;
    var firstPercent = resultsOnTheRightSide ? 0 : overlayDepth;
    var secondPercent = resultsOnTheRightSide ? overlayDepth : 100;

    $("#overlay").css("background-image", `linear-gradient(${overlayAngle}deg, ${firstColor} ${firstPercent}%, ${secondColor} ${secondPercent}%)`);
}

function resetPicturePosition() {
    $("#move-picture-horizontal").val(0).change();
    $("#move-picture-vertical").val(0).change();
}

function changeHeaderAlignment(alignment) {
    var flexAlignment = alignment === "right" ? "flex-end" : "flex-start";
    var flexFlow = alignment === "right" ? "row" : "row-reverse";
    $("#tournament-results").css("align-items", flexAlignment);
    $("#tournament-results > *").css("text-align", alignment);
    $("#tournament-subtitle").css("flex-flow", flexFlow)
}
