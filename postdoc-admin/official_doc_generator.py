#!/usr/bin/env python3
"""
行政公文生成器
支持通知、请示、报告、会议纪要等公文类型
符合 GB/T 9704-2012 格式规范
"""

import sys
import json
from datetime import datetime


DOC_TEMPLATES = {
    "通知": """【通知模板】

各单位：

{content}

{additional}

附件：{attachments}

{date}
""",

    "请示": """【请示模板】

{to_unit}：

{content}

{additional}

妥否，请批示。

{date}
""",

    "报告": """【报告模板】

{to_unit}：

{content}

{additional}

特此报告。

{date}
""",

    "会议纪要": """【会议纪要模板】

会议纪要

时间：{time}
地点：{location}
主持：{host}
出席：{attendees}
列席：{observers}
记录：{recorder}

一、会议议题
{topic}

二、会议内容
{content}

三、会议决定
{decisions}

四、工作安排
{work_items}

记录人：{recorder}    审核人：{host}    印发日期：{date}
""",

    "周报": """【工作周报模板】

{week_info}

一、本周工作完成情况
{completed}

二、下周工作计划
{planned}

三、问题与建议
{issues}

四、数据统计（如有）
{statistics}

汇报人：{reporter}
""",

    "月报": """【月度工作汇报模板】

{month_info}

一、本月工作完成情况
{completed}

二、重点工作进展
{highlights}

三、数据统计
{statistics}

四、下月工作计划
{planned}

五、问题与建议
{issues}

汇报人：{reporter}    审核人：{approver}
"""
}


def generate_doc(doc_type: str, params: dict) -> str:
    """生成公文"""
    if doc_type not in DOC_TEMPLATES:
        available = "、".join(DOC_TEMPLATES.keys())
        raise ValueError(f"不支持的公文类型。可用类型：{available}")
    
    template = DOC_TEMPLATES[doc_type]
    
    # 填充默认值
    defaults = {
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "attachments": "无",
        "additional": "",
        "time": "",
        "location": "",
        "host": "",
        "attendees": "",
        "observers": "",
        "recorder": "",
        "topic": "",
        "content": "",
        "decisions": "",
        "work_items": "",
        "week_info": "",
        "month_info": "",
        "completed": "",
        "planned": "",
        "issues": "",
        "statistics": "",
        "reporter": "",
        "approver": "",
        "highlights": "",
        "to_unit": "",
    }
    
    for k, v in defaults.items():
        if k not in params:
            params[k] = v
    
    try:
        return template.format(**params)
    except KeyError as e:
        raise ValueError(f"缺少必要参数：{e}")


def interactive_mode():
    """交互模式"""
    print("🔧 行政公文生成器 - 交互模式")
    print("-" * 40)
    
    print("\n请选择公文类型：")
    for i, name in enumerate(DOC_TEMPLATES.keys(), 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("\n请输入序号："))
    except ValueError:
        print("❌ 无效输入")
        sys.exit(1)
    
    doc_types = list(DOC_TEMPLATES.keys())
    if choice < 1 or choice > len(doc_types):
        print("❌ 无效选择")
        sys.exit(1)
    
    doc_type = doc_types[choice - 1]
    print(f"\n📄 生成类型：{doc_type}")
    
    params = {}
    
    # 通用参数
    params["content"] = input("\n主要内容（必填）：")
    if not params["content"]:
        print("❌ 内容不能为空")
        sys.exit(1)
    
    params["date"] = input("日期（默认今天）：") or datetime.now().strftime("%Y年%m月%d日")
    
    if doc_type == "通知":
        params["additional"] = input("补充说明（可选）：")
        params["attachments"] = input("附件（可选）：") or "无"
    
    elif doc_type == "请示" or doc_type == "报告":
        params["to_unit"] = input("主送单位（必填）：")
        params["additional"] = input("补充说明（可选）：")
    
    elif doc_type == "会议纪要":
        params["time"] = input("会议时间：")
        params["location"] = input("会议地点：")
        params["host"] = input("主持人：")
        params["attendees"] = input("出席人员（用顿号分隔）：")
        params["observers"] = input("列席人员（用顿号分隔）：")
        params["recorder"] = input("记录人：")
        params["topic"] = input("会议议题：")
        params["decisions"] = input("会议决定（用换行分隔）：")
        params["work_items"] = input("工作安排（格式：事项-负责人-完成时间）：")
    
    elif doc_type == "周报":
        params["week_info"] = input("周次（如：2026年第15周）：")
        params["completed"] = input("本周完成工作（用换行分隔）：")
        params["planned"] = input("下周计划（用换行分隔）：")
        params["issues"] = input("问题与建议（可选）：")
        params["reporter"] = input("汇报人：")
    
    elif doc_type == "月报":
        params["month_info"] = input("月份（如：2026年4月）：")
        params["completed"] = input("本月完成工作（用换行分隔）：")
        params["highlights"] = input("重点工作进展：")
        params["statistics"] = input("数据统计（如有）：")
        params["planned"] = input("下月工作计划：")
        params["issues"] = input("问题与建议（可选）：")
        params["reporter"] = input("汇报人：")
        params["approver"] = input("审核人：")
    
    print("\n" + "=" * 70)
    print("📄 生成结果：")
    print("=" * 70)
    
    try:
        result = generate_doc(doc_type, params)
        print(result)
        
        save = input("\n是否保存为文件？(y/n)：")
        if save.lower() == 'y':
            filename = f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ 已保存至：{filename}")
    except ValueError as e:
        print(f"❌ 生成失败：{e}")


def stats_mode():
    """数据统计模式"""
    print("🔧 博士后工作站数据统计")
    print("-" * 40)
    
    # 读取记忆系统数据（如果有）
    stats = {
        "统计日期": datetime.now().strftime("%Y-%m-%d"),
        "在站博士后": "?",
        "在研项目": "?",
        "本年新增专利": "?",
        "本年发表论文": "?",
        "财政资金执行率": "?",
        "CNAS进度": "?"
    }
    
    print("\n📊 工作站数据统计（请手动补充或从记忆系统读取）：")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    print("\n提示：可通过读取 memory/projects.md 和 memory/people.md 获取最新数据")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stats":
            stats_mode()
        elif sys.argv[1] == "--list":
            print("支持的公文类型：")
            for i, name in enumerate(DOC_TEMPLATES.keys(), 1):
                print(f"  {i}. {name}")
        else:
            doc_type = sys.argv[1]
            try:
                result = generate_doc(doc_type, {})
                print(result)
            except ValueError as e:
                print(f"❌ {e}")
                print("用法：python3 official_doc_generator.py [通知|请示|报告|会议纪要|周报|月报]")
    else:
        interactive_mode()
