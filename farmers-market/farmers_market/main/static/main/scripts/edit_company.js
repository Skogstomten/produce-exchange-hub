(function() {
    let cropper;

    document.getElementById("id_profile_picture").onchange = () => {
        if (this.files && this.files[0]) {
            let image = document.getElementById("image")
            let reader = new FileReader();
            reader.onload = function(e) {
                image.src = e.target.result;
            };
            reader.readAsDataURL(this.files[0]);

            $("#model_crop_image").modal("show");
        }
    };
    
    $("#model_crop_image").on("shown.bs.modal", () => {
        cropper = new Cropper(document.getElementById("image"), {
            aspectRatio: 16 / 16,
            viewMode: 2,
            autoCropArea: 0.9,
        });
    });

    $("#model_crop_image").on("hidden.bs.modal", () => {
        cropper.destroy();
    });

    document.getElementById("profile_picture_upload").onsubmit = () => {
        const data = cropper.getData();
        document.getElementById("id_x").value = data.x;
        document.getElementById("id_y").value = data.y;
        document.getElementById("id_width").value = data.width;
        document.getElementById("id_height").value = data.height;
        cropper.destroy();
        return true;
    };

    let forms = document.getElementsByClassName("delete_contact_form");
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
