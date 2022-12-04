(function() {

$("#set_lang_sv").on("click", () => {
    set_lang("sv");
});

$("#set_lang_en").on("click", () => {
    set_lang("en");
});

function set_lang(lang) {
    $("#lang_code").value = lang;
    $("#set_lang_form").submit();
};

}())