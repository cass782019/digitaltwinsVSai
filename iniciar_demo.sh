#!/usr/bin/env bash
# EN: Starts the demo on Linux/macOS and opens http://127.0.0.1:8765
#     Usage: ./iniciar_demo.sh   (first time: chmod +x iniciar_demo.sh)
# ES: Inicia la demo en Linux/macOS y abre http://127.0.0.1:8765
#     Uso: ./iniciar_demo.sh     (la primera vez: chmod +x iniciar_demo.sh)
set -euo pipefail
cd "$(dirname "$0")"

# EN: find Python 3.9+ / ES: buscar Python 3.9+
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  echo "EN: Python 3.9+ not found. Install it, e.g.: sudo apt install python3"
  echo "ES: No se encontró Python 3.9+. Instálelo, p. ej.: sudo apt install python3"
  exit 1
fi

# EN: create .env from the template on first run / ES: crear .env desde la plantilla la primera vez
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "EN: .env created. Put your key in OLLAMA_API_KEY (or use the Rehearsal button)."
  echo "ES: .env creado. Ponga su clave en OLLAMA_API_KEY (o use el botón Ensayo)."
fi

# EN: no graphical session -> do not try to open a browser / ES: sin entorno gráfico -> no abrir navegador
if [ -z "${DISPLAY:-}" ] && [ -z "${WAYLAND_DISPLAY:-}" ] && [ "$(uname)" != "Darwin" ]; then
  export DEMO_NO_BROWSER=1
  echo "EN: no desktop detected - open http://127.0.0.1:${DEMO_PORT:-8765} in your browser."
  echo "ES: sin escritorio - abra http://127.0.0.1:${DEMO_PORT:-8765} en su navegador."
fi

exec "$PY" server.py
