@echo off
echo 🧪 PROBANDO RUTAS DEL SISTEMA DE TURISMO
echo ========================================
cd /d "C:\Users\Win11-x64\Desktop\Proyectos\Sistema_Turismo"
call venv_nuevo\Scripts\activate.bat
echo ⏳ Esperando que la aplicación esté lista...
timeout /t 3 /nobreak > nul
python probar_rutas.py
echo.
echo ✅ Pruebas completadas. Presiona cualquier tecla para continuar...
pause > nul
