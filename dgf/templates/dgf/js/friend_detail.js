{% load dgf %}

$(window).on("load", function() {

    {% all_friends as friends %}

    // first we try to replace using the first and last name together
    {% for friend in friends %}
        replaceText("{{friend.first_and_last_name}}", "{{friend.short_name}}", "{% url 'dgf:friend_detail' friend.slug %}");
    {% endfor %}

    // and then we try to replace using only the short name (nickname or fist name)
    {% for friend in friends %}
        replaceText("{{friend.short_name}}", "{{friend.short_name}}", "{% url 'dgf:friend_detail' friend.slug %}");
    {% endfor %}

});

function replaceText(text, newText, url) {
    $(".container p:contains('" + text + "'):not(:has(*))").each(function() {
        this.innerHTML = this.innerHTML.replace(text, "<a href=\"" + url + "\">" + newText + "</a>");
    });
}