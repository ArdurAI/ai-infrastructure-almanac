"""Code Editor adapter for the smoke gate.
Tests: install, basic code generation/completion, cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

# Roster data for Tier A code editors
TOOLS = {
    'cursor': ToolInfo('Cursor', 'code-editors', 'Proprietary', 'US', 'VS Code fork; $20–$200/mo; acquired Supermaven', 'AI-native IDE'),
    'github-copilot': ToolInfo('GitHub Copilot', 'code-editors', 'Proprietary', 'US', 'Moved to usage-based credits June 2026', 'IDE assistant'),
    'claude-code': ToolInfo('Claude Code', 'code-editors', 'Proprietary', 'US', '1M context; Agent Teams; SWE-bench 82%', 'CLI agent'),
    'opencode': ToolInfo('OpenCode', 'code-editors', 'MIT', 'Global', '75+ LLM providers; Go-based; GitHub Actions', 'Terminal TUI'),
    'cline': ToolInfo('Cline', 'code-editors', 'Apache 2.0', 'Global', 'Native subagents; BYOK; browser automation', 'VS Code + CLI'),
    'aider': ToolInfo('Aider', 'code-editors', 'MIT', 'Global', 'Git-aware diffs; model-agnostic; 225 Exercism benchmark', 'Terminal pair-programmer'),
    'continue': ToolInfo('Continue', 'code-editors', 'Apache 2.0', 'Global', 'BYOK; code review; CI-enforceable checks', 'IDE extension'),
    'zed': ToolInfo('Zed', 'code-editors', 'Open source', 'Global', 'Multi-provider chat; real-time collab; GPU-accelerated', 'Rust-native editor'),
    'trae': ToolInfo('Trae', 'code-editors', 'Proprietary', 'China', 'Free; VS Code fork; 95% WeChat SDK accuracy', 'AI IDE'),
    'tabnine': ToolInfo('Tabnine', 'code-editors', 'Proprietary', 'Israel/US', 'On-prem; zero data retention; SOC 2/GDPR', 'Completion + chat'),
    'codex-cli': ToolInfo('Codex CLI', 'code-editors', 'Proprietary', 'US', 'OpenAI terminal agent; sandboxed execution', 'CLI agent'),
    'gemini-cli': ToolInfo('Gemini CLI', 'code-editors', 'Proprietary', 'US', 'Google terminal agent; multi-modal', 'CLI agent'),
    'kimi-cli': ToolInfo('Kimi CLI', 'code-editors', 'Proprietary', 'China', '300 sub-agents; multi-modal reasoning', 'CLI agent'),
    'devin': ToolInfo('Devin', 'code-editors', 'Proprietary', 'US', 'Autonomous software engineer; SWE-bench 82.9%', 'Autonomous agent'),
    'openhands': ToolInfo('OpenHands', 'code-editors', 'MIT', 'Global', 'Open-source Devin alternative; Docker-based', 'Autonomous agent'),
    'coderabbit': ToolInfo('CodeRabbit', 'code-editors', 'Proprietary', 'Global', 'AI code reviewer; PR analysis; 15+ languages', 'Code reviewer'),
}


class CodeEditorAdapter(BaseAdapter):
    """Adapter for code editor tools."""

    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        """Simulate installation/setup of the code editor."""
        name = self.tool_info.name.lower().replace(' ', '-')

        # Simulate setup based on tool type
        if self.tool_info.license in ['MIT', 'Apache 2.0']:
            self.setup_method = 'git_clone_or_package_manager'
        elif self.tool_info.license == 'Proprietary':
            self.setup_method = 'installer_or_web_signup'
        else:
            self.setup_method = 'manual_install'

        # Create a temp workspace for testing
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

        # Write a test file
        test_file = os.path.join(self.temp_dir, 'test.py')
        self._write_file(test_file, 'def hello_world():\n    return "Hello, World!"\n')

    def work(self, workload: Any) -> Dict[str, Any]:
        """Simulate the primary work: code generation/completion."""
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')

        # Simulate a code completion task
        test_file = os.path.join(self.temp_dir, 'test.py')
        content = self._read_file(test_file)

        # Simulate "AI completion"
        completion = content + '\n# AI-generated completion\nprint(hello_world())\n'
        self._write_file(test_file, completion)

        return {
            'input_length': len(content),
            'output_length': len(completion),
            'file_modified': test_file,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        """Clean up temp directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> CodeEditorAdapter:
    """Factory: return adapter for named tool."""
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown code editor tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return CodeEditorAdapter(TOOLS[key])
