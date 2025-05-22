// Este archivo JavaScript se encarga de manejar la lógica de autocompletar el correo
// al seleccionar una empresa en el formulario de consulta de empresa.
    document.addEventListener("DOMContentLoaded", function() {
        const inputEmpresa = document.getElementById("empresa");
        const inputCorreo = document.getElementById("correo");
        const datalist = document.getElementById("lista_empresas");
        let empresas = [];

        // Cargar empresas desde Flask
        fetch("/todas_empresas")
            .then(response => response.json())
            .then(data => {
                empresas = data;
                datalist.innerHTML = "";
                empresas.forEach(empresa => {
                    const option = document.createElement("option");
                    option.value = empresa.nombre;
                    datalist.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Error al cargar las empresas:", error);
                alert("No se pudieron cargar las empresas. Intente nuevamente más tarde.");
            });

        // Cuando se elige una empresa, autocompleta el correo
        inputEmpresa.addEventListener("input", function() {
            const seleccion = empresas.find(e => e.nombre === inputEmpresa.value);
            if (seleccion) {
                inputCorreo.value = seleccion.correo; // Autocompleta el correo
            } else {
                inputCorreo.value = ""; // Limpia el campo si no hay coincidencia
            }
        });
    });
