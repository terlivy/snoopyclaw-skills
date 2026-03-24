---
name: workspace-manager
description: Audit, optimize, and maintain OpenClaw workspace files (SOUL.md, AGENTS.md, MEMORY.md, etc.). Use when auditing workspace health, refining memories from daily logs into MEMORY.md, checking file sizes, removing redundancy, creating checklists, or optimizing token budget. Triggers on phrases like "audit workspace", "refine memory", "check file sizes", "workspace cleanup", "reduce token usage", "memory maintenance".
---

# Workspace Manager

Manage and optimize OpenClaw workspace files for token efficiency, consistency, and correctness.

## Quick Audit

Run this to assess workspace health:

```bash
# File size audit (core workspace files)
wc -c $WORKSPACE/*.md | sort -n

# Total startup load estimate
cat $WORKSPACE/SOUL.md $WORKSPACE/USER.md $WORKSPACE/IDENTITY.md \
    $WORKSPACE/AGENTS.md $WORKSPACE/MEMORY.md $WORKSPACE/TOOLS.md \
    $WORKSPACE/HEARTBEAT.md 2>/dev/null | wc -c
```

See [references/audit-guide.md](references/audit-guide.md) for thresholds and detailed audit procedures.

## Memory Refinery

### Daily Log → MEMORY.md

1. Read recent `memory/YYYY-MM-DD.md` files
2. Extract recurring patterns and hard-won lessons
3. Distill into atomic, actionable rules for MEMORY.md
4. Archive logs older than 30 days to `memory/archive/`

### MEMORY.md → SKILL.md Migration

When a rule in MEMORY.md has been stable for weeks and never violated:
1. Evaluate: does this rule belong in a specific skill's SKILL.md?
2. If yes, add it to that skill and remove from MEMORY.md
3. If no, keep it in MEMORY.md

See [references/memory-refinery.md](references/memory-refinery.md) for detailed workflows and examples.

## Checklist Management

High-risk operations should have step-by-step checklists in `checklists/`:

| Operation | Checklist File |
|-----------|---------------|
| Gateway restart | `checklists/gateway-restart.md` |
| Deploy service | `checklists/deploy-service.md` |
| Config change | `checklists/config-patch.md` |
| Memory maintenance | `checklists/memory-maintenance.md` |

Register new checklists in AGENTS.md routing table.

## Redundancy Rules

| Source A | Source B | Keep In |
|----------|----------|---------|
| SOUL.md (rules) | AGENTS.md (rules) | AGENTS.md |
| TOOLS.md | MEMORY.md | TOOLS.md |
| MEMORY.md | SKILL.md | SKILL.md (if stable) |
| USER.md | SOUL.md (preferences) | USER.md |

SOUL.md is for personality and values only. Rules, checklists, and procedures belong in AGENTS.md.

## File Size Thresholds

| Size | Status | Action |
|------|--------|--------|
| < 5K chars | ✅ Healthy | None |
| 5K–10K | ⚠️ Watch | Monitor growth |
| 10K–15K | 🔶 Review | Move content to `docs/` or `references/` |
| > 20K | 🔴 Truncated | Split immediately (OpenClaw truncates > 20K) |

## docs/ Directory

`docs/` stores on-demand content NOT auto-loaded every turn. Move here:
- Historical project documents
- Detailed integration guides
- One-off reports and analyses

Keep in workspace root only files needed every turn.
