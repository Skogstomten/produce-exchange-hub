window.blazorCulture = {
    get: () => window.localStorage['BlazorCulture'],
    set: (value) => window.localStorage['BlazorCulture'] = value
};

window.setFocus = (id) => {
    var element = document.getElementById(id);
    element.focus();
};