@echo off
echo 🏛️ Sistema de Turismo - Iniciador Automatico
echo ================================================

cd /d "c:\Users\nicol\OneDrive\Escritorio\SISTEMA_TURISMO"

echo.
echo 📍 Ubicación: %CD%
echo.

echo 🔧 Inicializando base de datos...
python inicializar_sistema.py

echo.
echo 🚀 Iniciando servidor Flask...
echo.
echo 💡 El sistema estará disponible en:
echo    - Página principal: http://localhost:5000
echo    - Ver datos: http://localhost:5000/ver_datos
echo.
echo 📋 Para detener el servidor, presiona Ctrl+C
echo.

python app.py

pause
