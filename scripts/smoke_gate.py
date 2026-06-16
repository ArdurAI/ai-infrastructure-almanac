#!/usr/bin/env python3
"""
Smoke Gate — The entry-level qualification for every tool on the almanac roster.

A 3-turn scenario:
1. SETUP: Install/configure the tool, measure time to first result.
2. WORK: Execute the tool's primary function with a standard workload.
3. TEARDOWN: Clean up, measure resource usage, check for leftover state.

Every tool must pass all 3 turns to be officially ranked. Failures are documented,
not hidden. This is the "canary" test before any benchmark runs.

Usage:
    python smoke_gate.py --category code-editors --tool cursor
    python smoke_gate.py --category vector-databases --tool qdrant
    python smoke_gate.py --category model-serving --tool vllm --output ../benchmarks/
"""

import argparse
import json
import logging
import os
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('smoke_gate')


@dataclass
class TurnResult:
    """Result of a single turn (setup, work, or teardown)."""
    turn: str
    passed: bool
    duration_seconds: float
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


@dataclass
class SmokeReport:
    """Full report for a smoke gate run."""
    tool_name: str
    category: str
    run_id: str
    timestamp: str
    overall_passed: bool
    turns: list
    summary: str
    raw_data_path: str


class CategoryAdapter(ABC):
    """
    Base adapter contract for the smoke gate.
    Every category implements its own adapter that satisfies this interface.
    """

    @abstractmethod
    def setup(self, config: Dict[str, Any]) -> None:
        """Install, configure, and start the tool. Return when ready."""
        pass

    @abstractmethod
    def work(self, workload: Any) -> Dict[str, Any]:
        """Execute the tool's primary function with the given workload."""
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Clean up, stop processes, remove temp files."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the human-readable tool name."""
        pass

    @abstractmethod
    def get_category(self) -> str:
        """Return the category key."""
        pass


def run_turn(adapter: CategoryAdapter, turn_name: str, config: Dict[str, Any],
             workload: Any) -> TurnResult:
    """Run a single turn (setup, work, or teardown) and capture metrics."""
    start = time.perf_counter()
    metrics = {}
    error = None
    passed = False

    try:
        if turn_name == 'setup':
            adapter.setup(config)
            metrics['setup_method'] = getattr(adapter, 'setup_method', 'unknown')
        elif turn_name == 'work':
            result = adapter.work(workload)
            metrics['result_keys'] = list(result.keys()) if isinstance(result, dict) else []
            metrics['result_type'] = type(result).__name__
        elif turn_name == 'teardown':
            adapter.teardown()
        passed = True
    except Exception as e:
        error = str(e)
        logger.error(f"Turn '{turn_name}' failed for {adapter.get_name()}: {error}")
    finally:
        duration = time.perf_counter() - start

    return TurnResult(
        turn=turn_name,
        passed=passed,
        duration_seconds=round(duration, 3),
        error=error,
        metrics=metrics
    )


def run_smoke_gate(adapter: CategoryAdapter, config: Dict[str, Any],
                   workload: Any, output_dir: str) -> SmokeReport:
    """Run the full 3-turn smoke gate for a single tool."""
    run_id = f"{adapter.get_category()}-{adapter.get_name().replace(' ', '-').lower()}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    timestamp = datetime.now(timezone.utc).isoformat()

    logger.info(f"Starting smoke gate: {adapter.get_name()} ({adapter.get_category()})")
    logger.info(f"Run ID: {run_id}")

    turns = []
    for turn_name in ['setup', 'work', 'teardown']:
        logger.info(f"  Running turn: {turn_name}")
        result = run_turn(adapter, turn_name, config, workload)
        turns.append(asdict(result))
        logger.info(f"    -> {'PASS' if result.passed else 'FAIL'} in {result.duration_seconds}s")

    overall_passed = all(t['passed'] for t in turns)
    summary = (
        f"Smoke gate {'PASSED' if overall_passed else 'FAILED'} for "
        f"{adapter.get_name()}. Setup: {turns[0]['duration_seconds']}s, "
        f"Work: {turns[1]['duration_seconds']}s, "
        f"Teardown: {turns[2]['duration_seconds']}s."
    )

    report = SmokeReport(
        tool_name=adapter.get_name(),
        category=adapter.get_category(),
        run_id=run_id,
        timestamp=timestamp,
        overall_passed=overall_passed,
        turns=turns,
        summary=summary,
        raw_data_path=f"{run_id}.json"
    )

    # Save raw JSON
    os.makedirs(output_dir, exist_ok=True)
    raw_path = os.path.join(output_dir, report.raw_data_path)
    with open(raw_path, 'w') as f:
        json.dump(asdict(report), f, indent=2)
    logger.info(f"Raw data saved: {raw_path}")

    return report


def main():
    parser = argparse.ArgumentParser(description='Smoke Gate — Tool qualification harness')
    parser.add_argument('--category', required=True, help='Category key (e.g. code-editors, vector-databases)')
    parser.add_argument('--tool', required=True, help='Tool name to test')
    parser.add_argument('--output', default='../benchmarks/', help='Output directory for raw JSON')
    parser.add_argument('--config', default='{}', help='JSON config for adapter')
    parser.add_argument('--workload', default='{}', help='JSON workload for the work turn')
    parser.add_argument('--list-categories', action='store_true', help='List available categories')

    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for cat in ['code-editors', 'agent-frameworks', 'observability', 'vector-databases',
                    'model-serving', 'security-guardrails', 'llmops-platforms', 'context-protocols']:
            print(f"  - {cat}")
        return

    # Dynamic adapter loading (import from category_adapters package)
    adapter_module_name = f"category_adapters.{args.category.replace('-', '_')}_adapter"
    try:
        adapter_module = __import__(adapter_module_name, fromlist=['get_adapter'])
        adapter = adapter_module.get_adapter(args.tool)
    except ImportError as e:
        logger.error(f"Could not load adapter for category '{args.category}': {e}")
        logger.error(f"Expected module: {adapter_module_name}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Could not create adapter for tool '{args.tool}': {e}")
        sys.exit(1)

    config = json.loads(args.config)
    workload = json.loads(args.workload)

    report = run_smoke_gate(adapter, config, workload, args.output)

    print(f"\n{'='*60}")
    print(report.summary)
    print(f"{'='*60}")
    print(f"Raw JSON: {report.raw_data_path}")
    print(f"Overall: {'PASS' if report.overall_passed else 'FAIL'}")


if __name__ == '__main__':
    main()
