#!/usr/bin/env python3
"""
政策情报监控工具
定时巡检政策网站，推送 relevant 通知
"""

import sys
import json
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class PolicyItem:
    """政策条目"""
    title: str
    source: str
    url: str
    publish_date: str
    deadline: Optional[str]
    category: str  # 基金申报/认证管理/人事政策/综合
    summary: str
    importance: str  # 高/中/低
    raw_tags: List[str]


# 模拟的政策数据（实际使用时应接入真实数据源）
SAMPLE_POLICIES = [
    PolicyItem(
        title="2026年度博士后创新人才支持计划申报通知",
        source="中国博士后网",
        url="http://www.chinapostdoctor.org.cn",
        publish_date="2026-04-01",
        deadline="2026-05-15",
        category="基金申报",
        summary="面向 top 高校/科研院所博士后，每年2次申请机会，最高资助60万元/年",
        importance="高",
        raw_tags=["博士后", "创新人才", "资助"]
    ),
    PolicyItem(
        title="国家自然科学基金委2026年度项目指南发布",
        source="NSFC",
        url="https://www.nsfc.gov.cn",
        publish_date="2026-03-15",
        deadline="2026-03-20",
        category="基金申报",
        summary="2026年NSFC项目申请已截止，集中接收期结束",
        importance="中",
        raw_tags=["NSFC", "自然科学基金", "项目指南"]
    ),
    PolicyItem(
        title="CNAS-CL01:2024 认可准则换版说明",
        source="CNAS",
        url="https://www.cnas.org.cn",
        publish_date="2026-02-20",
        deadline=None,
        category="认证管理",
        summary="CNAS-CL01:2024将于2026年7月1日实施，旧版标准过渡期至2026年12月31日",
        importance="高",
        raw_tags=["CNAS", "认可准则", "换版"]
    ),
    PolicyItem(
        title="博士后研究人员日常经费标准调整",
        source="人社部",
        url="http://www.mohrss.gov.cn",
        publish_date="2026-01-10",
        deadline=None,
        category="人事政策",
        summary="日常经费标准由每年8万元提高至10万元，适用于2026年进站人员",
        importance="中",
        raw_tags=["博士后", "日常经费", "补贴"]
    ),
    PolicyItem(
        title="某省2026年度第三批科技计划项目申报",
        source="某省科技厅",
        url="http://kjt.xxxx.gov.cn",
        publish_date="2026-04-05",
        deadline="2026-05-01",
        category="基金申报",
        summary="省级科技计划项目，单项最高200万元，重点支持人工智能/新能源领域",
        importance="中",
        raw_tags=["省级", "科技计划", "项目申报"]
    ),
]


def filter_policies(policies: List[PolicyItem], 
                   categories: List[str] = None,
                   days_ahead: int = 30,
                   keyword_filter: str = None) -> List[PolicyItem]:
    """过滤政策"""
    result = []
    
    now = datetime.now()
    deadline_threshold = now + timedelta(days=days_ahead)
    
    for p in policies:
        # 分类过滤
        if categories and p.category not in categories:
            continue
        
        # 关键词过滤
        if keyword_filter:
            text = f"{p.title} {p.summary} {' '.join(p.raw_tags)}"
            if keyword_filter.lower() not in text.lower():
                continue
        
        # 截止日期过滤（只显示近期截止的）
        if p.deadline:
            try:
                deadline = datetime.strptime(p.deadline, "%Y-%m-%d")
                if deadline < now:
                    continue  # 已过期
                if deadline > deadline_threshold:
                    continue  # 太远
            except ValueError:
                pass
        
        result.append(p)
    
    return result


def format_policy_message(policy: PolicyItem) -> str:
    """格式化政策消息"""
    deadline_str = f"\n⏰ 截止日期：{policy.deadline}" if policy.deadline else ""
    
    days_left = ""
    if policy.deadline:
        try:
            days = (datetime.strptime(policy.deadline, "%Y-%m-%d") - datetime.now()).days
            if days >= 0:
                days_left = f"（还剩 {days} 天）"
        except ValueError:
            pass
    
    importance_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(policy.importance, "⚪")
    
    return f"""{importance_icon} **{policy.title}**
- 来源：{policy.source}
- 类别：{policy.category}
- 发布：{policy.publish_date}{deadline_str} {days_left}
- 摘要：{policy.summary}
- 链接：{policy.url}"""


def print_dashboard(policies: List[PolicyItem]):
    """打印政策仪表板"""
    print("=" * 70)
    print("📡 博士后工作站政策情报 - 仪表板")
    print(f"   查询时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   监控来源：博士后基金 / NSFC / CNAS / 省级政策")
    print("=" * 70)
    
    if not policies:
        print("\n暂无 relevant 政策（可能在申报间隔期）")
        return
    
    # 按分类分组
    categories = {}
    for p in policies:
        if p.category not in categories:
            categories[p.category] = []
        categories[p.category].append(p)
    
    for cat, items in categories.items():
        print(f"\n【{cat}】")
        for p in items:
            deadline_str = f" ⏰{p.deadline}" if p.deadline else ""
            importance_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(p.importance, "⚪")
            print(f"  {importance_icon} {p.title}{deadline_str}")
    
    print("\n" + "-" * 70)
    print("📋 详情：")
    for p in policies:
        print(format_policy_message(p))
        print()


def interactive_mode():
    """交互模式"""
    print("🔧 政策情报监控 - 交互模式")
    print("-" * 40)
    
    print("\n请选择监控类别（可多选，用逗号分隔）：")
    categories = {
        "1": "基金申报",
        "2": "认证管理",
        "3": "人事政策",
        "4": "综合"
    }
    for k, v in categories.items():
        print(f"  {k}. {v}")
    print("  0. 全部")
    
    choice = input("\n选择：") or "0"
    
    selected = []
    if "0" in choice:
        selected = []
    else:
        for c in choice.split(","):
            c = c.strip()
            if c in categories:
                selected.append(categories[c])
    
    keyword = input("关键词过滤（直接回车跳过）：").strip() or None
    days = input("截止日期范围（天，默认30）：").strip()
    days_ahead = int(days) if days.isdigit() else 30
    
    # 实际使用时，这里应调用真实爬虫
    # 目前使用示例数据
    print("\n⚠️  使用示例数据（实际接入请配置真实数据源）\n")
    
    policies = filter_policies(SAMPLE_POLICIES, selected, days_ahead, keyword)
    print_dashboard(policies)
    
    save = input("\n是否保存为JSON？(y/n)：")
    if save.lower() == 'y':
        filename = f"policy_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = [asdict(p) for p in policies]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存：{filename}")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dashboard":
            policies = filter_policies(SAMPLE_POLICIES)
            print_dashboard(policies)
        elif sys.argv[1] == "--urgent":
            # 紧急截止（7天内）
            policies = filter_policies(SAMPLE_POLICIES, days_ahead=7)
            print_dashboard(policies)
        else:
            interactive_mode()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
