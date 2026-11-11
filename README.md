# Gemelos digitales vs. IA · Digital Twins vs. AI

<p align="center">
<em>La IA adivina, el gemelo calcula.</em> · <em>The AI guesses, the twin calculates.</em><br>
<sub>International Business Week · Unilasalle-RS · 11/11/2026 · MIT</sub>
</p>

![Pantalla de la demo (modo EN+ES) / Demo screen (EN+ES mode)](docs/screenshot_en-es.png)

<table>
<tr>
<th width="50%">🇪🇸 Español</th>
<th width="50%">🇬🇧 English</th>
</tr>

<tr>
<td valign="top" width="50%">

Demo didáctica para la **International Business Week** (Unilasalle-RS). Muestra a un público de negocios, sin conocimientos técnicos, cómo trabajan juntos la **IA generativa** y un **gemelo digital**:

1. **La IA entiende** una pregunta "¿y si…?" en lenguaje común.
2. **La IA adivina** la respuesta sola, sin calculadora.
3. **El gemelo calcula** el mismo escenario con un simulador de tienda simple y transparente.
4. **Comparar**: la apuesta de la sala, la de la IA y el resultado del gemelo, lado a lado.

**Mensaje:** *la IA conversa, el gemelo calcula, y ambos deben compararse con la realidad.*

</td>
<td valign="top" width="50%">

A teaching demo for **International Business Week** (Unilasalle-RS). It shows a business audience, with no technical background needed, how **generative AI** and a **digital twin** work together:

1. **The AI understands** a "what if…?" question in plain language.
2. **The AI guesses** the answer on its own, without a calculator.
3. **The twin calculates** the same scenario with a simple, transparent store simulator.
4. **Compare** the room's guess, the AI's guess and the twin's result side by side.

**Message:** *the AI talks, the twin calculates, and both must be checked against reality.*

</td>
</tr>

<tr>
<td valign="top">

### La tienda de ejemplo

Datos inventados: **helado, agua y café**, durante **8 semanas**. Cada semana la tienda repone para tener cerca de 1,6 semanas de ventas normales en el estante.

El modelo solo cambia **4 cosas**: **demanda**, **precio**, **retraso del proveedor** y **stock extra**. Las preguntas fuera de estas palancas se marcan como "fuera de este modelo". Los valores que superan los límites se ajustan, y la pantalla muestra el ajuste.

</td>
<td valign="top">

### The example store

Made-up data: **ice cream, water and coffee**, over **8 weeks**. Each week the store re-orders to keep about 1.6 weeks of normal sales on the shelf.

The model only changes **4 things**: **demand**, **price**, **supplier delay** and **extra stock**. Questions outside these levers are flagged as "outside this model". Values beyond the limits are adjusted, and the screen shows the adjustment.

</td>
</tr>

<tr>
<td valign="top">

### Funciones

- Idiomas: **ES**, **EN**, **EN+ES** (bilingüe) y PT.
- **↻ Preguntar de nuevo a la IA**: la misma pregunta puede recibir otra respuesta. El gemelo siempre repite su número.
- **Apuesta de la sala**: el público vota antes de revelar el resultado.
- **⏯ Ensayo** (plan B): respuestas grabadas de la IA cuando no hay internet. El gemelo sigue calculando en vivo.
- Indicadores: ingresos, margen bruto, demanda atendida (unidades) y ventas perdidas (US$).

</td>
<td valign="top">

### Features

- Languages: **ES**, **EN**, **EN+ES** (bilingual) and PT.
- **↻ Ask the AI again**: the same question may get a different answer. The twin always repeats its number.
- **Room's guess**: the audience votes before the reveal.
- **⏯ Rehearsal** (plan B): recorded AI answers when there is no internet. The twin still calculates live.
- KPIs: revenue, gross margin, demand fulfilled (units) and lost sales (US$).

</td>
</tr>

<tr>
<td valign="top">

### Cómo ejecutarla

Es **autocontenida**: solo necesita **Python 3.9+**, sin instalar paquetes, en **Windows, Linux o macOS**. La IA en vivo necesita internet y una clave de **Ollama Cloud**.

- **Windows:** doble clic en `INICIAR_DEMO.bat`.
- **Linux / macOS:** `./iniciar_demo.sh`.

La primera vez el script crea el `.env` a partir de `.env.example`. Ponga su clave en `OLLAMA_API_KEY` y abra http://127.0.0.1:8765.

Sin clave o sin internet, la página igual abre: use **⏯ Ensayo** con los 4 escenarios predefinidos.

Comandos paso a paso: ver [abajo](#quick-start).

</td>
<td valign="top">

### Run it

It is **self-contained**: it only needs **Python 3.9+**, with no packages to install, on **Windows, Linux or macOS**. The live AI needs internet and an **Ollama Cloud** key.

- **Windows:** double-click `INICIAR_DEMO.bat`.
- **Linux / macOS:** `./iniciar_demo.sh`.

On first run the script creates `.env` from `.env.example`. Put your key in `OLLAMA_API_KEY` and open http://127.0.0.1:8765.

Without a key or internet the page still opens: use **⏯ Rehearsal** with the 4 preset scenarios.

Step-by-step commands: see [below](#quick-start).

</td>
</tr>

<tr>
<td valign="top">

### Archivos

- `server.py`: servidor local, simulador (el gemelo) y prompts de la IA.
- `index.html`: toda la interfaz (ES / EN / EN+ES / PT).
- `ensaio_v2.json`: ensayo grabado (10/11/2026, `gpt-oss:120b`), usado por **Ensayo**.
- `ensaio_2026-11-10.json`: primer ensayo (por transparencia).
- `INICIAR_DEMO.bat` / `iniciar_demo.sh`: inicio en Windows / Linux-macOS.
- `.env.example`: plantilla de configuración.

</td>
<td valign="top">

### Files

- `server.py`: local server, simulator (the twin) and AI prompts.
- `index.html`: the whole interface (ES / EN / EN+ES / PT).
- `ensaio_v2.json`: recorded rehearsal (10 Nov 2026, `gpt-oss:120b`), used by **Rehearsal**.
- `ensaio_2026-11-10.json`: first rehearsal (kept for transparency).
- `INICIAR_DEMO.bat` / `iniciar_demo.sh`: start on Windows / Linux-macOS.
- `.env.example`: configuration template.

</td>
</tr>

<tr>
<td valign="top">

### Limitaciones

- Es un **modelo didáctico** con datos inventados, no un gemelo de una tienda real.
- El margen bruto no incluye almacenaje, merma ni personal. Los resultados dependen de los supuestos del modelo.
- Las respuestas de la IA varían en cada ejecución, y eso es parte de la lección.

</td>
<td valign="top">

### Limitations

- It is a **teaching model** with made-up data, not a twin of a real store.
- Gross margin ignores storage, waste and staff costs. Results depend on the model's assumptions.
- AI answers vary from run to run, and that is part of the lesson.

</td>
</tr>

<tr>
<td valign="top">

### Licencia

[MIT](LICENSE) © 2026 Cassiano R. N. Moralles — Unilasalle.
El nombre y el logotipo de Unilasalle no están cubiertos por la licencia.

</td>
<td valign="top">

### License

[MIT](LICENSE) © 2026 Cassiano R. N. Moralles — Unilasalle.
The Unilasalle name and logo are not covered by the license.

</td>
</tr>
</table>

<a id="quick-start"></a>

## Inicio rápido · Quick start

### 🐧 Linux / macOS

```bash
# ES: si falta Python (Debian/Ubuntu) · EN: if Python is missing (Debian/Ubuntu)
sudo apt install -y python3 git

git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
chmod +x iniciar_demo.sh
./iniciar_demo.sh          # ES: crea .env la 1.ª vez · EN: creates .env on first run
nano .env                  # ES: complete OLLAMA_API_KEY · EN: set OLLAMA_API_KEY
./iniciar_demo.sh
```

ES: en un servidor sin escritorio (SSH) no se abre el navegador; abra `http://127.0.0.1:8765` en su máquina (por ejemplo con `ssh -L 8765:127.0.0.1:8765 usuario@servidor`).
EN: on a server without a desktop (SSH) no browser opens; open `http://127.0.0.1:8765` on your machine (e.g. with `ssh -L 8765:127.0.0.1:8765 user@server`).

### 🪟 Windows

```bat
:: ES: instale Python desde python.org y marque "Add python.exe to PATH"
:: EN: install Python from python.org and tick "Add python.exe to PATH"
git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
INICIAR_DEMO.bat
notepad .env
INICIAR_DEMO.bat
```

ES: sin git, use **Code → Download ZIP** en GitHub, descomprima y haga doble clic en `INICIAR_DEMO.bat`.
EN: without git, use **Code → Download ZIP** on GitHub, unzip and double-click `INICIAR_DEMO.bat`.

### Configuración · Configuration (`.env`)

| Variable | Por defecto · Default | ES | EN |
|---|---|---|---|
| `OLLAMA_API_KEY` | — | Clave de Ollama Cloud (**nunca la suba**) | Ollama Cloud key (**never commit it**) |
| `OLLAMA_URL` | `https://ollama.com/api/chat` | Endpoint de chat | Chat endpoint |
| `DEMO_MODEL` | `gpt-oss:120b` | Modelo principal | Main model |
| `DEMO_FALLBACK_MODEL` | `glm-5.3-flash` | Modelo de respaldo | Fallback model |
| `DEMO_PORT` | `8765` | Puerto local | Local port |
| `DEMO_NO_BROWSER` | — | `1` = no abrir el navegador | `1` = do not open the browser |

ES: para Ollama local use `OLLAMA_URL=http://localhost:11434/api/chat`. · EN: for a local Ollama use `OLLAMA_URL=http://localhost:11434/api/chat`.
