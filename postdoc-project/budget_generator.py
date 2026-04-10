#!/usr/bin/env python3
"""
项目预算生成器
根据政府科研项目标准预算科目生成预算表
"""

import sys
import json
from datetime import datetime


BUDGET_ITEMS = [
    {
        "科目": "一、设备费",
        "子项": ["① 购置设备费", "② 试制设备费", "③ 设备改造与租赁费"],
        "说明": "单台套≥10万元的设备需单独说明",
        "比例参考": "一般≤20%"
    },
    {
        "科目": "二、材料费",
        "子项": ["原材料", "试剂", "药品", "实验动物", "其他消耗品"],
        "说明": "需列出主要材料清单及计算依据",
        "比例参考": "根据研究内容而定"
    },
    {
        "科目": "三、测试化验加工费",
        "子项": ["外单位测试", "化验", "加工"],
        "说明": "需附合同或协议",
        "比例参考": "理工科一般较高"
    },
    {
        "科目": "四、燃料动力费",
        "子项": ["水、电、气、燃料"],
        "说明": "按实际使用量估算",
        "比例参考": "一般≤5%"
    },
    {
        "科目": "五、差旅费",
        "子项": ["交通费", "住宿费", "伙食补助", "公杂费"],
        "说明": "按财务制度标准计算",
        "比例参考": "一般≤10%"
    },
    {
        "科目": "六、会议费",
        "子项": ["会议室租赁", "专家费", "资料费"],
        "说明": "会议次数和规模需合理",
        "比例参考": "一般≤5%"
    },
    {
        "科目": "七、国际合作与交流费",
        "子项": ["交通费", "住宿费", "注册费"],
        "说明": "需说明必要性",
        "比例参考": "一般≤10%"
    },
    {
        "科目": "八、出版/文献/信息传播费",
        "子项": ["论文发表", "专著出版", "软件购置", "文献检索"],
        "说明": "与研究相关",
        "比例参考": "一般≤5%"
    },
    {
        "科目": "九、专家咨询费",
        "子项": ["校内专家", "校外专家"],
        "说明": "高级专业技术职称≤500元/人天",
        "比例参考": "一般≤10%"
    },
    {
        "科目": "十、劳务费",
        "子项": ["研究生", "博士后", "临时工"],
        "说明": "不设上限，按实际支出",
        "比例参考": "根据项目需要"
    },
    {
        "科目": "十一、其他支出",
        "子项": ["项目验收费用", "专利维护费"],
        "说明": "需说明用途和计算依据",
        "比例参考": "一般≤5%"
    }
]


def generate_budget_template(total_amount: float, project_type: str = "省级科技计划") -> dict:
    """生成预算模板"""
    
    result = {
        "项目总经费": f"{total_amount:.2f} 万元",
        "项目类型": project_type,
        "生成时间": datetime.now().strftime("%Y-%m-%d"),
        "预算科目": []
    }
    
    # 按比例分配参考值（可根据实际情况调整）
    proportions = {
        "一、设备费": 0.15,
        "二、材料费": 0.20,
        "三、测试化验加工费": 0.15,
        "四、燃料动力费": 0.03,
        "五、差旅费": 0.08,
        "六、会议费": 0.05,
        "七、国际合作与交流费": 0.05,
        "八、出版/文献/信息传播费": 0.04,
        "九、专家咨询费": 0.08,
        "十、劳务费": 0.12,
        "十一、其他支出": 0.05
    }
    
    total_check = 0
    for item in BUDGET_ITEMS:
        name = item["科目"]
        prop = proportions.get(name, 0)
        amount = total_amount * prop
        total_check += amount
        
        budget_entry = {
            "科目": name,
            "金额(万元)": round(amount, 2),
            "占比": f"{prop*100:.1f}%",
            "子项": item["子项"],
            "说明": item["说明"],
            "计算依据": "",
            "形式审查": "⚠️ 需填写"
        }
        result["预算科目"].append(budget_entry)
    
    result["金额核对"] = {
        "合计": round(total_check, 2),
        "与总经费差额": round(total_amount - total_check, 2),
        "状态": "✅ 正常" if abs(total_amount - total_check) < 0.01 else "⚠️ 需调整"
    }
    
    return result


def print_budget_report(budget: dict):
    """打印预算报告"""
    print("=" * 70)
    print(f"📊 项目预算表")
    print(f"   项目类型：{budget['项目类型']}")
    print(f"   总经费：{budget['项目总经费']}")
    print(f"   生成时间：{budget['生成时间']}")
    print("=" * 70)
    
    print(f"\n{'科目':<30} {'金额(万元)':<12} {'占比':<8} {'形式审查'}")
    print("-" * 70)
    
    for item in budget["预算科目"]:
        name = item["科目"].replace("一、", "").replace("二、", "").replace("三、", "").replace("四、", "").replace("五、", "").replace("六、", "").replace("七、", "").replace("八、", "").replace("九、", "").replace("十、", "").replace("十一、", "")
        print(f"{item['科目']:<28} {item['金额(万元)']:<12} {item['占比']:<8} {item['形式审查']}")
    
    print("-" * 70)
    核对 = budget["金额核对"]
    print(f"{'合计':<28} {核对['合计']:<12} {'100.0%':<8} {核对['状态']}")
    print("=" * 70)
    
    print("\n📝 使用说明：")
    print("1. 根据实际研究内容调整各科目金额")
    print("2. 每个科目需填写详细的「计算依据」")
    print("3. 单台套≥10万元的设备需单独说明")
    print("4. 劳务费不设上限，但需与研究任务匹配")
    print("5. 设备费+材料费+测试化验加工费一般不超过直接经费的70%")


def interactive_mode():
    """交互模式"""
    print("🔧 项目预算生成器 - 交互模式")
    print("-" * 40)
    
    try:
        total = float(input("请输入项目总经费（万元）："))
    except ValueError:
        print("❌ 无效数字，请重新运行")
        sys.exit(1)
    
    project_type = input("请输入项目类型（默认：省级科技计划）：") or "省级科技计划"
    
    budget = generate_budget_template(total, project_type)
    print()
    print_budget_report(budget)
    
    save = input("\n是否保存为JSON文件？(y/n)：")
    if save.lower() == 'y':
        filename = f"budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(budget, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存至：{filename}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        try:
            total = float(sys.argv[1])
            project_type = sys.argv[2] if len(sys.argv) > 2 else "省级科技计划"
            budget = generate_budget_template(total, project_type)
            print_budget_report(budget)
        except ValueError:
            print("用法：python3 budget_generator.py <总经费(万元)> [项目类型]")
            sys.exit(1)
    else:
        interactive_mode()
