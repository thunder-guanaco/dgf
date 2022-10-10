/*

 This JS script takes the current Disc Golf Metrix Tournament and lists it's children tournaments that will happen in the future
 It needs to be used in a page where a div with "next-tournament" as ID exists.

 Example usage:
    <div id="next-tournaments"></div>
    <script type="text/javascript" src="https://discgolffriends.de/static/js/discgolfmetrix/next_tournaments.js"></script>

 Actually... this will never be used because Dis Golf Metrix does not allow loading JS from places they don't trust...
 So we are doing the following in Metrix:

    <div id="next-tournaments"></div>
    <script>
        $.ajax({
            url: "https://discgolffriends.de/friends/tremonia-series/future-dates",
            success: function(response) {
                $("#next-tournaments").html(response);
            }
        });
    </script>

*/

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "https://discgolfmetrix.com/api.php?content=result&id=" + document.URL.split('/').pop(),
        success: function(response) {
            const today = new Date().toISOString().slice(0, 10);
            const germanDate = (date) => {
               splittedDate = date.split('-');
               return splittedDate[2] + "." + splittedDate[1] + "." + splittedDate[0];
            };
            const sortNextTournaments = () => {
                const allTournaments = $("#next-tournaments li").sort((a, b) => $(a).data('date') - $(b).data('date'));
                $("#next-tournaments li").remove();
                allTournaments.each(function(){$("#next-tournaments").append(this.outerHTML)});
            };
            response.Competition.Events.forEach(function(event){
                $.ajax({
                    type: "GET",
                    url: "https://discgolfmetrix.com/api.php?content=result&id=" + event.ID,
                    success: function(response) {
                        const competition = response.Competition;
                        if (competition.Date > today) {
                            $("#next-tournaments").append("<li data-date='" + competition.Date.replaceAll('-', '') + "'><a href='https://discgolfmetrix.com/" + competition.ID + "' target='_blank'>" + competition.Name.substr(23) + " (" + germanDate(competition.Date) + ")</a></li>");
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
});