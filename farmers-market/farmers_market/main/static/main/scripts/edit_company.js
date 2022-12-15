(function() {
    $("#id_profile_picture").on("change", function() {
        if (this.files && this.files[0]) {
            const image = $("#image");
            const reader = new FileReader();
            reader.onload = function(e) {
                image.attr("src", e.target.result);
            };
            reader.readAsDataURL(this.files[0]); 

            $("#model_crop_image").modal("show");
        }
    });

    let cropper;
    $("#model_crop_image").on("shown.bs.modal", function() {
        cropper = new Cropper(image, {
            aspectRatio: 16 / 16,
            viewMode: 2,
            autoCropArea: 0.9,
            crop: function(event) {
                console.log(event);
            },
        });
    });
}());