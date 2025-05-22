document.addEventListener("DOMContentLoaded", function () {
    const spinner = document.getElementById("spinner");
    const datalist = document.getElementById("lista_empresas");

    // Mostrar el spinner al iniciar la carga
    spinner.style.display = "block";

    fetch("/todas_empresas")
        .then((response) => response.json())
        .then((data) => {
            spinner.style.display = "none"; // Ocultar el spinner
            datalist.innerHTML = "";
            data.forEach((empresa) => {
                const option = document.createElement("option");
                option.value = empresa.nombre;
                datalist.appendChild(option);
            });
        })
        .catch((error) => {
            spinner.style.display = "none"; // Ocultar el spinner
            console.error("Error al cargar las empresas:", error);
            alert("No se pudieron cargar las empresas. Intente nuevamente más tarde.");
        });
});