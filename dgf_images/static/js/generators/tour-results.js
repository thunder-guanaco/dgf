$(window).on("load", function() {

    sortResultsTable();

    $("#selected-tour").change(function() {
        $(".tour").hide();
        $(`#tour-${$(this).val()}`).show();
        changeGeneratedContentHeight();
    }).change();

    $("#results-amount").change(function() {
        hideNotWantedResults();
    });

    $("#show-last-changes").change(function() {
        showIfChecked(".last-tournament", this);
    }).change();

    $("#results-position").change(function() {
        changeAbsolutePosition(".tour", ["bottom", $(this).val()]);
        $("#dgf-logo-position").change();
        changeOverlayColor();
        resetPicturePosition();
        changeHeaderAlignment($(this).val());
    }).change();

    $("#dgf-logo-position").change(function() {
        var oppositePosition = $("#results-position").val() === "right" ? "left" : "right";
        changeAbsolutePosition(".dgf-logo", [$(this).val(), oppositePosition]);
    }).change();

    $("#results-justify-content").change(function() {
       $(".tour").css("justify-content", $(this).val());
    }).change();

    $("#text-color").change(function() {
        $('#generated-content').css('color', $(this).val());
    }).change();

    $("#dgf-logo-color").change(function() {
        $(".dgf-logo").hide();
        $($(this).val()).show();
    }).change();

    $("#background-color").change(function() {
        $('.results-table').css('background-color', `${$(this).val()}80`);
    }).change();

    $("#overlay-color").change(function() {
        changeOverlayColor();
    }).change();

    $("#background-picture").change(function() {
        var backgroundColor = $("#background-color").val();
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            $("#tour-picture").attr("src", reader.result);
            resetPicturePosition();
        });
        reader.readAsDataURL(this.files[0]);
    });

    $("#move-picture").change(function() {
        $("#tour-picture").css("left", `${$(this).val()}px`);
    }).change();

});

function sortResultsTable() {
    $(".tour").each(function() {

        // first: sort the table rows
        $(this).find(".results-table tbody tr")
            .sort((a, b) => $(b).data("total-points") - $(a).data("total-points"))
            .appendTo(`#${this.id} tbody`);

        // second: enumerate them
        $(this).find(".results-table tbody tr").each(function(index) {
            var position = index + 1;
            $(this).prepend(`<td>${position}</td>`);
            $(this).prepend(`<td class="position-${position}"></td>`);
        });
    });
    // third: hide extra results
    hideNotWantedResults();
}

function hideNotWantedResults() {
    var amountOfResultsToBeShown = $("#results-amount").val();
    $(".tour").each(function() {
        $(this).find(".results-table tbody tr").each(function(index) {
            var position = index + 1;
            if (position <= amountOfResultsToBeShown) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        });
    });
    changeGeneratedContentHeight();
}

const pxToInt = (text) => parseInt(text.replace("px", ""));


function changeGeneratedContentHeight() {

    var currentTourSelector = `#tour-${$("#selected-tour").val()}`;

    // make it big so that the results fit inside (.tour has the height set to auto)
    $("#generated-content").height(2000);
    $("#generated-content").width(2000);
    $(currentTourSelector).css("height", "auto");

    var resultsHeight = pxToInt($(currentTourSelector).css("height"));
    var resultsWidth = pxToInt($(currentTourSelector).css("width"));
    var sideLength = `${Math.max(resultsHeight, resultsWidth + 125)}px`;

    // and now let's resize it
    $("#generated-content").css("height", sideLength);
    $("#generated-content").css("width", sideLength);
    $(currentTourSelector).css("height", sideLength);
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
    var flexFlow = alignment === "right" ? "row" : "row-reverse";
    $(".tour").css("align-items", flexAlignment);
    $(".tour > *").css("text-align", alignment);
    $(".tour-subtitle").css("flex-flow", flexFlow)
}
