window.blazorCulture = {
    get: () => window.localStorage['BlazorCulture'],
    set: (value) => window.localStorage['BlazorCulture'] = value
};

window.setFocus = (id) => {
    var element = document.getElementById(id);
    element.focus();
};

window.addClass = (element, cls) => {
    element.classList.add(cls);
};

window.removeClass = (element, cls) => {
    element.classList.remove(cls);
};