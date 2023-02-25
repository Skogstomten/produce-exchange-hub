(function() {
    const deleteOrderLinks = document.getElementsByClassName("delete-order-link");
    for (const link of deleteOrderLinks) {
        link.onclick = function(event) {
            if (window.confirm(event.currentTarget.dataset.confirmmessage)) {
                event.currentTarget.parentElement.submit();
            }
        };
    }
}());
