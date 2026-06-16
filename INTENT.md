# Project Intent & Philosophy

## Why this almanac exists

The AI infrastructure landscape is exploding. Every week, a new "must-have" tool launches, a blog post claims 10x performance gains, and a vendor announces the next revolution. But **nobody independently verifies these claims**. The benchmarks are self-reported, the comparisons are marketing, and the "best tool" lists are affiliate SEO.

This almanac is the **public record of independent verification**. It exists because platform engineers need a single source of truth that answers:

- Does this tool actually work in production?
- What's the real ops burden of running it?
- How does it fail under stress?
- What's the total cost of ownership?
- Can I trust the vendor's benchmark numbers?

## Core principles

### 1. Frozen methodology before results

The harness, judge model, prompts, and scoring rubric are **fixed and published before any tool is tested**. This prevents "cherry-picking" the methodology that favors a particular vendor. If a tool doesn't fit the harness, we adapt the adapter — not the rules.

### 2. Ops-first evaluation

Most benchmarks measure accuracy or throughput. We measure **what a platform engineer actually lives with**:
- Time from `git clone` to first working result
- Dependency conflicts when installing alongside other tools
- Time to debug when the tool silently fails
- Upgrade pain when version N → N+1 breaks everything
- Cost predictability at scale

### 3. Raw data is always published

Every benchmark run produces a JSON file with every question, every answer, every token count, every latency measurement. These raw files are published alongside the summary. If you disagree with a ranking, you can re-analyze the data yourself.

### 4. No tool is above criticism

Every tool on the roster has been through a smoke gate. Every tool has bugs. We document them honestly. A vendor relationship or sponsorship does not influence rankings. The only way a tool improves its score is by actually improving.

### 5. Living document, not a static snapshot

The almanac is updated monthly. Tools enter and exit the roster. Scores change as tools improve or degrade. The "founding edition" is a snapshot; the current edition is the truth.

## Design philosophy

### The two-bar test

Every tool must clear two bars to justify its existence:
1. **Beat the naive baseline** on accuracy/quality/performance
2. **Beat the full-capability baseline** on cost/ops burden/complexity

If a tool can't do both, it has no reason to exist as infrastructure. A tool that is 5% more accurate but 10x more complex than a naive approach is not worth adopting.

### The seven dimensions

We score every tool on seven dimensions because no single number captures "good infrastructure":

| Dimension | Why it matters |
|-----------|---------------|
| **Accuracy** | Does it produce correct outputs? |
| **Latency** | Does it respond fast enough for real use? |
| **Token economics** | Does it cost what you expect? |
| **Scale behavior** | What happens when you 10x the load? |
| **Ops burden** | How much of your life does it consume? |
| **Developer experience** | Is it pleasant or painful to use? |
| **Data sovereignty** | Can you run it yourself? Audit it? |

### The adapter pattern

Every tool is tested through a **CategoryAdapter** — a frozen interface that the tool must satisfy. The adapter handles setup, ingestion, querying, and teardown. This means:
- Tools are tested identically
- The adapter is the only thing that changes per tool
- New tools can be added without changing the harness
- The adapter is published and open for review

### The canary

Every benchmark batch starts with a **no-tool baseline** (the "canary"). If the benchmark leaked answers anywhere, the canary would score above zero. The canary must score exactly zero — this is a hard invariant. If it doesn't, the entire batch is invalid.

## Who this is for

- **Platform engineers** evaluating which tool to adopt
- **CTOs/CIOs** making build-vs-buy decisions with actual data
- **Open-source maintainers** who want independent benchmarking of their project
- **Researchers** studying the AI infrastructure landscape
- **Vendors** who want to improve their tools based on real evidence

## What this is NOT

- Not a marketing site for any vendor
- Not a "best of" list based on GitHub stars or funding rounds
- Not a tutorial on how to use any tool
- Not a replacement for your own due diligence
- Not a static document that never changes

## The "Quest"

The "Platform Engineer's Quest for the Best" is the ongoing effort to test, measure, and rank every tool on the roster. It's not a one-time effort. It's a continuous process of:
1. **Discovery** — finding new tools via research, community, and submissions
2. **Triage** — deciding if a tool is serious enough to enter the roster
3. **Smoke gate** — running every tool through an identical 3-turn scenario to catch bugs
4. **Benchmark** — running standard + custom + stress tests
5. **Publication** — publishing raw data + summary + per-tool deep-dives
6. **Iteration** — re-testing as tools update, as methodology improves, as new benchmarks emerge

## How to challenge a result

If you believe a ranking or score is wrong:
1. Check the **raw results JSON** — the data is public
2. Check the **adapter implementation** — the adapter code is public
3. Check the **judge prompts** — the prompts are frozen and public
4. File an issue with a specific claim and evidence
5. We'll re-run the test or update the methodology if warranted

## Governance

- **ArdurAI** maintains the almanac and runs the Quest
- **Methodology changes** require a public RFC and at least one edition cycle of notice
- **Tool additions/removals** are decided by the triage criteria (stars, last push, community activity, seriousness)
- **Benchmark results** are machine-generated; summaries are human-reviewed for fairness
- **Conflicts of interest** are disclosed (e.g., ArdurAI contributes to some tools on the roster); mitigation is identical harness for all

## License

Content: CC BY 4.0  
Harness code: MIT  
Raw data: CC BY 4.0
