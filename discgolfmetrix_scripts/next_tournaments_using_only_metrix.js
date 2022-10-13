/*

 This JS script takes the current Disc Golf Metrix Tournament and lists it's children tournaments that will happen in the future.

 Actually... this will never be used because it does A LOT of requests to Disc Golf Metrix.
 We are using the contents of discgolfmetrix/next_tournaments.js

*/
<div id="next-tournaments"></div>
<script>
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
</script>