(function () {
    let elements = document.getElementsByClassName("data-link");
    for (let element of elements) {
        element.onclick = (event) => {
            window.location = event.currentTarget.dataset.href;
        };
    }
}());
