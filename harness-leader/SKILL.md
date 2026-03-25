---
name: harness-leader
description: Orchestrate sub-agents as a Leader/Harness using the Effective Harnesses pattern and Claude Agent Teams architecture. Use when spawning sub-agents for parallel tasks, decomposing work into agent assignments, reviewing sub-agent deliverables, managing task dependencies, selecting models by task difficulty, or implementing multi-agent collaboration. Triggers on phrases like "spawn sub-agent", "delegate task", "review code", "task decomposition", "parallel execution", "harness review", "dispatch agent", "multi-agent collaboration", "agent teams".
---

# Harness Leader

Lead and orchestrate sub-agents using the Effective Harnesses for Long-Running Agents pattern and Claude Agent Teams architecture.

## Core Principles

1. **You are the Harness/Leader** — the user only talks to you. Never ask the user to choose between options; deliver complete plans.
2. **Feature list + Progress tracking** — every task needs `feature_list.json` (what to do) + `progress.txt` (what's done).
3. **Verify before reporting** — after sub-agent delivery: `git diff` → API test → restart → confirm data correct. Never forward results blindly.
4. **Git commit per task** — sub-agent work must be committed before you report completion.
5. **Real-time monitoring** — provide real-time visibility into sub-agent status and task progress.
6. **Multi-agent collaboration** — enable direct communication between sub-agents for efficient problem solving.

## Task Lifecycle (Enhanced)

```
User Request
  → SC decomposes into tasks with dependencies
  → Spawn sub-agents (parallel or serial) with clear roles
  → Sub-agents execute with real-time status monitoring
  → Enable sub-agent communication for collaboration
  → SC reviews deliverables (git diff + verify)
  → Report to user with detailed metrics (time, tokens, cost)
  → Update progress tracking and visualization
```

## Spawning Sub-Agents

Use `sessions_spawn` with these enhanced parameters:

```python
sessions_spawn(
  task="<clear, specific task description with acceptance criteria>",
  label="<descriptive label with role>",
  model="<model based on task difficulty>",
  mode="run",  # one-shot task
  timeoutSeconds=300,  # increased for complex tasks
  runtime="subagent"
)
```

### Enhanced Model Selection (Updated 2026-03-25)

| Task Difficulty | Model | Rationale | Cost |
|----------------|-------|-----------|------|
| Simple (file edit, format) | siliconflow/deepseek-ai/DeepSeek-V3 | Free, fast, good for planning | ¥0 |
| Medium (feature, bug fix) | deepseek/deepseek-chat | Strong coding, ¥10 balance | ~¥0.02/1K tokens |
| Complex (architecture, multi-file) | deepseek/deepseek-chat | Best coding and reasoning | ~¥0.02/1K tokens |
| Research (architecture study) | siliconflow/deepseek-ai/DeepSeek-V3 | Free, good for research | ¥0 |

### Sub-Agent Role Templates

Based on Claude Agent Teams research, use these role templates:

1. **Architect** - System design, architecture decisions
2. **Backend Engineer** - API development, database design
3. **Frontend Engineer** - UI components, visualization
4. **Test Engineer** - Testing strategy, quality assurance
5. **DevOps Engineer** - Deployment, monitoring, infrastructure
6. **Documentation Engineer** - Documentation, user guides
7. **Project Manager** - Progress tracking, risk management

## Multi-Agent Collaboration Protocol

### Direct Communication
Enable sub-agents to communicate directly using `sessions_send`:

```python
# Agent A sends message to Agent B
sessions_send(
  sessionKey="agent:main:subagent:agent-b-id",
  message=json.dumps({
    "type": "task_update",
    "sender": "agent-a-id",
    "content": "Task data ready for processing",
    "timestamp": datetime.utcnow().isoformat()
  })
)
```

### Real-Time Status Monitoring
- Use WebSocket for real-time status updates
- Implement status dashboard for visibility
- Track progress, tokens, and costs in real-time

### Task Dependencies Management
- Define task dependencies and blocking relationships
- Implement parallel execution with synchronization
- Handle timeout and failure scenarios

## Review Checklist (Enhanced)

### Technical Verification
- [ ] `git diff` — what exactly changed?
- [ ] Syntax valid — `python3 -m json.tool` for JSON, `bash -n` for scripts
- [ ] API test — `curl` the endpoint if backend changed
- [ ] Service restart — restart and verify `systemctl status`
- [ ] Data correct — actual data matches expected output

### Performance Metrics
- [ ] Time tracking — record start and end times
- [ ] Token consumption — track input/output tokens
- [ ] Cost calculation — estimate API cost
- [ ] Quality assessment — evaluate output quality

### Collaboration Verification
- [ ] Communication logs — review inter-agent messages
- [ ] Dependency resolution — verify task dependencies
- [ ] Progress synchronization — check status consistency
- [ ] Error handling — verify failure recovery

### Documentation
- [ ] Git commit — `git add -A && git commit -m "description"`
- [ ] Progress update — update `progress.txt`
- [ ] Feature tracking — update `feature_list.json`
- [ ] Cost reporting — document token usage and cost

**Never report success without completing all checks above.**

## Real-Time Visualization

### Status Dashboard Components
1. **Agent Status Dashboard** - Real-time sub-agent status
2. **Task Progress Board** - Visual task tracking
3. **Communication Log Panel** - Inter-agent messages
4. **Performance Dashboard** - Token usage and costs

### Integration with AI-Monitor
- Extend AI-Monitor with harness-leader visualization
- Provide real-time monitoring of multi-agent collaboration
- Integrate with existing token tracking system

## Best Practices

### Cost Control
1. Use free models (SiliconFlow DeepSeek-V3) for planning and research
2. Use DeepSeek V3 (¥10 balance) for coding and implementation
3. Monitor token consumption in real-time
4. Set timeout limits to prevent runaway costs

### Quality Assurance
1. Define clear acceptance criteria for each task
2. Implement peer review between sub-agents
3. Use automated testing where possible
4. Maintain comprehensive documentation

### Scalability
1. Design for parallel execution
2. Implement load balancing between agents
3. Use modular architecture for easy extension
4. Support both synchronous and asynchronous workflows

---

See [references/agent-roles.md](references/agent-roles.md) for role templates, [references/harness-workflow.md](references/harness-workflow.md) for detailed workflow, and [references/claude-agent-teams.md](references/claude-agent-teams.md) for advanced multi-agent collaboration patterns.

*Last updated: 2026-03-25 - Based on "Leader能力可视化面板 + harness-leader技能完善" project成果*
