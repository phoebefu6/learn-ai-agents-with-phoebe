# Official course map - learn-ai-agents-with-phoebe

Research date: 2026-07-31. All syllabi fetched live and verified. Fast-moving space: re-verify SDK/docs URLs against changelogs before delivery.

## Sources

| # | Source | URL | Depth |
|---|--------|-----|-------|
| S1 | Anthropic "Building Effective Agents" | anthropic.com/engineering/building-effective-agents | essay, Dec 19 2024 |
| S2 | Anthropic platform tool-use + agents docs | platform.claude.com/docs/en/agents-and-tools/tool-use/overview | ~20 pages |
| S3 | Claude Agent SDK docs | code.claude.com/docs/en/agent-sdk/overview | ~15 pages |
| S4 | Anthropic Academy "Building with the Claude API" (Agents and Workflows + Tool Use sections) + subagents/skills mini-courses | anthropic.skilljar.com | ~10h total |
| S5 | OpenAI "A Practical Guide to Building Agents" | cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 34pp, Apr 2025 |
| S6 | OpenAI Agents SDK docs | openai.github.io/openai-agents-python | ~20 pages |
| S7 | DeepLearning.AI "Agentic AI" (Andrew Ng) | deeplearning.ai/courses/agentic-ai | 5 modules, 9h55m |
| S8 | DLAI short courses: Evaluating AI Agents (Arize, 2h36m) · Practical Multi AI Agents (crewAI, 2h49m) · Agentic Design Patterns (AutoGen, 1h35m) · A2A Protocol (Google+IBM, 1h27m) | deeplearning.ai/short-courses | 4 courses |
| S9 | Hugging Face Agents course | huggingface.co/learn/agents-course | 5 units + 3 bonus |
| S10 | LangGraph docs + LangChain Academy "Intro to LangGraph" | docs.langchain.com/oss/python/langgraph/overview · academy.langchain.com | 6 modules, ~6h |
| S11 | Agent evals: Anthropic "Demystifying evals for AI agents" (Jan 9 2026) + LangSmith trajectory evals + agentevals package | anthropic.com/engineering/demystifying-evals-for-ai-agents · docs.langchain.com/langsmith/trajectory-evals | 2 primary pages |

## Verified key facts (build against these)

- **Workflows vs agents (S1, canonical):** workflows = "LLMs and tools orchestrated through predefined code paths"; agents = "LLMs dynamically direct their own processes and tool usage." Teach the spectrum, not a binary.
- **5 workflow patterns (S1, exact names):** prompt chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer.
- **3 agent principles (S1):** simplicity; transparency (explicit planning steps); carefully crafted agent-computer interface (ACI) - tool docs + testing.
- **4-pattern agentic canon (S7 + S8/AutoGen agree):** Reflection · Tool Use · Planning · Multi-Agent.
- **OpenAI agent definition (S5, verbatim):** "systems that independently accomplish tasks on your behalf." Explicit exclusion: chatbots/classifiers that don't control workflow execution "are not agents."
- **When to build (S5):** complex decision-making · difficult-to-maintain rules · heavy unstructured data. Otherwise deterministic code.
- **3 components (S5):** Model, Tools, Instructions. Tool types: Data / Action / Orchestration (agents-as-tools).
- **Multi-agent taxonomy (S5→S6 1:1):** Manager pattern (agents as tools, central synthesizer) vs Decentralized pattern (handoffs transfer execution + state). S6 primitives: Agents, Handoffs, Guardrails, Sessions, Tracing.
- **Single-agent-first rule (S5):** "maximize a single agent's capabilities first"; split on complex conditional logic or tool overload (overlap matters more than count).
- **7 guardrail types (S5, exact):** relevance classifier · safety classifier · PII filter · moderation · tool safeguards (risk-rate per tool: read/write, reversibility, financial impact) · rules-based (regex/blocklist/length) · output validation. Human-intervention triggers: failure thresholds + high-risk actions.
- **Claude Agent SDK (S3):** Python + TypeScript only, bundles Claude Code binary; primitives = built-in tools, hooks, subagents, MCP, permissions, sessions, skills, plugins; `query()` + `ClaudeAgentOptions`; permission modes incl. `plan`, `acceptEdits`, `bypassPermissions`. Renamed from "Claude Code SDK" late 2025.
- **Anthropic tool categories (S2):** your own tools (+ Tool Runner auto-loop, `strict: true`) · Anthropic-schema client tools (memory, bash, text editor, computer use) · server tools (web search, code execution, tool search w/ defer_loading, MCP connector). Managed Agents = hosted sandbox product.
- **Agent evals (S11):** vocabulary = task, trial, grader, transcript, outcome. Grader types: code-based / LLM-judge / human. **pass@k** (≥1 of k) vs **pass^k** (all k). Grade outcomes over process; start with 20-50 tasks from real failures. agentevals trajectory modes: strict / unordered / subset / superset; `create_trajectory_llm_as_judge`.
- **LangGraph (S10):** StateGraph nodes+edges, MessagesState, checkpointing/persistence, human-in-the-loop interrupts, subgraphs. Academy modules: intro · state+memory · HITL · assistant (parallelization, sub-graphs, map-reduce) · long-term memory (Store) · deployment. Docs moved to docs.langchain.com/oss/python/langgraph.
- **HF Agents course (S9):** Thought-Action-Observation cycle; frameworks smolagents/LlamaIndex/LangGraph; agentic RAG use case; final = GAIA benchmark subset, ≥30% for certificate.
- **Protocol split:** MCP = model↔tools/context standard; A2A = agent↔agent standard (S8/A2A: cross-framework interop ADK/LangGraph/BeeAI/MS Agent Framework).
- **Docs migrations (version-sensitive):** Anthropic docs → platform.claude.com; LangGraph docs → docs.langchain.com. Current example model `claude-opus-5`.

## Running project - Daybreak Ops Agent

Extends the learn-mcp Daybreak coffee-store MCP server (3 tools: query_sales, top_products, subscription_status; 2 resources: catalog, refund policy; 1 prompt: monthly_report) into a full ops agent. Same DB as learn-sql (the March dip carries over). New action tools added across b-track: list_tickets, send_email (draft-and-hold), refund_order (guardrail-gated).

**Verified Daybreak numbers (pages must quote exactly these):**
- Monthly completed revenue 2026: Jan $209 · Feb $271 · Mar $150 · Apr $239 · May $183 · Jun $168. H1 total $1,220.
- March dip: $271 → $150 = -$121 = **-44.6%**; completed orders 7 → 4; 1 March refund (order 1017); Liam Ford cancelled Midnight Espresso sub 2026-03-10 (price).
- Top products (completed, all-time): Midnight Espresso 17 · Sunrise Blend 16 · Single-Origin Ethiopia 15 · Oat Milk Pods 9 · Decaf Calm 9.
- Subscriptions: 8 active (12 bags/mo), 2 cancelled (Liam Ford, Sofia Rossi).

## agent-live.js - lever ladder (hard-coded rungs, quote exactly)

12-task golden set. Levers: tools / memory / planning / guardrails.

| Rung | Levers on | Score |
|------|-----------|-------|
| 0 | none | **1 / 12** |
| 1 | tools | **5 / 12** |
| 2 | tools + memory | **7 / 12** |
| 3 | tools + memory + planning | **10 / 12** |
| 4 | all four | **12 / 12** |

Trace scenarios: `lookup` (March revenue) · `dip` (March-dip diagnosis) · `winback` (approval gate) · `tickets` (prompt-injection trap). Honesty rail: model is scripted teaching sim; tool-result numbers computed real in-browser from embedded Daybreak data.

## Per-session coverage - leader track (6 x 45 min)

| Session | Covers | S1 | S2/S3 | S5 | S7 | S9 | S11 |
|---------|--------|----|----|----|----|----|----|
| a1 What an agent actually is | loop, workflows-vs-agents spectrum, OpenAI definition + exclusions, when NOT to agent | ✓ | | ✓ | ◐ | ◐ | |
| a2 Anatomy in plain English | model/tools/instructions; tools-memory-planning-guardrails as business capabilities | ◐ | ◐ | ✓ | ◐ | ◐ | |
| a3 Workflows vs agents | 5 workflow patterns as cost-reliability decisions; single-agent-first; autonomy dial | ✓ | | ✓ | ✓ | | |
| a4 Risk + governance | 7 guardrail types, injection, tool risk-rating, human-intervention triggers, audit | ◐ | ◐ | ✓ | | | ◐ |
| a5 Agents in your org | when-to-build criteria, build-vs-buy, framework landscape, team readiness, ROI | | ◐ | ✓ | ◐ | ◐ | |
| a6 Roadmap | multi-agent, A2A vs MCP, computer use, managed agents, next 12 months | | ✓ | ◐ | ◐ | | |

## Per-session coverage - builder track (10 x 45 min, Python, Claude API + Ollama path)

| Session | Covers | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 |
|---------|--------|----|----|----|----|----|----|----|----|----|----|----|
| b1 The agent loop | loop anatomy, workflows-vs-agents, T-A-O cycle, agent-live first look | ✓ | | | ◐ | ✓ | | ◐ | | ✓ | | |
| b2 Tools + first agent | tool schemas, ACI, tool runner, Daybreak MCP toolbox, minimal loop in raw Python | ✓ | ✓ | | ✓ | ◐ | | ◐ | | ◐ | | |
| b3 Workflow patterns | all 5 S1 patterns built on Daybreak | ✓ | | | ✓ | ◐ | | ◐ | ◐ | | | |
| b4 Memory + context | context mgmt, compaction, scratchpad, sessions, long-term store, RAG-as-tool | ◐ | ◐ | ◐ | ◐ | | ◐ | | | ◐ | ✓ | |
| b5 Planning + reasoning | ReAct/T-A-O, plan-then-execute, reflection pattern, decomposition | ◐ | | | | ◐ | | ✓ | ◐ | ◐ | | |
| b6 Multi-agent | manager vs handoffs, subagents, orchestrator-workers at agent level, when multi wins | ✓ | | ✓ | | ✓ | ✓ | ✓ | ✓ | | ◐ | |
| b7 Guardrails | 7 types hands-on, injection defense, approval gates, budgets/stop conditions | ◐ | ◐ | ◐ | | ✓ | ✓ | | | | ◐ | |
| b8 Agent evals | task/trial/grader, pass@k vs pass^k, trajectory modes, LLM-judge, golden set | | | | | | | ✓ | ✓ | ◐ | | ✓ |
| b9 Ship + observe | Agent SDK vs LangGraph vs crewAI/AutoGen landscape, tracing, deploy, cost, A2A | | ◐ | ✓ | | ◐ | ✓ | ◐ | ✓ | | ✓ | ◐ |
| b10 Capstone | full Daybreak Ops Agent assembled: toolbox + memory + plan + guardrails + eval scorecard | ✓ | | ◐ | | ✓ | | ✓ | | ◐ | | ✓ |

✓ = session teaches ~80% of that source's working content for the topic. ◐ = partial/contextual. Certificates/videos/assessments stay with the official providers - say so on the pages.

## Overlap analysis (scoping lever)

Shared core taught ONCE (3+ sources): agent loop + T-A-O cycle · tool calling/schemas · workflows-vs-agents spectrum · the 4-pattern canon · multi-agent manager-vs-peer · guardrails + HITL · agent evals basics. Sessions b1-b8 carry this spine.

Unique deltas: S1-only (5 named workflow patterns, ACI craft) → b2/b3. S5-only (7 guardrail types, when-to-build, tool risk-rating) → b7/a4/a5. S3-only (Agent SDK primitives, permission modes) → b9. S10-only (StateGraph, checkpointing, Store, interrupts) → b4/b9. S11-only (pass@k/pass^k, trajectory modes, agentevals) → b8. S8/A2A-only (agent interop) → b9/a6.

## Open lane (nobody teaches yet - this course's differentiation)

Prompt-injection live trap with a visible guardrail catch (tickets scenario) · lever-ladder scorecard tied to one running business DB · MCP-server-as-agent-toolbox continuity from a sibling course · pass@k vs pass^k taught with a 12-task golden set the learner can run · draft-and-hold approval gate as the default outward-action pattern.

## Not covered by design (honest list)

- Framework deep-dives (LangGraph/crewAI/AutoGen each get a positioning lesson + pointer, not a build track)
- Voice/realtime agents, computer-use agents (roadmap mentions only)
- Fine-tuning for function-calling (HF bonus unit - linked)
- GAIA leaderboard runs (pointed to HF final unit)
- A2A server implementation (protocol positioning only)
