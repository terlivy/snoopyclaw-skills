# Health Checks

Comprehensive health check procedures for OpenClaw infrastructure.

## Quick Health Check

Run these first when diagnosing issues:

```bash
# Ollama (embedding dependency)
pgrep -x ollama >/dev/null && echo "Ollama: ✅" || echo "Ollama: ❌ DOWN"

# Gateway
systemctl --user is-active openclaw-gateway.service >/dev/null 2>&1 \
  && echo "Gateway: ✅" || echo "Gateway: ❌ DOWN"

# Key ports
ss -tlnp 2>/dev/null | grep -E "18789|11434" \
  && echo "Ports: ✅" || echo "Ports: ⚠️ not listening"
```

## Service Status Checks

```bash
# All OpenClaw-related user services
systemctl --user list-units 'openclaw*' 'ai-monitor*' --all

# Detailed Gateway status
systemctl --user status openclaw-gateway.service -l

# Recent Gateway logs
journalctl --user -u openclaw-gateway.service --no-pager -n 30
```

## Resource Checks

### Disk Space

```bash
# Overall disk usage
df -h / /home

# OpenClaw data directory
du -sh $HOME/.openclaw/

# Large files (>100MB) in workspace
find $HOME/.openclaw/ -type f -size +100M 2>/dev/null
```

Thresholds:
| Usage | Status | Action |
|-------|--------|--------|
| < 70% | ✅ | None |
| 70-85% | ⚠️ | Monitor, clean up old logs |
| 85-95% | 🔶 | Urgent cleanup |
| > 95% | 🔴 | Critical — service may fail |

### Memory

```bash
free -h
echo "==="
# OpenClaw process memory
ps aux | grep -E "openclaw|ollama|node" | grep -v grep | awk '{printf "%s\t%s\t%s\n", $11, $6"KB", $4"%"}'
```

### CPU

```bash
# Top processes
ps aux --sort=-%cpu | head -10
```

## Port Checks

```bash
# Check if expected ports are listening
echo "Expected ports:"
echo "  18789 - OpenClaw Gateway"
echo "  11434 - Ollama"
echo "  3000  - AI Monitor Frontend (if running)"
echo "  8000  - AI Monitor Backend (if running)"
echo ""
ss -tlnp | grep -E "18789|11434|3000|8000"
```

## Memory Plugin Check

```bash
# Plugin status
openclaw plugins list 2>&1 | grep memory

# LanceDB data integrity
ls -la $HOME/.openclaw/memory/lancedb-pro/ 2>/dev/null

# Memory stats (if memory-pro CLI available)
openclaw memory-pro stats 2>/dev/null
```

## Heartbeat Check Template

Use this template in HEARTBEAT.md or cron jobs:

```bash
#!/bin/bash
# Quick heartbeat health check
ISSUES=""

pgrep -x ollama >/dev/null || ISSUES+="Ollama is DOWN. "
systemctl --user is-active openclaw-gateway.service >/dev/null 2>&1 \
  || ISSUES+="Gateway is DOWN. "

DISK_PCT=$(df /home | awk 'NR==2{print $5}' | tr -d '%')
[ "$DISK_PCT" -gt 85 ] && ISSUES+="Disk at ${DISK_PCT}%. "

if [ -n "$ISSUES" ]; then
  echo "⚠️ HEALTH ISSUES: $ISSUES"
  echo "Fix: ~/clawd/scripts/openclaw-fix.sh"
else
  echo "✅ All systems healthy"
fi
```

## Diagnostic Commands

When things go wrong, run these in order:

```bash
# 1. What's the error?
journalctl --user -u openclaw-gateway.service --no-pager -n 50 | grep -iE "error|fatal|failed"

# 2. Is the config valid?
python3 -m json.tool $HOME/.openclaw/openclaw.json >/dev/null 2>&1 && echo "Config OK" || echo "Config INVALID"

# 3. Are ports free?
ss -tlnp | grep -E "18789|11434"

# 4. Is there enough disk?
df -h /home | tail -1

# 5. Run auto-fix
~/clawd/scripts/openclaw-fix.sh
```
