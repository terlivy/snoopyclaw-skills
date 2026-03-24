# Workspace Audit Guide

Detailed procedures for auditing and optimizing OpenClaw workspace files.

## File Responsibilities

| File | Purpose | Loaded When | Sub-Agent Visible |
|------|---------|-------------|-------------------|
| AGENTS.md | Startup sequence, rules, checklist routing | Every turn | Yes |
| SOUL.md | Personality, tone, values | Every turn | Yes |
| TOOLS.md | Environment-specific info (SSH, TTS, cameras) | Every turn | Yes |
| USER.md | User profile, preferences | Main session only | No |
| IDENTITY.md | Name, emoji, avatar | Every turn | Yes |
| HEARTBEAT.md | Periodic check tasks | Heartbeat | Conditional |
| MEMORY.md | Long-term rules and red lines | Main session only | **Never** |
| BOOTSTRAP.md | First-run initialization | New workspace only | No |
| DEPLOYMENTS.md | Service deployment records | On-demand | Yes |

## Audit Commands

```bash
# Full size audit
for f in $WORKSPACE/*.md; do
  printf "%-25s %6d chars  %4d lines\n" "$(basename $f)" "$(wc -c < "$f")" "$(wc -l < "$f")"
done

# Memory directory audit
for f in $WORKSPACE/memory/*.md; do
  printf "%-30s %6d chars\n" "$(basename $f)" "$(wc -c < "$f")"
done

# Total startup cost
cat $WORKSPACE/SOUL.md $WORKSPACE/USER.md $WORKSPACE/IDENTITY.md \
    $WORKSPACE/AGENTS.md $WORKSPACE/MEMORY.md $WORKSPACE/TOOLS.md \
    $WORKSPACE/HEARTBEAT.md 2>/dev/null | wc -c
```

## Token Budget

| Constraint | Limit |
|-----------|-------|
| Single file hard max | 20,000 chars (OpenClaw truncates beyond this) |
| Recommended single file | < 10,000 chars |
| Total startup files | < 50,000 chars |
| Ideal single file | 3,000–7,000 chars |

## Redundancy Detection

Check for duplicate content across files:

```bash
# SOUL.md vs AGENTS.md rules overlap
grep -c "红线\|red line\|铁律\|规则\|rule" $WORKSPACE/SOUL.md
grep -c "红线\|red line\|铁律\|规则\|rule" $WORKSPACE/AGENTS.md

# TOOLS.md vs MEMORY.md overlap
comm -12 <(grep -oP '(?<=`)[^`]+`' $WORKSPACE/TOOLS.md | sort) \
         <(grep -oP '(?<=`)[^`]+`' $WORKSPACE/MEMORY.md | sort)
```

### Resolution Rules

1. **SOUL.md has rules** → Move to AGENTS.md. SOUL is personality only.
2. **MEMORY.md has tool info** → Move to TOOLS.md. MEMORY is rules only.
3. **MEMORY.md and SKILL.md share rules** → Keep stable rules in SKILL.md.
4. **USER.md and SOUL.md share preferences** → Keep in USER.md only.
5. **AGENTS.md has long procedures** → Extract to `checklists/`.

## Content Optimization Patterns

### Move to docs/ (on-demand loading)
- Historical project reports
- Detailed integration guides
- One-off analyses
- Long reference tables

### Move to checklists/ (on-demand loading)
- Step-by-step deployment procedures
- Gateway restart procedures
- Configuration change procedures

### Move to references/ (skill-level loading)
- Domain-specific schemas
- API documentation
- Detailed workflow guides

### Delete
- BOOTSTRAP.md after first run
- Completed task plans
- Superseded configuration notes

## Workspace Directory Structure

```
$WORKSPACE/
├── AGENTS.md          # Procedures, startup sequence, routing
├── SOUL.md            # Personality, values (no rules)
├── TOOLS.md           # Environment notes
├── USER.md            # User profile (main session only)
├── IDENTITY.md        # Name, emoji, mission
├── HEARTBEAT.md       # Periodic check instructions
├── DEPLOYMENTS.md     # Service deployment records
├── MEMORY.md          # Red-line rules (main session only, NEVER sub-agents)
├── memory/
│   ├── session-index.md
│   ├── YYYY-MM-DD.md
│   └── archive/
├── checklists/        # Step-by-step procedures for risky ops
├── docs/              # On-demand documents (not auto-loaded)
└── templates/         # Sub-agent prompt templates
```
