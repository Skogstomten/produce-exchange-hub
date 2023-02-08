(function(){
    const searchableDropdowns = document.getElementsByClassName("searchable-dropdown");

    function addCreateNewEventHandler(el) {
        el.onclick = function(event) {
            alert("It's clicked!");
        };
    }

    for (const el of searchableDropdowns) {
        const input = el.getElementsByTagName("input")[0];
        const content = el.getElementsByClassName("dropdown-content")[0];
        input.onfocus = function () {
            options = content.getElementsByTagName("div");
            if (options.length < 1) {
                let addItemNode = document.createElement("div");
                addItemNode.appendChild(document.createTextNode("Create new"));
                addCreateNewEventHandler(addItemNode);
                content.appendChild(addItemNode);
            }

            content.classList.toggle("show");
        };

        input.onchange = function() {
            const options = content.getElementsByTagName("div");
            for (const option of options) {
                const text = option.innerText;
            }
        };
    }
}());
