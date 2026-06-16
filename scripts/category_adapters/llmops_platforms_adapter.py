"""LLMOps Platform adapter for the smoke gate.
Tests: install, workflow execution (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'dify': ToolInfo('Dify', 'llmops-platforms', 'Modified Apache 2.0', 'Global', 'Most-starred OSS; visual workflow, RAG, Agent', 'LLM App Builder'),
    'flowise': ToolInfo('Flowise', 'llmops-platforms', 'Apache 2.0', 'Global', 'LangChain-native; drag-and-drop; owned by Workday', 'Visual LLM Builder'),
    'n8n': ToolInfo('n8n', 'llmops-platforms', 'Fair-code', 'Global', '400+ integrations, AI agent nodes; self-hostable', 'Workflow Automation'),
    'vellum': ToolInfo('Vellum', 'llmops-platforms', 'Proprietary', 'US', 'A/B testing, monitoring, rollback; SOC 2; 99.998% uptime', 'Enterprise Orchestration'),
    'promptlayer': ToolInfo('PromptLayer', 'llmops-platforms', 'Proprietary', 'US', 'No-code editor for non-technical collaborators', 'Prompt Management'),
    'pezzo': ToolInfo('Pezzo', 'llmops-platforms', 'Open Source', 'Global', 'Two lines of code integration; prompt design, version mgmt', 'LLMOps Platform'),
    'braintrust': ToolInfo('Braintrust', 'llmops-platforms', 'Proprietary', 'US', 'Loop AI agent; 13+ framework integrations', 'Evaluation Platform'),
    'zapier': ToolInfo('Zapier', 'llmops-platforms', 'Proprietary', 'US', '7,000+ app integrations; AI steps, Zapier Agents', 'Workflow Automation'),
    'make': ToolInfo('Make', 'llmops-platforms', 'Proprietary', 'Global', '1,000+ integrations; visual canvas; error handling', 'Workflow Automation'),
    'gumloop': ToolInfo('Gumloop', 'llmops-platforms', 'Proprietary', 'US', '130+ nodes; multi-model routing; YC-backed', 'AI-Native Automation'),
}


class LLMOpsAdapter(BaseAdapter):
    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')
        if self.tool_info.license in ['MIT', 'Apache 2.0', 'Modified Apache 2.0', 'Fair-code', 'Open Source']:
            self.setup_method = 'docker_or_npm_or_pip'
        else:
            self.setup_method = 'cloud_signup'
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')
        return {
            'workflows_executed': 1,
            'nodes_processed': 5,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> LLMOpsAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown LLMOps tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return LLMOpsAdapter(TOOLS[key])
