# Digital Twins vs. AI — *the AI guesses, the twin calculates*
### Gemelos digitales vs. IA — *la IA adivina, el gemelo calcula*

**EN** · [Español ↓](#español)

A teaching demo built for **International Business Week** (Unilasalle-RS). It shows a business audience, with no technical background needed, how **generative AI** and a **digital twin** work together:

1. **The AI understands** a "what if…?" question in plain language (English or Spanish).
2. **The AI guesses** the answer on its own, without any calculator.
3. **The twin calculates** the same scenario with a simple, transparent store simulator.
4. **Compare** the room's guess, the AI's guess and the twin's result side by side.

The message: *the AI talks, the twin calculates, and both must be checked against reality.*

![Demo screen (EN+ES mode)](docs/screenshot_en-es.png)

## The example store
Made-up data for teaching: **ice cream, water and coffee**, over **8 weeks**. Each week the store re-orders to keep about 1.6 weeks of normal sales on the shelf.
The model only changes **4 things**: **demand**, **price**, **supplier delay** and **extra stock**. Questions outside these levers are flagged as "outside this model". Values beyond the limits are adjusted, and the screen shows the adjustment.

## Features
- Languages: **EN**, **ES**, **EN+ES** (bilingual, same screen) and PT.
- **↻ Ask the AI again**: the same question, asked again, may get a different answer from the AI. The twin always repeats its number.
- **Room's guess** box: the audience votes before the reveal.
- **⏯ Rehearsal** (plan B): replays recorded AI answers when there is no internet. The twin still calculates live.
- KPIs: revenue, gross margin (sales minus unit cost), demand fulfilled (in units) and lost sales (US$).

## Run it
Requirements: **Python 3.9+** (standard library only, nothing to install) and an **Ollama Cloud** API key for the live AI.

```bash
git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
cp .env.example .env          # Windows: copy .env.example .env
# edit .env and set OLLAMA_API_KEY=...
python server.py              # opens http://127.0.0.1:8765
```
On Windows you can also double-click `INICIAR_DEMO.bat`.
Without a key the page still opens: use the **⏯ Rehearsal** button with the 4 preset scenarios.

### Configuration (`.env`)
| Variable | Default | Meaning |
|---|---|---|
| `OLLAMA_API_KEY` | — | Ollama Cloud key (**never commit it**) |
| `OLLAMA_URL` | `https://ollama.com/api/chat` | Chat endpoint (use `http://localhost:11434/api/chat` for a local Ollama) |
| `DEMO_MODEL` | `gpt-oss:120b` | Main model |
| `DEMO_FALLBACK_MODEL` | `glm-5.3-flash` | Fallback model |
| `DEMO_PORT` | `8765` | Local port |

## Files
| File | What it is |
|---|---|
| `server.py` | Local web server, store simulator (the twin) and AI prompts |
| `index.html` | The whole interface (EN / ES / EN+ES / PT) |
| `ensaio_v2.json` | Recorded rehearsal (10 Nov 2026, `gpt-oss:120b`): 3 AI guesses per scenario in EN and ES, used by the Rehearsal button |
| `ensaio_2026-11-10.json` | First rehearsal (kept for transparency) |
| `.env.example` | Configuration template |

## Limitations (please read)
- It is a **teaching toy model** with made-up data, not a twin of any real store.
- Gross margin ignores storage, waste and staff costs. Results depend entirely on the model's assumptions.
- AI answers vary from run to run, and that is part of the lesson.

## License
[MIT](LICENSE) © 2026 Cassiano R. N. Moralles — Unilasalle.

---

## Español

Demo didáctica creada para la **International Business Week** (Unilasalle-RS). Muestra a un público de negocios, sin necesidad de conocimientos técnicos, cómo trabajan juntos la **IA generativa** y un **gemelo digital**:

1. **La IA entiende** una pregunta "¿y si…?" en lenguaje común (inglés o español).
2. **La IA adivina** la respuesta sola, sin calculadora.
3. **El gemelo calcula** el mismo escenario con un simulador de tienda simple y transparente.
4. **Comparar**: la apuesta de la sala, la de la IA y el resultado del gemelo, lado a lado.

El mensaje: *la IA conversa, el gemelo calcula, y ambos deben compararse con la realidad.*

![Pantalla de la demo (modo EN+ES)](docs/screenshot_en-es.png)

## La tienda de ejemplo
Datos inventados para enseñar: **helado, agua y café**, durante **8 semanas**. Cada semana la tienda repone para tener cerca de 1,6 semanas de ventas normales en el estante.
El modelo solo cambia **4 cosas**: **demanda**, **precio**, **retraso del proveedor** y **stock extra**. Las preguntas fuera de estas palancas se marcan como "fuera de este modelo". Los valores que superan los límites se ajustan, y la pantalla muestra el ajuste.

## Funciones
- Idiomas: **EN**, **ES**, **EN+ES** (bilingüe, en la misma pantalla) y PT.
- **↻ Preguntar de nuevo a la IA**: la misma pregunta, repetida, puede recibir otra respuesta de la IA. El gemelo siempre repite su número.
- Campo **Apuesta de la sala**: el público vota antes de revelar el resultado.
- **⏯ Ensayo** (plan B): reproduce respuestas grabadas de la IA cuando no hay internet. El gemelo sigue calculando en vivo.
- Indicadores: ingresos, margen bruto (ventas menos costo unitario), demanda atendida (en unidades) y ventas perdidas (US$).

## Cómo ejecutarla
Requisitos: **Python 3.9+** (solo biblioteca estándar, no hay nada que instalar) y una clave de API de **Ollama Cloud** para la IA en vivo.

```bash
git clone https://github.com/cass782019/digitaltwinsVSai.git
cd digitaltwinsVSai
cp .env.example .env          # Windows: copy .env.example .env
# edite .env y complete OLLAMA_API_KEY=...
python server.py              # abre http://127.0.0.1:8765
```
En Windows también puede hacer doble clic en `INICIAR_DEMO.bat`.
Sin clave la página igual abre: use el botón **⏯ Ensayo** con los 4 escenarios predefinidos.

### Configuración (`.env`)
| Variable | Valor por defecto | Significado |
|---|---|---|
| `OLLAMA_API_KEY` | — | Clave de Ollama Cloud (**nunca la suba**) |
| `OLLAMA_URL` | `https://ollama.com/api/chat` | Endpoint de chat (use `http://localhost:11434/api/chat` para Ollama local) |
| `DEMO_MODEL` | `gpt-oss:120b` | Modelo principal |
| `DEMO_FALLBACK_MODEL` | `glm-5.3-flash` | Modelo de respaldo |
| `DEMO_PORT` | `8765` | Puerto local |

## Archivos
| Archivo | Qué es |
|---|---|
| `server.py` | Servidor web local, simulador de la tienda (el gemelo) y prompts de la IA |
| `index.html` | Toda la interfaz (EN / ES / EN+ES / PT) |
| `ensaio_v2.json` | Ensayo grabado (10/11/2026, `gpt-oss:120b`): 3 respuestas de la IA por escenario en EN y ES, usado por el botón Ensayo |
| `ensaio_2026-11-10.json` | Primer ensayo (se conserva por transparencia) |
| `.env.example` | Plantilla de configuración |

## Limitaciones (lea esto)
- Es un **modelo didáctico de juguete** con datos inventados, no un gemelo de ninguna tienda real.
- El margen bruto no incluye costos de almacenaje, merma ni personal. Los resultados dependen totalmente de los supuestos del modelo.
- Las respuestas de la IA varían en cada ejecución, y eso es parte de la lección.

## Licencia
[MIT](LICENSE) © 2026 Cassiano R. N. Moralles — Unilasalle.
