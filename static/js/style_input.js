document.querySelector(".upload-file-btn-wrap").addEventListener("click", () => {
    const clickEvent = document.createEvent('MouseEvents');

    clickEvent.initMouseEvent('click', true, true, window,
        0, 0, 0, 0, 0,
        false, false, false, false, 0, null);

    document.querySelector(".upload-file-btn").dispatchEvent(clickEvent);
});