document.addEventListener("DOMContentLoaded", function () {

    const modal =
        document.getElementById("modalEditarPerfil");

    const abrir =
        document.getElementById("abrirEditarPerfil");

    const cerrar =
        document.getElementById("cerrarEditarPerfil");

    const cancelar =
        document.getElementById("cancelarEditarPerfil");

    const inputFoto =
        document.getElementById("foto_perfil");

    const imagenPreview =
        document.getElementById("imagenPreview");

    const sinFoto =
        document.getElementById("sinFotoPreview");


    /* ABRIR */

    abrir.addEventListener("click", function () {

        modal.classList.add("activo");

        document.body.style.overflow = "hidden";

    });


    /* CERRAR */

    function cerrarModal() {

        modal.classList.remove("activo");

        document.body.style.overflow = "";

    }


    cerrar.addEventListener(
        "click",
        cerrarModal
    );


    cancelar.addEventListener(
        "click",
        cerrarModal
    );


    /* Cerrar al pulsar fuera */

    modal.addEventListener("click", function (event) {

        if (event.target === modal) {

            cerrarModal();

        }

    });


    /* ESC */

    document.addEventListener("keydown", function (event) {

        if (
            event.key === "Escape" &&
            modal.classList.contains("activo")
        ) {

            cerrarModal();

        }

    });


    /* =========================================
       PREVISUALIZAR FOTO
    ========================================= */

    inputFoto.addEventListener("change", function () {

        const archivo =
            inputFoto.files[0];


        if (!archivo) {
            return;
        }


        const tiposPermitidos = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ];


        if (!tiposPermitidos.includes(archivo.type)) {

            alert(
                "Selecciona una imagen JPG, PNG o WEBP."
            );

            inputFoto.value = "";

            return;

        }


        const lector =
            new FileReader();


        lector.onload = function (event) {

            imagenPreview.src =
                event.target.result;

            imagenPreview.style.display =
                "block";


            if (sinFoto) {

                sinFoto.style.display =
                    "none";

            }

        };


        lector.readAsDataURL(
            archivo
        );

    });

});