# Agent Frameworks & Orchestration

The market reached $13.7B in 2026, projected at $88.6B by 2035. Consolidation happened fast: from dozens of frameworks in 2024 to ~8 serious production options by mid-2026.

## The Roster

| Tier | Tools |
|------|-------|
| **A** | LangGraph, CrewAI, Mastra, Pydantic AI, Claude Agent SDK, OpenAI Agents SDK, Google ADK, Microsoft Agent Framework, Agno, LlamaIndex, LangChain, Deep Agents, AutoGen/AG2, smolagents, Haystack, Letta, DSPy, Vercel AI SDK, Salesforce Agentforce, ServiceNow Now Assist, Microsoft Copilot Studio, Google Vertex AI Agent Builder, Dify, Flowise, n8n |
| **B** | Genkit, Spring AI, LangChain4j, Embabel, Koog, AgentScope Java, Semantic Kernel, Rig, AutoAgents, OpenFANG, kagent, Coze, RAGflow, Botpress, Rasa, Voiceflow, Relevance AI, Langflow, UiPath Agentic Automation, IBM watsonx Orchestrate, Adobe AEP Agent Orchestrator, Airia, Chapter Enterprise, Domo Agent Catalyst, Harness AI Agent Framework, ArkClaw, MoltBook, QwenPaw, 文心智能体平台, 智谱 AutoClaw, Kimi Claw, AstronClaw, MaxClaw, OpenClaw, Hermes Agent Framework |
| **C** | ROSA, RAI, BUMBLE, LeRobot, TARS, MetaGPT, Instructor, Cognosys, OrchestrAI, EchoLeads, Retell AI, Bland AI, Synthflow, Vapi, SuperAGI, Kore.ai, Appsmith, JVSClaw, QoderWork, WorkBuddy, CodeBuddy, 红手指Operator |

## Key Trends

- **Language ecosystem diversification**: Python no longer has a monopoly. TypeScript (Mastra), Java (Spring AI, LangChain4j), Rust (Rig, AutoAgents, OpenFANG), Go (kagent) all have first-class production-viable frameworks.
- **MCP + A2A are the "TCP/IP of AI"**: Complementary, not competing (MCP = vertical tool access; A2A = horizontal agent coordination).
- **No-code to code-first migration arc**: Teams prototype in Dify/Flowise/n8n, then migrate to LangGraph/CrewAI/Mastra at scale.
- **China's domestic ecosystem**: 40+ tools from BATB + new players, often not interoperable with Western protocols.
- **Rust for performance tier**: Independent benchmarks claim 5x memory efficiency, 13x throughput vs. Python. Needs third-party validation.

## Benchmarks

- **Standard**: GAIA, WebArena, SWE-bench
- **Custom**: Setup time, dependency conflicts, multi-agent reliability, checkpointing durability
- **Stress**: Concurrent agent storms, kill-the-coordinator chaos, tool-call failure cascades

## See also

- Full catalog: [`../data/roster.json`](../data/roster.json)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
- Benchmark methodology: [`../methodology/benchmark-harness.md`](../methodology/benchmark-harness.md)
