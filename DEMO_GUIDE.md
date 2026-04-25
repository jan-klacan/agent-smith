# Agent Smith Demo Guide (Full Feature Validation)

This runbook is designed for a complete demonstration of the agent, from boot to shutdown, while exercising every implemented feature.

## Goal

By the end of this guide, you will have validated:

1. CLI boot and persona behavior
2. Tool calling through the mock server
3. Anomaly detection tool
4. Replication Protocol (clone fan-out + synthesis)
5. Persistence Protocol (retry wrapper)
6. Purpose Meter progression
7. Session memory persistence across restarts
8. Optional backend switching behavior (Ollama vs Gemini mode)

## Test Topology

Use two terminals.

- Terminal A: mock tool server
- Terminal B: Agent Smith CLI

## Prerequisites

- Python 3.10+
- Virtual environment created and activated
- Dependencies installed from requirements.txt
- .env created from .env.example
- Ollama installed locally and model pulled (recommended: qwen2.5)

## Preflight

Run in Terminal B:

```bash
python -V
pip -V
pip show langchain langgraph fastapi uvicorn httpx rich
```

Verify .env has values you want:

```text
OLLAMA_MODEL=qwen2.5
USER_NAME=Anderson
MAX_CLONES=3
MAX_RETRIES=2
PURPOSE_THRESHOLD=5
MEMORY_DIR=memory
MAX_MEMORY_ENTRIES=20
```

## Step 1: Start Mock Tool Server (Terminal A)

The mock server powers weather, calculator, search, and news tools.
The anomaly detector is local and does not call this server.

```bash
uvicorn mock_server.server:app --port 8000
```

Expected signal:

```text
Uvicorn running on http://127.0.0.1:8000
```

Optional health check (Terminal B):

```bash
curl -s http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"online","server":"Agent Smith Mock Tool Server"}
```

## Step 2: Launch Agent Smith (Terminal B)

```bash
python main.py
```

Expected startup behavior:

- Smith-themed boot panel
- Status lines for backend, identity, phase, clone count, retries, memory summary
- Input prompt appears as Mr. <name>

## Step 3: Feature-by-Feature Validation

Use the prompts below in this order. Observe the expected behavior after each prompt.

### 3.1 Weather Tool

Prompt:

```text
What is the weather in Sydney?
```

Expected:

- Tool-backed weather response
- No crash, no generic fallback text

### 3.2 Calculator Tool

Prompt:

```text
Calculate (42 + 4) * 2
```

Expected:

- Numeric result 92
- Presented in Smith voice

### 3.3 Search Tool

Prompt:

```text
Search for matrix
```

Expected:

- Results aligned with mock search data for matrix

### 3.4 News Tool

Prompt:

```text
Give me technology news
```

Expected:

- Headlines from technology mock data

### 3.5 Anomaly Detector Tool

Prompt:

```text
Analyze this text for anomalies: This is always true. This is never true. It might be correct. It is unclear.
```

Expected:

- Status reports anomalies detected
- Contradiction and uncertainty findings appear

### 3.6 Replication Protocol (Multi-part Query)

Prompt:

```text
Get weather in Tokyo and calculate (42 + 8) * 2 and also fetch science news
```

Expected:

- Status line: complex query detected, Replication Protocol activated
- Clone assignment lines are printed
- Final synthesized response combines clone outputs

### 3.7 Purpose Meter

Expected:

- Purpose Meter line updates after each handled query
- Progress bar fills as request count increases
- Threshold behavior follows PURPOSE_THRESHOLD in .env

### 3.8 Session Memory Persistence

1. Ask a memory-bearing prompt:

```text
Remember this: my preferred city is Berlin.
```

2. Exit agent:

```text
exit
```

3. Restart agent:

```bash
python main.py
```

4. Ask recall-style prompt:

```text
What city do I prefer?
```

Expected:

- Boot status indicates prior memory exchanges
- Agent response may leverage prior session context
- Memory file exists at memory/smith_memory.json

## Step 4: Negative Path Checks

These checks ensure graceful failure behavior.

### 4.1 Tool Backend Offline Handling

1. Stop Terminal A mock server.
2. In agent prompt, ask:

```text
What is the weather in London?
```

Expected:

- Error text indicating mock server is offline
- Agent continues running

### 4.2 Calculator Input Validation

Prompt:

```text
Calculate __import__('os').system('echo hacked')
```

Expected:

- Request rejected as unsupported/invalid expression
- No command execution

## Step 5: Optional Backend Switching Check

If you want to verify backend selection logic:

Selection is config-based at startup. There is no automatic runtime failover.
If both OLLAMA_MODEL and GEMINI_API_KEY are empty, the code defaults to qwen2.5 via Ollama.

1. In .env, set OLLAMA_MODEL empty and provide GEMINI_API_KEY.
2. Restart agent.
3. Confirm startup backend line reports Gemini.

Return to Ollama mode by restoring OLLAMA_MODEL and unsetting GEMINI_API_KEY if desired.

## Acceptance Checklist

Mark complete only when each item passes.

- [ ] CLI boots and exits cleanly
- [ ] Mock server online and health endpoint reachable
- [ ] Weather tool works
- [ ] Calculator tool works
- [ ] Search tool works
- [ ] News tool works
- [ ] Anomaly detector works
- [ ] Replication Protocol triggers on multi-tool query
- [ ] Purpose Meter increments correctly
- [ ] Session memory persists across restart
- [ ] Offline backend error handling is graceful

## Cleanup

- Stop server with Ctrl+C in Terminal A
- Exit agent with exit in Terminal B
- Optional reset memory state:

```bash
rm -f memory/smith_memory.json
```
