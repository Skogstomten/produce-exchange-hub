(function () {
    let elements = document.getElementsByClassName("data-link");
    for (let element of elements) {
        element.onclick = (event) => {
            let url = event.currentTarget.dataset.href;
            window.location = url;
        };
    }
}());
