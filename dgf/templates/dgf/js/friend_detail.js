{% load dgf %}

$(window).on("load", function() {

    {% all_friends as friends %}

    {% for friend in friends %}

        ["{{friend.username}}", "{{friend.nickname}}", "{{friend.first_name}}"].forEach(function(text){

            if (text != null) {
                $(".container p:contains('" + text + "')").each(function(){
                    this.innerHTML = this.innerHTML.replace(text, "<a href=\"{% url 'dgf:friend_detail' friend.slug %}\">" + text + "</a>");
                });
            }
        });

    {% endfor %}

});