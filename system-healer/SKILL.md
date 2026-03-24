---
name: system-healer
description: Self-healing, health checks, and service management for OpenClaw Gateway and dependent services. Use when Gateway crashes repeatedly, Ollama is down, ports are occupied, systemd services need management, or fault diagnosis is required. Triggers on phrases like "heal gateway", "fix gateway", "check service status", "restart gateway", "health check", "fault diagnosis", "Ollama down", "port conflict", "systemd service".
---

# System Healer

Self-healing infrastructure for OpenClaw Gateway and dependent services.

## Quick Health Check

```bash
# Core services
pgrep -x ollama >/dev/null && echo "Ollama: ✅" || echo "Ollama: ❌"
systemctl --user is-active openclaw-gateway.service >/dev/null && echo "Gateway: ✅" || echo "Gateway: ❌"

# Port check
ss -tlnp | grep -E "18789|11434|3000|8000" || echo "No port conflicts"
```

See [references/health-checks.md](references/health-checks.md) for comprehensive health check procedures.

## Self-Healing Architecture

Gateway crashes trigger an automatic healing chain:

```
Gateway crash
  → systemd restart (5s interval, up to 5 times/60s)
  → If still failing → OnFailure triggers fix service
  → Auto-fix script runs diagnostics and repair
  → Gateway restarts and health verified
  → If still failing → alert user with error details
```

See [references/self-healing-architecture.md](references/self-healing-architecture.md) for full architecture.

## Safe Restart

Always use the safe restart script for Gateway:

```bash
~/clawd/scripts/safe-gateway-restart.sh "reason for restart"
```

Or follow the manual checklist: `checklists/gateway-restart.md`.

## Manual Fix

```bash
# Run auto-fix manually
~/clawd/scripts/openclaw-fix.sh

# Check fix logs
ls /tmp/openclaw-fix/
```

## Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Gateway won't start | JSON config invalid | `python3 -m json.tool openclaw.json` |
| Port 18789 in use | Orphan process | Kill orphan, then restart |
| Memory errors | OOM | Check `free -h`, restart heavy services |
| Ollama not responding | Process hung | `killall ollama && ollama serve` |
| Plugin not loading | Config error | Check `openclaw plugins list` |
