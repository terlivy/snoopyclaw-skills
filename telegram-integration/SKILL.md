---
name: telegram-integration
description: "Telegram bot 集成配置：隐私模式、Gateway 设置、常见问题排查"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [telegram, messaging, integration, bot, privacy-mode, gateway]
created_by: hermes-agent
created_at: 2026-05-27
---

# Telegram Integration

Telegram 机器人集成到 Hermes Gateway 的完整指南。

## 快速设置

### 1. 创建 Telegram Bot

1. 在 Telegram 搜索 **@BotFather**
2. 发送 `/newbot`
3. 给 bot 起名字
4. 设置用户名（必须以 `bot` 结尾，如 `myagent_bot`）
5. 保存 BotFather 给的 **HTTP API Token**

### 2. 配置 Hermes Gateway

```bash
hermes gateway setup
```

选择 Telegram，填入 API Token。

### 3. 启动 Gateway

```bash
hermes gateway run
```

---

## 核心问题：群组中 Bot 不响应

### 症状

Bot 被拉进群组后，发送消息没有反应。

### 原因

Telegram Bot 默认 **隐私模式（Privacy Mode）** 是开启的，只能接收：
- @命令（如 `/start`）
- 回复 Bot 的消息
- 特殊消息

无法接收普通群聊消息。

### 解决方案：关闭隐私模式

1. 在 Telegram 打开 **@BotFather**
2. 发送 `/mybots`
3. 选择你的机器人
4. → **Bot Settings** → **Privacy Mode** → **Groups**
5. 选择 **Disable**

**或者命令行方式：**
```
/setprivacy
```
选择你的 bot，然后选择 `Disable`

### 验证

关闭后，重新在群组发送消息测试。

---

## 架构说明

```
用户消息 → Telegram Server → Hermes Gateway → AIAgent → 回复
```

- **Gateway**：运行在 18789 端口（默认），接收 Telegram 消息
- **Privacy Mode**：Telegram 层面的限制，不影响 Gateway 运行
- **多 Bot 支持**：可为不同用途创建不同 Bot

---

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 群组无响应 | 隐私模式开启 | 关闭 BotFather 隐私模式 |
| Gateway 不启动 | 端口被占用 | `ss -tlnp \| grep 18789` 检查 |
| Token 错误 | API Token 配置错误 | 重新配置 `hermes gateway setup` |
| 消息延迟 | 网络问题 | 检查服务器网络连接 |

### 检查 Gateway 状态

```bash
hermes gateway status
hermes logs gateway.log | tail -20
```

### 重启 Gateway

```bash
hermes gateway restart
```

---

## 相关命令

```bash
hermes gateway setup        # 配置平台
hermes gateway run          # 启动
hermes gateway status       # 状态
hermes gateway restart      # 重启
hermes platforms            # 查看已连接平台
```

---

## 参考文档

- [Hermes Gateway 文档](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
