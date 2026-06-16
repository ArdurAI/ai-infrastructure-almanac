# Model Serving & Inference Engines

Three dominant open-source engines: vLLM (broadest support), SGLang (RAG/multi-turn leader), TensorRT-LLM (highest throughput on NVIDIA). NVIDIA Dynamo 1.0 (Mar 2026) is the production-grade distributed orchestration layer, replacing Triton for LLMs. K8s-native serving is the production default.

## The Roster

| Tier | Tools |
|------|-------|
| **A** | vLLM, SGLang, TensorRT-LLM, llama.cpp, NVIDIA Dynamo, KServe, BentoML, Ray Serve, Ollama, LMDeploy, Fireworks AI, Together AI, RunPod, Lambda Labs, LiteLLM, Portkey |
| **B** | TGI (Text Generation Inference), DeepSpeed-MII, Aphrodite Engine, MLX, ExLlamaV2, CTranslate2, TensorRT Edge-LLM, MindIE, RTP-LLM, NVIDIA Nim, Triton Inference Server, Seldon Core v2, llm-d, KAITO, Kueue, NVIDIA GPU Operator, TorchServe, TensorFlow Serving, Replicate, Modal, Baseten, Deep Infra, Vast.ai, CoreWeave, Nebius, Crusoe, GMI Cloud, Bifrost, TensorZero, ExecuTorch |
| **C** | MLC-LLM |

## Key Trends

- **TGI entered maintenance mode** as of late 2025; new optimizations land in vLLM and SGLang first.
- **Ollama is not production-ready** for multi-tenant: collapses under 5 concurrent users in benchmarks.
- **Specialized AI hardware**: Groq acquired by NVIDIA ($20B), Cerebras filed for IPO ($1B+ revenue), SambaNova acquired by Intel ($1.6B).
- **Edge/on-device now production-ready**: ExecuTorch (Meta, 1.0 GA Oct 2025, 50KB footprint); MLX (Apple, 24.6K+ stars, 4,255+ HF models).
- **China-developed engines**: LMDeploy (Shanghai AI Lab), MindIE (Huawei), RTP-LLM (Alibaba) gaining global traction.

## Benchmarks

- **Standard**: LLMPerf, AnyScale serving benchmark
- **Custom**: Setup time, cold start latency, throughput under load, memory efficiency
- **Stress**: Request flood, model swap under load, KV cache eviction, GPU memory exhaustion

## See also

- Full catalog: [`../data/roster.json`](../data/roster.json)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
- Benchmark methodology: [`../methodology/benchmark-harness.md`](../methodology/benchmark-harness.md)
