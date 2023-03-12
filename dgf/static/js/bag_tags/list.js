$(window).on("load", function() {
    showBestBagTagImprovement();
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
