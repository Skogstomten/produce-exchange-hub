(function(){
    const searchableDropdowns = document.getElementsByClassName("searchable-dropdown");
    for (const el of searchableDropdowns) {
        const input = el.getElementsByTagName("input")[0]
        const content = el.getElementsByClassName("dropdown-content")[0]
        input.onfocus = function () {
            content.classList.toggle("show")
        };

        input.onchange = function() {
            const options = content.getElementsByTagName("div")
            for (const option of options) {
                const text = option.innerText;
            }
        };
    }
}());