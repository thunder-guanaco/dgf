$(document).keyup(function(e) {
     if (e.key === "Escape") {
        closePopups();
    }
});

$(window).on("load", function() {

    $(".container").click(function() {
        closePopups();
    });

    $(".league-popup").click(function(event) {
        event.stopPropagation();
    });

    $(".close-league-popup").click(function(event) {
        closePopups();
        event.stopPropagation();
    });

    $("#league-year-select").chosen({
        disable_search_threshold: 10,
        width: "100%"
    });

    $("#team-partner").chosen({
        disable_search_threshold: 10,
        width: "100%"
    });

    $("#rival-team").chosen({
        disable_search_threshold: 10,
        width: "70%"
    });

});

function onChangeYear() {
    selectedYear = $("#league-year-select").val();
    window.location.pathname = change_year_url.replace('1111', selectedYear);
}

function closePopups() {
    $(".league-popup").hide();
}

function showPopup(selector) {
    $(selector).css("display", "flex");
    event.stopPropagation();
}

function searchForTeam() {
    $.ajax({
        type: "POST",
        url: searchForTeamUrl,
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, error) {
            console.log(response.statusText);
        }
    });
}

function createTeam() {
    $.ajax({
        type: "POST",
        url: createTeamUrl,
        data: {
            "partner": $("#team-partner").val(),
            "name": $("#team-name").val()
        },
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, error) {
            console.log(response.statusText);
            $("#create-new-team .error").text(response.statusText);
        }
    });
}

function createResult() {
    $.ajax({
        type: "POST",
        url: createResultUrl,
        data: {
            "own_points": $("#own-points").val(),
            "rival_team": $("#rival-team").val(),
            "rival_points": $("#rival-points").val(),
        },
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, error) {
            console.log(response.statusText);
            $("#add-result .error").text(response.statusText);
        }
    });
}

function switchResults(teamId) {
    $(".results-button[data-team='" + teamId + "']").toggleClass("closed");
    $(".results-button[data-team='" + teamId + "']").toggleClass("open");
    $(".results[data-team='" + teamId + "']").toggle();
}