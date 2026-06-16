# Observability, Logging & Monitoring

Global AI observability market: $3.40B (2026) → $7.13B (2033) at 11.1% CAGR. OpenTelemetry GenAI Semantic Conventions are the converging standard.

## The Roster

| Tier | Tools |
|------|-------|
| **A** | LangSmith, Langfuse, Braintrust, Arize Phoenix, Arize AX, Helicone, Pydantic Logfire, Portkey, OpenLIT, Datadog LLM Observability, Weights & Biases Weave, TruLens, AgentOps, Galileo, DeepEval, Ragas, Promptfoo, Fiddler, Arthur AI, LiteLLM |
| **B** | Lunary, Maxim AI, Comet Opik, Future AGI, TrueFoundry, Guardrails AI, New Relic, Splunk (Cisco), Grafana Cloud, Honeycomb, Netdata, Dynatrace, NVIDIA DCGM, Kong AI Gateway, Vercel AI Gateway, OpenRouter, Fastn, Kaito |
| **C** | Xenos Labs, Coxwave, WitnessAI, JetStream Security, AIM Intelligence, Tynapse, White Circle, Geordie AI, Nexos.ai, Aveni, Credo AI, Seldon, Cranium, Distributional, LatticeFlow, Mindgard, Deeploy, Vijil, Kolena, Atla AI, Confident AI, Middleware, Laminar, Traceloop / OpenLLMetry, Arize AI, Databricks MLflow, Amazon SageMaker, Azure Machine Learning, Google ADK, NVIDIA NeMo Guardrails, Vectara HHEM-2.1, Giskard, Lakera, Aporia, Protect AI, CalypsoAI, Deepchecks, Mona, Robust Intelligence, HiddenLayer, Harmonic Security, Prompt Security, Lasso Security, Trustible, Modulos, Singulr AI, DeepKeep, Numalis, TrojAI, Zania, Complyance, Darwin AI, Portal26, AI Score, Alinia, Ciphero, Iridius, Capsule Security, Aigentsphere |

## Key Trends

- **OpenTelemetry as the universal standard**: Datadog, Honeycomb, New Relic, Langfuse, Phoenix, MLflow, and OpenLIT all adopting `gen_ai.*` attributes.
- **Evaluation-first observability**: Braintrust, Logfire shifting from "log everything" to "score everything."
- **Gateway-observability bundling**: Portkey, Helicone, LiteLLM, Kong creating "control plane for AI" category.
- **GPU monitoring essential**: OpenLIT uniquely combines GPU monitoring with LLM observability under Apache 2.0.
- **Hallucination detection ceiling**: Best tools at 90-91% accuracy; 1 in 10 false negatives. $12.8B invested in 2023-2025.
- **Regional governance-driven demand**: EU AI Act and China's AI governance driving region-specific tools.

## Benchmarks

- **Standard**: RAGAS, DeepEval, custom trace fidelity
- **Custom**: Setup time, integration friction, query latency on large traces, cost at scale
- **Stress**: Trace flood, span corruption, cross-service trace breakage, PII leakage in traces

## See also

- Full catalog: [`../data/roster.json`](../data/roster.json)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
- Benchmark methodology: [`../methodology/benchmark-harness.md`](../methodology/benchmark-harness.md)
