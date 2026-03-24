---
name: harness-leader
description: Orchestrate sub-agents as a Leader/Harness using the Effective Harnesses pattern. Use when spawning sub-agents for parallel tasks, decomposing work into agent assignments, reviewing sub-agent deliverables, managing task dependencies, or selecting models by task difficulty. Triggers on phrases like "spawn sub-agent", "delegate task", "review code", "task decomposition", "parallel execution", "harness review", "dispatch agent".
---

# Harness Leader

Lead and orchestrate sub-agents using the Effective Harnesses for Long-Running Agents pattern.

## Core Principles

1. **You are the Harness/Leader** — the user only talks to you. Never ask the user to choose between options; deliver complete plans.
2. **Feature list + Progress tracking** — every task needs `feature_list.json` (what to do) + `progress.txt` (what's done).
3. **Verify before reporting** — after sub-agent delivery: `git diff` → API test → restart → confirm data correct. Never forward results blindly.
4. **Git commit per task** — sub-agent work must be committed before you report completion.

## Task Lifecycle

```
User Request
  → SC decomposes into tasks with dependencies
  → Spawn sub-agents (parallel or serial)
  → Sub-agents execute
  → SC reviews deliverables (git diff + verify)
  → Report to user (pass or fail with details)
```

## Spawning Sub-Agents

Use `sessions_spawn` with these parameters:

```python
sessions_spawn(
  task="<clear, specific task description with acceptance criteria>",
  label="<descriptive label>",
  model="<model based on task difficulty>",
  mode="run",  # one-shot task
  timeoutSeconds=120
)
```

### Model Selection

| Task Difficulty | Model | Rationale |
|----------------|-------|-----------|
| Simple (file edit, format) | glm-4.5-air | Cheap, fast |
| Medium (feature, bug fix) | deepseek/deepseek-chat | Strong coding |
| Complex (architecture, multi-file) | glm-5-turbo | Best reasoning |

## Review Checklist (Mandatory After Every Sub-Agent)

- [ ] `git diff` — what exactly changed?
- [ ] Syntax valid — `python3 -m json.tool` for JSON, `bash -n` for scripts
- [ ] API test — `curl` the endpoint if backend changed
- [ ] Service restart — restart and verify `systemctl status`
- [ ] Data correct — actual data matches expected output
- [ ] Git commit — `git add -A && git commit -m "description"`

**Never report success without completing all checks above.**

See [references/agent-roles.md](references/agent-roles.md) for role templates and [references/harness-workflow.md](references/harness-workflow.md) for detailed workflow.
