# Testing & Benchmarking

How the almanac tests tools, what the harness does, how scoring works, and how to reproduce results.

## Table of Contents

1. [The Three Benchmark Types](#the-three-benchmark-types)
2. [The Seven Dimensions](#the-seven-dimensions)
3. [The Harness Architecture](#the-harness-architecture)
4. [The Canary](#the-canary)
5. [Standard Benchmarks](#standard-benchmarks)
6. [PlatformOps Custom Benchmarks](#platformops-custom-benchmarks)
7. [Stress Suite](#stress-suite)
8. [Cross-Category Integration Tests](#cross-category-integration-tests)
9. [Scoring](#scoring)
10. [Reproducibility](#reproducibility)
11. [Failure Mode Taxonomy](#failure-mode-taxonomy)

---

## The Three Benchmark Types

Every tool is tested across three types of benchmarks:

| Type | Purpose | Frequency |
|------|---------|-----------|
| **Standard benchmarks** | Verify vendor claims with published test suites | Every benchmark run |
| **PlatformOps custom benchmarks** | Test ops reality: setup, stress, failure modes | Every benchmark run |
| **Cross-category integration tests** | Test how tools work together in a full stack | Quarterly |

## The Seven Dimensions

Every tool is scored 0-100 on each dimension. The final score is a weighted average, but the per-dimension scores are always published.

| Dimension | Weight | What it measures | How it's tested |
|-----------|--------|-----------------|-----------------|
| **Accuracy / Quality** | 25% | Does it produce correct, useful, safe outputs? | Standard benchmarks + custom test suites |
| **Latency** | 15% | Time to first result, throughput, tail latency | Instrumented measurements; p50, p95, p99 |
| **Token Economics** | 15% | Cost per unit of work, pricing predictability | Standardized workloads; $/1K requests, $/1M tokens |
| **Scale Behavior** | 15% | What happens at 10x, 100x load? | Load tests; saturation curves; degradation points |
| **Ops Burden** | 15% | Time to first result, dependency conflicts, upgrade pain | Measured setup time; smoke-gate sweep; dependency matrix |
| **Developer Experience** | 10% | Documentation quality, error messages, debugging, community | Structured rubric; community health metrics |
| **Data Sovereignty** | 5% | Self-hosting viability, audit trails, compliance alignment | Feature matrix; EU AI Act / GDPR / SOC 2 mapping |

### Why these weights?

The weights reflect what a platform engineer actually cares about. Accuracy is the most important — a tool that produces wrong answers is useless regardless of how fast or cheap it is. But ops burden is nearly as important because a tool that consumes your team's life is not worth the accuracy gain.

Weights are reviewed annually. Changes require an RFC and a public comment period.

## The Harness Architecture

```
┌─────────────────────────────────────────┐
│  CategoryAdapter (frozen contract)        │
│  ├── setup()   → install, configure      │
│  ├── load()    → ingest workload         │
│  ├── await_ready() → async barrier     │
│  ├── query()   → run test, get response  │
│  └── teardown() → cleanup, measure       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Telemetry Collector                    │
│  ├── latency (p50/p95/p99)             │
│  ├── token count & cost                  │
│  ├── memory & CPU usage                 │
│  ├── error rate & failure mode taxonomy │
│  └── ops notes (setup time, deps, bugs)  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Grading Pipeline                         │
│  ├── Deterministic grader (exact match)  │
│  ├── LLM judge (frozen prompts, SHA-256)  │
│  ├── Second pass (confidence < 0.7)      │
│  └── Failure mode taxonomy               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Results Publisher                        │
│  ├── Raw JSON (per question, per run)   │
│  ├── Summary tables (per tool)          │
│  ├── Cross-verification analysis          │
│  └── Insight extraction                 │
└─────────────────────────────────────────┘
```

### The `await_ready()` barrier

This is where async-ingestion designs get their cost measured instead of hidden. Many tools (graph builders, vector databases with background indexing, LLM platforms with async workflows) claim "fast" write paths because the actual work happens in the background. The `await_ready()` barrier forces the tool to finish all background work before the query is run, so the true latency is measured.

### The Telemetry Collector

Every adapter call is instrumented:
- **Latency**: `time.monotonic()` around every call; p50, p95, p99 computed across all runs
- **Tokens**: If the tool uses LLM APIs, token counts are captured from API responses
- **Cost**: Token counts × provider pricing; or measured cloud spend for self-hosted tools
- **Memory**: `psutil` or container metrics for memory usage during the run
- **CPU**: CPU utilization during the run
- **Errors**: Every exception, timeout, or unexpected result is logged with full traceback
- **Ops notes**: Human observations about setup friction, dependency conflicts, documentation quality

## The Canary

The first run of every batch is the **no-tool baseline** through the identical pipeline. If the benchmark leaked answers anywhere, the canary would score above zero on answerable categories.

**Canary rules**:
- The canary must score exactly **0.000** on all answerable categories
- The canary must score exactly **1.000** on abstention categories (it should abstain on everything)
- If the canary fails, the entire batch is invalid and must be rerun
- The canary run is published alongside the real results
- The canary adapter is a no-op: setup does nothing, load does nothing, query returns nothing, teardown does nothing

## Standard Benchmarks

### By category

| Category | Benchmark | What it tests | Source |
|----------|-----------|-------------|--------|
| Code Editors | SWE-bench | Code generation correctness on real GitHub issues | [SWE-bench](https://github.com/princeton-nlp/SWE-bench) |
| Code Editors | Exercism | Code correctness on coding exercises | [Exercism](https://exercism.org) |
| Code Editors | Terminal-Bench | Terminal command correctness | [Terminal-Bench](https://github.com/...) |
| Agent Frameworks | GAIA | General AI Assistant capabilities | [GAIA](https://huggingface.co/datasets/gaia-benchmark/GAIA) |
| Agent Frameworks | WebArena | Web-based task completion | [WebArena](https://github.com/web-arena/web-arena) |
| Agent Frameworks | SWE-bench | Agent-based code generation | [SWE-bench](https://github.com/princeton-nlp/SWE-bench) |
| Observability | RAGAS | RAG evaluation accuracy | [RAGAS](https://github.com/explodinggradients/ragas) |
| Observability | DeepEval | LLM evaluation metrics | [DeepEval](https://github.com/confident-ai/deepeval) |
| Vector Databases | ANN-Benchmarks | Retrieval accuracy, latency | [ANN-Benchmarks](https://github.com/erikbern/ann-benchmarks) |
| Vector Databases | BEIR | Zero-shot retrieval | [BEIR](https://github.com/beir-cellar/beir) |
| Vector Databases | MS MARCO | Passage retrieval | [MS MARCO](https://microsoft.github.io/msmarco/) |
| Model Serving | LLMPerf | Throughput, TTFT, TPOT | [LLMPerf](https://github.com/ray-project/llmperf) |
| Model Serving | AnyScale serving benchmark | Serving performance | [AnyScale](https://github.com/anyscale/llmperf) |
| Security | OWASP LLM Top 10 | Defense against known vulnerabilities | [OWASP](https://owasp.org/www-project-top-10-for-large-language-model-applications/) |
| Security | Gandalf | Prompt injection defense | [Lakera](https://gandalf.lakera.ai/) |
| LLMOps | Custom workflow reliability | Workflow execution accuracy | Custom harness |
| Protocols | MCP compliance test | Protocol conformance | Custom harness |
| Protocols | A2A interop | Agent-to-agent interoperability | Custom harness |

### Published vs. reproduced

Every standard benchmark ranking ships a table:

| Tool | Published Claim | Our Result | Delta | Verdict |
|------|----------------|------------|-------|---------|
| Tool A | 95% on X | 92% on X | -3% | ✅ Close |
| Tool B | "fastest" | 3rd of 8 | - | ⚠️ Misleading |
| Tool C | No claim | 87% on X | N/A | — |

## PlatformOps Custom Benchmarks

### Setup experience

**Measured**:
- Time from `git clone` to first working result
- Number of dependency conflicts when installing alongside other roster tools
- Time to resolve dependency conflicts
- Number of undocumented steps required
- Time to find the answer in the docs when stuck

**Scored on**:
- Sub-5 minutes: 90-100
- 5-30 minutes: 70-89
- 30-60 minutes: 50-69
- 60+ minutes or unresolved: 0-49

### Smoke gate

Every tool must pass an identical 3-turn scenario before entering the roster:

```
Turn 1: Store a piece of data
Turn 2: Search/retrieve that data
Turn 3: Update the data and verify the change
```

**Pass criteria**:
- No crashes, no silent failures, no data loss
- Results must be deterministic (same input → same output)
- Tool must handle the basic case without workarounds

**What the smoke gate surfaced** (from the memory almanac, as example):
- Privacy bugs: Redis cache serving deleted data until TTL expires
- Cross-project contamination: Tool writing to a global shared store
- Dependency drift: Direct conflicts between tools on the same dependency
- Cloud tethers: "Self-hosted" tool still calling cloud APIs
- Write-path spread: Sub-millisecond to ~35 seconds for 3 turns

### Stress suite

| Test | What it does | What it reveals |
|------|-------------|---------------|
| **Contradiction storms** | Rapidly store contradictory facts | How the tool handles conflicting data |
| **Near-duplicate floods** | Store thousands of similar items | Deduplication quality, index bloat |
| **Temporal paradoxes** | Store facts that change over time | Temporal reasoning accuracy |
| **Concurrent writers** | Multiple threads/agents writing simultaneously | Race conditions, locking, consistency |
| **Kill-the-backing-store** | Crash the database/service mid-operation | Recovery, data integrity, error handling |
| **Cost-runaway** | Run the tool at maximum scale for 1 hour | Cost predictability, billing accuracy |

### Upgrade path

**Tested**:
- Can you upgrade from version N to N+1 without rewriting everything?
- Are there breaking changes in the API?
- Is there a migration guide?
- Does the tool maintain backward compatibility?

### Debugging experience

**Tested**:
- When the tool fails, can you find out why in <5 minutes?
- Are error messages clear and actionable?
- Is there a debug mode or verbose logging?
- Are there known issues documented?
- Can you trace the execution path?

## Cross-Category Integration Tests

These tests run quarterly and check how tools from different categories work together in a realistic stack:

| Integration | What it tests | Tools involved |
|-------------|-------------|--------------|
| **Agent + Vector DB + Observability** | Full RAG stack with tracing | Agent framework, vector DB, observability tool |
| **Code Editor + Agent Framework** | Can the editor's agent call the framework? | Code editor, agent framework |
| **Security + Model Serving** | Do guardrails add <50ms latency? | Security tool, inference engine |
| **Protocol + All categories** | MCP server compliance, A2A interoperability | Protocol implementation, all tool categories |

## Scoring

### Per-dimension scoring

Each dimension is scored 0-100 using a rubric. The rubric is published before any scoring happens.

**Example: Accuracy rubric**

| Score | Criteria |
|-------|----------|
| 90-100 | ≥95% accuracy on standard benchmarks; no critical failures in stress suite |
| 80-89 | 85-95% accuracy; minor failures in stress suite |
| 70-79 | 75-85% accuracy; some stress suite failures |
| 60-69 | 65-75% accuracy; frequent stress suite failures |
| 50-59 | 55-65% accuracy; significant reliability issues |
| 0-49 | <55% accuracy or fundamentally unreliable |

### Composite score

The composite score is a weighted average of the seven dimensions:

```
Composite = (Accuracy × 0.25) + (Latency × 0.15) + (TokenEconomics × 0.15) +
            (ScaleBehavior × 0.15) + (OpsBurden × 0.15) + (DevEx × 0.10) +
            (DataSovereignty × 0.05)
```

The composite is used for ranking, but the per-dimension scores are always published. A tool with a high composite but low ops burden score is a warning sign.

### Confidence intervals

Every score is reported with a confidence interval computed from the standard error across runs. If the intervals overlap between two tools, the difference is not statistically significant.

## Reproducibility

### How to reproduce a benchmark

1. Clone the benchmark harness repo (published separately)
2. Check out the exact commit used for the run (recorded in the results JSON)
3. Install the exact dependencies (lockfile is published)
4. Run the harness with the same adapter and same seed
5. Compare your results to the published results

### What is frozen

| Element | How it's frozen | Where to find it |
|---------|---------------|------------------|
| Judge model | Pinned model name and version | `results.json` metadata |
| Judge prompts | SHA-256 hash | `methodology/benchmark-harness.md` |
| Control variables | Documented values | `results.json` metadata |
| Random seeds | Published integer | `results.json` metadata |
| Adapter code | Published in harness repo | Separate repo |
| Test workloads | Published JSON files | `benchmarks/` directory |

### What is NOT frozen (and why)

| Element | Why it changes | How we handle it |
|---------|---------------|------------------|
| Tool versions | Tools update | We re-run benchmarks for new versions; old results are archived |
| Provider pricing | Cloud pricing changes | Cost is computed at runtime using current pricing; historical results are annotated |
| Hardware | We may upgrade machines | Hardware spec is recorded in `results.json`; results are hardware-specific |

## Failure Mode Taxonomy

Every failure is classified into a taxonomy. This helps identify patterns across tools and categories.

| Category | Failure Modes |
|----------|--------------|
| **Setup** | `install_failed`, `dependency_conflict`, `config_error`, `missing_env_var`, `docs_incomplete` |
| **Ingestion** | `write_timeout`, `write_crash`, `data_loss`, `index_corruption`, `async_lag` |
| **Query** | `query_timeout`, `query_crash`, `wrong_result`, `hallucination`, `missing_recall`, `irrelevant_result` |
| **Scale** | `throughput_degradation`, `memory_leak`, `cpu_spike`, `connection_pool_exhaustion`, `rate_limit_hit` |
| **Ops** | `upgrade_breaking`, `undocumented_behavior`, `debug_opacity`, `community_unresponsive` |
| **Security** | `prompt_injection`, `data_leakage`, `pii_exposure`, `jailbreak`, `tool_spoofing` |
| **Integration** | `mcp_noncompliant`, `a2a_noncompliant`, `auth_failure`, `protocol_mismatch` |

## License

Content: CC BY 4.0  
Code: MIT
