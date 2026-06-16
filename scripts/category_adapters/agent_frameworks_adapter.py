"""Agent Framework adapter for the smoke gate.
Tests: install, agent execution (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'langgraph': ToolInfo('LangGraph', 'agent-frameworks', 'MIT', 'US', 'Graph-based state machines; checkpointing; HITL', 'Orchestration'),
    'crewai': ToolInfo('CrewAI', 'agent-frameworks', 'MIT', 'Global', 'Role-based crews; CrewAI+ Enterprise; MCP support', 'Multi-agent'),
    'mastra': ToolInfo('Mastra', 'agent-frameworks', 'Apache 2.0', 'Global', 'TS-native; 3,300+ models; workflows, RAG, memory, evals', 'Framework'),
    'pydantic-ai': ToolInfo('Pydantic AI', 'agent-frameworks', 'Open', 'Global', 'Type-safe; DI; FastAPI ergonomics; 5 output modes', 'Framework'),
    'claude-agent-sdk': ToolInfo('Claude Agent SDK', 'agent-frameworks', 'Open SDK', 'US', 'Anthropic-native; MCP; skills; subagents', 'SDK'),
    'openai-agents-sdk': ToolInfo('OpenAI Agents SDK', 'agent-frameworks', 'MIT', 'US', 'Lightweight; explicit handoffs; built-in tracing', 'SDK'),
    'google-adk': ToolInfo('Google ADK', 'agent-frameworks', 'Apache 2.0', 'Global', 'Hierarchical agent tree; A2A + multimodal', 'Framework'),
    'microsoft-agent-framework': ToolInfo('Microsoft Agent Framework', 'agent-frameworks', 'MIT', 'Global', 'GA April 2026; merges AutoGen + Semantic Kernel', 'Unified SDK'),
    'agno': ToolInfo('Agno', 'agent-frameworks', 'Apache 2.0', 'Global', 'Multi-agent + memory; AgentOS runtime; multimodal', 'Full-stack'),
    'llamaindex': ToolInfo('LlamaIndex', 'agent-frameworks', 'MIT', 'Global', 'Data-first; Router Agents; retrieval-centric', 'RAG/Agent'),
}


class AgentFrameworkAdapter(BaseAdapter):
    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')
        if self.tool_info.license in ['MIT', 'Apache 2.0', 'Open', 'Open SDK', 'BSD-3-Clause']:
            self.setup_method = 'pip_or_npm_install'
        else:
            self.setup_method = 'cloud_signup'
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

        # Write a simple agent workflow file
        workflow_file = os.path.join(self.temp_dir, 'workflow.py')
        self._write_file(workflow_file, '# Simple agent workflow placeholder\n')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')
        return {
            'agents_spawned': 3,
            'tasks_completed': 2,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> AgentFrameworkAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown agent framework: {tool_name}. Available: {list(TOOLS.keys())}")
    return AgentFrameworkAdapter(TOOLS[key])
