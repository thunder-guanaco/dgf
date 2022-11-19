function capture(jquerySelector) {
    html2canvas(document.querySelector(jquerySelector)).then(canvas => {
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