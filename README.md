# Gemelos digitales vs. IA · Digital Twins vs. AI

<p align="center">
<em>La IA adivina, el gemelo calcula.</em> · <em>The AI guesses, the twin calculates.</em><br>
<sub>International Business Week · Unilasalle-RS · 11/11/2026 · MIT</sub>
</p>

<table>
<tr>
<th width="50%">🇪🇸 Español</th>
<th width="50%">🇬🇧 English</th>
</tr>

<tr>
<td valign="top">

Demo didáctica para la **International Business Week** (Unilasalle-RS). Muestra a un público de negocios, sin conocimientos técnicos, cómo trabajan juntos la **IA generativa** y un **gemelo digital**:

1. **La IA entiende** una pregunta "¿y si…?" en lenguaje común.
2. **La IA adivina** la respuesta sola, sin calculadora.
3. **El gemelo calcula** el mismo escenario con un simulador de tienda simple y transparente.
4. **Comparar**: la apuesta de la sala, la de la IA y el resultado del gemelo, lado a lado.

**Mensaje:** *la IA conversa, el gemelo calcula, y ambos deben compararse con la realidad.*

</td>
<td valign="top">

A teaching demo for **International Business Week** (Unilasalle-RS). It shows a business audience, with no technical background needed, how **generative AI** and a **digital twin** work together:

1. **The AI understands** a "what if…?" question in plain language.
2. **The AI guesses** the answer on its own, without a calculator.
3. **The twin calculates** the same scenario with a simple, transparent store simulator.
4. **Compare** the room's guess, the AI's guess and the twin's result side by side.

**Message:** *the AI talks, the twin calculates, and both must be checked against reality.*

</td>
</tr>

<tr>
<td colspan="2" align="center">

<img src="docs/screenshot_en-es.png" alt="Pantalla de la demo (modo EN+ES) / Demo screen (EN+ES mode)" width="100%">

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

Requisitos: **Python 3.9+** (solo biblioteca estándar) y una clave de **Ollama Cloud**.

```bash
git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
cp .env.example .env
# edite .env: OLLAMA_API_KEY=...
python server.py
```

En Windows: `copy .env.example .env` y doble clic en `INICIAR_DEMO.bat`. Abre http://127.0.0.1:8765.

Sin clave la página igual abre: use **⏯ Ensayo** con los 4 escenarios predefinidos.

</td>
<td valign="top">

### Run it

Requirements: **Python 3.9+** (standard library only) and an **Ollama Cloud** key.

```bash
git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
cp .env.example .env
# edit .env: OLLAMA_API_KEY=...
python server.py
```

On Windows: `copy .env.example .env` and double-click `INICIAR_DEMO.bat`. Opens http://127.0.0.1:8765.

Without a key the page still opens: use **⏯ Rehearsal** with the 4 preset scenarios.

</td>
</tr>

<tr>
<td valign="top">

### Configuración (`.env`)

| Variable | Por defecto | Uso |
|---|---|---|
| `OLLAMA_API_KEY` | — | Clave de Ollama Cloud (**nunca la suba**) |
| `OLLAMA_URL` | `https://ollama.com/api/chat` | Endpoint (Ollama local: `http://localhost:11434/api/chat`) |
| `DEMO_MODEL` | `gpt-oss:120b` | Modelo principal |
| `DEMO_FALLBACK_MODEL` | `glm-5.3-flash` | Modelo de respaldo |
| `DEMO_PORT` | `8765` | Puerto local |

</td>
<td valign="top">

### Configuration (`.env`)

| Variable | Default | Use |
|---|---|---|
| `OLLAMA_API_KEY` | — | Ollama Cloud key (**never commit it**) |
| `OLLAMA_URL` | `https://ollama.com/api/chat` | Endpoint (local Ollama: `http://localhost:11434/api/chat`) |
| `DEMO_MODEL` | `gpt-oss:120b` | Main model |
| `DEMO_FALLBACK_MODEL` | `glm-5.3-flash` | Fallback model |
| `DEMO_PORT` | `8765` | Local port |

</td>
</tr>

<tr>
<td valign="top">

### Archivos

| Archivo | Qué es |
|---|---|
| `server.py` | Servidor local, simulador (el gemelo) y prompts de la IA |
| `index.html` | Toda la interfaz (ES / EN / EN+ES / PT) |
| `ensaio_v2.json` | Ensayo grabado (10/11/2026, `gpt-oss:120b`), usado por **Ensayo** |
| `ensaio_2026-11-10.json` | Primer ensayo (por transparencia) |
| `.env.example` | Plantilla de configuración |

</td>
<td valign="top">

### Files

| File | What it is |
|---|---|
| `server.py` | Local server, simulator (the twin) and AI prompts |
| `index.html` | The whole interface (ES / EN / EN+ES / PT) |
| `ensaio_v2.json` | Recorded rehearsal (10 Nov 2026, `gpt-oss:120b`), used by **Rehearsal** |
| `ensaio_2026-11-10.json` | First rehearsal (kept for transparency) |
| `.env.example` | Configuration template |

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
