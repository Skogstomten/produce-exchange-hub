(function () {
    let elements = document.getElementsByClassName("data-link");
    for (let element of elements) {
        element.onclick = (event) => {
            window.location = event.currentTarget.dataset.href;
        };
    }

    let forms = document.getElementsByClassName("confirm-action");
    for (let form of forms) {
        form.onsubmit = (event) => {
            try {
                return window.confirm(event.currentTarget.dataset.confirmmessage)
            } catch (err) {
                console.error(err)
            }
            return false
        };
    }
}());
