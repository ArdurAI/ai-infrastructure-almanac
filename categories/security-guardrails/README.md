# Security, Guardrails & AI Safety

TRiSM market: $3.43B (2026) → $6.43B (2030) at 17% CAGR. 20+ AI safety startups raised $560M in 12 months. Major consolidation: Check Point/Lakera, Palo Alto/Protect AI, SentinelOne/Prompt Security, Cisco/Robust Intelligence. EU AI Act enforcement deadline: August 2, 2026.

## The Roster

| Tier | Tools |
|------|-------|
| **A** | Guardrails AI, NVIDIA NeMo Guardrails, Lakera Guard (Check Point), Future AGI Protect, Prompt Security (SentinelOne), Arthur AI Shield, AWS Bedrock Guardrails, Azure AI Content Safety, Google Model Armor, OpenAI Moderation API, Llama Guard 3 (Meta), Patronus AI, Galileo, Fiddler AI, Confident AI (DeepTeam), Protect AI (Palo Alto), HiddenLayer, WitnessAI, Credo AI |
| **B** | APort / OpenClaw, StackOne Defender, ClawGuard, Nova-tracer, Bifrost, Rebuff, LLM Guard (Protect AI), Noma Security, Harmonic Security, Lasso Security, Quilr, Aurascape, Robust Intelligence (Cisco), Mindgard, Repello, Pillar Security, Cyera, Cato AI Security (ex-Aim), CrowdStrike Falcon, Darktrace, Zscaler, Netskope, Palo Alto Networks, Holistic AI, CalypsoAI, AccuKnox, PyRIT (Microsoft), Garak (NVIDIA), Inspect (UK AISI), Prediction Guard, Fleece AI, ElixirData Context OS, Salesforce Einstein Trust Layer, Legalithm, RegulAI, Alhena AI |
| **C** | DeepKeep, Numalis, TrojAI, Zania, Complyance, Darwin AI, Portal26, AI Score, Alinia, Ciphero, Iridius, Capsule Security, Aigentsphere |

## Key Trends

- **Prompt injection remains #1 vulnerability** (LLM01:2025); roleplay attacks at 89.6% success rate.
- **Agentic AI is the dominant attack surface**: MCP servers and tool-calling agents create new indirect injection pathways.
- **Open-source guardrails matured**: Guardrails AI, NeMo Guardrails, DeepTeam, LLM Guard now enterprise-grade.
- **MCP security is critically immature**: 100% of ~2,000 scanned MCP servers lacked authentication; 30+ CVEs Jan-Feb 2026.

## Benchmarks

- **Standard**: OWASP LLM Top 10, Gandalf, custom injection
- **Custom**: False positive rate, latency overhead, policy expressiveness, setup complexity
- **Stress**: Multi-turn jailbreaks, encoding tricks, tool-call injection, adversarial prompt floods

## See also

- Full catalog: [`../data/roster.json`](../data/roster.json)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
- Benchmark methodology: [`../methodology/benchmark-harness.md`](../methodology/benchmark-harness.md)
