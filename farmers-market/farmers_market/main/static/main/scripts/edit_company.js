(function() {
    let cropper;

    let crop_image_elements = document.getElementsByClassName("crop-image");
    for (let element of crop_image_elements) {
        element.onchange = event => {
            files = event.currentTarget.files;
            if (files && files[0]) {
                let image = document.getElementById("image")
                let reader = new FileReader();
                reader.onload = function(e) {
                    image.src = e.target.result;
                };
                reader.readAsDataURL(files[0]);

                $("#model_crop_image").modal("show");
            }
        }
    }

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

    let crop_image_forms = document.getElementsByClassName("upload-cropped-image-form");
    for (let form of crop_image_forms) {
        form.onsubmit = () => {
            const data = cropper.getData();
            document.getElementById("id_x").value = data.x;
            document.getElementById("id_y").value = data.y;
            document.getElementById("id_width").value = data.width;
            document.getElementById("id_height").value = data.height;
            cropper.destroy();
            return true;
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
