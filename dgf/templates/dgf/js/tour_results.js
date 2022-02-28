{% load i18n dgf dgf_cms %}

$(window).on("load", function() {
    friends = parseData();
    generateTable(friends);
});

function parseData() {

    friends = [
        {% for friend_results in results %}
            {
                id: {{friend_results.friend}},
                results: getBestResults({{friend_results|json|safe}}, {{tour.evaluate_how_many}})
            },
        {% endfor %}
    ];

    friends.sort(function(a, b) {
        return b.results.total - a.results.total;
    });

    return friends;
}

function generateTable(friends) {

    var summaryPart = $("#tour-results .table .summary")[0];

    friends.forEach(function(friend, index) {

        var summaryRow = addElement(summaryPart, "div", ["line"]);

        position = addElement(summaryRow, "div", ["position", "statistics-tooltip"], index + 1);
        addElement(position, "div", ["statistics", "tooltip-text"], generateStatistics(friend.results));
        addFriendBall(summaryRow, "div", ["player"], friend.id);

        // MOBILE
        {% if request.user_agent.is_mobile %}

            cell = addElement(summaryRow, "div", ["points", "link"], friend.results.total);
            cell.onclick = function () {
                $(this).parent().next().toggleClass("hidden");
                $(this).parent().next().next().toggleClass("hidden");
            };

        // DESKTOP
        {% else %}

            addElement(summaryRow, "div", ["points"], friend.results.total);

        {% endif %}

        // MOBILE
        {% if request.user_agent.is_mobile %}

            var detailsRow = addElement(summaryPart, "div", ["details", "hidden-scrollbar", "hidden"]);
            addElement(summaryPart, "div", ["details-fade-out", "hidden"]);
            var headerRow = addElement(detailsRow, "div", ["line", "header"]);
            var pointsRow = addElement(detailsRow, "div", ["line"]);

            {% for tournament in tournaments %}

                var headerWrapper = addElement(headerRow, "div", ["results-wrapper"]);

                {% if tournament.url %}
                    addElement(headerWrapper, "div", ["result"], "{{tournament|ts_number_mobile}}", "{{tournament.url}}", "_blank");
                {% else %}
                    addElement(headerWrapper, "div", ["result"], "{{tournament|ts_number_mobile}}");
                {% endif %}

                result = friend.results[{{tournament.id}}]
                var resultsWrapper = addElement(pointsRow, "div", ["results-wrapper"]);
                addElement(resultsWrapper, "div", ["result", "position-" + result.position], result.points);

            {% endfor %}

            addElement(headerRow, "div", ["results-wrapper", "empty"]);
            addElement(pointsRow, "div", ["results-wrapper", "empty"]);

        // DESKTOP
        {% else %}

            var detailsPart = $("#tour-results .table .details")[0];
            var detailsRow = addElement(detailsPart, "div", ["line"]);

            {% for tournament in tournaments %}
                result = friend.results[{{tournament.id}}]
                var resultsWrapper = addElement(detailsRow, "div", ["results-wrapper"]);
                addElement(resultsWrapper, "div", ["result", "position-" + result.position], result.points);
            {% endfor %}

        {% endif %}

    });

    $("#tour-results .table").fadeIn(500);
}

function getBestResults(results, evaluateHowMany) {

    playerAmount = {{tour|players_count}};

    var sortable = [];
    for (var key in results) {
        if (key.startsWith("points_")) {
            sortable.push([key, results[key]]);
        }
    }
    sortable.sort(function(a, b) {
        return negativeIfNull(b[1]) - negativeIfNull(a[1]);
    });

    var bestResults = {}
    var total = 0;
    var statistics = {
        totalPoints: 0,
        totalEfficiency: 0,
        playedTournaments: 0,
    }

    var tournamentAmount = 0;
    sortable.forEach(function(item, index){
        tournamentId = item[0].split("_")[1];
        points = item[1]
        position = results["position_" + tournamentId]

        if (points == null) {
            points = '-';
        }
        else {

            // IMPORTANT: do this before changing the points in the next if-else
            statistics.playedTournaments += 1;
            statistics.totalPoints += points;
            beatenPlayers = playerAmount[tournamentId] - position;
            possibleBeatenPlayers = playerAmount[tournamentId] - 1;
            statistics.totalEfficiency += beatenPlayers / possibleBeatenPlayers;

            if (index < evaluateHowMany) {
                total += points;
            }
            else {
                points = "[" + points + "]";
                position = "X";
            }

        }

        bestResults[tournamentId] = {"points": points, "position": position};
    })

    bestResults.total = total;
    bestResults.averagePoints = (statistics.totalPoints / statistics.playedTournaments).toFixed(0);
    bestResults.averageEfficiency = (statistics.totalEfficiency / statistics.playedTournaments * 100).toFixed(0) + "%";

    return bestResults;
}

function negativeIfNull(x) {
    return x == null ? -1 : x;
}

function addElement(parent, type, classes, text, url, target) {

    var element = document.createElement(type);
    parent.appendChild(element);

    classes.forEach(function(item){
        element.classList.add(item);
    });

    var addTextTo = element;

    if (url != undefined) {
        var a = document.createElement("a");
        element.appendChild(a);

        a.href = url;
        if (target != undefined) {
            a.target = target;
        }

        addTextTo = a;

    }

    if (text != undefined) {

        text = String(text);

        if (text.includes('\n')) {
            text.split('\n').forEach(function(item){
                var textNode = document.createTextNode(item);
                var brNode = document.createElement("br");
                addTextTo.appendChild(textNode);
                addTextTo.appendChild(brNode);
            });
        }
        else {
            var textNode = document.createTextNode(text);
            addTextTo.appendChild(textNode);
        }

    }

    return element;
}

function addFriendBall(parent, type, classes, friendId) {
    var element = document.createElement(type);
    classes.forEach(function(item){
        element.classList.add(item);
    });

    var ball = $("#friend-ball-" + friendId)[0];
    $(ball).show();

    element.appendChild(ball);
    parent.appendChild(element);

    return element;
}

function generateStatistics(results) {
    var averageEfficiency = "{% trans "Efficiency" %}: " + results.averageEfficiency;
    var averagePoints = "{% trans "Average points" %}: " + results.averagePoints;
    return averageEfficiency + "\n" + averagePoints;
}
