document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const inputEmpresa = document.getElementById("empresa");
    const inputFecha = document.getElementById("fecha");
    const inputHora = document.getElementById("hora");

    form.addEventListener("submit", function (event) {
        let errores = [];

        // Validar que se haya seleccionado una empresa
        if (!inputEmpresa.value.trim()) {
            errores.push("Debe seleccionar una empresa.");
        }

        // Validar que se haya ingresado una fecha
        if (!inputFecha.value) {
            errores.push("Debe ingresar una fecha.");
        }

        // Validar que se haya ingresado una hora
        if (!inputHora.value) {
            errores.push("Debe ingresar una hora.");
        }

        // Mostrar errores si existen
        if (errores.length > 0) {
            event.preventDefault(); // Evita el envío del formulario
            alert(errores.join("\n"));
        }
    });
});