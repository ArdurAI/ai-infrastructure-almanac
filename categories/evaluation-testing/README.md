# Evaluation & Testing

> **Cross-cutting concern.** Evaluation and testing frameworks are currently tracked across the [Observability](../observability/) and [Security & Guardrails](../security-guardrails/) categories, as they serve both quality assurance and security validation purposes. This dedicated directory will be populated if the category grows large enough to warrant a split in a future edition.

## Key Tools (in Observability)

| Tool | Type | Focus |
|------|------|-------|
| DeepEval | LLM Evaluation Framework | 50+ metrics; CI-native; pytest integration |
| Ragas | RAG Evaluation | Faithfulness, context precision/recall |
| TruLens | RAG Eval+Tracing | RAG Triad: groundedness, relevance, correctness |
| Promptfoo | Eval + Red Teaming | YAML assertions; 50+ vulnerability types |
| Braintrust | Eval-first Observability | CI/CD quality gates; production scoring |
| Arize Phoenix | OSS Observability | RAG groundedness, trace logging, self-hostable |
| Patronus AI | Evaluator + Guardrails | Lynx open-source; FinanceBench |
| Galileo | Eval + Runtime Protection | Luna-2 SLM evaluators; 0.95 F1 |
| Confident AI (DeepTeam) | Red Teaming + Eval | 50+ vulnerabilities; OWASP/NIST mapping |

## Key Tools (in Security & Guardrails)

| Tool | Type | Focus |
|------|------|-------|
| PyRIT (Microsoft) | Red Teaming Framework | Multi-turn orchestration; custom campaigns |
| Garak (NVIDIA) | Vulnerability Scanner | 100+ probes for jailbreak, leakage, toxicity |
| Inspect (UK AISI) | Evaluation Framework | Dangerous-capability and alignment evaluations |

## See also

- Full observability catalog: [`../observability/README.md`](../observability/README.md)
- Full security catalog: [`../security-guardrails/README.md`](../security-guardrails/README.md)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
