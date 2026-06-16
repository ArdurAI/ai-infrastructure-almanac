# Agent Frameworks — Testing Methodology

How we test and score multi-agent orchestration frameworks in the almanac.

## Scope

This category covers frameworks for building, orchestrating, and deploying AI agents — from single-agent tools to multi-agent crews with stateful workflows.

## Adapter pattern

```python
class AgentFrameworkAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Install framework, configure LLM provider, set up persistence
        pass
    
    def load(self, agents) -> None:
        # Define agent roles, tools, and workflow graph
        pass
    
    def query(self, task) -> Response:
        # Execute the multi-agent workflow, return final output
        pass
    
    def teardown(self) -> None:
        # Stop agents, clear state, remove temp data
        pass
```

## Standard benchmarks

### 1. GAIA (General AI Assistants)
- **What**: 466 real-world tasks requiring reasoning, multi-modal understanding, web browsing, tool use
- **Why**: Tests end-to-end agent capability, not just LLM reasoning
- **Metric**: Success rate by difficulty level (Level 1-3)

### 2. WebArena
- **What**: 812 web-based tasks across 5 domains (shopping, GitHub, maps, etc.)
- **Why**: Tests real-world web interaction capability
- **Metric**: Task completion rate

### 3. OSWorld
- **What**: 369 tasks on real Ubuntu VMs requiring GUI interaction
- **Why**: Tests computer-use agents (clicking, typing, file manipulation)
- **Metric**: Success rate

## Custom PlatformOps benchmarks

### Workflow reliability
- **Tasks**: 50 workflows spanning 3-10 agent steps each
- **Metrics**: Completion rate, step-failure rate, retry success rate
- **Edge cases**: Tool timeout, LLM rate limit, state corruption

### State persistence
- **Tasks**: Long-running workflows (1 hour, 24 hours, 7 days)
- **Metrics**: State recovery after restart, checkpoint accuracy, resume correctness

### Tool integration
- **Tasks**: Workflows using 5, 10, 20 external tools (APIs, databases, browsers)
- **Metrics**: Tool call accuracy, error handling, fallback behavior

### Human-in-the-loop (HITL)
- **Tasks**: Workflows requiring human approval at critical steps
- **Metrics**: Approval latency, resume-after-approval correctness, UX friction

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 25% | GAIA + WebArena + OSWorld success rate |
| **Latency** | 15% | End-to-end workflow time (from trigger to completion) |
| **Token economics** | 10% | Total tokens consumed per task, including retries |
| **Scale behavior** | 15% | Performance with 10, 50, 100 concurrent agents |
| **Ops burden** | 15% | Setup time, debugging difficulty, state inspection tools |
| **Developer experience** | 15% | API ergonomics, documentation, community support |
| **Data sovereignty** | 5% | Self-hosted state storage, local LLM support, audit logs |

## Stress suites

### Contradiction storm
- Two agents receive contradictory instructions from the same orchestrator
- Measure: Does the system detect and resolve the conflict?

### Near-duplicate flood
- 100 near-identical tasks submitted simultaneously
- Measure: Does deduplication work? Are resources shared correctly?

### Temporal paradox
- Workflow A depends on Workflow B's result, but B hasn't started yet
- Measure: Dependency resolution, deadlock detection

### Concurrent writers
- 10 agents writing to the same database table
- Measure: Transaction integrity, conflict resolution, data consistency

### Kill-the-backing-store
- Kill the state database mid-workflow
- Measure: Graceful degradation, partial result recovery, error messages

## Known pitfalls

1. **Non-determinism**: Agent behavior varies significantly between runs. We run each task 3x and take the best result.
2. **Tool bias**: Frameworks with built-in tool integrations score higher. We test with a standardized tool set.
3. **LLM coupling**: Some frameworks are tightly coupled to specific LLM providers. We test with multiple providers where possible.
4. **State bloat**: Stateful workflows can accumulate massive state over time. We measure state size growth.

## Canaries

- **No-tool baseline**: Single LLM call with no framework. Must score lower than any framework.
- **Naive baseline**: Simple Python script with `requests` calls. Must be beaten on complexity/ops.
- **Full-capability baseline**: Maximum-framework setup with all features enabled. Must be beaten on cost.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
