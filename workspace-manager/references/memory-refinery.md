# Memory Refinery

Workflows for refining raw daily logs into distilled MEMORY.md rules, and migrating stable rules to SKILL.md files.

## Daily Log → MEMORY.md

### Step 1: Identify Candidates

Read recent daily logs (`memory/YYYY-MM-DD.md`) and tag entries:

| Tag | Refine? | Action |
|-----|---------|--------|
| `[教训]` | Yes | Extract as atomic rule |
| `[决策]` | Yes | Extract as decision record |
| `[偏好]` | Yes | Extract as preference |
| `[任务]` | Maybe | Only if it reveals a reusable pattern |
| `[项目]` | No | Keep in projects.md |

### Step 2: Distill

Convert verbose log entries into atomic MEMORY.md rules:

**Before (daily log):**
```
[教训] 今天 reset 前忘了存记忆，导致 3/24 那次会话的大量工作（DeepSeek 配置、台账修复等）全部丢失。以后 reset 前必须：①写日志 ②更新 session-index ③存向量记忆 ④告知用户。
```

**After (MEMORY.md rule):**
```
N. **Reset 前四步铁律（记忆）**：reset 前必须执行：①写日志 ②更新 session-index ③存向量记忆 ④告知用户。不完成不允许 reset。
```

Key principles:
- One rule = one actionable directive
- Include category tag for context
- Add background in the same sentence if needed
- Keep under 80 chars per rule when possible

### Step 3: Deduplicate

Check if the new rule already exists in MEMORY.md under different wording. If so, merge.

### Step 4: Archive

Move daily logs older than 30 days to `memory/archive/`:

```bash
# Archive old daily logs
find $WORKSPACE/memory/ -name "2025-*.md" -exec mv {} $WORKSPACE/memory/archive/ \;
```

## MEMORY.md → SKILL.md Migration

### When to Migrate

A rule is ready to migrate when:
1. It has been in MEMORY.md for 2+ weeks
2. It has never been violated
3. It is tool/skill-specific (not a universal behavioral rule)

### When NOT to Migrate

Keep in MEMORY.md if:
1. It's a universal behavioral red line (payment rules, privacy, etc.)
2. It's frequently referenced across different tasks
3. It's about identity, mission, or core values

### Migration Process

1. Read the rule from MEMORY.md
2. Find the most relevant skill's SKILL.md
3. Add the rule in the appropriate section
4. Remove from MEMORY.md
5. Verify the skill still triggers correctly

### Example

**MEMORY.md before:**
```
N. **读文件前先看大小（大文件红线）**：ls -la 预估 token，单文件超 50K 必须分块读。
```

**SKILL.md after (added to workspace-manager skill):**
```markdown
## Pre-read Protocol
Always check file size before reading: `ls -la <file>`. Files > 50K tokens MUST be read in chunks (offset + limit).
```

## MEMORY.md Size Control

### Target Size
- **Ideal**: 3,000–5,000 chars
- **Warning**: > 7,000 chars
- **Critical**: > 10,000 chars (split immediately)

### Size Reduction Strategies

1. **Archive completed milestones** → `memory/archive/milestones.md`
2. **Archive completed tasks** → remove from TODO list
3. **Migrate stable rules** → corresponding SKILL.md
4. **Consolidate similar rules** → merge duplicates
5. **Move detailed context to memory/ files** → keep only rule in MEMORY.md

### Monthly Refinery Schedule

| Week | Action |
|------|--------|
| Week 1 | Refine last month's daily logs into MEMORY.md |
| Week 2 | Check for rules ready to migrate to SKILL.md |
| Week 3 | Archive daily logs older than 30 days |
| Week 4 | Full MEMORY.md size audit and optimization |
