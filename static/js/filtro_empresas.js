/**
 * Script para el filtrado dinámico de empresas según tipo de institución y nivel educativo
 */

document.addEventListener('DOMContentLoaded', function() {
    const tipoInstitucionSelect = document.getElementById('tipo_institucion');
    const nivelEducativoSelect = document.getElementById('nivel_educativo');
    const empresasContainer = document.getElementById('empresas-container');
    
    console.log('🔧 Filtro de empresas inicializado');
    
    // Función para actualizar la visibilidad de las empresas
    function actualizarEmpresas() {
        const tipoInstitucion = tipoInstitucionSelect.value;
        const nivelEducativo = nivelEducativoSelect.value;

        console.log('� Actualizando empresas:', { tipoInstitucion, nivelEducativo });

        // Si ambos campos están seleccionados
        if (tipoInstitucion && nivelEducativo) {
            empresasPlaceholder.style.display = 'none';
            empresasSection.style.display = 'block';

            // Obtener todas las empresas
            const empresas = document.querySelectorAll('.lugar-item');
            let empresasVisibles = false;

            // Filtrar empresas según los criterios seleccionados
            empresas.forEach(empresa => {
                const empresaTipo = empresa.dataset.tipoInstitucion;
                const empresaNivel = empresa.dataset.nivelEducativo;
                
                console.log('Evaluando empresa:', {
                    tipo: empresaTipo,
                    nivel: empresaNivel,
                    coincideTipo: empresaTipo === tipoInstitucion || empresaTipo === 'ambos',
                    coincideNivel: empresaNivel === nivelEducativo || empresaNivel === 'ambos'
                });

                // Mostrar solo las empresas que coinciden con ambos criterios
                if (
                    (empresaTipo === tipoInstitucion || empresaTipo === 'ambos') &&
                    (empresaNivel === nivelEducativo || empresaNivel === 'ambos')
                ) {
                    empresa.style.display = 'block';
                    empresasVisibles = true;
                } else {
                    empresa.style.display = 'none';
                    // Desmarcar el checkbox si la empresa está oculta
                    const checkbox = empresa.querySelector('input[type="checkbox"]');
                    if (checkbox) checkbox.checked = false;
                }
            });

            // Mostrar mensaje si no hay empresas disponibles
            if (!empresasVisibles) {
                empresasSection.innerHTML = `
                    <div class="info-panel warning">
                        <p>⚠️ No hay empresas disponibles para el tipo de institución y nivel educativo seleccionados.</p>
                    </div>
                `;
            }
        } else {
            // Si falta algún campo, mostrar el placeholder
            empresasPlaceholder.style.display = 'block';
            empresasSection.style.display = 'none';
        }
    }
    
    // Función para actualizar la lista de empresas en el DOM
    function actualizarListaEmpresas(empresas, esEsperanza, nivelEducativo) {
        console.log('🎨 Actualizando DOM con', empresas.length, 'empresas');
        
        if (!empresasContainer) {
            console.error('❌ Container de empresas no encontrado');
            return;
        }
        
        // Limpiar contenedor
        empresasContainer.innerHTML = '';
        
        if (empresas.length === 0) {
            const tipoCategoria = esEsperanza ? 'Turismo de Identidad' : 'Turismo Educativo';
            if (cargandoEmpresasP) {
                cargandoEmpresasP.textContent = `No hay empresas disponibles para ${tipoCategoria} - ${nivelEducativo}`;
                cargandoEmpresasP.style.display = 'block';
            }
            console.log('ℹ️ No hay empresas disponibles para los criterios seleccionados');
            return;
        }
        
        // Ocultar mensaje de carga
        if (cargandoEmpresasP) {
            cargandoEmpresasP.style.display = 'none';
        }
        
        // Crear elementos para cada empresa
        empresas.forEach((empresa, index) => {
            console.log(`🏢 Creando elemento para empresa ${index + 1}:`, empresa.nombre);
            
            const empresaDiv = document.createElement('div');
            empresaDiv.className = 'lugar-item empresa-item';
            
            empresaDiv.innerHTML = `
                <label for="empresa_${empresa.id}" class="empresa-label">
                    <input type="checkbox" id="empresa_${empresa.id}" name="lugares[]" value="${empresa.nombre}">
                    <div class="empresa-info">
                        <div class="empresa-header">
                            <strong class="empresa-nombre">${empresa.nombre}</strong>
                            <span class="categoria-badge ${empresa.categoria_turismo}">
                                ${empresa.categoria_turismo === 'identidad' ? 'Identidad' : 'Educativo'}
                            </span>
                        </div>
                        <div class="empresa-detalles">
                            <span class="direccion">📍 ${empresa.direccion || 'Dirección no especificada'}</span>
                            <span class="servicios">🎯 ${empresa.servicios_ofrecidos || 'Servicios no especificados'}</span>
                            ${empresa.costo_por_persona ? `<span class="costo">💰 $${empresa.costo_por_persona} por persona</span>` : ''}
                        </div>
                    </div>
                </label>
            `;
            
            empresasContainer.appendChild(empresaDiv);
        });
        
        // Agregar información de ayuda
        const infoDiv = document.createElement('div');
        infoDiv.className = 'info-categorias';
        infoDiv.style.cssText = `
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.9em;
        `;
        
        const tipoCategoria = esEsperanza ? 'Turismo de Identidad' : 'Turismo Educativo';
        const descripcion = esEsperanza ? 
            'Visitas enfocadas en mostrar la identidad y cultura local de Esperanza.' :
            'Visitas educativas para instituciones externas que desean conocer la región.';
        
        infoDiv.innerHTML = `
            <h4 style="margin-top: 0; color: #495057;">ℹ️ ${tipoCategoria} - ${nivelEducativo}</h4>
            <p style="margin-bottom: 0; color: #6c757d;">${descripcion}</p>
        `;
        
        empresasContainer.appendChild(infoDiv);
        
        console.log('✅ DOM actualizado correctamente');
    }
    
    // Escuchar cambios en los selectores
    tipoInstitucionSelect.addEventListener('change', actualizarEmpresas);
    nivelEducativoSelect.addEventListener('change', actualizarEmpresas);

    // Inicializar el estado
    actualizarEmpresas();
    
    console.log('✅ Event listeners configurados');
});
