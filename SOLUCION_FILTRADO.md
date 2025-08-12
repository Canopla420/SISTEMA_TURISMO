# 🔧 GUÍA DE SOLUCIÓN: Empresas no aparecen en el formulario

## ❗ PROBLEMA IDENTIFICADO
Las empresas no se muestran cuando seleccionas el tipo de institución y nivel educativo.

## 🛠️ SOLUCIÓN PASO A PASO

### PASO 1: Verificar que hay empresas en la base de datos
```powershell
python -c "from app import app, db, EmpresaTuristica; app.app_context().push(); print('Empresas:', EmpresaTuristica.query.count())"
```

Si muestra 0 empresas, ejecuta:
```powershell
python init_db.py
```

### PASO 2: Ejecutar la aplicación
```powershell
python app.py
```

### PASO 3: Probar el sistema
1. Ve a: **http://localhost:5000**
2. Haz clic en **"Cargar nueva visita"**
3. **Abre las herramientas de desarrollador del navegador (F12)**
4. Ve a la pestaña **"Console"**
5. Completa el formulario:
   - **Nombre de institución**: "Escuela Test"
   - **Localidad**: "Santa Fe" (para externa) o "Esperanza" (para local)
   - **Tipo de institución**: Selecciona "Local" o "Externa"
   - **Nivel educativo**: Selecciona "Primario" o "Secundario"

### PASO 4: Observar los logs en la consola
Deberías ver mensajes como:
- ✅ `🔧 Filtro de empresas inicializado`
- ✅ `🔄 Cambio en tipo de institución: local`
- ✅ `🚀 Iniciando carga de empresas filtradas`
- ✅ `📡 Respuesta recibida: 200`
- ✅ `📋 Empresas recibidas: X`

### PASO 5: Si NO aparecen empresas, revisar:

#### A) Verificar que el JavaScript se carga:
- En la consola del navegador, busca errores en rojo
- Si hay error "404" para `filtro_empresas.js`, el archivo no se está sirviendo

#### B) Verificar ruta del filtrado manualmente:
- Ve a: http://localhost:5000/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Primario
- Deberías ver un JSON con empresas

#### C) Verificar elementos HTML:
- En la consola del navegador, ejecuta:
```javascript
console.log('Elementos:', {
  tipoInstitucion: document.getElementById('tipo_institucion'),
  nivelEducativo: document.getElementById('nivel_educativo'),
  empresasContainer: document.getElementById('empresas-container')
});
```

## 🚨 SOLUCIONES RÁPIDAS

### Si el JavaScript no funciona:
1. Refresca la página con **Ctrl+F5**
2. Verifica que el archivo existe: `static/js/filtro_empresas.js`

### Si no hay empresas en la BD:
```powershell
python -c "
from app import app, db, EmpresaTuristica
with app.app_context():
    db.create_all()
    if EmpresaTuristica.query.count() == 0:
        e1 = EmpresaTuristica(nombre='Museo Test', correo='test@test.com', categoria_turismo='identidad', nivel_educativo_objetivo='Primario', activa=True)
        e2 = EmpresaTuristica(nombre='Granja Test', correo='test2@test.com', categoria_turismo='educativo', nivel_educativo_objetivo='Secundario', activa=True)
        db.session.add(e1)
        db.session.add(e2)
        db.session.commit()
        print('Empresas creadas:', EmpresaTuristica.query.count())
"
```

### Si el filtrado no responde:
1. Verifica que la ruta `/empresas_filtradas` funciona
2. Revisa que los parámetros se envían correctamente
3. Asegúrate de que `es_de_esperanza` sea `true` o `false` (no otros valores)

## ✅ VERIFICACIÓN FINAL
Cuando funcione correctamente verás:
1. Al seleccionar **"Institución Local"** → aparecen empresas de **"Turismo de Identidad"**
2. Al seleccionar **"Institución Externa"** → aparecen empresas de **"Turismo Educativo"**
3. El filtro por nivel educativo reduce las opciones mostradas

## 🆘 SI NADA FUNCIONA
Ejecuta este comando para restablecer todo:
```powershell
python -c "
from app import app, db, EmpresaTuristica
import os
if os.path.exists('instance/visitas.db'):
    os.remove('instance/visitas.db')
with app.app_context():
    db.create_all()
    # Crear empresas de prueba...
    print('Sistema restablecido')
"
```
