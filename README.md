# AI Infrastructure Almanac

A living encyclopedia of the tools, platforms, and standards that make AI/LLM systems production-ready. Updated monthly with fresh metadata, releases, landscape shifts, and independent benchmark results from the *"Platform Engineer's Quest for the Best"* series.

> Vendors publish their own benchmark numbers. Nobody reproduces them independently, and nobody evaluates infrastructure tools the way a platform engineer has to live with them: ops burden, failure modes, scale curves, cost, and real-world edge cases. This almanac is the public record of that work.

## Scope

This almanac covers the full AI infrastructure stack — everything that sits between the foundation model and the end user:

| Category | What it covers |
|----------|---------------|
| **Code Editors** | AI-native IDEs, IDE assistants, terminal coding agents, code review tools |
| **Agent Frameworks** | Multi-agent orchestration, stateful workflows, role-based crews, protocol implementations |
| **Observability** | LLM tracing, agent monitoring, cost tracking, GPU monitoring, evaluation platforms |
| **Vector Databases** | Vector stores, ANN libraries, RAG frameworks, document parsers, rerankers |
| **Model Serving** | Inference engines, deployment platforms, API gateways, edge/on-device inference |
| **Security & Guardrails** | Input/output validation, prompt injection defense, PII protection, AI governance |
| **LLMOps Platforms** | Workflow builders, prompt management, no-code/low-code AI platforms, CI/CD for AI |
| **Context & Protocols** | MCP, A2A, authentication standards, integration patterns, agent identity |
| **Memory** | *(Tracked separately at [agent-memory-almanac](https://github.com/ArdurAI/agent-memory-almanac))* |

## How to use this repo

| You want… | Go to |
|-----------|-------|
| The state of the landscape right now | The latest file in `editions/` |
| Everything we know about one tool | `categories/<category>/tools/<name>.md` |
| Machine-readable roster + metadata | `data/roster.json` |
| Architecture diagrams + stack layers | `architecture.md` |
| Benchmark results (rolling) | `benchmarks/` |
| How tools are tested and ranked | `methodology/benchmark-harness.md` |

## The roster at a glance (June 2026)

**Tier A — Code Editors**: Cursor · GitHub Copilot · Claude Code · Windsurf · OpenCode · Cline · Aider · Continue · Trae · Tabnine · Zed · Devin

**Tier A — Agent Frameworks**: LangGraph · CrewAI · Claude Agent SDK · OpenAI Agents SDK · Mastra · Pydantic AI · Google ADK · Microsoft Agent Framework · Agno · LlamaIndex

**Tier A — Observability**: LangSmith · Langfuse · Braintrust · Arize · Helicone · Portkey · Pydantic Logfire · OpenLIT · Datadog LLM Observability · Weights & Biases Weave

**Tier A — Vector Databases**: Pinecone · Qdrant · Weaviate · Milvus · Chroma · pgvector · Zilliz · Turbopuffer · Elasticsearch · Redis Vector

**Tier A — Model Serving**: vLLM · SGLang · TensorRT-LLM · llama.cpp · NVIDIA Dynamo · KServe · BentoML · Ray Serve · Ollama · LMDeploy

**Tier A — Security & Guardrails**: Guardrails AI · NVIDIA NeMo Guardrails · Lakera · Arthur AI · Fiddler · Protect AI · HiddenLayer · WitnessAI · Credo AI

**Tier A — LLMOps Platforms**: Dify · Flowise · n8n · Vellum · PromptLayer · Pezzo · Zapier · Gumloop · Make

**Tier A — Protocols & Standards**: MCP · A2A · UCP · x402 · OAuth 2.1 for AI · WIMSE · OpenTelemetry GenAI

## Methodology

Results published here come from a frozen-before-results harness:

- **Standard benchmarks** for comparability with published claims — every ranking ships a *published vs. reproduced* table.
- **Custom PlatformOps benchmarks**: memory on infrastructure work, code generation quality, retrieval accuracy, inference latency, security robustness, and workflow reliability.
- **Stress suites**: contradiction storms, near-duplicate floods, temporal paradoxes, concurrent writers, kill-the-backing-store chaos, cost-runaway measurement.
- **Seven scored dimensions**: accuracy, latency, token economics, scale behavior, **ops burden**, developer experience, data sovereignty.

The judge model, prompts (SHA-256-frozen), and control variables are fixed before any tool runs. Raw results JSON is published with every ranking. The benchmark harness repo goes public alongside the first article of the series.

## Update cadence

One edition per month under `editions/YYYY-MM.md`: refreshed GitHub metadata for every roster entry, notable releases, new entrants triaged in or out, and a short diary of what the Quest tested that month.

## Benchmark cadence

One benchmark release per quarter under `benchmarks/<category>-<suite>-<date>.md`: frozen methodology, raw results JSON, per-tool deep-dives, and cross-category insight synthesis.

## License

Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
