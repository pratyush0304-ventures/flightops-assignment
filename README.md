# Assignment 04: FlightOps Tool Calling & Building AI Agents

## Course Information

| Field | Details |
|-------|---------|
| **Course** | Agentic AI: From Concepts to Practice |
| **Assignment** | 04 — FlightOps Tool Calling & Building AI Agents |
| **Instructor** | Prof. Karthik Vaidhyanathan |
| **TAs** | Aviral Gupta, Aneeta Sara Shany, Ch Pavan Harshit, Shreyash Chandak |
|**Student**| Sumedha Banerjee |
|**Student ID**| evernorth-aai-817080 |

---------------------------------------------------------------------

## Mission Briefing

AeroBrain could answer manual questions but could not act on live operations data. **FlightOps** upgrades that read-only assistant into an operations officer that calls internal tools — flight status, gates, maintenance, weather — and chains them together before answering.

---------------------------------------------------------------------

This project implements a **FlightOps** airline operations assistant using plain Python function calling — no LangChain, CrewAI, AutoGen, MCP, or other agent frameworks. The agent retrieves live operational data through structured tools, plans before acting, and reflects after answering.

---------------------------------------------------------------------

## Architecture

| File | Responsibility |
|------|----------------|
| `config.py` | Reads `OLLAMA_HOST` and `OLLAMA_MODEL` from environment variables (via `.env`) and hands back a shared `OllamaClient`. Nothing provider-specific is hardcoded. |
| `data.py` | Mock dictionaries for Flights, Aircraft, Passengers, Maintenance, Weather, and Gates. AI203 is configured with a 25-minute delay, thunderstorms at DEL, and recent maintenance on VT-EXA. |
| `tools.py` | Seven plain Python tool functions with structured success/error responses. All exceptions are caught internally. |
| `schemas.py` | JSON-schema style MODEL tool declarations. Exports **lazy** and **careful** versions of `get_flight_status`; default uses the careful schema. |
| `llm_client.py` | Isolated MODEL-compatible client wrapper — the rest of the codebase is model-agnostic. |
| `agent.py` | Multi-tool function calling loop: while the model requests tools, execute, append results, and re-prompt until a final answer. Logs the tool call sequence. |
| `planner.py` | Pre-execution LLM step that generates a "Goal" and numbered "Plan". |
| `reflector.py` | Post-answer LLM step that critiques tool usage, missing info, and confidence. |
| `app.py` | Part 3 smoke tests — calls every tool directly with print output (no LLM used). |
| `main.py` | CLI entry point orchestrating "Plan → Agent → Reflection" with presentable console output. |
| `memory.py` | JSON file store for `remember` / `recall`. Loaded into the system prompt at startup. |
| `requirements.txt` | Minimal dependencies: `MODEL`, `python-dotenv`. |

----------------------------------------------------------------------

## Model Provider & Model

- **Provider:** Ollama (local, MODEL-compatible API)
- **Default model:** `qwen3.5:4b` (override via `MODEL_NAME` in `.env`)
- **Endpoint:** `http://localhost:11434/v1` (override via `MODEL_BASE_URL`)
- **Client module:** `llm_client.py`

Ollama accepts any placeholder API key (default: `ollama`). To use cloud MODEL instead, set `MODEL_USED`, `MODEL_NAME`, and `MODEL_BASE_URL=https://api.MODEL.com/v1` in `.env`.

-----------------------------------------------------------------------

## Setup & Run Instructions

### Prerequisites: Ollama + qwen3.5:4b

Install [Ollama](https://ollama.com/) and pull the model:

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Keep Ollama running in the background (on Windows it usually starts automatically).

### VS Code / Windows: the Downloads `app.py` error

If the traceback still says Python can't open

`C:\Users\Admin\Downloads\flightops-assignment-cursor-skyvault-memory-238c\app.py`

then the **Run button is still using that folder**. `tools.py` living under `C:\Users\Admin\Projects\Skyvault` does not change that. Close the Downloads window entirely.

Do this once:

1. Close VS Code.
2. In File Explorer go to `C:\Users\Admin\Projects\Skyvault`.
3. Confirm `app.py`, `memory.py`, and `tools.py` are **in that same folder** (not only `tools.py`). If `app.py` is missing, copy it from this repo — the smoke-test file is `app.py` at the project root.
4. Double-click `run.bat` in that folder (added in this branch). It `cd`s to its own directory and then runs `app.py`.
5. Re-open VS Code with **File → Open Folder** on `C:\Users\Admin\Projects\Skyvault` only.
6. `Ctrl+Shift+P` → **Python: Select Interpreter** → pick  
   `C:\Users\Admin\Projects\Skyvault\.venv\Scripts\python.exe`  
   Do **not** pick the Downloads `.venv`.
7. Open `run_local.py` and run that file (not a phantom `app.py` from Downloads).

The interpreter path is printed at the top of `run_local.py`. If it still starts with `Downloads\flightops-assignment-...`, the wrong environment is selected.

### Project setup

```powershell
# 1. Navigate to project
cd C:\Users\Admin\Projects\flightops-assignment

# 2. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (defaults already target Ollama)
copy .env.example .env

# 5. Run tool smoke tests (Part 3 — no LLM needed)
python app.py

# 6. Run full agent pipeline (Part 5–8)
python main.py

# 7. List example prompts
python main.py --examples
```

--------------------------------------------------------------------------

## Sample Prompts

```powershell
python main.py "Is AI203 likely to depart on time?"
python main.py "Is AI203 likely to depart on time?Check gate availibility and weather confitions"
python main.py "Find passenger Priya Sharma and her flight status."
python main.py "What maintenance was done on VT-EXA?"
python main.py "Is there an available gate at T3?"
python main.py "What's the weather at HYD and BLR?"
python main.py "What's the weather at HYD and CHN?"
```

The default query (`Is AI203 likely to depart on time?`) is designed to require **3+ tools**: flight status, weather at DEL, and maintenance history for VT-EXA.

### Memory (Assignment 05 Part 1)

Facts live in `skyvault_memory.json` next to the Python files. `remember(key, value, source)` writes a fact; `recall(query)` searches keys and values. On every agent run, `working_context()` is appended to the system prompt so SkyVault does not wait to be asked.

**Conflict rule:** last write wins on the same key (keys are compared case-insensitively). The old value is not kept as a second live fact; it is only recorded as `previous_value` on that record so the overwrite is visible. Example: `preferred_terminal=T2` then `preferred_terminal=T3` leaves a single fact (`T3`).

Restart demo — run these from the folder that contains `memory.py` (not a different SkyVault copy):

```powershell
python memory.py
```

Or call the functions directly (do not import `execute_tool` unless your `tools.py` defines it):

```powershell
python -c "from memory import remember; print(remember('preferred_terminal', 'T2', 'user'))"
python -c "from memory import recall; print(recall('terminal'))"
```

`python main.py --demo "..."` still needs the LLM client import in `llm_client.py` to succeed.

--------------------------------------------------------------------------

## Part 2 Observation: Lazy vs Careful Tool Descriptions

We exported two schemas in `schemas.py`: `LAZY_GET_FLIGHT_STATUS_SCHEMA` ("Get flight info.") and `CAREFUL_GET_FLIGHT_STATUS_SCHEMA` (detailed operational description including delay minutes, gate, and when to use the tool). The careful description worked better in testing because the lazy version caused the model to sometimes skip the tool entirely and guess from context or call it without extracting delay specific fields. The careful schema mentions "delay minutes" and "delay reason" which helped the model to pull the right fields for on the time of assessment, even the condition of checking weather tool when asked by user has been tested successfully. Though Lazy descriptions save tokens but increase hallucination risk when the model needs to decide wheather and how to use a tool. For operational domains like flight status, precision in the tool description materially improves grounding. 

--------------------------------------------------------------------------

## Final Report

### 1. Grounding by Retrieval vs Function Calling — Risk Profile Differences

RAG injects unstructured text chunks into the prompt, which can include irrelevant or conflicting passages. the model may synthesize across them without strong provenance, but that is read-only and reversible and the worst outcome is a wrong or incomplete answer. Function calling grounding is structured where each tool returns typed JSON with explicit success or error status so the model receives discrete facts. The risk profile differs: RAG risks confident blending of partial context but read only haalucinations, while function calling risks schema drift or wrong tool selection but produces auditable tool call logs. Function-calling grounding can trigger a real side effect when the wrong tool is chosen or called with the wrong arguments; looking up the wrong flight is harmless, but the same failure mode on a write-capable tool (cancelling a booking, reassigning a gate)
changes real state that a human then has to notice and undo. The risk also compounds across multiple calls in a single loop: a wrong tool choice at step one can feed a plausible looking but wrong argument into step two. On the other hand Function calling is lower risk for operational queries where field-level accuracy where(delay minutes, tail number) matters, provided tools are well-described and errors are handled gracefully.

### 2. Function/Schema Drift — What Happens and How to Detect

Schema drift occurs when the tool implementation changes (new parameters, renamed fields, different error shapes) but the JSON schema or agent prompt is not updated. The model may call outdated function signatures, omit required arguments, or misinterpret new response fields leading to silent failures or hallucinated responses. Drift can be detected by: 
(a) versioning tool schemas and comparing them to `tools.py` signatures in CI 
(b) logging tool call arguments and validating them against JSON Schema before execution
(c) monitoring error rates for `status: "error"` responses and `TypeError` argument mismatches. Regular contract tests in `app.py` catch breaking changes early.

### 3. Write Tools (Cancel Booking, Reassign Gate) — Risk and Safeguards

Write tools mutate operational state and carry significantly higher risk than read-only lookups. A mistake in gate reassignment or a booking cancellation has real customer and safety impact. The safeguard I would add before
shipping either tool is a human-confirmation step in the agent loop itself: any tool tagged as a write or side-effecting action would return a "pending confirmation" result with the exact action and arguments instead
of executing immediately, main.py would surface that to the human operator explicitly, and only a second, separate confirmed call would actually perform the cancellation or reassignment. turning an autonomous action into a proposed action that a person approves, which is the same pattern this assignment already uses for approval-gated actions in other tools.

### 4. Function Descriptions vs System Prompt — Which Mattered More?

Function descriptions mattered more for tool selection and argument filling in our tests. The system prompt sets general tone ("be concise, use tools"), but the per-function schema description determines which tool the model picks and which parameters it extracts from the user query. When we shortened `get_flight_status` to "Get flight info," the model sometimes answered delay questions without calling any tool. Expanding the description to mention "delay minutes" and "on-time" triggers fixed this without changing the system prompt. System prompts help with overall behavior; function descriptions are the primary lever for correct tool routing.

-----------------------------------------------------------------------

## Exploration Notes: 3 Tools vs 6 Tools

In informal testing, exposing 3 tightly scoped tools (flight status, weather, maintenance) reduced erroneous tool calls and kept latency low — the model chose correctly almost every time. Exposing 6–7 tools increased occasional unnecessary calls (e.g., `lookup_aircraft` when the tail number was already in the flight record) but improved coverage for open-ended questions like "Find passenger X and assess their flight's delay risk." The trade-off is precision vs breadth: fewer tools mean simpler routing but require richer tool responses; more tools give flexibility but demand careful descriptions to avoid misfires. For production FlightOps, we'd group tools by role (read vs write) and use a planner step (as in `planner.py`) to prune the active tool set per query.

-----------------------------------------------------------------------

## Screenshots
**For success test added the below screenshots:**
Part6 MultiTool Success 1.png
Part6 MultiTool Success 2.png
Part6 MultiTool Success 3.png

**For Failure test added the below screenshots:**
Part6 Failure 1.png
Part6 Failure 2.png
----------------------------------------------------------------------


