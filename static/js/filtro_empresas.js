/**
 * Script para el filtrado dinámico de empresas según tipo de institución y nivel educativo
 */

document.addEventListener('DOMContentLoaded', function() {
    const localidadInput = document.getElementById('localidad');
    const tipoInstitucionSelect = document.getElementById('tipo_institucion');
    const nivelEducativoSelect = document.getElementById('nivel_educativo');
    const empresasContainer = document.getElementById('empresas-container');
    const cargandoEmpresasP = document.getElementById('cargando-empresas');
    
    console.log('🔧 Filtro de empresas inicializado');
    console.log('📍 Elementos encontrados:', {
        localidad: !!localidadInput,
        tipoInstitucion: !!tipoInstitucionSelect,
        nivelEducativo: !!nivelEducativoSelect,
        empresasContainer: !!empresasContainer,
        cargandoEmpresas: !!cargandoEmpresasP
    });
    
    // Función para determinar si la institución es de Esperanza
    function esDeEsperanza() {
        const tipoInstitucion = tipoInstitucionSelect ? tipoInstitucionSelect.value : '';
        const localidad = localidadInput ? localidadInput.value.toLowerCase() : '';
        
        console.log('🔍 Determinando tipo de institución:', { tipoInstitucion, localidad });
        
        // Priorizar el campo tipo_institucion si existe y está seleccionado
        if (tipoInstitucion === 'local') {
            console.log('✅ Institución LOCAL detectada');
            return true;
        } else if (tipoInstitucion === 'externa') {
            console.log('✅ Institución EXTERNA detectada');
            return false;
        }
        
        // Fallback: detectar por localidad
        const esEsperanzaPorLocalidad = localidad.includes('esperanza');
        console.log('🔍 Detección por localidad:', esEsperanzaPorLocalidad);
        return esEsperanzaPorLocalidad;
    }
    
    // Función para limpiar la lista de empresas
    function limpiarListaEmpresas() {
        if (empresasContainer) {
            empresasContainer.innerHTML = '';
        }
    }
    
    // Función para cargar empresas filtradas
    function cargarEmpresasFiltradas() {
        console.log('🚀 Iniciando carga de empresas filtradas');
        
        const nivelEducativo = nivelEducativoSelect ? nivelEducativoSelect.value : '';
        
        console.log('📊 Parámetros de filtrado:', {
            nivelEducativo: nivelEducativo,
            tipoInstitucion: tipoInstitucionSelect ? tipoInstitucionSelect.value : '',
            localidad: localidadInput ? localidadInput.value : ''
        });
        
        if (!nivelEducativo) {
            console.log('⚠️ Nivel educativo no seleccionado');
            if (cargandoEmpresasP) {
                cargandoEmpresasP.textContent = 'Seleccione el nivel educativo para ver las opciones disponibles.';
                cargandoEmpresasP.style.display = 'block';
            }
            limpiarListaEmpresas();
            return;
        }
        
        const esEsperanza = esDeEsperanza();
        
        if (cargandoEmpresasP) {
            cargandoEmpresasP.textContent = 'Cargando empresas disponibles...';
            cargandoEmpresasP.style.display = 'block';
        }
        
        // Construir URL con parámetros
        const url = `/empresas_filtradas?es_de_esperanza=${esEsperanza}&nivel_educativo=${nivelEducativo}`;
        console.log('🌐 Realizando petición a:', url);
        
        fetch(url)
            .then(response => {
                console.log('📡 Respuesta recibida:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(empresas => {
                console.log('📋 Empresas recibidas:', empresas.length);
                console.log('📄 Datos:', empresas);
                actualizarListaEmpresas(empresas, esEsperanza, nivelEducativo);
            })
            .catch(error => {
                console.error('❌ Error al cargar empresas:', error);
                if (cargandoEmpresasP) {
                    cargandoEmpresasP.textContent = 'Error al cargar las empresas. Intente nuevamente.';
                    cargandoEmpresasP.style.display = 'block';
                }
            });
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
    
    // Event listeners
    if (tipoInstitucionSelect) {
        tipoInstitucionSelect.addEventListener('change', function() {
            console.log('🔄 Cambio en tipo de institución:', this.value);
            cargarEmpresasFiltradas();
        });
    }
    
    if (localidadInput) {
        localidadInput.addEventListener('input', function() {
            console.log('🔄 Cambio en localidad:', this.value);
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(cargarEmpresasFiltradas, 500);
        });
    }
    
    if (nivelEducativoSelect) {
        nivelEducativoSelect.addEventListener('change', function() {
            console.log('🔄 Cambio en nivel educativo:', this.value);
            cargarEmpresasFiltradas();
        });
    }
    
    console.log('✅ Event listeners configurados');
});
