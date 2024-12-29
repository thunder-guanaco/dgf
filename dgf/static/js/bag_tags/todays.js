function goToSelectTodaysBagTags() {

    $("#todays-bag-tag-list").empty();
    $("#select-bag-tags .content .line:has(.number.selected)").clone().appendTo("#todays-bag-tag-list");
    $(".number").removeClass("selected");

    $(".at-least-2-bag-tags-hint").hide();

    showPage('#todays-bag-tags,#unassigned-bag-tags');

}
