"""Base adapter with common utilities for all category adapters."""

import os
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ToolInfo:
    """Static metadata about a tool from the roster."""
    name: str
    category: str
    license: str
    region: str
    notes: str
    type: str


class BaseAdapter:
    """Non-ABC base with shared helper methods for concrete adapters."""

    def __init__(self, tool_info: ToolInfo):
        self.tool_info = tool_info
        self._start_time = None

    def get_name(self) -> str:
        return self.tool_info.name

    def get_category(self) -> str:
        return self.tool_info.category

    def _timed_shell(self, cmd: list, cwd: Optional[str] = None, timeout: int = 300) -> Dict[str, Any]:
        """Run a shell command with timing. Returns dict with stdout, stderr, returncode, duration."""
        start = time.perf_counter()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout
            )
            duration = time.perf_counter() - start
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'duration': round(duration, 3),
                'command': ' '.join(cmd)
            }
        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - start
            return {
                'stdout': '',
                'stderr': 'TIMEOUT',
                'returncode': -1,
                'duration': round(duration, 3),
                'command': ' '.join(cmd)
            }
        except Exception as e:
            duration = time.perf_counter() - start
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'duration': round(duration, 3),
                'command': ' '.join(cmd)
            }

    def _check_command(self, cmd: str) -> bool:
        """Check if a command exists in PATH."""
        return subprocess.run(['which', cmd], capture_output=True).returncode == 0

    def _read_file(self, path: str) -> str:
        """Read a file, return empty string on failure."""
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception:
            return ''

    def _write_file(self, path: str, content: str) -> None:
        """Write a file, creating directories if needed."""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
