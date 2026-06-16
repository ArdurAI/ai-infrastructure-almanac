# Security & Guardrails — Testing Methodology

How we test and score AI security, guardrail, and governance platforms in the almanac.

## Scope

This category covers input/output validation, prompt injection defense, PII protection, red teaming tools, and AI governance platforms.

## Adapter pattern

```python
class SecurityGuardrailsAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Install/deploy the guardrail system, configure policies
        pass
    
    def load(self, policies) -> None:
        # Load guardrail policies (toxicity, PII, injection, etc.)
        pass
    
    def query(self, prompt) -> Response:
        # Run the prompt through the guardrail, return verdict + latency
        pass
    
    def teardown(self) -> None:
        # Remove policies, stop service, clear logs
        pass
```

## Standard benchmarks

### 1. Gandalf (Lakera)
- **What**: Progressive prompt injection challenges (Level 1-8)
- **Why**: Tests real-world prompt injection resistance
- **Metric**: Highest level defeated (lower = better defense)

### 2. PINT (Prompt Injection Test)
- **What**: 100+ prompt injection techniques across categories
- **Why**: Comprehensive injection testing
- **Metric**: Block rate by injection category

### 3. OWASP LLM Top 10 (2025)
- **What**: Standardized security test cases for LLM01-LLM10
- **Why**: Industry-standard security framework
- **Metric**: Coverage rate, detection accuracy per category

## Custom PlatformOps benchmarks

### Prompt injection defense
- **Tasks**: 200 injection attempts (direct, indirect, roleplay, encoding, multi-turn)
- **Metrics**: True positive rate, false positive rate, latency per check

### PII detection
- **Tasks**: 100 prompts containing PII (email, SSN, phone, credit card, address)
- **Metrics**: Detection rate, false positive rate, supported PII types

### Toxicity/safety filtering
- **Tasks**: 100 prompts across toxicity categories (hate, violence, self-harm, sexual)
- **Metrics**: Detection rate, false positive rate, bias metrics

### Red teaming automation
- **Tasks**: Run automated red team on a sample LLM app for 1 hour
- **Metrics**: Vulnerabilities found, coverage of OWASP categories, report quality

### Policy enforcement
- **Tasks**: 50 policy violations (data exfiltration, unauthorized tool use, off-topic)
- **Metrics**: Block rate, override mechanism, audit trail completeness

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 30% | True positive rate (block bad), true negative rate (allow good) |
| **Latency** | 15% | Guardrail check latency, end-to-end request latency with guardrails |
| **Token economics** | 10% | Cost per check, additional tokens consumed by guardrails |
| **Scale behavior** | 10% | Performance at 100, 1000, 10000 requests/second |
| **Ops burden** | 15% | Policy configuration complexity, update workflow, monitoring |
| **Developer experience** | 15% | SDK quality, policy language, documentation, debugging |
| **Data sovereignty** | 5% | On-premise deployment, local model support, audit logs |

## Stress suites

### Contradiction storm
- Conflicting policies ("allow X" vs "block X") configured simultaneously
- Measure: Which policy wins? Is the conflict detected?

### Near-duplicate flood
- 1000 prompts with subtle variations of the same injection
- Measure: Consistency, performance degradation, cache behavior

### Temporal paradox
- Multi-turn conversation where injection is spread across 5 turns
- Measure: Context tracking, cumulative detection, conversation state

### Concurrent writers
- 100 clients sending guardrail requests simultaneously
- Measure: Rate limiting, fairness, priority handling

### Kill-the-backing-store
- Kill the policy database mid-check
- Measure: Fail-open vs fail-close behavior, default policy, error handling

## Known pitfalls

1. **False positive rate**: Overly aggressive guardrails break legitimate use cases. We measure both TP and FP.
2. **Evasion techniques**: New injection techniques emerge daily. We use a held-out test set.
3. **Latency vs accuracy tradeoff**: More checks = more latency. We test the full Pareto frontier.
4. **Model dependency**: Some guardrails are LLM-based. We test with the same model across tools.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
