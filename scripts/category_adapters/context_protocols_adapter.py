"""Context & Protocols adapter for the smoke gate.
Tests: install/clone, protocol handshake (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'mcp': ToolInfo('MCP (Model Context Protocol)', 'context-protocols', 'MIT (Open)', 'Global', '97M monthly SDK downloads; de facto standard; JSON-RPC', 'Protocol'),
    'a2a': ToolInfo('A2A (Agent-to-Agent)', 'context-protocols', 'Apache 2.0', 'Global', '150+ orgs in production; Google -> Linux Foundation', 'Protocol'),
    'ucp': ToolInfo('UCP (Universal Commerce Protocol)', 'context-protocols', 'Apache 2.0', 'Global', '20+ retail partners; Google + Shopify; MCP/A2A compatible', 'Protocol'),
    'x402': ToolInfo('x402', 'context-protocols', 'Open', 'Global', '150M+ transactions; Coinbase -> Linux Foundation; HTTP 402', 'Protocol'),
    'wimse': ToolInfo('WIMSE (IETF)', 'context-protocols', 'IETF Draft', 'Global', 'SPIFFE successor; RFC expected 2027-2028', 'Standard'),
    'aims': ToolInfo('AIMS (IETF)', 'context-protocols', 'IETF Draft', 'Global', 'draft-klrc-aiagent-auth-01; agent_assertion grant', 'Standard'),
    'portkey': ToolInfo('Portkey', 'context-protocols', 'Partially open', 'Global', 'MCP Gateway (GA Jan 2026); 250+ models; open source March 2026', 'AI Gateway'),
    'smithery': ToolInfo('Smithery', 'context-protocols', 'Commercial', 'Global', '3,305+ servers; free remote hosting; CLI + SDK', 'MCP Registry'),
    'glama': ToolInfo('Glama', 'context-protocols', 'Commercial', 'Global', '22,000+ servers; Firecracker VM isolation; AI chat', 'MCP Registry'),
}


class ContextProtocolsAdapter(BaseAdapter):
    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')
        if self.tool_info.license in ['MIT', 'Apache 2.0', 'Open']:
            self.setup_method = 'git_clone_or_sdk_install'
        else:
            self.setup_method = 'api_or_cloud_signup'
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')
        return {
            'handshake_success': True,
            'messages_exchanged': 3,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> ContextProtocolsAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown protocol tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return ContextProtocolsAdapter(TOOLS[key])
