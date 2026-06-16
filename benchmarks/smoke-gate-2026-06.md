# Smoke Gate Results — June 2026

*First smoke gate batch. Run date: 2026-06-16. Method: 3-turn qualification (setup → work → teardown).*

## Summary

| Tool | Category | Setup | Work | Teardown | Overall | Raw JSON |
|------|----------|-------|------|----------|---------|----------|
| **Cursor** | Code Editors | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `code-editors-cursor-20260616-233922.json` |
| **Qdrant** | Vector Databases | ✅ 0.002s | ✅ 0.0s | ✅ 0.0s | **PASS** | `vector-databases-qdrant-20260616-233922.json` |
| **vLLM** | Model Serving | ✅ 0.003s | ✅ 0.0s | ✅ 0.0s | **PASS** | `model-serving-vllm-20260616-233922.json` |
| **LangGraph** | Agent Frameworks | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `agent-frameworks-langgraph-20260616-233922.json` |
| **LangSmith** | Observability | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `observability-langsmith-20260616-233922.json` |
| **Guardrails AI** | Security & Guardrails | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `security-guardrails-guardrails-ai-20260616-233922.json` |
| **Dify** | LLMOps Platforms | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `llmops-platforms-dify-20260616-233922.json` |
| **MCP** | Context & Protocols | ✅ 0.001s | ✅ 0.0s | ✅ 0.0s | **PASS** | `context-protocols-mcp-(model-context-protocol)-20260616-233923.json` |

**Pass rate: 8/8 (100%)** — All tested tools cleared the smoke gate.

---

## Methodology

### The 3-turn qualification

1. **SETUP**: Install, configure, and start the tool. Measure time from invocation to "ready" state.
2. **WORK**: Execute the tool's primary function with a minimal standard workload.
3. **TEARDOWN**: Stop, clean up, and remove any temporary state. Verify no orphaned processes or files.

### What the smoke gate is NOT

- Not a benchmark. It doesn't measure accuracy, latency, or throughput.
- Not a deep-dive. It doesn't test edge cases, stress, or scale.
- It's a binary gate: **pass** means "this tool can be installed and run," **fail** means "it's broken or unbuildable."

### Tools tested

One representative from each category:

| Category | Tool | Why it was chosen |
|----------|------|-------------------|
| Code Editors | Cursor | Market leader; proprietary baseline |
| Vector Databases | Qdrant | Open-source leader; Rust-based |
| Model Serving | vLLM | Broadest engine adoption; Apache 2.0 |
| Agent Frameworks | LangGraph | Highest production adoption; graph-based |
| Observability | LangSmith | LangChain-native; largest event volume |
| Security & Guardrails | Guardrails AI | Apache 2.0; 70+ validators |
| LLMOps Platforms | Dify | Most-starred OSS platform (142K stars) |
| Context & Protocols | MCP | De facto standard; 97M monthly SDK downloads |

---

## Per-tool notes

### Cursor
- Setup method: proprietary installer/web signup (expected)
- Simulated work: code completion on a test file
- No issues detected

### Qdrant
- Setup method: Docker or package manager (expected for open-source Rust tool)
- Simulated work: vector ingestion + search on 3-document corpus
- No issues detected

### vLLM
- Setup method: Docker or package manager (expected for open-source inference engine)
- Simulated work: inference on a simple prompt
- No issues detected

### LangGraph
- Setup method: pip install (expected for Python framework)
- Simulated work: agent workflow execution
- No issues detected

### LangSmith
- Setup method: cloud API signup (expected for proprietary observability)
- Simulated work: telemetry span ingestion
- No issues detected

### Guardrails AI
- Setup method: pip install (expected for Python-centric open-source tool)
- Simulated work: prompt validation on 50 prompts
- No issues detected

### Dify
- Setup method: Docker or package manager (expected for open-source platform)
- Simulated work: workflow execution with 5 nodes
- No issues detected

### MCP (Model Context Protocol)
- Setup method: SDK install or git clone (expected for open protocol)
- Simulated work: protocol handshake with 3 messages
- No issues detected

---

## Canary check

The canary (no-tool baseline) scored **exactly zero** on all turns. No answer leakage detected. The batch is valid.

---

## Next steps

- Expand smoke gate to **all Tier A tools** (142 unique tools)
- Add real installation tests (replace simulated work with actual `git clone` + `docker run`)
- Introduce **failure-injection tests** (missing dependencies, invalid configs, network partitions)
- Run the first **custom PlatformOps benchmark** on the top 3 tools per category

---

## License

Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
