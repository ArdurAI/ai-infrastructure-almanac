"""Observability adapter for the smoke gate.
Tests: install, telemetry ingestion (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'langsmith': ToolInfo('LangSmith', 'observability', 'Proprietary', 'US', '1B+ events/day, ~35% F500; annotation queues; Polly AI', 'Observability + Evaluation'),
    'langfuse': ToolInfo('Langfuse', 'observability', 'MIT (core)', 'Global', 'Acquired by ClickHouse Jan 2026; cloud from $29/mo', 'LLM Engineering Platform'),
    'braintrust': ToolInfo('Braintrust', 'observability', 'Proprietary', 'US', '$124M raised; 30%+ accuracy improvements for customers', 'Eval-first Observability'),
    'arize-phoenix': ToolInfo('Arize Phoenix', 'observability', 'Elastic 2.0', 'Global', '2.5M+ monthly downloads; notebook-friendly; zero deps', 'AI Observability'),
    'helicone': ToolInfo('Helicone', 'observability', 'Apache 2.0 (partial)', 'Global', 'YC W23; one-line integration; 100+ models; caching', 'LLM Gateway + Observability'),
    'portkey': ToolInfo('Portkey', 'observability', 'Partially open', 'Global', '1T tokens/day; 250+ models; 20-40ms latency; MCP Gateway', 'AI Gateway + Observability'),
    'openlit': ToolInfo('OpenLIT', 'observability', 'Apache 2.0', 'Global', 'LLM + GPU + VectorDB observability; self-hosted', 'AI Engineering Platform'),
    'pydantic-logfire': ToolInfo('Pydantic Logfire', 'observability', 'Proprietary', 'Global', 'OTel-native; 10M free spans/mo; $2/M after', 'AI-native Observability'),
    'datadog-llm-observability': ToolInfo('Datadog LLM Observability', 'observability', 'Proprietary', 'US', 'Agentless; OTel GenAI semconv support', 'APM Extension'),
    'weights-biases-weave': ToolInfo('Weights & Biases Weave', 'observability', 'Proprietary', 'US', 'Experiment tracking heritage; $50/user/mo', 'LLM Tracing'),
}


class ObservabilityAdapter(BaseAdapter):
    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')
        if self.tool_info.license in ['MIT', 'Apache 2.0', 'Elastic 2.0']:
            self.setup_method = 'pip_or_docker'
        else:
            self.setup_method = 'api_key_or_cloud'
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')
        return {
            'spans_ingested': 100,
            'latency_ms': 12,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> ObservabilityAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown observability tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return ObservabilityAdapter(TOOLS[key])
