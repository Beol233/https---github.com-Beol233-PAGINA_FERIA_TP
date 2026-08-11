const contenedor = document.getElementById("contenedorScanner");
const scanner = document.getElementById("scanner");
const resultado = document.getElementById("resultado");

// Mostrar el escáner automáticamente
contenedor.style.display = "block";
resultado.innerHTML = "Esperando lectura...";
scanner.focus();

// Mantener el foco en el input oculto
window.addEventListener("click", () => {
    scanner.focus();
});

// Cuando el escáner envía ENTER
scanner.addEventListener("keydown", async function (e) {

    if (e.key !== "Enter") return;

    e.preventDefault();

    const codigo = scanner.value.trim();

    // Limpiar el input para la siguiente lectura
    scanner.value = "";

    if (codigo === "") {
        scanner.focus();
        return;
    }

    // Mostrar el código leído
        resultado.textContent = codigo;
    try {

        const respuesta = await fetch("/buscar_codigo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                codigo: codigo
            })
        });

        const libro = await respuesta.json();

        if (libro.encontrado) {

            alert(
                "Libro encontrado\n\n" +
                "Título: " + libro.titulo +
                "\nAutor: " + libro.autor +
                "\nEditorial: " + libro.editorial
            );

        } else {

            alert("Libro no registrado.");

        }

    } catch (error) {

        console.error("Error:", error);
        alert("Error al consultar el servidor.");

    }


});

// Al cargar la página, asegurar que el foco esté en el input
window.addEventListener("load", () => {
    scanner.focus();
});

// Si el usuario cambia de pestaña y vuelve, recuperar el foco
window.addEventListener("focus", () => {
    scanner.focus();
});