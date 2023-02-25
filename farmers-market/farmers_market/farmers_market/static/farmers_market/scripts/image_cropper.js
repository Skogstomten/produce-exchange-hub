(function() {
    import Cropper from "https://cdn.jsdelivr.net/npm/cropperjs@1.5.13/dist/cropper.min.js"

    let cropper;

    let crop_image_elements = document.getElementsByClassName("crop-image");
    for (let element of crop_image_elements) {
        element.onchange = event => {
            let files = event.currentTarget.files;
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

    document.getElementById("modal_crop_image").addEventListener("shown.bs.modal", function() {
        cropper = new Cropper(document.getElementById("image"), {
            aspectRatio: 16 / 16,
            viewMode: 2,
            autoCropArea: 0.9,
        });
    });

    document.getElementById("model_crop_image").addEventListener("hidden.bs.modal", function() {
        cropper.destroy();
    });

    let crop_image_forms = document.getElementsByClassName("upload-cropped-image-form");
    for (let form of crop_image_forms) {
        form.onsubmit = () => {
            const data = cropper.getData(null);
            document.getElementById("id_x").value = data.x;
            document.getElementById("id_y").value = data.y;
            document.getElementById("id_width").value = data.width;
            document.getElementById("id_height").value = data.height;
            cropper.destroy();
            return true;
        };
    }
}());
