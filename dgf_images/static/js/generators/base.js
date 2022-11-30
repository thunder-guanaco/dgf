$(window).on("load", function() {
    loadLessMoreInput();
});

function capture(jquerySelector) {
    const element = document.querySelector(jquerySelector);
    html2canvas(element, {
        scale: 5,
        allowTaint: true,
    }).then(canvas => {
        download(canvas);
    });
}

function download(canvas) {
    const a = document.createElement("a")
    a.href = canvas.toDataURL()
    const now = new Date();
    const filename = now.toISOString().split('Z')[0].replace('T', '_')
    a.download = `generated_image_${filename}.png`
    a.dispatchEvent(new MouseEvent("click"))
}

function showIfChecked(selector, element) {
    $(selector).css('display', $(element).is(':checked') ? 'unset' : 'none');
}

function changeAbsolutePosition(selector, positions) {
    ["top", "bottom", "left", "right"].forEach((position) => {
        $(selector).css(position, "unset");
    });
    positions.forEach((position) => {
        $(selector).css(position, "0");
    });
}

function loadLessMoreInput() {
    $(".less-more-input .less").click(function(){
        input = $(this).parent().find('input')[0];
        input.stepDown();
        $(input).change();
    });
    $(".less-more-input .more").click(function(){
        input = $(this).parent().find('input')[0];
        input.stepUp();
        $(input).change();
    });
}