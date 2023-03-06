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

function claimBagTag(bagTag) {

    var element = $("#select-bag-tags .number[data-bag-tag='" + bagTag + "']")
    var url = element.data("url");

    if (bagTag == ownBagTagNumer) {
        alert(youAlreadyHaveThatBagTag + bagTag);
        return;
    }

    text = bagTagClaimText + bagTag + "?";
    if (!confirm(text)) {
        return;
    }

    $.ajax({
        type: "POST",
        url: url,
        beforeSend:function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response) {
            location.reload();
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(e);
        }
    });
}

function switchStatistics(bagTag) {
    $(".statistics-button[data-bag-tag='" + bagTag + "']").toggleClass("closed");
    $(".statistics-button[data-bag-tag='" + bagTag + "']").toggleClass("open");
    $(".statistics[data-bag-tag='" + bagTag + "']").toggle();
}
