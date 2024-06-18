$(window).on("load", function() {
    showBestBagTagImprovement();
    loadBagTagHistory();
});

const SAD_EMOJIS = ['😭', '😞', '💩', '🥶', '😢', '🥲', '📉', '🧊', '☃️', '❄️'];

function randomSadEmoji() {
    var randomIndex = Math.floor(Math.random() * (SAD_EMOJIS.length));
    return randomIndex, SAD_EMOJIS[randomIndex];
}

function showBestBagTagImprovement() {
    var min = 0;
    var max = 0;
    $("#list-bag-tags .content .news-best").each(function(){
        var bagTagDifference = $(this).data("bag-tag-difference");
        if (bagTagDifference < min) {
            min = bagTagDifference;
        }
        if (bagTagDifference > max) {
            max = bagTagDifference;
        }
    });
    $("#list-bag-tags .content .news-best[data-bag-tag-difference='" + min + "']").addClass("fire");
    $("#list-bag-tags .content .news-best[data-bag-tag-difference='" + max + "']").addClass("sad").attr("data-content", randomSadEmoji());
}

function switchStatistics(bagTag) {
    $(".statistics-button[data-bag-tag='" + bagTag + "']").toggleClass("closed");
    $(".statistics-button[data-bag-tag='" + bagTag + "']").toggleClass("open");
    $(".statistics[data-bag-tag='" + bagTag + "']").toggle();
}

function loadBagTagHistory() {

    $.ajax({
        type: "GET",
        url: getBagTagHistoryUrl,
        success: function(response) {
            Object.entries(response).forEach(entry => plotBagTagHistory(entry));
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

function plotBagTagHistory([friendSlug, bagTagChanges]) {
    var changesAsObject = Object.fromEntries(bagTagChanges);
    var dates = Object.keys(changesAsObject);
    var bagTags = Object.values(changesAsObject);

    var data = [{
        x: dates,
        y: bagTags,
        type: 'scatter',
        mode: 'lines+markers',
        line: {
            color: '#8d1950'
        }
    }];

    var bestBagTag = Math.min(...bagTags);
    var worstBagTag = Math.max(...bagTags);
    var dtick = 5;
    if (worstBagTag - bestBagTag < 10) {
        dtick = "D1";
    }
    var autorangeInclude = bestBagTag;
    if (bestBagTag < 10) {
        autorangeInclude = 0;
    }

    var layout = {
        yaxis: {
            autorange: "reversed",
            autorangeoptions: {
                include: autorangeInclude
            },
            zeroline: false,
            tick0: 0,
            dtick: dtick
        },
        autosize: true,
        margin: {
            l: 30,
            r: 0
        }
    };

    var config = {
        responsive: true,
        staticPlot: true
    }

    Plotly.newPlot(`chart-${friendSlug}`, data, layout, config);
}

function switchHistory(friendSlug) {
    $(".history-button[data-bag-tag='" + friendSlug + "']").toggleClass("closed");
    $(".history-button[data-bag-tag='" + friendSlug + "']").toggleClass("open");
    $(`#chart-${friendSlug}`).toggle();
    if ($(`#chart-${friendSlug}`).is(":visible")) {
        Plotly.relayout(`chart-${friendSlug}`, {
            "xaxis.autorange": true,
            "yaxis.autorange": true
        });
    }
}