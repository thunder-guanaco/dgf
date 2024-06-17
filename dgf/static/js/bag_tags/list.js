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

    var data = [{
        x: Object.keys(changesAsObject),
        y: Object.values(changesAsObject),
        type: 'scatter',
        mode: 'lines+markers',
        line: {
            color: '#8d1950'
        },
        marker: {
            color: '#000000',
      }
    }];

    var layout = {
        yaxis: {
            autorange: "reversed",
            zeroline: false
        },
        autosize: true,
        margin: {
            l: 30
        }
    };

    var config = {
        responsive: true
    }

    Plotly.newPlot(`chart-${friendSlug}`, data, layout, config);
}

function switchHistory(friendSlug) {
    $(".history-button[data-bag-tag='" + friendSlug + "']").toggleClass("closed");
    $(".history-button[data-bag-tag='" + friendSlug + "']").toggleClass("open");
    $(`#chart-${friendSlug}`).toggle();
}