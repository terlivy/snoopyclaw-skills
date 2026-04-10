#!/usr/bin/env python3
"""
kpi_dashboard.py - 博士后工作站 KPI 看板生成器
版本: v1.0
日期: 2026-04-10

用途：
  - 从 memory/projects.md 和 memory/people.md 读取当前项目状态
  - 计算 KPI 进度（财政资金目标 400万）
  - 生成结构化 KPI 看板输出
"""

import os
import re
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".openclaw/workspace/memory"

# ─────────────────────────────────────────────
# 核心 KPI 配置（硬编码，与 Skill 文档保持一致）
# ─────────────────────────────────────────────
KPI_CONFIG = {
    "财政资金目标_万": 400,
    "省级项目权重": 0.12,
    "CNAS认证状态": "进行中",
    "专利年度目标": 5,
}

# 人员分工
STAFF = {
    "张思聪": {
        "title": "博士后研究员",
        "主责": ["省级项目申报", "专利技术方案撰写"],
        "kpi权重": "12%",
    },
    "武林": {
        "title": "研究员助理",
        "主责": ["制度建设", "知产/资质/审计支撑"],
        "kpi权重": "支撑",
    },
    "terlivy": {
        "title": "工作站实际负责人",
        "主责": ["整体统筹", "CTO汇报"],
        "kpi权重": "主指标",
    },
}


def load_memory_file(filename: str) -> str:
    """加载 memory 目录下指定文件"""
    path = MEMORY_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def parse_projects() -> dict:
    """解析 projects.md，提取各项目状态"""
    content = load_memory_file("projects.md")
    projects = {}

    # 匹配形如 "## X. 项目名" 的章节
    pattern = re.compile(r"^##?\s*(\d+)\.?\s*(.+?)\n(.+?)(?=^##|\Z)", re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(content):
        name = m.group(2).strip()
        body = m.group(3).strip()

        status = ""
        if "状态" in body:
            st_match = re.search(r"状态[：:]\s*(.+)", body)
            if st_match:
                status = st_match.group(1).strip()

        projects[name] = {"status": status, "raw": body[:200]}

    return projects


def parse_people() -> dict:
    """解析 people.md，提取人员信息"""
    content = load_memory_file("people.md")
    # 简化：返回包含博士后工作站相关人员的子集
    return STAFF  # 人员配置已在全局定义


def estimate_fiscal_progress() -> dict:
    """
    根据 projects.md 内容估算财政资金进度
    逻辑：检查是否有明确的"财政资金"条目，否则用项目数量估算
    """
    projects = parse_projects()
    # 实际项目中未记录具体资金数字，此处按项目完成度估算
    # 假设每个活跃项目平均贡献约 50 万（需根据实际情况调整）
    active_count = sum(
        1 for p in projects.values() if "进行中" in p["status"] or "开发中" in p["status"]
    )
    estimated = min(active_count * 50, 400)  # 上限 400 万
    return {
        "estimated_万": estimated,
        "active_projects": active_count,
        "note": "估算值，实际以财务数据为准",
    }


def generate_kpi_report() -> str:
    """生成完整 KPI 看板报告"""
    fiscal = estimate_fiscal_progress()
    projects = parse_projects()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    target = KPI_CONFIG["财政资金目标_万"]
    current = fiscal["estimated_万"]
    gap = target - current
    pct = (current / target) * 100 if target > 0 else 0

    # 风险等级判断
    if pct >= 75:
        risk = "🟢 低"
    elif pct >= 40:
        risk = "🟡 中"
    else:
        risk = "🔴 高"

    # 专利统计（projects.md 中的知产条目）
    ip_project = projects.get("知识产权转化 - 专利撰写", {})
    ip_status = ip_project.get("status", "未知")

    lines = [
        f"【工作站 KPI 看板】  _{now}_",
        "=" * 42,
        f"📊 财政资金目标：{target} 万",
        f"   当前估算：{current} 万（{pct:.1f}%）",
        f"   差距：-{gap} 万",
        f"   风险等级：{risk}",
        "=" * 42,
        f"📌 省级项目申报：进行中（张思聪负责，权重12%）",
        f"📌 CNAS 认证：{KPI_CONFIG['CNAS认证状态']}",
        f"📌 专利产出：{ip_status}",
        "=" * 42,
        "【人员分工】",
    ]

    for name, info in STAFF.items():
        lines.append(f"  👤 {name}（{info['title']}）")
        for duty in info["主责"]:
            lines.append(f"     · {duty}")

    lines += [
        "=" * 42,
        "【活跃项目】",
    ]

    for name, info in projects.items():
        lines.append(f"  · {name}：{info['status']}")

    lines += [
        "=" * 42,
        f"⚠️  财政资金为估算值，实际以财务系统数据为准",
        f"⚠️  本看板由 kpi_dashboard.py 自动生成",
    ]

    return "\n".join(lines)


def main():
    print(generate_kpi_report())


if __name__ == "__main__":
    main()
