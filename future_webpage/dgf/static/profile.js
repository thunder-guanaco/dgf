ALL_DISC_TYPES = ["P", "M", "F", "D"];

$(window).on("load", function() {

    // append discs to the correct part
    $("#all-discs .discs").each(function(index) {
        type = $(this).children("select[id*='-type']").first().children("option[selected]").attr("value")
        if (type != "") {
            $(this).appendTo("#bag div[data-type=" + type + "]");
        }
        else {
            $(this).addClass("hidden");
        }
    });

    // hide all types
    $("select[name$='-type']").addClass("hidden");

    // add empty disc to every part
    ALL_DISC_TYPES.forEach(function(type){
        addNewDisc(type);
    });

    activateChosen($("#bag .chosen-select"));
    hideDeletedElements();

});

function activateChosen(selector) {
    selector.chosen({
        disable_search_threshold: 10,
        width: "80%"
    });
    selector.on('change', function(event, params) {

        target = event.target;
        typeSelector = target.getAttribute("id").replace(/-disc$/g, "-type");
        targetType = $("#" + typeSelector).children("option:selected").val();

        bagPart = target.parentElement.parentElement;
        bagType = bagPart.getAttribute("data-type");

        if ("selected" in params && params.selected != "" && targetType == "") {

            console.log("Selected disc from bag part '" + bagType + "'");
            $("#" + typeSelector).find("option[value='" + bagType + "']").attr("selected", true);

            var new_index = addNewDisc(bagType);
            console.log("Added new empty disc to bag part '" + bagType + "' with index: " + new_index)
            activateChosen($("select[name='discs-" + new_index + "-disc']"));
        }
    });
}

function addNewDisc(type) {
    var form_index = $('#id_discs-TOTAL_FORMS').val();
    $('#bag div[data-type=' + type + ']').append($('#empty-form').html().replace(/__prefix__/g, form_index).replace("display: none;", ""));
    $('#id_discs-TOTAL_FORMS').val(parseInt(form_index) + 1);
    return form_index;
}

function hideDeletedElements() {
    $("input[name$='DELETE']").change(function() {
        $(this).parent().addClass("hidden");
    });
}