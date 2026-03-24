# Self-Healing Architecture

Detailed design for the OpenClaw Gateway auto-recovery system.

## Architecture Overview

```
                    ┌──────────────────────┐
                    │   OpenClaw Gateway   │
                    │   (systemd service)  │
                    └──────────┬───────────┘
                               │ crash
                               ▼
                    ┌──────────────────────┐
                    │  systemd auto-restart│
                    │  (5s interval)       │
                    └──────────┬───────────┘
                               │ 5 failures in 60s
                               ▼
                    ┌──────────────────────┐
                    │  Mark as FAILED      │
                    │  (OnFailure trigger) │
                    └──────────┬───────────┘
                               │
                               ▼
                ┌──────────────────────────┐
                │  openclaw-fix.service    │
                │  (oneshot)               │
                │  ┌────────────────────┐  │
                │  │ openclaw-fix.sh    │  │
                │  │ 1. Single-instance │  │
                │  │    lock (flock)    │  │
                │  │ 2. Collect errors  │  │
                │  │ 3. Validate config │  │
                │  │ 4. Check Node.js   │  │
                │  │ 5. Check ports     │  │
                │  │ 6. Check Ollama    │  │
                │  │ 7. Restart Gateway │  │
                │  │ 8. Verify active   │  │
                │  │ 9. Retry up to 2x  │  │
                │  └────────────────────┘  │
                └──────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         success                   still failing
              │                         │
              ▼                         ▼
        ┌──────────┐          ┌──────────────┐
        │ Continue  │          │ Alert user   │
        │ Running   │          │ (log details)│
        └──────────┘          └──────────────┘
```

## systemd Configuration

### Gateway Service Drop-In (`auto-fix.conf`)

```ini
[Unit]
OnFailure=openclaw-fix.service
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Restart=always
```

### Fix Service

```ini
[Unit]
Description=OpenClaw Gateway Auto-Fix
After=network-online.target

[Service]
Type=oneshot
ExecStart=%h/clawd/scripts/openclaw-fix.sh
TimeoutStartSec=120
```

## Fix Script Design Principles

1. **Single-instance lock** — `flock` on lockfile prevents concurrent execution
2. **JSON config validation** — `python3 -m json.tool` before any restart attempt
3. **Node.js check** — verify `node` command exists and version
4. **Port conflict detection** — `ss -tlnp` to find orphan processes
5. **Ollama dependency check** — auto-start Ollama if down (embedding requires it)
6. **Restart and verify** — `systemctl restart` + `systemctl is-active` check
7. **Retry limit** — max 2 attempts, then log and exit
8. **Result file** — write JSON result to `$XDG_RUNTIME_DIR/openclaw-fix-result.json`

## Error Classification & Auto-Fix

| Error Type | Detection | Auto-Fix |
|-----------|-----------|----------|
| Invalid JSON config | `python3 -m json.tool` fails | Backup config, report error |
| Port already in use | `ss -tlnp` shows PID | Kill orphan process if not current Gateway |
| Ollama not running | `pgrep -x ollama` fails | `ollama serve` in background |
| Node.js missing | `command -v node` fails | Report error (cannot auto-fix) |
| Disk full | `df -h` shows >95% | Report error (cannot auto-fix) |
| Permission denied | Error log shows EACCES | Report error (cannot auto-fix) |

## Safe Restart Protocol

The `safe-gateway-restart.sh` script adds pre-checks before restarting:

```
1. Check Node.js availability
2. Validate JSON config
3. Check for port conflicts (kill orphans)
4. Restart Gateway
5. Wait 8 seconds
6. Verify active status
7. If failed: collect logs, retry up to 2 times
8. If still failed: report with diagnostic commands
```

## Trigger Mechanisms

| Trigger | Type | When |
|---------|------|------|
| systemd OnFailure | Automatic | Gateway crashes 5 times in 60 seconds |
| Heartbeat cron | Periodic | Every ~30 minutes during heartbeat |
| Manual | On-demand | `~/clawd/scripts/openclaw-fix.sh` |
| Safe restart | On-demand | `~/clawd/scripts/safe-gateway-restart.sh "reason"` |

## Monitoring

Check fix results:

```bash
# Last fix result
cat $XDG_RUNTIME_DIR/openclaw-fix-result.json 2>/dev/null

# Fix logs
ls -lt /tmp/openclaw-fix/

# Recent Gateway failures
journalctl --user -u openclaw-gateway.service --no-pager -n 20 | grep -E "Failed|Stopped|error"
```
