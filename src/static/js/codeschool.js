$("#id_logo").change(function () {
    const reader = new FileReader();
    reader.onload = function (e) {
        // get loaded data and render thumbnail.
        $("#image")[0].src = e.target.result;
    };

    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
});