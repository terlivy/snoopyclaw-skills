# Harness Workflow

Detailed workflow for the Harness/Leader pattern based on "Effective Harnesses for Long-Running Agents".

## Effective Harnesses Core Concepts

### Feature List

Every non-trivial task should have a `feature_list.json` tracking what needs to be done:

```json
{
  "task": "Fix ledger module data display",
  "features": [
    {"id": 1, "name": "Fix field name mapping", "status": "todo"},
    {"id": 2, "name": "Verify API response", "status": "todo"},
    {"id": 3, "name": "Test frontend rendering", "status": "todo"}
  ],
  "model": "deepseek/deepseek-chat",
  "started": "2026-03-24T12:00:00Z"
}
```

### Progress Tracking

Maintain a `progress.txt` in the task directory:

```
[12:00] Task started: Fix ledger module
[12:05] Sub-agent spawned: deepseek/deepseek-chat
[12:15] Sub-agent reported: field mapping fixed
[12:16] SC review: git diff shows 3 files changed
[12:17] SC verify: curl shows correct API response
[12:18] SC commit: abc123 "fix: ledger field name mapping"
[12:20] Task complete ✅
```

## Sub-Agent Lifecycle

### Phase 1: Task Decomposition

1. Receive user request
2. Break into atomic sub-tasks
3. Identify dependencies (DAG model)
4. Assign models based on difficulty
5. Create execution plan

### Phase 2: Spawn and Execute

**Serial tasks** (dependencies exist):
```
Task A → Task B → Task C
```
Spawn B only after A passes review.

**Parallel tasks** (no dependencies):
```
Task A ─┐
Task B ─┤→ Merge & Verify
Task C ─┘
```
Spawn all simultaneously, review all when complete.

### Phase 3: Review (Mandatory)

After EVERY sub-agent completion, the Harness MUST:

1. **Read the changes**: `git diff` — what exactly was modified?
2. **Validate syntax**: JSON valid? Script syntax correct?
3. **Test functionality**: `curl` API endpoints, check service status
4. **Restart if needed**: `systemctl restart` and verify
5. **Confirm data**: actual output matches expected
6. **Commit**: `git add -A && git commit -m "description"`

**Anti-pattern (NEVER do this):**
- Forward sub-agent output to user without reviewing
- Report success based on sub-agent's self-assessment
- Skip the git diff step

### Phase 4: Report

```
## Task Complete ✅

**What was done:** {brief description}
**Files changed:** {list from git diff}
**Verification:** {what tests were run and results}
**Git commit:** {commit hash, message}
**Next steps:** {if any}
```

## Dependency Management (DAG Model)

### Serial Dependency
```python
# Task B depends on Task A
result_a = spawn(task_a)  # Wait for completion
if a_passed_review:
    result_b = spawn(task_b)
```

### Parallel Execution
```python
# Tasks A, B, C are independent
spawn(task_a)  # Fire and wait for all
spawn(task_b)
spawn(task_c)
# Review all results when all complete
```

### Mixed DAG
```python
# A → B, A → C, B+C → D
result_a = spawn(task_a)
if a_passed:
    result_b = spawn(task_b)
    result_c = spawn(task_c)
    if b_passed and c_passed:
        result_d = spawn(task_d)
```

## Cost Optimization

| Strategy | When to Use |
|----------|------------|
| Use cheapest model (glm-4.5-air) | Simple formatting, file moves, docs |
| Use deepseek-chat | Coding tasks, bug fixes, features |
| Use glm-5-turbo | Architecture decisions, complex analysis |
| Batch related tasks | Reduce overhead of multiple spawns |
| Reuse sub-agent context | For iterative tasks (fix → verify → fix) |
