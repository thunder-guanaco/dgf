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
