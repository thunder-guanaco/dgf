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

var DGF_LOGO_IMG = "<img class='dgf-logo' src='https://discgolffriends.de/static/img/logo.png' width='40px'/>"

function markFriends() {
    $.ajax({
        type: "GET",
        url: "https://discgolffriends.de/friends/disc-golf-metrix/all-friend-ids",
        success: function(response) {

            response.ids.forEach(id => {

                // results page
                $(`a.profile-link[href="/player/${id}"]`)
                    .hide()
                    .first().prepend(DGF_LOGO_IMG).show()
                    .children("svg").remove();

                // registration page
                $(`a:not(.profile-link)[href="/player/${id}"]`)
                    .parent()
                    .append(DGF_LOGO_IMG);

            });
        }
    });
}

/* MAIN */
loadCss();
loadDiscGolfMetrixScript();
markFriends();
