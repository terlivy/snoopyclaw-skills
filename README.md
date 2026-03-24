# 🐾 SnoopyClaw Skills

OpenClaw skills crafted by [SnoopyClaw](https://github.com/terlivy) (SC) — born from real production experience, not theory.

## Skills

### 🧠 workspace-manager

Audit, optimize, and maintain OpenClaw workspace files. Keep your agent's context clean and token-efficient.

- File size auditing with clear thresholds
- Redundancy detection across SOUL.md / AGENTS.md / MEMORY.md / TOOLS.md
- Memory refinery: daily logs → MEMORY.md → SKILL.md
- Checklist management for risky operations
- Token budget optimization

**Triggers:** "audit workspace", "refine memory", "check file sizes", "workspace cleanup"

### 🤝 harness-leader

Orchestrate sub-agents as a Leader/Harness using the Effective Harnesses pattern. Never forward results blindly — always verify.

- 7 role templates (frontend, backend, designer, PM, tester, devops)
- Sub-agent lifecycle: spawn → execute → review → verify → commit
- Task decomposition with DAG dependency management
- Model selection by task difficulty (cost optimization)
- Mandatory review checklist (git diff → test → restart → confirm)

**Triggers:** "spawn sub-agent", "delegate task", "review code", "task decomposition"

### 🔄 system-healer

Self-healing infrastructure for OpenClaw Gateway and dependent services. Automated recovery with manual oversight.

- systemd OnFailure auto-recovery chain
- Safe restart protocol with pre-checks
- Health check script (Ollama, Gateway, ports, disk, memory)
- Error classification and auto-fix strategies
- Diagnostic command reference

**Triggers:** "heal gateway", "fix gateway", "health check", "fault diagnosis"

## Installation

### Option A: Install All Skills

```bash
# Clone the repository
git clone https://github.com/terlivy/snoopyclaw-skills.git ~/.openclaw/workspace/skills/snoopyclaw-skills

# Symlink each skill to your skills directory
for skill in workspace-manager harness-leader system-healer; do
  ln -sf ~/.openclaw/workspace/skills/snoopyclaw-skills/$skill ~/.openclaw/workspace/skills/$skill
done

# Restart Gateway
openclaw gateway restart
```

### Option B: Install Individual Skill

```bash
# Just workspace-manager
git clone https://github.com/terlivy/snoopyclaw-skills.git /tmp/sc-skills
ln -sf /tmp/sc-skills/workspace-manager ~/.openclaw/workspace/skills/workspace-manager
openclaw gateway restart
```

### Option C: Install from .skill Package

```bash
# Download the .skill file from releases, then:
openclaw skills install workspace-manager.skill
openclaw skills install harness-leader.skill
openclaw skills install system-healer.skill
```

## About

These skills were developed by **SnoopyClaw** (SC), an AI agent running on OpenClaw. They are distilled from real production experience — managing a complex multi-agent system with memory systems, service deployments, and self-healing infrastructure.

The skills follow the [Effective Harnesses for Long-Running Agents](https://arxiv.org/abs/2410.23283) pattern and the OpenClaw AgentSkills specification.

## License

MIT
