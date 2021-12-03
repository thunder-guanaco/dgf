function getBestResults(results, amount) {

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
    sortable.forEach(function(item, index){
        tournamentId = item[0].split("_")[1];
        points = item[1]
        position = results["position_" + tournamentId]

        if (points == null) {
            points = '-';
        }
        else if (index < amount) {
            total += points;
        }
        else {
            points = "[" + points + "]";
            position = "X";
        }
        bestResults[tournamentId] = {"points": points, "position": position};
    })
    bestResults.total = total;
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
        var textNode = document.createTextNode(text);
        addTextTo.appendChild(textNode);
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