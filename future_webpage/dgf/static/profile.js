ALL_DISC_TYPES = ["P", "M", "F", "D"];

$(window).on("load", function() {

    // append discs to the correct part
    $("#all-discs .discs").each(function(index) {
        type = $(this).children("select[id*='-type']").first().children("option[selected]").attr("value")
        if (type != "") {
            $(this).appendTo("#bag-" + type);
        }
        else {
            $(this).hide();
        }
    });

    // add empty disc to every part
    ALL_DISC_TYPES.forEach(function(type){
        addNewDisc(type);
    });

    // activate chosen
    activateChosen();

});

function activateChosen() {
    $("#bag .chosen-select").chosen({
        disable_search_threshold: 10,
        width: "90%"
    });
    ALL_DISC_TYPES.forEach(function(type){
        $("#bag-" + type + " .chosen-select").on('change', function(event, params) {
            if ("selected" in params) {
                console.log("selected disc from part: " + type)
                addNewDisc(type);
                activateChosen();
            }
        });
    });
}

function addNewDisc(type) {
    var form_index = $('#id_discs-TOTAL_FORMS').val();
    console.log('index: ' + form_index)
    $('#bag-' + type).append($('#empty-form').html().replace(/__prefix__/g, form_index).replace("display: none;", ""));
    $('#id_discs-TOTAL_FORMS').val(parseInt(form_index) + 1);
}