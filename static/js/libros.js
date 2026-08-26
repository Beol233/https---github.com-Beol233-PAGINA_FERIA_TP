document.addEventListener("DOMContentLoaded", function () {

    /* =========================================
       ELEMENTOS DE LA PÁGINA
    ========================================= */

    const tarjetasLibros = Array.from(
        document.querySelectorAll(".tarjeta_libro")
    );

    const contenedorLibros =
        document.querySelector(".contenedor_libros");

    const contadorLibros =
        document.getElementById("contador_libros");

    const paginacion =
        document.getElementById("paginacion");

    const numerosPaginacion =
        document.getElementById("numeros_paginacion");

    const botonAnterior =
        document.getElementById("pagina_anterior");

    const botonSiguiente =
        document.getElementById("pagina_siguiente");


    /* =========================================
       CONFIGURACIÓN
    ========================================= */

    const librosPorPagina = 6;

    let paginaActual = 1;

    const totalLibros =
        tarjetasLibros.length;

    const totalPaginas =
        Math.ceil(
            totalLibros / librosPorPagina
        );


    /* =========================================
       SI NO HAY LIBROS
    ========================================= */

    if (totalLibros === 0) {

        if (paginacion) {
            paginacion.style.display = "none";
        }

        if (contadorLibros) {

            contadorLibros.innerHTML =
                "Mostrando <strong>0 libros</strong>";

        }

    } else {

        /* =====================================
           MOSTRAR PÁGINA
        ===================================== */

        function mostrarPagina(numeroPagina) {

            if (numeroPagina < 1) {
                numeroPagina = 1;
            }

            if (numeroPagina > totalPaginas) {
                numeroPagina = totalPaginas;
            }


            paginaActual =
                numeroPagina;


            const inicio =
                (paginaActual - 1) *
                librosPorPagina;


            const fin =
                inicio + librosPorPagina;


            tarjetasLibros.forEach(
                function (tarjeta, indice) {

                    if (
                        indice >= inicio &&
                        indice < fin
                    ) {

                        tarjeta.classList.remove(
                            "oculto_paginacion"
                        );

                    } else {

                        tarjeta.classList.add(
                            "oculto_paginacion"
                        );

                    }

                }
            );


            actualizarContador();

            crearBotones();

            actualizarFlechas();

        }


        /* =====================================
           CONTADOR
        ===================================== */

        function actualizarContador() {

            const primerLibro =
                (paginaActual - 1) *
                librosPorPagina + 1;


            const ultimoLibro =
                Math.min(
                    paginaActual *
                    librosPorPagina,

                    totalLibros
                );


            contadorLibros.innerHTML = `
                Mostrando
                <strong>
                    ${primerLibro} - ${ultimoLibro}
                    de ${totalLibros} libros
                </strong>
            `;

        }


        /* =====================================
           CREAR 1 - 2 - 3 - 4...
        ===================================== */

        function crearBotones() {

            numerosPaginacion.innerHTML = "";


            for (
                let pagina = 1;
                pagina <= totalPaginas;
                pagina++
            ) {

                const boton =
                    document.createElement("button");


                boton.type = "button";

                boton.textContent =
                    pagina;


                boton.setAttribute(
                    "aria-label",
                    "Ir a página " + pagina
                );


                if (
                    pagina === paginaActual
                ) {

                    boton.classList.add(
                        "pagina_actual"
                    );

                }


                boton.addEventListener(
                    "click",
                    function () {

                        mostrarPagina(
                            pagina
                        );

                        window.scrollTo({
                            top:
                                document
                                    .querySelector(
                                        ".seccion_libros"
                                    )
                                    .offsetTop - 30,

                            behavior: "smooth"
                        });

                    }
                );


                numerosPaginacion.appendChild(
                    boton
                );

            }

        }


        /* =====================================
           FLECHAS
        ===================================== */

        function actualizarFlechas() {

            botonAnterior.disabled =
                paginaActual === 1;


            botonSiguiente.disabled =
                paginaActual === totalPaginas;

        }


        /* =====================================
           ANTERIOR
        ===================================== */

        botonAnterior.addEventListener(
            "click",
            function () {

                if (
                    paginaActual > 1
                ) {

                    mostrarPagina(
                        paginaActual - 1
                    );

                }

            }
        );


        /* =====================================
           SIGUIENTE
        ===================================== */

        botonSiguiente.addEventListener(
            "click",
            function () {

                if (
                    paginaActual <
                    totalPaginas
                ) {

                    mostrarPagina(
                        paginaActual + 1
                    );

                }

            }
        );


        /* =====================================
           INICIAR
        ===================================== */

        mostrarPagina(1);

    }



    /* =========================================
       CAMBIO ENTRE CUADRÍCULA Y LISTA
    ========================================= */

    const botonesVista =
        document.querySelectorAll(
            ".boton_vista"
        );


    if (
        botonesVista.length >= 2 &&
        contenedorLibros
    ) {

        const botonCuadricula =
            botonesVista[0];

        const botonLista =
            botonesVista[1];


        /* =====================================
           CUADRÍCULA
        ===================================== */

        botonCuadricula.addEventListener(
            "click",
            function () {

                contenedorLibros.classList.remove(
                    "vista_lista"
                );


                botonCuadricula.classList.add(
                    "boton_vista_activo"
                );


                botonLista.classList.remove(
                    "boton_vista_activo"
                );


                localStorage.setItem(
                    "vistaLibros",
                    "cuadricula"
                );

            }
        );


        /* =====================================
           LISTA
        ===================================== */

        botonLista.addEventListener(
            "click",
            function () {

                contenedorLibros.classList.add(
                    "vista_lista"
                );


                botonLista.classList.add(
                    "boton_vista_activo"
                );


                botonCuadricula.classList.remove(
                    "boton_vista_activo"
                );


                localStorage.setItem(
                    "vistaLibros",
                    "lista"
                );

            }
        );


        /* =====================================
           RECORDAR VISTA
        ===================================== */

        const vistaGuardada =
            localStorage.getItem(
                "vistaLibros"
            );


        if (
            vistaGuardada === "lista"
        ) {

            contenedorLibros.classList.add(
                "vista_lista"
            );


            botonLista.classList.add(
                "boton_vista_activo"
            );


            botonCuadricula.classList.remove(
                "boton_vista_activo"
            );

        }

    }

});