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
