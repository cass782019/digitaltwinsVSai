@echo off
REM EN: Starts the demo and opens the browser at http://127.0.0.1:8765
REM ES: Inicia la demo y abre el navegador en http://127.0.0.1:8765
cd /d "%~dp0"
python server.py
if errorlevel 1 py server.py
pause
