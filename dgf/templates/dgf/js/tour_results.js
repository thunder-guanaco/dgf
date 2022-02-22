{% load dgf dgf_cms %}

$(window).on("load", function() {
    console.log("Generating results table...");
    friends = parseData();
    generateTable(friends);
    console.log("Results table was generated");
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

        addElement(summaryRow, "div", ["position"], index + 1);
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

            var detailsPart = $("#tour-results .table .details")[0];
            var detailsRow = addElement(detailsPart, "div", ["line"]);

            {% for tournament in tournaments %}
                result = friend.results[{{tournament.id}}]
                var resultsWrapper = addElement(detailsRow, "div", ["results-wrapper"]);
                addElement(resultsWrapper, "div", ["result", "position-" + result.position], result.points);
            {% endfor %}

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

        {% endif %}

    });
    $("#tour-results .table").fadeIn(500);
}