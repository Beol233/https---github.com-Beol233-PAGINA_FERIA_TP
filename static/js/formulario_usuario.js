document.addEventListener("DOMContentLoaded", function () {

    const password =
        document.getElementById("password");

    const confirmar =
        document.getElementById("confirmar");

    const verPassword =
        document.getElementById("verPassword");

    const verConfirmar =
        document.getElementById("verConfirmar");


    /* =========================================
       MOSTRAR / OCULTAR CONTRASEÑA
    ========================================= */

    if (password && verPassword) {

        verPassword.addEventListener(
            "click",
            function () {

                cambiarVisibilidad(
                    password,
                    verPassword
                );

            }
        );

    }


    /* =========================================
       MOSTRAR / OCULTAR CONFIRMACIÓN
    ========================================= */

    if (confirmar && verConfirmar) {

        verConfirmar.addEventListener(
            "click",
            function () {

                cambiarVisibilidad(
                    confirmar,
                    verConfirmar
                );

            }
        );

    }


    /* =========================================
       FUNCIÓN GENERAL
    ========================================= */

    function cambiarVisibilidad(
        input,
        boton
    ) {

        const icono =
            boton.querySelector("i");


        if (input.type === "password") {

            input.type = "text";

            icono.classList.remove(
                "bi-eye"
            );

            icono.classList.add(
                "bi-eye-slash"
            );

            boton.setAttribute(
                "aria-label",
                "Ocultar contraseña"
            );

        } else {

            input.type = "password";

            icono.classList.remove(
                "bi-eye-slash"
            );

            icono.classList.add(
                "bi-eye"
            );

            boton.setAttribute(
                "aria-label",
                "Mostrar contraseña"
            );

        }

    }

});