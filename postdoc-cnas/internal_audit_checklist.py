#!/usr/bin/env python3
"""
CNAS 内审检查表生成器
按 CNAS-CL01:2018 要素生成内审检查表
"""

import sys
import json
from datetime import datetime


AUDIT_ELEMENTS = {
    "4.1 组织": [
        ("法律地位", "是否具有明确的法律地位，能够承担法律责任"),
        ("公正性声明", "是否发布公正性声明，承诺保持公正"),
        ("组织架构", "组织架构是否清晰，职责是否明确"),
    ],
    "4.4 外部信息/采购": [
        ("供应商评价", "是否对关键供应商进行评价和监控"),
        ("采购流程", "采购流程是否符合规定"),
    ],
    "5.1 人员": [
        ("人员资质", "所有人员是否具备必要的教育和培训"),
        ("授权", "关键岗位是否有明确授权"),
        ("人员记录", "人员档案是否完整（学历、培训、授权记录）"),
        ("培训计划", "是否制定年度培训计划"),
    ],
    "5.2 设备": [
        ("设备管理", "设备是否受控（唯一编号、标识）"),
        ("期间核查", "是否按计划进行期间核查"),
        ("维护记录", "是否保存设备维护记录"),
        ("溯源", "需要溯源的设备是否溯源至国家基准"),
    ],
    "5.3 设施和环境条件": [
        ("环境监控", "对环境有要求的区域是否监控并记录"),
        ("安全", "是否配备必要的安全设施"),
        ("区域隔离", "不同区域是否有有效的隔离措施"),
    ],
    "5.4 测量溯源": [
        ("溯源计划", "是否制定测量溯源计划"),
        ("校准证书", "校准证书是否在有效期内"),
        ("参考物质", "参考物质是否可溯源"),
    ],
    "5.5 外部提供的产品和服务": [
        ("服务评价", "对外部服务是否定期评价"),
        ("验收准则", "验收准则是否明确"),
    ],
    "6.2 风险和机遇": [
        ("风险评估", "是否识别相关风险和机遇并采取措施"),
        ("应对措施", "应对措施是否实施并有效"),
    ],
    "6.3 变更管理": [
        ("变更控制", "涉及能力的变更是否受控"),
    ],
    "6.4 要求、标书和合同评审": [
        ("合同评审", "合同/协议是否经过评审"),
        ("偏离处理", "对客户要求的偏离是否与客户沟通并确认"),
    ],
    "6.5 方法开发确认": [
        ("方法验证", "非标方法是否经过验证"),
        ("方法选择", "是否使用符合要求的检测方法"),
        ("方法文件", "检测方法是否形成文件（SOP）"),
    ],
    "6.6 测量不确定度": [
        ("MU评估", "是否评估测量不确定度"),
        ("MU评定记录", "不确定度评定是否符合规定"),
    ],
    "6.7 样品处置": [
        ("样品标识", "样品是否有唯一性标识"),
        ("样品接收", "样品接收是否记录，状态是否确认"),
        ("样品储存", "样品储存条件是否符合要求"),
        ("样品归还/处置", "样品处置是否符合规定"),
    ],
    "7.1 质量控制": [
        ("质控计划", "是否制定质量控制计划"),
        ("质控实施", "质量控制措施是否按计划实施"),
        ("质控结果评价", "质控结果是否进行评价"),
    ],
    "7.2 比对和能力验证": [
        ("室间比对", "是否参加室间比对"),
        ("能力验证", "是否参加能力验证"),
        ("结果利用", "比对/能力验证结果是否分析利用"),
    ],
    "7.3 文件控制": [
        ("文件批准", "文件是否经过授权人员批准"),
        ("文件受控", "受控文件是否有受控标识"),
        ("文件更改", "文件更改是否经过评审和批准"),
    ],
    "7.4 记录控制": [
        ("记录完整", "记录是否完整、清晰"),
        ("记录修改", "记录修改是否可追溯"),
        ("保密", "是否对客户信息和所有权实施保密"),
    ],
    "7.5 不符合工作控制": [
        ("不符合识别", "不符合工作是否被及时识别"),
        ("NCR处理", "不符合项是否按程序处理"),
        ("整改验证", "整改措施是否有效验证"),
    ],
    "7.7 数据信息管理": [
        ("数据完整性", "数据是否完整、可追溯"),
        ("计算核查", "关键数据是否经过两人独立核查"),
        ("信息系统", "信息系统是否经过验证/确认"),
    ],
    "8.2 申诉投诉": [
        ("申诉处理", "是否建立申诉投诉处理程序"),
        ("记录保存", "申诉投诉记录是否保存"),
    ],
    "8.3 纠正措施": [
        ("根本原因分析", "不符合项是否进行根本原因分析"),
        ("纠正措施", "纠正措施是否有效"),
    ],
    "8.4 内部审核": [
        ("内审计划", "是否制定年度内审计划"),
        ("内审实施", "内审是否按计划实施"),
        ("内审记录", "内审记录是否完整"),
        ("不符合整改", "内审不符合项是否关闭"),
    ],
    "8.5 管理评审": [
        ("管理评审输入", "管理评审输入是否充分"),
        ("评审输出", "管理评审输出是否包含改进决策"),
    ],
}


def generate_audit_checklist(audit_date: str = None, auditor: str = None) -> dict:
    """生成内审检查表"""
    checklist = {
        "内审日期": audit_date or datetime.now().strftime("%Y-%m-%d"),
        "内审员": auditor or "待指定",
        "生成时间": datetime.now().strftime("%Y-%m-%d"),
        "要素": []
    }
    
    for element, items in AUDIT_ELEMENTS.items():
        section = {
            "要素编号": element,
            "检查项": []
        }
        for item_name, desc in items:
            section["检查项"].append({
                "检查内容": item_name,
                "检查方法": "查文件/记录/现场观察",
                "判定依据": desc,
                "状态": "⭕ 待查",
                "发现": "",
                "不符合项编号": ""
            })
        checklist["要素"].append(section)
    
    return checklist


def print_checklist_summary(checklist: dict):
    """打印检查表摘要"""
    print("=" * 70)
    print(f"🔍 CNAS 内审检查表")
    print(f"   内审日期：{checklist['内审日期']}")
    print(f"   内审员：{checklist['内审员']}")
    print(f"   生成时间：{checklist['生成时间']}")
    print("=" * 70)
    
    total = 0
    for section in checklist["要素"]:
        print(f"\n【{section['要素编号']}】")
        for item in section["检查项"]:
            total += 1
            status_icon = item["状态"]
            finding = f" → {item['发现']}" if item["发现"] else ""
            ncr = f" [NCR:{item['不符合项编号']}]" if item["不符合项编号"] else ""
            print(f"  {status_icon} {item['检查内容']}{finding}{ncr}")
    
    print("\n" + "=" * 70)
    print(f"共 {total} 个检查项")
    print("状态：⭕待查  ✅符合  ⚠️观察项  ❌不符合")
    print("=" * 70)


def interactive_audit(checklist: dict):
    """交互式内审"""
    print("\n开始交互式内审（直接回车跳过）：\n")
    
    total = 0
    compliant = 0
    observation = 0
    non_conform = 0
    
    for section in checklist["要素"]:
        print(f"\n{'='*50}")
        print(f"【{section['要素编号']}】")
        for item in section["检查项"]:
            total += 1
            print(f"\n  检查内容：{item['检查内容']}")
            print(f"  判定依据：{item['判定依据']}")
            user_input = input(f"  结果（1=✅ 2=⚠️ 3=❌ 回车=⭕）：").strip()
            
            if user_input == "1":
                item["状态"] = "✅ 符合"
                compliant += 1
            elif user_input == "2":
                item["状态"] = "⚠️ 观察项"
                item["发现"] = input("  请输入观察描述：")
                observation += 1
            elif user_input == "3":
                item["状态"] = "❌ 不符合"
                item["发现"] = input("  请输入不符合描述：")
                item["不符合项编号"] = input("  不符合项编号（如NCR-001）：") or f"NCR-{total:03d}"
                non_conform += 1
            else:
                item["状态"] = "⭕ 待查"
    
    print(f"\n\n{'='*50}")
    print("📊 内审结果汇总")
    print(f"  ✅ 符合：{compliant}")
    print(f"  ⚠️ 观察项：{observation}")
    print(f"  ❌ 不符合：{non_conform}")
    print(f"  ⭕ 待查：{total - compliant - observation - non_conform}")
    
    return checklist


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            print("CNAS-CL01:2018 内审要素清单：")
            for element in AUDIT_ELEMENTS:
                print(f"  {element}")
        elif sys.argv[1] == "--summary":
            checklist = generate_audit_checklist()
            print_checklist_summary(checklist)
        elif sys.argv[1] == "--audit":
            auditor = input("内审员姓名：") or "待指定"
            audit_date = input("内审日期（YYYY-MM-DD）：") or datetime.now().strftime("%Y-%m-%d")
            checklist = generate_audit_checklist(audit_date, auditor)
            checklist = interactive_audit(checklist)
            print_checklist_summary(checklist)
            save = input("\n是否保存为JSON？(y/n)：")
            if save.lower() == 'y':
                filename = f"cnas_audit_{audit_date}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(checklist, f, ensure_ascii=False, indent=2)
                print(f"✅ 已保存：{filename}")
        else:
            checklist = generate_audit_checklist()
            print_checklist_summary(checklist)
    else:
        checklist = generate_audit_checklist()
        print_checklist_summary(checklist)
        print("\n用法：")
        print("  python3 internal_audit_checklist.py --summary   # 摘要模式")
        print("  python3 internal_audit_checklist.py --audit     # 交互式内审")
        print("  python3 internal_audit_checklist.py --list      # 要素清单")


if __name__ == "__main__":
    main()
