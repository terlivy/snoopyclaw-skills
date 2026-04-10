#!/usr/bin/env python3
"""
申报材料完整性检查工具
根据不同项目类型，生成形式审查清单
"""

import sys
import json
from datetime import datetime


CHECKLIST_TEMPLATES = {
    "省级科技计划": {
        "基础信息": [
            ("项目名称", "是否填写完整、无错别字"),
            ("项目负责人", "是否与申报资格匹配"),
            ("申报单位", "单位名称/代码是否正确"),
            ("申报日期", "是否在申报期内"),
        ],
        "申请书正文": [
            ("一、项目意义/立项依据", "字数/格式是否符合要求"),
            ("二、研究内容/主要创新点", "创新点是否突出"),
            ("三、研究方案/技术路线", "技术路线是否清晰可行"),
            ("四、研究基础", "是否突出相关研究积累"),
            ("五、预期成果", "指标是否可量化"),
            ("六、经费预算", "预算说明是否完整"),
        ],
        "附件材料": [
            ("可行性报告", "是否需要单独附上"),
            ("查重报告", "是否在有效期内（一般1年内）"),
            ("伦理审批", "涉及人体/动物的实验是否已审批"),
            ("合作协议", "合作单位是否有协议"),
        ],
        "形式审查": [
            ("签名/盖章", "是否需要负责人签字/单位盖章"),
            ("份数/格式", "纸质版份数、是否需要电子版"),
            ("回避声明", "项目负责人/成员是否存在回避情形"),
        ]
    },
    "博士后基金": {
        "基础信息": [
            ("流动站名称", "是否与实际流动站一致"),
            ("合作导师", "是否具有博士后指导资格"),
            ("进站时间/预期出站时间", "时间是否符合基金要求"),
        ],
        "申请书正文": [
            ("一、摘要（中英文）", "字数是否符合要求"),
            ("二、研究意义", "创新性是否突出"),
            ("三、研究内容与方法", "方案是否具体可行"),
            ("四、研究基础", "是否展示相关积累"),
            ("五、预期目标", "目标是否明确可考核"),
        ],
        "附件材料": [
            ("博士学位证书", "是否在有效期内"),
            ("进站批复", "是否已办理进站手续"),
            ("导师推荐信", "是否按模板签署"),
        ]
    },
    "NSFC申请书": {
        "基础信息": [
            ("项目名称", "是否准确反映研究内容"),
            ("申请代码", "代码选择是否准确"),
            ("项目类型", "选择是否正确（面上/青年等）"),
        ],
        "申请书正文": [
            ("一、立项依据与研究内容", "参考文献是否新颖"),
            ("二、研究方案", "技术路线是否详细"),
            ("三、研究基础", "预实验/相关成果是否充分"),
            ("四、可行性分析", "条件/团队是否具备"),
        ],
        "附件材料": [
            ("代表作", "是否满足限项要求"),
            ("其他附件", "需要时是否齐全"),
        ],
        "形式审查": [
            ("伦理审查", "涉及人体/动物的实验"),
            ("生物安全", "病原微生物相关实验"),
            ("知情同意", "涉及人体标本/数据"),
        ]
    }
}


def generate_checklist(project_type: str) -> dict:
    """生成检查清单"""
    template = CHECKLIST_TEMPLATES.get(project_type, CHECKLIST_TEMPLATES["省级科技计划"])
    
    checklist = {
        "项目类型": project_type,
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "检查项": []
    }
    
    for section, items in template.items():
        for item_name, check_point in items:
            checklist["检查项"].append({
                "分类": section,
                "项目": item_name,
                "审查要点": check_point,
                "状态": "⭕ 待检查"
            })
    
    return checklist


def print_checklist(checklist: dict):
    """打印检查清单"""
    print("=" * 70)
    print(f"📋 申报材料形式审查清单")
    print(f"   项目类型：{checklist['项目类型']}")
    print(f"   生成时间：{checklist['生成时间']}")
    print("=" * 70)
    
    current_section = None
    for item in checklist["检查项"]:
        if item["分类"] != current_section:
            current_section = item["分类"]
            print(f"\n【{current_section}】")
            print(f"  {'项目':<30} {'审查要点':<20} {'状态'}")
            print(f"  {'-'*60}")
        
        print(f"  {item['项目']:<28} {item['审查要点']:<18} {item['状态']}")
    
    print("\n" + "=" * 70)
    print("状态说明：")
    print("  ⭕ 待检查 — 尚未核实")
    print("  ✅ 符合   — 已确认无误")
    print("  ⚠️ 需补充 — 需要补充材料")
    print("  ❌ 缺失   — 材料缺失或不符")
    print("=" * 70)


def interactive_mode():
    """交互模式"""
    print("🔧 申报材料完整性检查工具 - 交互模式")
    print("-" * 40)
    
    print("\n请选择项目类型：")
    for i, name in enumerate(CHECKLIST_TEMPLATES.keys(), 1):
        print(f"  {i}. {name}")
    print(f"  {len(CHECKLIST_TEMPLATES)+1}. 其他（自定义）")
    
    try:
        choice = int(input("\n请输入序号："))
    except ValueError:
        print("❌ 无效输入")
        sys.exit(1)
    
    if 1 <= choice <= len(CHECKLIST_TEMPLATES):
        project_type = list(CHECKLIST_TEMPLATES.keys())[choice-1]
    else:
        project_type = input("请输入项目类型名称：") or "省级科技计划"
    
    checklist = generate_checklist(project_type)
    print()
    print_checklist(checklist)
    
    # 可选：逐项更新状态
    update = input("\n是否逐项更新状态？(y/n)：")
    if update.lower() == 'y':
        print("\n请输入每项状态（直接回车保持 ⭕ 待检查，输入 ✅/⚠️/❌）：")
        for i, item in enumerate(checklist["检查项"], 1):
            status_map = {"1": "✅ 符合", "2": "⚠️ 需补充", "3": "❌ 缺失"}
            print(f"\n[{i}/{len(checklist['检查项'])}] {item['分类']} - {item['项目']}")
            print(f"  审查要点：{item['审查要点']}")
            user_input = input(f"  当前：{item['状态']} → 输入 1=✅ 2=⚠️ 3=❌ 回车=⭕：")
            if user_input in status_map:
                item["状态"] = status_map[user_input]
        
        print("\n" + "=" * 70)
        print_checklist(checklist)
        
        save = input("\n是否保存为JSON文件？(y/n)：")
        if save.lower() == 'y':
            filename = f"checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(checklist, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存至：{filename}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        project_type = sys.argv[1]
        checklist = generate_checklist(project_type)
        print_checklist(checklist)
    else:
        interactive_mode()
