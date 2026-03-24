#!/usr/bin/env bash
# check-health.sh — OpenClaw infrastructure health check
# Usage: bash check-health.sh [--json]
#
set -euo pipefail

JSON_OUTPUT=false
[ "${1:-}" = "--json" ] && JSON_OUTPUT=true

# ── Helper functions ──
ok() { [ "$JSON_OUTPUT" = true ] && echo "\"$1\": true" || echo "  ✅ $1"; }
fail() { [ "$JSON_OUTPUT" = true ] && echo "\"$1\": false" || echo "  ❌ $1"; }
warn() { [ "$JSON_OUTPUT" = true ] && echo "\"$1\": \"warning\"" || echo "  ⚠️  $1"; }
info() { [ "$JSON_OUTPUT" = true ] && echo "\"$1\": \"$2\"" || echo "  ℹ️  $1: $2"; }

# ── Ollama ──
if pgrep -x ollama >/dev/null 2>&1; then
  ok "Ollama running"
else
  fail "Ollama NOT running"
fi

# ── Gateway ──
if systemctl --user is-active openclaw-gateway.service >/dev/null 2>&1; then
  ok "Gateway active"
else
  fail "Gateway NOT active"
fi

# ── Ports ──
for port_name in "18789:Gateway" "11434:Ollama"; do
  port="${port_name%%:*}"
  name="${port_name##*:}"
  if ss -tlnp 2>/dev/null | grep -q ":${port} "; then
    ok "${name} port ${port} listening"
  else
    warn "${name} port ${port} NOT listening"
  fi
done

# ── Disk ──
DISK_PCT=$(df /home 2>/dev/null | awk 'NR==2{sub(/%/,"",$5); print $5}')
if [ -n "$DISK_PCT" ]; then
  if [ "$DISK_PCT" -lt 70 ]; then
    ok "Disk usage ${DISK_PCT}%"
  elif [ "$DISK_PCT" -lt 85 ]; then
    warn "Disk usage ${DISK_PCT}% (getting high)"
  else
    fail "Disk usage ${DISK_PCT}% (critical)"
  fi
  info "disk_path" "/home"
fi

# ── Memory ──
MEM_AVAIL=$(free -m 2>/dev/null | awk 'NR==2{print $7}')
if [ -n "$MEM_AVAIL" ]; then
  if [ "$MEM_AVAIL" -gt 500 ]; then
    ok "Available memory ${MEM_AVAIL}MB"
  elif [ "$MEM_AVAIL" -gt 100 ]; then
    warn "Available memory ${MEM_AVAIL}MB (low)"
  else
    fail "Available memory ${MEM_AVAIL}MB (critical)"
  fi
fi

# ── JSON config ──
OPENCLAW_CONFIG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
if [ -f "$OPENCLAW_CONFIG" ]; then
  if python3 -m json.tool "$OPENCLAW_CONFIG" >/dev/null 2>&1; then
    ok "openclaw.json valid"
  else
    fail "openclaw.json INVALID"
  fi
else
  warn "openclaw.json not found"
fi

# ── Memory plugin ──
if [ -d "${HOME}/.openclaw/memory/lancedb-pro" ]; then
  ok "Memory plugin data exists"
else
  warn "Memory plugin data not found"
fi

# ── Fix service available ──
if [ -x "${HOME}/clawd/scripts/openclaw-fix.sh" ]; then
  ok "Auto-fix script available"
else
  warn "Auto-fix script not found"
fi

# ── Timestamp ──
[ "$JSON_OUTPUT" = true ] && echo "\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\""
[ "$JSON_OUTPUT" != true ] && echo ""
[ "$JSON_OUTPUT" != true ] && echo "Checked at: $(date)"
