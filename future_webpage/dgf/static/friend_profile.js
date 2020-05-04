ALL_DISC_TYPES = ["P", "M", "F", "D"];

$(window).on("load", function() {
    scrollToErrors();
    loadInTheBag();
    loadFavoriteCourses();
    loadHighlights();
    loadAces();
    loadVideos();
    loadOther();
});

function loadInTheBag(){
    // append discs to the correct part
    $("#all-discs .disc").each(function(index) {
        type = $(this).children("select[id*='-type']").first().children("option[selected]").attr("value")
        if (type != "") {
            $(this).appendTo("#bag div[data-type=" + type + "]");
        }
        else {
            $(this).addClass("hidden");
        }
    });

    // hide all types
    $(".disc select[name$='-type']").addClass("hidden");

    // add empty disc to every part
    ALL_DISC_TYPES.forEach(function(type){
        addNewForm("discs", "#bag div[data-type=" + type + "]", "#empty-disc-form")
    });

    activateDiscChosen("#bag .chosen-select");
    hideParentElementsOnClick("#bag");
}

function activateDiscChosen(selector) {
    $(selector).chosen({
        disable_search_threshold: 10,
        width: "80%"
    });
    $(selector).on('change', function(event, params) {

        target = event.target;
        typeSelector = target.getAttribute("id").replace(/-disc$/g, "-type");
        targetType = $("#" + typeSelector).children("option:selected").val();

        bagPart = target.parentElement.parentElement;
        bagType = bagPart.getAttribute("data-type");

        if ("selected" in params && params.selected != "" && targetType == "") {

            console.log("Selected disc from bag part '" + bagType + "'");
            $("#" + typeSelector).find("option[value='" + bagType + "']").attr("selected", true);

            var new_index = addNewForm("discs", "#bag div[data-type=" + bagType + "]", "#empty-disc-form")
            console.log("Added new empty disc to bag part '" + bagType + "' with index: " + new_index)
            activateDiscChosen("select[name='discs-" + new_index + "-disc']");
        }
    });
}

function loadFavoriteCourses(){
    $("#favorite-courses select").chosen({
        disable_search_threshold: 10,
        width: "90%"
    });
    hideParentElementsOnClick("#favorite-courses");
}

function loadHighlights(){
    hideParentElementsOnClick("#highlights");
}

function loadAces() {

    activateAceChosen("#aces .ace select")

    hideGrandParentElementsOnClick("#aces");

    $("#add-ace").click(function(){
        var new_index = addNewForm("aces", "#aces", "#empty-ace-form");
        activateAceChosen("select[name='aces-" + new_index + "-disc']");
        activateAceChosen("select[name='aces-" + new_index + "-course']");
        activateAceChosen("select[name='aces-" + new_index + "-type']");
        activateAceChosen("select[name='aces-" + new_index + "-date_day']");
        activateAceChosen("select[name='aces-" + new_index + "-date_month']");
        activateAceChosen("select[name='aces-" + new_index + "-date_year']");
    });

}

function activateAceChosen(selector){
    $(selector).chosen({
        disable_search_threshold: 10,
        width: "70%"
    });
}

function loadVideos() {

    activateVideoChosen("#videos .field select");

    hideParentElementsOnClick("#videos");

    $("#add-video").click(function(){
        var new_index = addNewForm("videos", "#videos", "#empty-video-form");
        activateVideoChosen("select[name='videos-" + new_index + "-type']");
    });

}

function activateVideoChosen(selector){
    $(selector).chosen({
        disable_search_threshold: 10,
        width: "20%"
    });
}

function addNewForm(formset_id, parent_div_id, empty_form_id) {
    var form_index = $("#id_" + formset_id + "-TOTAL_FORMS").val();
    $(parent_div_id).append($(empty_form_id).html().replace(/__prefix__/g, form_index));
    $("#id_" + formset_id + "-TOTAL_FORMS").val(parseInt(form_index) + 1);
    return form_index;
}

function loadOther() {
    $("#id_division").chosen({
        disable_search_threshold: 10,
        width: "80%"
    });
}

function hideParentElementsOnClick(selector) {
    $(selector +  " input[name$='DELETE']").change(function() {
        $(this).parent().addClass("hidden");
    });
}

function hideGrandParentElementsOnClick(selector) {
    $(selector +  " input[name$='DELETE']").change(function() {
        $(this).parent().parent().addClass("hidden");
    });
}

function scrollToErrors() {

    if ($('.errorlist').length) {
        $('html, body').animate({
            scrollTop: ($('.errorlist').offset().top - $(".errorlist").height()*5)
        }, 500);
    }
}