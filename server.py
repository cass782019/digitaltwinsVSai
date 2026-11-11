# -*- coding: utf-8 -*-
"""Digital Twins vs. AI - "the AI guesses, the twin calculates".

EN: Teaching demo for International Business Week. Run `python server.py` and open
    http://127.0.0.1:8765. The AI key is read from the OLLAMA_API_KEY environment
    variable or from a local `.env` file (copy `.env.example`). Without a key, use
    the Rehearsal button (recorded answers). Python standard library only.
ES: Demo didáctica para la International Business Week. Ejecute `python server.py`
    y abra http://127.0.0.1:8765. La clave de IA se lee de la variable de entorno
    OLLAMA_API_KEY o de un archivo `.env` local (copie `.env.example`). Sin clave,
    use el botón Ensayo (respuestas grabadas). Solo biblioteca estándar de Python.

MIT License - (c) 2026 Cassiano R. N. Moralles - Unilasalle.
"""
import json
import os
import sys
import threading
import time
import urllib.request
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_dotenv(path=HERE / ".env"):
    """EN: minimal .env loader (KEY=value); real environment variables win.
    ES: lector mínimo de .env (CLAVE=valor); las variables de entorno reales tienen prioridad."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_dotenv()
PORT = int(os.environ.get("DEMO_PORT", "8765"))
MODELS = [os.environ.get("DEMO_MODEL", "gpt-oss:120b"), os.environ.get("DEMO_FALLBACK_MODEL", "glm-5.3-flash")]
OLLAMA_URL = os.environ.get("OLLAMA_URL", "https://ollama.com/api/chat")
WEEKS = 8

# ---------------------------------------------------------------- the twin
# Toy store, synthetic data (declared on screen). Units per week, prices in USD.
PRODUCTS = {
    "ice_cream": {"base": 300, "price": 4.00, "cost": 2.00, "elasticity": -1.5},
    "water":     {"base": 500, "price": 1.50, "cost": 0.60, "elasticity": -1.0},
    "coffee":    {"base": 200, "price": 8.00, "cost": 4.50, "elasticity": -0.8},
}
TARGET_WEEKS = 1.6   # order-up-to level = 1.6 weeks of NORMAL demand
LEAD = 1             # normal supplier lead time (weeks)


def _clamp(v, lo, hi, default=0):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return default
    return max(lo, min(hi, v))


LIMITS = {"demand_change_pct": (-90, 300), "price_change_pct": (-50, 50),
          "supplier_delay_weeks": (0, 4), "extra_stock_units": (0, 5000)}


def normalize(p):
    """Returns (params, adjusted) where adjusted lists the levers cut to the model's limits."""
    p = dict(p or {})
    prod = p.get("product", "all")
    if prod not in PRODUCTS and prod != "all":
        prod = "all"
    out = {"product": prod, "start_week": int(_clamp(p.get("start_week"), 1, WEEKS, 2))}
    adjusted = []
    for k, (lo, hi) in LIMITS.items():
        raw = p.get(k, p.get("extra_order_units") if k == "extra_stock_units" else None)
        v = _clamp(raw, lo, hi, 0)
        try:
            if raw is not None and float(raw) != v:
                adjusted.append({"lever": k, "asked": float(raw), "used": v})
        except (TypeError, ValueError):
            pass
        out[k] = int(v) if k in ("supplier_delay_weeks", "extra_stock_units") else v
    return out, adjusted


def simulate_product(name, prm, scenario=True):
    d = PRODUCTS[name]
    b = d["base"]
    hit = scenario and prm["product"] in ("all", name)
    s_normal = round(TARGET_WEEKS * b)
    stock = s_normal - b
    arrivals = {1: b}
    extra = prm["extra_stock_units"] if hit else 0
    weeks = []
    for t in range(1, WEEKS + 1):
        inwin = hit and t >= prm["start_week"]
        dc = prm["demand_change_pct"] / 100 if inwin else 0
        pc = prm["price_change_pct"] / 100 if inwin else 0
        demand = max(0, round(b * (1 + dc) * (1 + d["elasticity"] * pc)))
        stock += arrivals.pop(t, 0)
        sold = min(stock, demand)
        lost = demand - sold
        stock -= sold
        pipeline = sum(q for w, q in arrivals.items() if w > t)
        # manager keeps `extra` units more on the shelf, planned one week ahead
        s_level = s_normal + (extra if t >= prm["start_week"] - 1 else 0)
        order = max(0, round(s_level - stock - pipeline))
        lead = LEAD + (prm["supplier_delay_weeks"] if inwin else 0)
        if order:
            arrivals[t + lead] = arrivals.get(t + lead, 0) + order
        price = d["price"] * (1 + pc)
        weeks.append({"week": t, "demand": demand, "sold": sold, "lost": lost,
                      "stock_end": round(stock), "revenue": round(sold * price, 2),
                      "profit": round(sold * (price - d["cost"]), 2)})
    return weeks


def kpis(weeks_by_prod):
    dem = sum(w["demand"] for ws in weeks_by_prod.values() for w in ws)
    sold = sum(w["sold"] for ws in weeks_by_prod.values() for w in ws)
    return {
        "revenue": round(sum(w["revenue"] for ws in weeks_by_prod.values() for w in ws), 2),
        "gross_margin": round(sum(w["profit"] for ws in weeks_by_prod.values() for w in ws), 2),
        "demand_fulfilled_pct": round(100 * sold / dem, 1) if dem else 100.0,
        "lost_units": sum(w["lost"] for ws in weeks_by_prod.values() for w in ws),
        "weeks_with_empty_shelves": len({w["week"] for ws in weeks_by_prod.values() for w in ws if w["lost"] > 0}),
    }


def run_twin(params):
    prm, adjusted = normalize(params)
    in_scope = bool(params.get("in_scope", True)) if isinstance(params, dict) else True
    any_lever = any(prm[k] for k in LIMITS)
    base = {n: simulate_product(n, prm, scenario=False) for n in PRODUCTS}
    scen = {n: simulate_product(n, prm, scenario=True) for n in PRODUCTS}
    kb, ks = kpis(base), kpis(scen)
    delta = {
        "revenue_change_pct": round(100 * (ks["revenue"] - kb["revenue"]) / kb["revenue"], 1),
        "gross_margin_change_pct": round(100 * (ks["gross_margin"] - kb["gross_margin"]) / kb["gross_margin"], 1),
    }
    lost_value = round(sum(w["lost"] * PRODUCTS[n]["price"] * (1 + (prm["price_change_pct"] / 100 if prm["product"] in ("all", n) and w["week"] >= prm["start_week"] else 0))
                           for n, ws in scen.items() for w in ws), 2)
    ks["lost_sales_usd"] = lost_value
    return {"params": prm, "adjusted": adjusted, "in_scope": in_scope and any_lever,
            "baseline": kb, "scenario": ks, "delta": delta,
            "weeks": scen, "weeks_baseline": base}


# ---------------------------------------------------------------- the AI
def api_key():
    """EN: key from OLLAMA_API_KEY (environment or local .env). ES: clave de OLLAMA_API_KEY (entorno o .env local)."""
    k = os.environ.get("OLLAMA_API_KEY", "").strip()
    return k or None


def llm(system, user, want_json=True, temperature=0.2):
    """temperature=None -> model default (like an ordinary chat app)."""
    key = api_key()
    if not key:
        raise RuntimeError("OLLAMA_API_KEY not found")
    last = None
    for model in MODELS:
        body = {"model": model, "stream": False,
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": user}]}
        if temperature is not None:
            body["options"] = {"temperature": temperature}
        if want_json:
            body["format"] = "json"
        req = urllib.request.Request(OLLAMA_URL,
                                     data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json"})
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)["message"]["content"]
            txt = out.strip()
            if want_json:
                txt = txt[txt.find("{"): txt.rfind("}") + 1]
                return json.loads(txt), model, round(time.time() - t0, 1)
            return txt, model, round(time.time() - t0, 1)
        except Exception as e:  # try the fallback model
            last = e
    raise RuntimeError(f"LLM failed: {last}")


LANG = {"en": "English", "es": "Spanish", "pt": "Brazilian Portuguese"}

PARSE_SYS = """You translate a store manager's 'what if' question into parameters for a store simulator.
The toy store sells exactly three products: ice_cream, water, coffee. Horizon: 8 weeks.
Return ONLY a JSON object with these keys:
 "product": "ice_cream" | "water" | "coffee" | "all",
 "demand_change_pct": number (e.g. heat wave on ice cream = +40 to +100; recession = -10 to -30),
 "price_change_pct": number (discount 20% = -20),
 "supplier_delay_weeks": integer 0-4,
 "extra_stock_units": integer (extra units the manager decides to keep on the shelf, prepared in advance; 0 if not mentioned),
 "start_week": integer 1-8 (default 2),
 "in_scope": true if the question can be expressed with these levers (demand, price, supplier delay, extra stock); false otherwise
   (e.g. a new competitor, opening a store, a 2-for-1 promotion, staff, marketing),
 "restated": one short sentence restating the scenario, in the SAME language as the question,
 "restated_en": the same sentence in English,
 "restated_es": the same sentence in Spanish,
If something is not mentioned use 0. Do not cap numbers yourself. Never add other keys."""

GUESS_SYS = """You are a fast-talking AI assistant WITHOUT any calculation tool or simulator.
A store manager asks a what-if question about an 8-week period for a small store selling ice cream, water and coffee
(normal weekly sales: 300 ice creams at $4, 500 waters at $1.50, 200 coffees at $8).
Give your best quick intuitive guess. Return ONLY JSON:
{"revenue_change_pct": number (change of the 8-week total revenue vs. a normal 8 weeks),
 "demand_fulfilled_pct": number (share of the demand, in units, that the store manages to sell; 100 = no empty shelves),
 "sentence": one confident sentence in LANGUAGE}"""

EXPLAIN_SYS = """You explain simulation results to a BUSINESS audience (no jargon, no formulas).
Use ONLY the numbers given. Write in LANGUAGE. Rules:
- Money in US dollars written as US$ with whole numbers (no decimals). Percentages with at most one decimal.
- Revenue and margin are TOTALS FOR 8 WEEKS (never call them weekly).
- 'demand fulfilled' is the share of demand in UNITS that was sold (not number of customers).
- 'gross margin' = sales minus unit product cost (no storage, waste or staff costs).
- In Spanish say 'la IA' and 'el gemelo'; in Portuguese 'a IA' and 'o gêmeo'; in English 'the AI' and 'the twin'.
Exactly 3 short sentences: 1) what happened in the store, 2) how the quick AI guess compared with the twin's calculation,
3) one practical action the manager could test next in the twin. Max 70 words."""


def _guess_sys(lang):
    if lang == "bi":
        return GUESS_SYS.replace("LANGUAGE", "English") + \
            '\nAlso add the key "sentence_es": the same sentence in Spanish.'
    return GUESS_SYS.replace("LANGUAGE", LANG.get(lang, "English"))


def handle_guess(q, lang):
    # the quick guess runs at the model's default temperature, like an ordinary chat app
    guess, m, s = llm(_guess_sys(lang), q, temperature=None)
    return {"guess": guess, "model": m, "seconds": s}


def handle_ask(q, lang):
    out = {"ai": True, "lang": lang}
    params, m1, s1 = llm(PARSE_SYS, q)
    g = handle_guess(q, lang)
    guess, m2, s2 = g["guess"], g["model"], g["seconds"]
    twin = run_twin(params)
    rest = {"restated": params.get("restated", ""), "restated_en": params.get("restated_en", ""),
            "restated_es": params.get("restated_es", "")}
    if not twin["in_scope"]:
        out.update(twin=twin, guess=guess, explanation="", models=[m1, m2], seconds=[s1, s2], **rest)
        return out
    facts = json.dumps({"question": q, "ai_quick_guess": guess, "twin_baseline_8_weeks": twin["baseline"],
                        "twin_scenario_8_weeks": twin["scenario"], "twin_change": twin["delta"],
                        "levers_cut_to_model_limits": twin["adjusted"]})
    langs = ["en", "es"] if lang == "bi" else [lang]
    with ThreadPoolExecutor(2) as ex:
        res = list(ex.map(lambda l: llm(EXPLAIN_SYS.replace("LANGUAGE", LANG.get(l, "English")), facts,
                                        want_json=False), langs))
    out.update(twin=twin, guess=guess, explanation=res[0][0],
               explanation_es=res[1][0] if lang == "bi" else "",
               models=[m1, m2] + [r[1] for r in res], seconds=[s1, s2, max(r[2] for r in res)], **rest)
    return out


def replay(idx, lang):
    """Offline plan B: real rehearsal answers (ensaio_v2.json) + live twin calculation."""
    data = json.loads((HERE / "ensaio_v2.json").read_text(encoding="utf-8"))
    base = "es" if lang == "es" else "en"
    r = data["runs"][base][int(idx)]
    out = {"ai": False, "replay": True, "twin": run_twin(r["params"]), "restated": r["restated"],
           "guess": r["guesses"][0], "guesses": r["guesses"], "explanation": r["explanation"],
           "recorded_at": data["run_at"]}
    if lang == "bi":
        r_es = data["runs"]["es"][int(idx)]
        out.update(restated_en=r["restated"], restated_es=r_es["restated"], explanation_es=r_es["explanation"],
                   guesses_es=r_es["guesses"])
    return out


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj, ctype="application/json"):
        data = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, (HERE / "index.html").read_bytes(), "text/html")
        if self.path == "/logo_unilasalle.png":
            return self._send(200, (HERE / "logo_unilasalle.png").read_bytes(), "image/png")
        if self.path == "/api/health":
            return self._send(200, {"ok": True, "has_key": bool(api_key())})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        try:
            if self.path == "/api/ask":
                return self._send(200, handle_ask(body.get("question", ""), body.get("lang", "en")))
            if self.path == "/api/guess":
                return self._send(200, handle_guess(body.get("question", ""), body.get("lang", "en")))
            if self.path == "/api/replay":
                return self._send(200, replay(body.get("idx", 0), body.get("lang", "en")))
            if self.path == "/api/twin":
                return self._send(200, {"ai": False, "twin": run_twin(body.get("params", {}))})
        except Exception as e:
            return self._send(502, {"error": str(e)})
        self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        for p in [{}, {"product": "ice_cream", "demand_change_pct": 40},
                  {"product": "ice_cream", "demand_change_pct": 80},
                  {"product": "all", "supplier_delay_weeks": 2}]:
            r = run_twin(p)
            print(p, "->", r["scenario"], r["delta"])
        sys.exit(0)
    host = os.environ.get("DEMO_HOST", "127.0.0.1")
    try:
        srv = ThreadingHTTPServer((host, PORT), H)
    except OSError as e:
        print(f"EN: port {PORT} is busy ({e}). Close the other demo window or set DEMO_PORT in .env.")
        print(f"ES: el puerto {PORT} está ocupado ({e}). Cierre la otra ventana de la demo o defina DEMO_PORT en .env.")
        sys.exit(1)
    url = f"http://127.0.0.1:{PORT}/"
    print("Demo running at / Demo en", url, "| AI key found / clave de IA:", bool(api_key()),
          "| Ctrl+C to stop / para detener")
    if os.environ.get("DEMO_NO_BROWSER", "").strip() not in ("1", "true", "yes"):
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped / Detenida.")
