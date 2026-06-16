"""Security & Guardrails adapter for the smoke gate.
Tests: install, policy validation (simulated), cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'guardrails-ai': ToolInfo('Guardrails AI', 'security-guardrails', 'Apache 2.0', 'Global', '70+ Hub validators; Python-centric', 'Guardrail Framework'),
    'nvidia-nemo-guardrails': ToolInfo('NVIDIA NeMo Guardrails', 'security-guardrails', 'Apache 2.0', 'US', 'Dialog/input/output/retrieval rails; Colang DSL; sub-100ms', 'Guardrail Framework'),
    'lakera-guard': ToolInfo('Lakera Guard (Check Point)', 'security-guardrails', 'Proprietary', 'Global', 'Gandalf dataset; sub-50ms; acquired by Check Point', 'Runtime Firewall'),
    'arthur-ai-shield': ToolInfo('Arthur AI Shield', 'security-guardrails', 'Proprietary', 'US', 'Prompt injection, hallucination scoring; SOC 2', 'LLM Firewall'),
    'fiddler-ai': ToolInfo('Fiddler AI', 'security-guardrails', 'Proprietary', 'US', 'Trust Models run in customer env; <100ms', 'Observability + Guardrails'),
    'protect-ai': ToolInfo('Protect AI (Palo Alto)', 'security-guardrails', 'Proprietary', 'US', 'Model scanning, red teaming, firewall; NB Defense', 'Full Lifecycle Security'),
    'hiddenlayer': ToolInfo('HiddenLayer', 'security-guardrails', 'Proprietary', 'US', 'MITRE ATLAS aligned; model theft detection', 'AI Security Posture'),
    'witnessai': ToolInfo('WitnessAI', 'security-guardrails', 'Proprietary', 'US', 'Behavioral intent analysis, policy routing', 'Network-level Governance'),
    'credo-ai': ToolInfo('Credo AI', 'security-guardrails', 'Proprietary', 'US', 'AI inventory, risk assessments, policy packs; EU AI Act', 'AI Governance Platform'),
    'confident-ai': ToolInfo('Confident AI (DeepTeam)', 'security-guardrails', 'Apache 2.0 (OSS)', 'Global', '50+ vulnerabilities, OWASP/NIST mapping; pytest', 'Red Teaming + Eval'),
}


class SecurityGuardrailsAdapter(BaseAdapter):
    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')
        if self.tool_info.license in ['MIT', 'Apache 2.0']:
            self.setup_method = 'pip_install'
        else:
            self.setup_method = 'api_key_or_cloud'
        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')
        return {
            'prompts_checked': 50,
            'violations_detected': 3,
            'latency_ms': 18,
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> SecurityGuardrailsAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown security tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return SecurityGuardrailsAdapter(TOOLS[key])
