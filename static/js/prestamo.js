const buscadorPrestamos = document.getElementById("buscadorPrestamos");
const filasPrestamos = document.querySelectorAll(".fila-prestamo");


function normalizarTexto(texto) {
    return texto
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();
}


if (buscadorPrestamos) {

    buscadorPrestamos.addEventListener("input", function () {

        const busqueda = normalizarTexto(
            buscadorPrestamos.value
        );

        filasPrestamos.forEach(function (fila) {

            const usuario = normalizarTexto(
                fila.dataset.usuario || ""
            );

            const libro = normalizarTexto(
                fila.dataset.libro || ""
            );

            const coincideUsuario = usuario.includes(busqueda);
            const coincideLibro = libro.includes(busqueda);

            if (coincideUsuario || coincideLibro) {

                fila.style.display = "";

            } else {

                fila.style.display = "none";

            }

        });

    });

}