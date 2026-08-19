const botones = document.querySelectorAll(".tipo_usuario button");

botones.forEach(boton => {
    boton.addEventListener("click", () => {

        botones.forEach(b => b.classList.remove("activo"));

        boton.classList.add("activo");
    });
});

const password = document.getElementById("password");
const verPassword = document.getElementById("verPassword");

verPassword.addEventListener("click", function () {

    if (password.type === "password") {
        password.type = "text";
        verPassword.innerHTML = '<i class="bi bi-eye-slash"></i>';
    } else {
        password.type = "password";
        verPassword.innerHTML = '<i class="bi bi-eye"></i>';
    }

});
