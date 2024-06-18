function loadCss() {
    $.ajax({
        url: "https://discgolffriends.de/static/css/discgolfmetrix.css",
        success: function(response) {
            $("head").append(`<style>${response}</style>`);
        }
    });
}

function loadDiscGolfMetrixScript() {
    $.ajax({
        url: "https://raw.githubusercontent.com/manologg/discgolfmetrix/main/discgolfmetrix.js",
        success: function(response) {
            $("body").append("<script>" + response); // yes, the ending "script" tag is missing
        }
    });

}

var DGF_LOGO_IMG = "<img class='dgf-logo' src='https://discgolffriends.de/static/img/logo.png' width='40px'/>";
var DGF_BAG_TAG = (number) => `<div class='${number ? "bag-tag-number" : "bag-tag-number empty"}' style='display: none;'><span>${number || "&nbsp"}</span></div>`;
var DGF_PART = (number) => `<div class='dgf-part'>${DGF_LOGO_IMG}${DGF_BAG_TAG(number)}</div>`;

function markFriends() {
    $.ajax({
        type: "GET",
        url: "https://discgolffriends.de/friends/disc-golf-metrix/friends",
        success: function(response) {

            metrix_friends = response.friends;

            var show_bag_tags = false;

            response.friends.forEach(friend => {

                if (user_id == friend.metrix_user_id) {
                    show_bag_tags = true;
                }

                // results page
                $(`a.profile-link[href="/player/${friend.metrix_user_id}"]`)
                    .parent()
                    .append(DGF_PART(friend.bag_tag));

                // registration page
                $(`a:not(.profile-link)[href="/player/${friend.metrix_user_id}"]`)
                    .parent()
                    .append(DGF_PART(friend.bag_tag));

            });

            $("tbody:has(.dgf-part").addClass("dgf-table")

            if (show_bag_tags) {
                $(".bag-tag-number").show();
            }
        }
    });
}

/* MAIN */
loadCss();
loadDiscGolfMetrixScript();
markFriends();
