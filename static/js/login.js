const botones = document.querySelectorAll(".tipo_usuario button");

botones.forEach(boton => {
    boton.addEventListener("click", () => {

        botones.forEach(b => b.classList.remove("activo"));

        boton.classList.add("activo");
    });
});