document.addEventListener('DOMContentLoaded', function() {
    const tipoInstitucionSelect = document.getElementById('tipo_institucion');
    const nivelEducativoSelect = document.getElementById('nivel_educativo');
    const empresasSection = document.getElementById('empresas-section');
    const empresasPlaceholder = document.getElementById('empresas-placeholder');
    const empresasContainer = document.getElementById('empresas-container');
    
    console.log('🔧 Filtro de empresas inicializado');

    function filtrarEmpresas() {
        const tipoInstitucion = tipoInstitucionSelect.value;
        const nivelEducativo = nivelEducativoSelect.value;

        console.log('🔄 Filtrando empresas:', { tipoInstitucion, nivelEducativo });

        // Si no se han seleccionado ambos criterios, mostrar placeholder y ocultar sección
        if (!tipoInstitucion || !nivelEducativo) {
            console.log('❌ Faltan criterios de selección');
            empresasPlaceholder.style.display = 'block';
            empresasSection.style.display = 'none';
            return;
        }

        // Ocultar placeholder y mostrar sección
        empresasPlaceholder.style.display = 'none';
        empresasSection.style.display = 'block';

        // Determinar si es institución local o externa
        const esTurismoIdentidad = tipoInstitucion === 'local';

        // Filtrar empresas
        const empresas = document.querySelectorAll('.lugar-item');
        let hayEmpresasVisibles = false;

        console.log('Empresas encontradas:', empresas.length);

        empresas.forEach(empresa => {
            // Verificar si la empresa coincide con el tipo de institución
            const categoriaElement = empresa.querySelector('.categoria');
            if (categoriaElement) {
                const categoriaEmpresa = categoriaElement.textContent.toLowerCase();
                const coincideTipo = esTurismoIdentidad ? 
                    categoriaEmpresa.includes('identidad') : 
                    !categoriaEmpresa.includes('identidad');

                console.log('Evaluando empresa:', {
                    categoria: categoriaEmpresa,
                    esTurismoIdentidad,
                    coincideTipo
                });

                if (coincideTipo) {
                    empresa.style.display = 'block';
                    hayEmpresasVisibles = true;
                } else {
                    empresa.style.display = 'none';
                    // Desmarcar el checkbox si la empresa está oculta
                    const checkbox = empresa.querySelector('input[type="checkbox"]');
                    if (checkbox) checkbox.checked = false;
                }
            }
        });

        // Si no hay empresas visibles, mostrar mensaje
        if (!hayEmpresasVisibles) {
            const contenedorOriginal = empresasContainer.innerHTML;
            const mensaje = `
                <div class="info-panel warning">
                    <p>⚠️ No hay empresas disponibles para ${esTurismoIdentidad ? 'Turismo de Identidad' : 'Turismo Educativo'} 
                       - Nivel ${nivelEducativo}</p>
                </div>
            `;
            // Guardar las empresas originales en un div oculto
            empresasContainer.innerHTML = `
                <div style="display: none" id="empresas-backup">${contenedorOriginal}</div>
                ${mensaje}
            `;
        } else {
            // Restaurar las empresas originales si existen
            const backup = document.getElementById('empresas-backup');
            if (backup) {
                empresasContainer.innerHTML = backup.innerHTML;
                // Volver a aplicar el filtrado
                filtrarEmpresas();
            }
        }
    }

    // Asignar eventos
    tipoInstitucionSelect.addEventListener('change', filtrarEmpresas);
    nivelEducativoSelect.addEventListener('change', filtrarEmpresas);

    // Ocultar empresas inicialmente
    empresasPlaceholder.style.display = 'block';
    empresasSection.style.display = 'none';
    
    // Filtrar al cargar la página
    filtrarEmpresas();
});
