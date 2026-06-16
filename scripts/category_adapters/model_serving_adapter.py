"""Model Serving adapter for the smoke gate.
Tests: install, inference (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'vllm': ToolInfo('vLLM', 'model-serving', 'Apache 2.0', 'Global', 'PagedAttention; 200+ models; multi-GPU (NVIDIA, AMD, Intel, TPU)', 'Inference Engine'),
    'sglang': ToolInfo('SGLang', 'model-serving', 'Apache 2.0', 'Global', 'RadixAttention; 29% throughput advantage on RAG', 'Inference Engine'),
    'tensorrt-llm': ToolInfo('TensorRT-LLM', 'model-serving', 'Apache 2.0 + closed', 'NVIDIA', 'Highest throughput; 30-60% faster than vLLM on H100', 'Inference Engine'),
    'llamacpp': ToolInfo('llama.cpp', 'model-serving', 'MIT', 'Global', 'GGUF format; Metal/CUDA/Vulkan/ROCm; ARM, Raspberry Pi', 'Inference Engine'),
    'nvidia-dynamo': ToolInfo('NVIDIA Dynamo', 'model-serving', 'Open source', 'NVIDIA', 'Disaggregated serving; KV-aware routing; 7x Blackwell boost', 'Orchestration'),
    'kserve': ToolInfo('KServe', 'model-serving', 'Apache 2.0', 'Global', 'CNCF Incubating; InferenceService CRD; scale-to-zero; canary', 'K8s Model Serving'),
    'bentoml': ToolInfo('BentoML', 'model-serving', 'Apache 2.0', 'Global', 'Python-first packaging; multi-framework', 'Model Serving'),
    'ray-serve': ToolInfo('Ray Serve', 'model-serving', 'Apache 2.0', 'Global', 'Multi-model serving graphs; online RAG', 'Distributed Serving'),
    'ollama': ToolInfo('Ollama', 'model-serving', 'MIT', 'Global', '52M monthly downloads; not for multi-tenant production', 'Local LLM Serving'),
    'lmdeploy': ToolInfo('LMDeploy', 'model-serving', 'Apache 2.0', 'China', 'TurboMind C++/CUDA; 1.5x vLLM on AWQ/MXFP4', 'Inference Engine'),
    'fireworks-ai': ToolInfo('Fireworks AI', 'model-serving', 'Proprietary', 'US', 'FireAttention sub-100ms TTFT', 'Managed API'),
    'together-ai': ToolInfo('Together AI', 'model-serving', 'Proprietary', 'US', 'Broad model catalog; fine-tuned deployment', 'Managed API'),
    'runpod': ToolInfo('RunPod', 'model-serving', 'Proprietary', 'Global', 'Pods + Serverless + Community Cloud; 30+ regions', 'GPU Cloud'),
    'lambda-labs': ToolInfo('Lambda Labs', 'model-serving', 'Proprietary', 'US', '99.9% SLA; 1-Click Clusters (16-2,000 GPUs)', 'GPU Cloud'),
    'litellm': ToolInfo('LiteLLM', 'model-serving', 'MIT', 'Global', '100+ providers; OpenAI-compatible proxy; 18K+ stars', 'LLM Gateway'),
    'portkey': ToolInfo('Portkey', 'model-serving', 'Partially open', 'Global', '250+ models; 20-40ms latency; MCP Gateway', 'AI Gateway'),
}


class ModelServingAdapter(BaseAdapter):
    """Adapter for model serving tools."""

    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')

        if self.tool_info.license in ['MIT', 'Apache 2.0']:
            self.setup_method = 'docker_or_package_manager'
        else:
            self.setup_method = 'cloud_api_signup'

        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

        # Write a test prompt file
        prompt_file = os.path.join(self.temp_dir, 'prompt.txt')
        self._write_file(prompt_file, 'What is the capital of France?\n')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')

        prompt_file = os.path.join(self.temp_dir, 'prompt.txt')
        prompt = self._read_file(prompt_file)

        # Simulate inference
        return {
            'prompt_length': len(prompt),
            'response': 'Paris',
            'tokens_generated': 1,
            'ttft_ms': 25,  # time to first token
            'tps': 85,       # tokens per second
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> ModelServingAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown model serving tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return ModelServingAdapter(TOOLS[key])
