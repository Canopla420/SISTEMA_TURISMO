document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const nivelEducativoSelect = document.getElementById('nivel_educativo');
    const empresasContainer = document.getElementById('empresas-container');
    const empresasItems = document.querySelectorAll('.lugar-item');

    // Función para filtrar empresas según el nivel educativo
    function filtrarEmpresas() {
        const nivelEducativo = nivelEducativoSelect.value;
        
        empresasItems.forEach(item => {
            const empresaNivelEducativo = item.dataset.nivelEducativo;
            
            // Mostrar empresa si coincide con el nivel educativo seleccionado
            if (empresaNivelEducativo.includes(nivelEducativo)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Agregar evento para cambios en el nivel educativo
    if (nivelEducativoSelect) {
        nivelEducativoSelect.addEventListener('change', filtrarEmpresas);
    }

    // Filtrado inicial
    filtrarEmpresas();
});