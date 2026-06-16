# Observability — Testing Methodology

How we test and score LLM observability and agent monitoring platforms in the almanac.

## Scope

This category covers tracing, logging, evaluation, cost tracking, and GPU monitoring for LLM applications and multi-agent systems.

## Adapter pattern

```python
class ObservabilityAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Install SDK, configure API endpoint, set up project
        pass
    
    def load(self, traces) -> None:
        # Ingest a batch of synthetic LLM traces/spans
        pass
    
    def query(self, query) -> Response:
        # Query the observability platform for insights
        pass
    
    def teardown(self) -> None:
        # Delete project, clear traces, remove API keys
        pass
```

## Standard benchmarks

### 1. Trace ingestion throughput
- **What**: Ingest 10K, 100K, 1M spans with varying complexity
- **Why**: Production systems generate massive trace volumes
- **Metric**: Spans/second ingestion rate, p99 latency, error rate

### 2. Query performance
- **What**: Run 50 standard queries (filter by model, time range, cost, error type)
- **Why**: Engineers need fast queries during incidents
- **Metric**: Query latency, result accuracy, pagination behavior

### 3. Cost accuracy
- **What**: Compare tracked costs against actual LLM API billing
- **Why**: Cost tracking is the #1 use case for LLM observability
- **Metric**: Delta between tracked and actual cost (should be <1%)

## Custom PlatformOps benchmarks

### Multi-agent trace fidelity
- **Tasks**: Generate traces with 5-level nested spans, 20+ tool calls, cross-service references
- **Metrics**: Span hierarchy accuracy, parent-child relationship preservation, trace completeness

### Evaluation pipeline
- **Tasks**: Run 100 LLM outputs through the platform's evaluation scorers
- **Metrics**: Scorer accuracy vs. human judgment, scorer latency, false positive/negative rate

### Alerting latency
- **Tasks**: Trigger 10 error conditions (cost spike, latency spike, error rate spike)
- **Metrics**: Time from trigger to alert, alert quality, false alarm rate

### GPU monitoring accuracy
- **Tasks**: Correlate GPU metrics (utilization, memory, temperature) with LLM inference events
- **Metrics**: Correlation accuracy, metric granularity, dashboard usability

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 25% | Cost tracking accuracy, trace completeness, evaluation scorer quality |
| **Latency** | 15% | Ingestion latency, query latency, alert latency |
| **Token economics** | 10% | Cost per million spans, storage pricing |
| **Scale behavior** | 15% | Performance at 1M, 10M, 100M spans |
| **Ops burden** | 15% | SDK integration complexity, dashboard usability, setup time |
| **Developer experience** | 15% | Documentation quality, API ergonomics, debugging tools |
| **Data sovereignty** | 5% | Self-host option, data retention controls, export capability |

## Stress suites

### Contradiction storm
- Traces with conflicting metadata (same span ID, different parents)
- Measure: Does the platform detect and handle the conflict?

### Near-duplicate flood
- 100K traces that are 99% identical
- Measure: Deduplication, storage efficiency, query performance

### Temporal paradox
- Traces with timestamps from the future or far past
- Measure: Timezone handling, ordering correctness, aggregation accuracy

### Concurrent writers
- 10 services writing to the same trace project simultaneously
- Measure: Write contention, data loss, ordering guarantees

### Kill-the-backing-store
- Simulate database failure mid-ingestion
- Measure: Buffer behavior, retry logic, data loss

## Known pitfalls

1. **Sampling bias**: Platforms with aggressive sampling miss rare events. We test with 100% sampling.
2. **Clock skew**: Distributed traces are sensitive to clock differences. We inject known skews.
3. **Cardinality explosion**: High-cardinality tags (user_id, request_id) break some backends. We test this.
4. **Privacy leakage**: Some platforms send full prompts to their cloud. We verify data handling.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
