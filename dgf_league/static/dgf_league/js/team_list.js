$(window).on("load", function() {

    $(".container").click(function() {
      $(".league-popup").hide();
    });

    $(".league-popup").click(function(event) {
      event.stopPropagation();
    });

    $("#team-partner").chosen({
        disable_search_threshold: 10,
        width: "100%"
    });

    $("#rival-team").chosen({
        disable_search_threshold: 10,
        width: "80%"
    });

});

function showPopup(selector) {
    $(selector).css("display", "flex");
    event.stopPropagation();
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
            console.log(response)
            console.log(response.statusText);
            $("#add-result .error").text(response.statusText);
        }
    });
}