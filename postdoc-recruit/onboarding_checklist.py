#!/usr/bin/env python3
"""
博士后入职办理清单
生成进站手续完整清单，支持交互式状态更新
"""

import sys
import json
from datetime import datetime, timedelta


ONBOARDING_STEPS = {
    "进站前准备": [
        ("研究方向确认", "与导师确认研究课题和计划"),
        ("名额申请", "确认当年博士后招收名额"),
        ("体检", "一般体检 + 特殊项目（如有）"),
        ("原单位离职证明", "上一份工作的离职证明"),
        ("档案调入", "人事档案转移至工作站"),
    ],
    "进站手续": [
        ("进站申请表", "填写并由导师签字"),
        ("博士后研究人员登记表", "中国博士后网站在线填报"),
        ("学历学位证书", "博士学历+学位证书原件及复印件"),
        ("身份证明", "身份证原件及复印件"),
        ("政治审查表", "无犯罪记录证明"),
        ("学术委员会审批", "工作站学术委员会审批"),
        ("工作站负责人审批", "terslivy签字"),
    ],
    "合同签订": [
        ("博士后工作协议", "明确研究任务、出站条件"),
        ("劳动合同", "与工作站签订"),
        ("保密协议", "知识产权保护"),
        ("竞业限制（如有）", "特殊情况需单独签署"),
    ],
    "薪酬与福利": [
        ("工资核定", "人事部门核定工资级别"),
        ("社保开户", "五险一金办理"),
        ("公积金", "缴存基数确认"),
        ("住房补贴", "如有宿舍或货币补贴"),
        ("工资卡办理", "指定银行"),
    ],
    "日常安排": [
        ("工位分配", "实验室/办公室工位"),
        ("门禁权限", "门禁卡/指纹录入"),
        ("邮件/账号", "工作站邮箱开通"),
        ("OA系统", "办公自动化系统账号"),
        ("党团组织", "党组织关系转入（如有）"),
    ],
    "进站后一周内": [
        ("课题组介绍", "组内成员、研究方向介绍"),
        ("实验室安全培训", "安全操作规程"),
        ("研究计划汇报", "向导师汇报研究计划"),
        ("设备使用培训", "所需设备操作培训"),
    ],
}


def generate_checklist(name: str, start_date: str = None) -> dict:
    """生成入职清单"""
    checklist = {
        "博士后姓名": name,
        "预计进站日期": start_date or "待定",
        "生成时间": datetime.now().strftime("%Y-%m-%d"),
        "状态": "⭕ 待办理",
        "阶段": []
    }
    
    for section, items in ONBOARDING_STEPS.items():
        phase = {
            "阶段": section,
            "项目": []
        }
        for item_name, desc in items:
            phase["项目"].append({
                "名称": item_name,
                "说明": desc,
                "状态": "⭕ 待办理",
                "完成日期": None,
                "备注": ""
            })
        checklist["阶段"].append(phase)
    
    return checklist


def print_checklist(checklist: dict):
    """打印清单"""
    print("=" * 70)
    print(f"📋 博士后入职办理清单")
    print(f"   博士后：{checklist['博士后姓名']}")
    print(f"   预计进站：{checklist['预计进站日期']}")
    print(f"   生成时间：{checklist['生成时间']}")
    print("=" * 70)
    
    total = 0
    completed = 0
    
    for phase in checklist["阶段"]:
        print(f"\n【{phase['阶段']}】")
        for item in phase["项目"]:
            total += 1
            if item["状态"] == "✅ 完成":
                completed += 1
            print(f"  {item['状态']} {item['名称']}")
            if item.get("完成日期"):
                print(f"       完成于：{item['完成日期']}")
            print(f"       {item['说明']}")
    
    print("\n" + "=" * 70)
    print(f"进度：{completed}/{total} 项已完成（{completed*100//total if total > 0 else 0}%）")
    print("状态说明：⭕待办理  ✅完成  ⚠️进行中  ❌缺失")
    print("=" * 70)


def interactive_update(checklist: dict):
    """交互式更新状态"""
    print("\n请逐项更新状态（直接回车保持 ⭕ 待办理）：")
    print("输入 1=✅完成  2=⚠️进行中  3=❌缺失\n")
    
    item_num = 0
    for phase in checklist["阶段"]:
        for item in phase["项目"]:
            item_num += 1
            print(f"[{item_num}] {phase['阶段']} - {item['名称']}")
            user_input = input(f"    {item['说明']} → ")
            
            if user_input == "1":
                item["状态"] = "✅ 完成"
                item["完成日期"] = datetime.now().strftime("%Y-%m-%d")
            elif user_input == "2":
                item["状态"] = "⚠️ 进行中"
            elif user_input == "3":
                item["状态"] = "❌ 缺失"
    
    return checklist


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        # 更新模式
        name = input("博士后姓名：") or "待定"
        start_date = input("预计进站日期（YYYY-MM-DD）：") or None
        checklist = generate_checklist(name, start_date)
        checklist = interactive_update(checklist)
        print_checklist(checklist)
        
        save = input("\n是否保存为JSON？(y/n)：")
        if save.lower() == 'y':
            filename = f"onboarding_{name}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(checklist, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存：{filename}")
    
    elif len(sys.argv) > 1 and sys.argv[1] == "--generate":
        # 生成模式
        name = sys.argv[2] if len(sys.argv) > 2 else "博士后"
        start_date = sys.argv[3] if len(sys.argv) > 3 else None
        checklist = generate_checklist(name, start_date)
        print_checklist(checklist)
    
    else:
        # 交互模式
        print("🔧 博士后入职办理清单 - 交互模式")
        print("-" * 40)
        name = input("博士后姓名：")
        start_date = input("预计进站日期（YYYY-MM-DD，可直接回车）：") or None
        
        checklist = generate_checklist(name, start_date)
        print_checklist(checklist)
        
        update = input("\n是否更新各项状态？(y/n)：")
        if update.lower() == 'y':
            checklist = interactive_update(checklist)
            print_checklist(checklist)
        
        save = input("\n是否保存为JSON？(y/n)：")
        if save.lower() == 'y':
            filename = f"onboarding_{name}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(checklist, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存：{filename}")


if __name__ == "__main__":
    main()
