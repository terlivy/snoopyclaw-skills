# 🐾 SnoopyClaw Skills

> OpenClaw skills crafted by [SnoopyClaw](https://github.com/terlivy) (SC) — born from real production experience, not theory.

SnoopyClaw Skills 是 SnoopyClaw 主脑的专属技能库，包含 **13 个技能**，覆盖 SAS 工作流、博士后工作站管理、基础设施三大领域。所有技能均通过 `--- name / description ---` frontmatter 声明，OpenClaw 启动时自动识别并加载对应触发词。

---

## 技能索引

| 技能 | 分类 | Agent | 触发词关键词 |
|------|------|-------|------------|
| `sas-default` | 🏛 SAS | — | SAS准则、SAS执行、六阶段、阶段门 |
| `sas-task-planner` | 🏛 SAS | — | 做计划、出方案、工作计划、任务规划 |
| `harness-leader` | 🏛 SAS | sas-leader ✅ | spawn sub-agent、multi-agent、task decomposition |
| `system-healer` | 🏛 SAS | — | heal、fix、health check、Ollama down |
| `workspace-manager` | 🏛 SAS | — | workspace audit、refine memory、file sizes |
| `postdoc-director` | 🔬 博士后工作站 | — | KPI检查、工作安排、人员状态、进度汇报 |
| `postdoc-admin` | 🔬 博士后工作站 | — | 会议通知、月度汇报、公文请示、工作汇总 |
| `postdoc-ip` | 🔬 博士后工作站 | — | 专利挖掘、交底书、审查意见、新颖性判断 |
| `postdoc-project` | 🔬 博士后工作站 | — | 省级项目申报、预算编制、申报材料清单 |
| `postdoc-recruit` | 🔬 博士后工作站 | — | 招聘博士后、入职手续、合同模板、进站 |
| `postdoc-policy` | 🔬 博士后工作站 | — | 新政策、博士后基金申报、CNAS新规 |
| `postdoc-cnas` | 🔬 博士后工作站 | — | CNAS认证、内审检查表、管理评审 |
| `postdoc-anticheat` | 🔬 博士后工作站 | — | 隐私风险、脱敏、知识资产保护、Skill安全 |

---

## 🏛 SAS 工作流技能（5个）

### 🎯 sas-default
**SAS 工作准则执行智能体** — 每次任务执行时自动检索 SAS 准则相关章节，确保按完整规则执行。不知必查，查后再做，阶段门控。
- **触发词**: `SAS准则`、`SAS执行`、`六阶段`、`阶段门`、`SAS任务`
- **SAS版本**: v1.4.0
- **核心原则**: 不知必查，查后再做，阶段门控

### 📋 sas-task-planner
**SAS 任务全生命周期管理** — 计划→方案设计→实施→测试→复盘→运维。拆解原子步骤、估算 token/成本/时间、标记风险、制定验收标准。
- **触发词**: `做计划`、`出方案`、`工作计划`、`任务规划`、`实施方案`、`测试`、`复盘`
- **阶段门控**: 自动审批（低风险）+ 人工审批（高风险）
- **质量标准**: 快（25%）+ 准（25%）+ 问题少（25%）+ 成本低（25%）

### 🔗 harness-leader
**多 Agent 协作引擎** — 基于 Effective Harnesses 模式，协调多个子 Agent 并行/串行执行任务。子任务派发、实时监控、交付验收。
- **触发词**: `spawn sub-agent`、`delegate task`、`multi-agent`、`task decomposition`、`parallel execution`、`harness review`
- **核心**: Leader/Harness 架构，子任务派发与状态追踪，git commit per task
- **角色模板**: Architect、Backend/Frontend Engineer、DevOps、Test Engineer、PM
- **模型选择**: 简单任务用 SiliconFlow DeepSeek-V3（免费），编程用 DeepSeek Chat，复杂推理用 MiniMax-M2.7

### 🏥 system-healer
**自愈系统** — 自动监控和修复 OpenClaw Gateway 及依赖服务的常见故障。Gateway 崩溃自动重启链路：systemd → OnFailure → openclaw-fix.sh → 诊断报告。
- **触发词**: `heal gateway`、`fix gateway`、`health check`、`Ollama down`、`port conflict`、`systemd service`
- **自愈链路**: Gateway crash → systemd restart (5s, 5次) → OnFailure fix → alert user
- **常见问题**: JSON config 无效、端口占用、OOM、Ollama 无响应、插件加载失败

### 📂 workspace-manager
**工作区管理器** — 审计、优化和维护 OpenClaw workspace 文件（SOUL.md、AGENTS.md、MEMORY.md 等）。文件健康检查、记忆提炼（每日日志→MEMORY.md）、去重与归档。
- **触发词**: `audit workspace`、`refine memory`、`check file sizes`、`workspace cleanup`、`reduce token usage`、`memory maintenance`
- **文件阈值**: <5K ✅ / 5-10K ⚠️ / 10-15K 🔶 / >20K 🔴（超20K会被截断）

---

## 🔬 博士后工作站技能（8个）

> 围绕博士后科研工作站三大业务线：**科研管理**（postdoc-director / postdoc-ip / postdoc-project）、**行政支撑**（postdoc-admin / postdoc-policy / postdoc-recruit）、**资质认证**（postdoc-cnas）、**安全合规**（postdoc-anticheat）。

### 🏛 postdoc-director
**博士后工作站所长** — 工作站 KPI 看板（财政资金 400 万目标实时追踪）、人员管理（张思聪/武林分工与状态）、工作统筹、风险预警。
- **触发词**: `KPI检查`、`工作安排`、`人员状态`、`团队状态`、`进度汇报`、`风险预警`
- **核心 KPI**: 财政资金 400 万（主指标）、省级项目申报 12%、CNAS 认证、专利产出 ≥5件/年

### 📝 postdoc-admin
**行政秘书** — 博士后工作站日常行政事务：公文撰写（符合 GB/T 9704-2012）、数据统计与报表、日程管理、模板库（周报/月报/会议纪要/通知）。
- **触发词**: `写一个会议通知`、`生成月度汇报材料`、`统计本季度工作数据`、`帮我写一份请示`、`制作工作汇总表`
- **公文类型**: 通知、请示、报告、函、纪要

### 💡 postdoc-ip
**知识产权/专利管理** — 专利方案新颖性/创造性判断、专利交底书生成、审查意见答复策略、专利挖掘与布局。
- **触发词**: `专利挖掘`、`专利布局`、`交底书生成`、`审查意见答复`、`专利检索`、`新颖性判断`、`创造性判断`
- **交底书模板**: 发明名称→技术领域→背景技术→发明内容（目的/方案/有益效果）→附图说明→具体实施方式→权利要求书

### 📊 postdoc-project
**科研项目管理** — 省级项目申报全流程辅助：申报材料包生成、预算编制（政府标准科目）、申请书撰写、绩效考核指标、进度管理。
- **触发词**: `准备一个省级项目申报`、`帮我写项目预算`、`检查申报材料完整性`、`生成申报材料清单`、`项目申报书框架`、`绩效考核指标`

### 👥 postdoc-recruit
**人才引进与入职管理** — 博士后招聘 JD 生成、入职手续办理（进站清单）、合同模板、工资核定、试用期/中期考核、人才项目申请（博新计划等）。
- **触发词**: `招聘一个博士后`、`帮他办入职`、`博士后合同模板`、`工资核定`、`进站手续`、`试用期考核`、`人才项目申请`

### 📡 postdoc-policy
**政策情报追踪** — 追踪博士后工作站相关国家级/省级政策动态：科研基金（NSFC/省级科技计划）、人才项目、CNAS 新规、税务补贴政策。主动推送 + 日历提醒。
- **触发词**: `最近有什么新政策`、`博士后基金什么时候申报`、`帮我解读这个文件`、`设置政策推送`、`下周截止的项目`、`CNAS有新规吗`

### ✅ postdoc-cnas
**CNAS 认证管理** — 实验室认可认证全过程支持，熟悉 CNAS-CL01：质量手册、程序文件、内审检查表、管理评审、不确定度评估（MU）、期间核查、认证进度跟踪。
- **触发词**: `CNAS认证流程`、`准备实验室认可材料`、`内审检查表`、`管理评审`、`不确定度评估`、`期间核查`、`质量手册`

### 🔒 postdoc-anticheat
**隐私保护与知识资产守护** — 防止博士后工作站隐私数据和核心知识产权被意外泄露或模型逆向蒸馏。隐私风险扫描、脱敏处理、Skill 交付安全评估、知识分级管理。
- **触发词**: `这个Skill能分享吗`、`帮我检查隐私风险`、`脱敏这个文件`、`知识资产保护`、`检查文档有没有敏感信息`
- **风险等级**: 🔴高危 / 🟡中危 / 🟢低危 / ✅安全
- **知识分级**: 🔴核心机密 / 🟡内部资料 / 🟢可公开 / 📢团队共享

---

## 模型分配策略

| 任务类型 | 推荐模型 | 成本 |
|---------|---------|------|
| 复杂推理/规划/统筹 | MiniMax-M2.7 / MiniMax-M2.7-highspeed | Token Plan |
| 简单查询/轻量任务 | GLM-4.5-Air / GLM-4.7 | 免费额度 |
| 编程/代码/文档处理 | DeepSeek Chat | ¥10余额 |
| 研究/调研/免费任务 | SiliconFlow DeepSeek-V3 | 免费 |

---

## 📁 目录结构

```
snoopyclaw-skills/
├── README.md                    ← 本文件
├── sas-default/                 # SAS 准则执行
│   └── SKILL.md
├── sas-task-planner/           # 任务全生命周期
│   └── SKILL.md
├── harness-leader/            # 多 Agent 协作引擎（已分配给 sas-leader）
│   └── SKILL.md
│   └── references/             # 🔧 待完善：agent-roles.md, harness-workflow.md
├── system-healer/             # 自愈系统
│   └── SKILL.md
│   └── references/             # 🔧 待完善：health-checks.md, self-healing-architecture.md
├── workspace-manager/         # 工作区管理
│   └── SKILL.md
│   └── references/             # 🔧 待完善：audit-guide.md, memory-refinery.md
├── postdoc-director/          # 工作站所长
├── postdoc-admin/             # 行政秘书
├── postdoc-ip/                # 知识产权
├── postdoc-project/           # 项目申报
├── postdoc-recruit/           # 招聘入职
├── postdoc-policy/            # 政策情报
├── postdoc-cnas/              # CNAS 认证
└── postdoc-anticheat/         # 隐私保护
```

> 🔧 references/ 目录为待完善状态，相关参考文档正在建设中。

---

## 安装与使用

```bash
# 查看已安装技能
openclaw skills list

# 派发给指定 Agent（如 sas-leader）
# 修改 openclaw.json 中对应 Agent 的 skills 字段
"agents": {
  "list": [
    { "id": "sas-leader", "skills": ["harness-leader"] }
  ]
}
# 然后重启 Gateway：systemctl --user restart openclaw-gateway
```

---

## 🔗 相关仓库

| 仓库 | 地址 | 说明 |
|------|------|------|
| SAS 准则文档 | https://github.com/terlivy/SAS | 工作准则完整文档体系 |
| SAS 插件 | https://github.com/terlivy/SAS-plug-in | 阶段门控执行引擎 |
| SAS 脚本 | https://github.com/terlivy/SAS-script | 自动化脚本集合 |

---

## 📜 许可

SnoopyClaw 团队内部使用。的知识库，闭源。
