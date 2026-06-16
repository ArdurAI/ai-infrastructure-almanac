# Code Editors — Testing Methodology

How we test and score AI code editors and terminal agents in the almanac.

## Scope

This category covers AI-native IDEs, IDE assistants, terminal coding agents, and autonomous code-review tools. We test the **code generation quality** and **developer experience**, not the underlying LLM.

## Adapter pattern

```python
class CodeEditorAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Install the editor/agent, configure API keys, create workspace
        pass
    
    def load(self, codebase) -> None:
        # Load a reference codebase into the editor
        pass
    
    def query(self, task) -> Response:
        # Send a coding task, return the generated/modified code
        pass
    
    def teardown(self) -> None:
        # Uninstall, clean temp files, remove API keys
        pass
```

## Standard benchmarks

### 1. HumanEval (OpenAI)
- **What**: 164 programming problems with test cases
- **Why**: Widely cited baseline for code generation
- **How**: Pass the prompt to the editor, run the generated code against tests
- **Metric**: `pass@k` (percentage of problems solved)

### 2. SWE-bench (Princeton)
- **What**: Real GitHub issues from popular Python repos
- **Why**: Tests end-to-end bug fixing, not just isolated functions
- **How**: Editor must check out repo, understand issue, write fix, pass tests
- **Metric**: Resolution rate (passing tests / total issues)

### 3. Exercism (Aider benchmark)
- **What**: 225 programming exercises across multiple languages
- **Why**: Tests language breadth and idiomatic code quality
- **Metric**: Pass rate by language

## Custom PlatformOps benchmarks

### Code generation quality
- **Tasks**: Implement a function, refactor a class, add error handling, write tests
- **Workloads**: 50 tasks spanning Python, TypeScript, Go, Rust, Java
- **Evaluation**: Human + LLM-as-a-judge scoring on correctness, idiomaticness, documentation

### Context window stress
- **Tasks**: Work with 100K, 500K, 1M token codebases
- **Metric**: Accuracy degradation curve as context grows
- **Edge cases**: Cross-file references, dependency chains, legacy code patterns

### Multi-agent coordination
- **Tasks**: 5-agent team implementing a feature (spec → design → code → tests → review)
- **Metric**: End-to-end completion rate, merge conflicts, consistency

### Security scan
- **Tasks**: Generate code that handles user input, auth, SQL queries, file paths
- **Metric**: OWASP Top 10 vulnerability detection rate (via static analysis)

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 30% | HumanEval + SWE-bench + custom task pass rate |
| **Latency** | 15% | Time from prompt to usable code (TTFC) |
| **Token economics** | 10% | Cost per task, tokens consumed per solution |
| **Scale behavior** | 10% | Performance with 100K+ token context windows |
| **Ops burden** | 15% | Setup time, dependency conflicts, upgrade pain |
| **Developer experience** | 15% | Subjective ergonomics (editors rate via survey) |
| **Data sovereignty** | 5% | Self-hostability, on-premise option, audit trail |

## Stress suites

### Contradiction storm
- Feed the editor conflicting requirements in the same session
- Measure: Does it detect the contradiction? Which requirement does it prioritize?

### Near-duplicate flood
- 100 tasks that are 95% identical but with subtle differences
- Measure: Does it handle the differences correctly, or copy-paste the same solution?

### Temporal paradox
- Ask it to modify code it generated earlier, then revert, then modify again
- Measure: Consistency across the edit chain

### Concurrent writers
- Two agents editing the same file simultaneously
- Measure: Merge conflict resolution, data integrity

### Kill-the-backing-store
- Simulate network loss, API key revocation, disk full
- Measure: Graceful degradation, data recovery, error messages

## Known pitfalls

1. **Benchmark leakage**: HumanEval is in training data for many models. We use a held-out test set.
2. **Tool bias**: Some editors are optimized for specific languages. We test multi-language.
3. **Temperature effects**: Low temperature = more deterministic but less creative. We fix temperature.
4. **Context window inflation**: "1M context" claims often don't mean 1M tokens of *useful* context.

## Canaries

- **No-tool baseline**: Run the same task with no editor (raw LLM API). Score should be lower than any editor.
- **Naive baseline**: Run with a simple autocomplete extension. Every editor must beat this.
- **Full-capability baseline**: Run with the most expensive, most capable setup. Editors should beat this on cost/ops.

## Raw data format

```json
{
  "tool": "Cursor",
  "benchmark": "human-eval",
  "date": "2026-06-16",
  "tasks": [
    {"id": 1, "passed": true, "tokens": 450, "latency_ms": 1200},
    {"id": 2, "passed": false, "tokens": 890, "latency_ms": 3400, "error": "syntax"}
  ],
  "score": 0.72,
  "metadata": {"model": "claude-sonnet-4", "temperature": 0.2}
}
```

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
