const contenedor = document.getElementById("contenedorScanner");
const scanner = document.getElementById("scanner");
const resultado = document.getElementById("resultado");
const listaEscaneos = document.getElementById("listaEscaneos");
const botonPrestar = document.getElementById("botonPrestar");


// ==========================================
// MOSTRAR ESCANEOS GUARDADOS
// ==========================================

function mostrarEscaneos() {

    const escaneos = JSON.parse(
        localStorage.getItem("escaneosRecientes")
    ) || [];

    listaEscaneos.innerHTML = "";

    if (escaneos.length === 0) {

        listaEscaneos.innerHTML = `
            <p id="sinEscaneos">
                Todavía no has escaneado ningún libro.
            </p>
        `;

        return;
    }


    escaneos.forEach(libro => {

        const elemento = document.createElement("div");

        elemento.classList.add("book-item");

        elemento.innerHTML = `
            <div>
                <h4>${libro.titulo}</h4>
                <p>${libro.autor}</p>
                <small>
                    Escaneado a las ${libro.hora}
                </small>
            </div>
        `;

        listaEscaneos.appendChild(elemento);

    });

}


// ==========================================
// GUARDAR ESCANEO
// ==========================================

function guardarEscaneo(libro) {

    let escaneos = JSON.parse(
        localStorage.getItem("escaneosRecientes")
    ) || [];


    const nuevoEscaneo = {

        titulo: libro.titulo,

        autor: libro.autor,

        hora: new Date().toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        )

    };


    // Agregar al principio
    escaneos.unshift(nuevoEscaneo);


    // Guardar máximo 5
    escaneos = escaneos.slice(0, 5);


    localStorage.setItem(
        "escaneosRecientes",
        JSON.stringify(escaneos)
    );


    mostrarEscaneos();

}


// ==========================================
// INICIAR ESCÁNER
// ==========================================

contenedor.style.display = "block";

resultado.innerHTML = "Esperando lectura...";

scanner.focus();


// Mostrar historial guardado
mostrarEscaneos();


// Ocultar botón de préstamo al iniciar
if (botonPrestar) {
    botonPrestar.style.display = "none";
}


// ==========================================
// MANTENER FOCO
// ==========================================

window.addEventListener("click", () => {

    scanner.focus();

});


// ==========================================
// CUANDO EL LECTOR ENVÍA ENTER
// ==========================================

scanner.addEventListener("keydown", async function (e) {

    if (e.key !== "Enter") return;


    e.preventDefault();


    const codigo = scanner.value.trim();


    scanner.value = "";


    if (codigo === "") {

        scanner.focus();

        return;

    }


    resultado.textContent =
        "Buscando código: " + codigo;


    // Ocultar botón mientras busca
    if (botonPrestar) {
        botonPrestar.style.display = "none";
    }


    try {

        const respuesta = await fetch(
            "/buscar_codigo",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    codigo: codigo
                })

            }
        );


        const libro = await respuesta.json();


        // ==========================================
        // LIBRO ENCONTRADO
        // ==========================================

        if (libro.encontrado) {


            resultado.innerHTML = `

                <strong>
                    ${libro.titulo}
                </strong>

                <br>

                Autor:
                ${libro.autor}

                <br>

                Editorial:
                ${libro.editorial || "Sin editorial"}

                <br>

                Disponibles:
                ${libro.cantidad_disponible}

            `;


            // Guardar historial
            guardarEscaneo(libro);


            // ==========================================
            // BOTÓN PRESTAR
            // ==========================================

            if (botonPrestar) {

                if (libro.cantidad_disponible > 0) {

                    botonPrestar.style.display = "inline-flex";

                    botonPrestar.href =
                        "/prestamo?libro_id=" + libro.id;

                } else {

                    botonPrestar.style.display = "none";

                }

            }


            alert(

                "Libro encontrado\n\n" +

                "Título: " +
                libro.titulo +

                "\nAutor: " +
                libro.autor +

                "\nEditorial: " +
                (libro.editorial || "Sin editorial") +

                "\nDisponibles: " +
                libro.cantidad_disponible

            );


        }


        // ==========================================
        // LIBRO NO ENCONTRADO
        // ==========================================

        else {


            resultado.textContent =
                "Libro no registrado.";


            if (botonPrestar) {
                botonPrestar.style.display = "none";
            }


            alert(
                "Libro no registrado."
            );

        }


    }


    // ==========================================
    // ERROR
    // ==========================================

    catch (error) {


        console.error(
            "Error:",
            error
        );


        resultado.textContent =
            "Error al consultar el servidor.";


        if (botonPrestar) {
            botonPrestar.style.display = "none";
        }


        alert(
            "Error al consultar el servidor."
        );

    }


    scanner.focus();

});


// ==========================================
// AL CARGAR
// ==========================================

window.addEventListener("load", () => {

    scanner.focus();

});


// ==========================================
// AL VOLVER A LA PESTAÑA
// ==========================================

window.addEventListener("focus", () => {

    scanner.focus();

});