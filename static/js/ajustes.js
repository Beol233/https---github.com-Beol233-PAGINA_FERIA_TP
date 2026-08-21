const modoOscuro = document.getElementById("modoOscuro");
const notificaciones = document.getElementById("notificaciones");
const idioma = document.getElementById("idioma");

// Aplicar el modo oscuro guardado en cualquier página
if (localStorage.getItem("modoOscuro") === "activado") {
    document.body.classList.add("oscuro");
}

// Esta parte solo funciona si estamos en ajustes.html
if (modoOscuro) {

    if (localStorage.getItem("modoOscuro") === "activado") {
        modoOscuro.checked = true;
    }

    modoOscuro.addEventListener("change", function () {

        if (modoOscuro.checked) {

            document.body.classList.add("oscuro");
            localStorage.setItem("modoOscuro", "activado");

        } else {

            document.body.classList.remove("oscuro");
            localStorage.setItem("modoOscuro", "desactivado");

        }

    });

}

// Notificaciones
if (notificaciones) {

    if (localStorage.getItem("notificaciones") === "activadas") {
        notificaciones.checked = true;
    }

    notificaciones.addEventListener("change", function () {

        if (notificaciones.checked) {

            localStorage.setItem("notificaciones", "activadas");

        } else {

            localStorage.setItem("notificaciones", "desactivadas");

        }

    });

}

// Idioma
if (idioma) {

    const idiomaGuardado = localStorage.getItem("idioma");

    if (idiomaGuardado) {
        idioma.value = idiomaGuardado;
    }

    idioma.addEventListener("change", function () {

        localStorage.setItem("idioma", idioma.value);

    });

}