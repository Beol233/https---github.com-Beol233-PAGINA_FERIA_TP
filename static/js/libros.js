const boton = document.getElementById("btnEscaner");
const contenedor = document.getElementById("contenedorScanner");
const scanner = document.getElementById("scanner");
const resultado = document.getElementById("resultado");

let activo = false;

// Mostrar/Ocultar lector
boton.addEventListener("click", () => {

    activo = !activo;

    if (activo) {
        contenedor.style.display = "block";
        resultado.innerHTML = "Esperando lectura...";
        scanner.focus();

    } else {

        contenedor.style.display = "none";
        scanner.value = "";

    }
});

// Mantener el foco en el input oculto
window.addEventListener("click", () => {

    if (activo) {
        scanner.focus();
    }

});

// Cuando el escáner envía ENTER
scanner.addEventListener("keydown", async function (e) {

    if (e.key !== "Enter") return;

    e.preventDefault();

    const codigo = scanner.value.trim();

    scanner.value = "";

    if (codigo === "") return;

    resultado.innerHTML =
        "<strong>Código:</strong> " + codigo;

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
        console.error(error);
        alert("Error al consultar el servidor.");
    }
    scanner.focus();
});

