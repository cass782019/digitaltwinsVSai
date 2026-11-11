@echo off
REM EN: Starts the demo on Windows and opens http://127.0.0.1:8765
REM ES: Inicia la demo en Windows y abre http://127.0.0.1:8765
cd /d "%~dp0"
if not exist ".env" if exist ".env.example" (
  copy ".env.example" ".env" >nul
  echo EN: .env created. Put your key in OLLAMA_API_KEY ^(or use the Rehearsal button^).
  echo ES: .env creado. Ponga su clave en OLLAMA_API_KEY ^(o use el boton Ensayo^).
)
where python >nul 2>nul && (python server.py & goto :end)
where py >nul 2>nul && (py -3 server.py & goto :end)
echo EN: Python 3.9+ not found. Install it from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^).
echo ES: No se encontro Python 3.9+. Instalelo desde https://www.python.org/downloads/ ^(marque "Add python.exe to PATH"^).
:end
pause
