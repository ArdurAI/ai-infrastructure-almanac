# Architecture of the AI Infrastructure Stack

How the AI infrastructure landscape is shaped, and how the Quest tests it.

## The eight layers

Every tool on the roster, whatever its marketing, resolves to one of eight architectural layers — plus the protocol layer that cuts across them all:

```mermaid
flowchart TD
    subgraph L1["1 · Code Editors"]
        direction TB
        l1a["IDE / Editor"] --> l1b["AI assistant layer"] --> l1c["Agent harness"]
    end
    subgraph L2["2 · Agent Frameworks"]
        direction TB
        l2a["Orchestration model"] --> l2b["State / memory management"] --> l2c["Tool / protocol binding"]
    end
    subgraph L3["3 · Observability"]
        direction TB
        l3a["Telemetry ingestion"] --> l3b["Trace reconstruction"] --> l3c["Evaluation / scoring"]
    end
    subgraph L4["4 · Vector Databases"]
        direction TB
        l4a["Embedding ingestion"] --> l4b["Index build / ANN"] --> l4c["Retrieval / reranking"]
    end
    subgraph L5["5 · Model Serving"]
        direction TB
        l5a["Model loading / quantization"] --> l5b["Request scheduling"] --> l5c["Token streaming"]
    end
    subgraph L6["6 · Security & Guardrails"]
        direction TB
        l6a["Input validation"] --> l6b["Output filtering"] --> l6c["Policy enforcement / audit"]
    end
    subgraph L7["7 · LLMOps Platforms"]
        direction TB
        l7a["Workflow design"] --> l7b["Prompt lifecycle"] --> l7c["Deployment / CI"]
    end
    subgraph L8["8 · Context & Protocols"]
        direction TB
        l8a["Discovery / identity"] --> l8b["Authentication / authorization"] --> l8c["Message transport"]
    end

    L1 -.-> CodeEditors["Cursor · Copilot · Claude Code · OpenCode · Cline"]
    L2 -.-> AgentFrameworks["LangGraph · CrewAI · Mastra · Pydantic AI · ADK"]
    L3 -.-> Observability["LangSmith · Langfuse · Braintrust · Arize · Helicone"]
    L4 -.-> VectorDBs["Pinecone · Qdrant · Weaviate · Milvus · Chroma · pgvector"]
    L5 -.-> ModelServing["vLLM · SGLang · TensorRT-LLM · llama.cpp · Dynamo"]
    L6 -.-> Security["Guardrails AI · NeMo · Lakera · Arthur · Fiddler"]
    L7 -.-> LLMOps["Dify · Flowise · n8n · Vellum · PromptLayer"]
    L8 -.-> Protocols["MCP · A2A · UCP · x402 · OAuth 2.1 · WIMSE"]
```

**Protocol layer** — MCP, A2A, UCP, x402, OpenTelemetry GenAI conventions — cuts across all eight layers, providing the connective tissue that lets tools interoperate.

## The four write-path shapes (for stateful layers)

Within the stateful layers (memory, vector DB, observability, LLMOps), every tool resolves to one of four write-path designs:

| Shape | Description | Examples |
|-------|-------------|----------|
| **Fact extractors** | LLM extracts salient facts → reconcile → vector store | Mem0, Memori |
| **Graph builders** | LLM extracts entities + relations → temporal edges → graph DB | Graphiti, Cognee |
| **Profile / user-modelers** | LLM updates structured profile → profile + event log | Memobase, Honcho |
| **OS-style managers** | Agent loop manages its own memory → core ↔ archival store | Letta, MemOS |

## How the Quest tests a category

Same harness philosophy for all eight categories: the judge was frozen before any tool ran.

```mermaid
flowchart LR
    subgraph Adapter[frozen CategoryAdapter contract]
        direction LR
        A["setup()\ninstall & configure"] --> B["load()\ningest workload"] --> C["await_ready()\nasync barrier"] --> D["query()\ninjectable context"]
    end
    D --> E[answering / measuring system]
    E --> F{deterministic grader}
    F -->|exact-match types| V[verdict]
    F -->|free-form / subjective| J[LLM judge · frozen prompts]
    J -->|confidence < 0.7| J2[second independent pass]
    J --> V
    J2 --> V
    V --> L[(raw results JSON\npublished)]
    T[telemetry: latency · tokens · $ · ops notes] -.-> A & B & C & D
```

The `await_ready()` barrier is where async-ingestion designs (graph extraction, cognify, deriver queues, re-encodes) get their cost measured instead of hidden.

## Current landscape readings

- **Code editors**: Terminal-native agents are the fastest-growing subcategory; 60%+ of devs use AI coding daily.
- **Agent frameworks**: Consolidated to ~8 serious production options; TypeScript (Mastra) and Rust (Rig, OpenFANG) now have first-class frameworks.
- **Observability**: OpenTelemetry GenAI conventions are the converging standard; Langfuse acquired by ClickHouse; Braintrust raised $80M Series B.
- **Vector DBs**: Postgres vs. dedicated DB is the central fork; parser quality is the #1 RAG bottleneck.
- **Model serving**: vLLM + SGLang + TensorRT-LLM dominate; NVIDIA Dynamo 1.0 replaces Triton for LLMs; K8s-native serving is the production default.
- **Security**: $3.43B TRiSM market; 20+ startups raised $560M; major consolidation (Check Point/Lakera, Palo Alto/Protect AI).
- **LLMOps**: Dify at 142K stars; evaluation-first development replaced "ship and pray"; 73% of enterprises require agent monitoring.
- **Protocols**: MCP is the undisputed agent-to-tool standard (97M monthly downloads); A2A converging for agent-to-agent; security is the critical gap (100% of scanned MCP servers lacked authentication).
