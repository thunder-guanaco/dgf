function loadCss() {
    $.ajax({
        url: "https://discgolffriends.de/static/css/discgolfmetrix.css",
        success: function(response) {
            $("head").append(`<style>${response}</style>`);
        }
    });
}

function fixIcons(){
    $(".main-header-meta svg").after("<i class='fi-map'></i> ");
    $(".main-header-meta svg").remove();
}

function isMobile() {
    return window.matchMedia("only screen and (max-width: 1024px)").matches;
}

function loadBanner(image) {
    const childName = $("#competition-submenu .selected b").text();
    const textRegex = /#\d+|\d+er\ Runde|Finale|\d+\.\ Runde/gm;
    const bannerText = (childName.match(textRegex) || ['']).pop(); // empty in case it doesn't match
    const largerClass = bannerText.length < 4 ? 'larger' : ''; // if the name is something like "#123" it will be larger
    const bannerDiv = `<div class='discgolffriends-banner'><img src='${image}'></img><span class='${largerClass}'>${bannerText}</span></div>`;
    if (isMobile()) {
        $("#content").before(`<div class='mobile'>${bannerDiv}</div>`);
    }
    else {
        $(".breadcrumbs").after(`<div class='desktop'>${bannerDiv}</div>`);
    }
}

function loadSubcompetitionButtons(onlyFuture) {
    $.ajax({
        type: "GET",
        url: "https://discgolfmetrix.com/api.php?content=result&id=" + document.URL.split('/').pop(),
        success: function(response) {
            const today = new Date().toISOString().slice(0, 10);
            const sortNextTournaments = () => {
                const allTournaments = $("#subcompetitions .button").sort((a, b) => $(a).data('date') > $(b).data('date') ? 1 : -1);
                $("#subcompetitions .button").remove();
                allTournaments.each(function(){$("#subcompetitions").append(this.outerHTML)});
            };
            const childName = (competition) => competition.Name.split(" &rarr; ").pop();
            if (response.Competition.Events) {
                $(".main-header .main-title").after("<div id='subcompetitions'/>");
            }
            response.Competition.Events?.forEach(function(event){
                $.ajax({
                    type: "GET",
                    url: "https://discgolfmetrix.com/api.php?content=result&id=" + event.ID,
                    success: function(response) {
                        const competition = response.Competition;
                        if (!onlyFuture || competition.Date > today) {
                            $("#subcompetitions").append(`<a
                                                                class='button'
                                                                href='https://discgolfmetrix.com/${competition.ID}'
                                                                data-date='${competition.Date} ${competition.Time}'>
                                                            ${childName(competition)}
                                                        </a>
                                                        `);
                            sortNextTournaments();
                        }
                    }
                });
            });
        },
        error: function(response, e) {
            console.log(response.statusText);
            console.log(response);
            console.log(e);
        }
    });
}

/* MAIN */

loadCss();
fixIcons();
if (typeof image !== "undefined") {
    loadBanner(image);
}
const onlyFuture = (typeof showOnlyFutureSubcompetitions !== "undefined") && showOnlyFutureSubcompetitions; // default: show all
loadSubcompetitionButtons(onlyFuture);

$(".breadcrumbs").hide();
