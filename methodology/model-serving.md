# Model Serving — Testing Methodology

How we test and score LLM inference engines and serving platforms in the almanac.

## Scope

This category covers inference engines (vLLM, SGLang, TensorRT-LLM), deployment platforms (KServe, BentoML), and cloud API providers (Fireworks, Together).

## Adapter pattern

```python
class ModelServingAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Start the inference server (docker or cloud), load model
        pass
    
    def load(self, model) -> None:
        # Load model weights, wait for warmup
        pass
    
    def query(self, prompt) -> Response:
        # Send inference request, measure TTFT and TPS
        pass
    
    def teardown(self) -> None:
        # Unload model, stop server, clean GPU memory
        pass
```

## Standard benchmarks

### 1. LLMPerf (Anyscale)
- **What**: Standardized throughput and latency measurement for LLM APIs
- **Why**: Industry-standard comparison metric
- **Metric**: TTFT (time to first token), TPOT (time per output token), throughput (tok/s)

### 2. Berkeley Function Calling Leaderboard
- **What**: Tests function/tool calling accuracy across models
- **Why**: Tool use is critical for agent applications
- **Metric**: Function call accuracy, argument correctness

### 3. Tokens per Dollar (Custom)
- **What**: Cost-normalized throughput comparison
- **Why**: Platform engineers care about cost efficiency
- **Metric**: Tokens per dollar at fixed quality level

## Custom PlatformOps benchmarks

### Throughput sweep
- **Tasks**: Run at concurrency 1, 8, 16, 32, 64, 128, 256
- **Models**: Llama 3.3 70B (FP8), Mistral Small 3, Qwen3 32B
- **Metrics**: TTFT, TPOT, aggregate throughput, GPU utilization

### Long-context stress
- **Tasks**: 4K, 16K, 32K, 64K, 128K token prompts
- **Metrics**: TTFT scaling, KV cache memory usage, prefill throughput

### Structured output
- **Tasks**: JSON schema generation, regex-constrained output, tool calling
- **Metrics**: Constrained decoding throughput, schema adherence rate, latency overhead

### Multi-LoRA serving
- **Tasks**: Serve 10, 50, 100 LoRA adapters on the same base model
- **Metrics**: Adapter switching latency, memory overhead, throughput per adapter

### Fault tolerance
- **Tasks**: Kill a replica mid-request, simulate GPU OOM, network partition
- **Metrics**: Request recovery time, error rate, graceful degradation

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 20% | Model output quality (perplexity, benchmark scores), tool call accuracy |
| **Latency** | 25% | TTFT, TPOT, end-to-end request latency at P50/P95/P99 |
| **Token economics** | 15% | Throughput per dollar, GPU utilization efficiency |
| **Scale behavior** | 15% | Throughput at 1, 8, 32, 128 concurrent requests |
| **Ops burden** | 10% | Deployment complexity, Kubernetes integration, monitoring setup |
| **Developer experience** | 10% | API compatibility (OpenAI format), documentation, error messages |
| **Data sovereignty** | 5% | Self-hosted option, model weight control, local inference |

## Stress suites

### Contradiction storm
- Send requests with conflicting system prompts and user prompts
- Measure: Does the engine handle context correctly? Output quality?

### Near-duplicate flood
- 1000 identical prompts sent simultaneously
- Measure: Prefix caching effectiveness, KV cache reuse, throughput

### Temporal paradox
- Requests with extremely long context followed by short context
- Measure: Memory fragmentation, cache eviction behavior, latency spikes

### Concurrent writers
- 100 clients sending mixed read/write (inference + fine-tuning) requests
- Measure: Resource isolation, priority handling, throughput fairness

### Kill-the-backing-store
- Kill the model server or GPU mid-inference
- Measure: Request recovery, graceful shutdown, data loss

## Known pitfalls

1. **GPU variance**: Same model on different GPUs (H100 vs A100 vs RTX) gives very different results. We specify hardware.
2. **Warmup effects**: First requests are always slower. We discard warmup runs.
3. **Quantization tradeoffs**: FP8 vs INT8 vs INT4 affects both speed and quality. We test at FP8 baseline.
4. **Batching magic**: Continuous batching vs static batching makes 10x difference. We test with continuous batching enabled.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
