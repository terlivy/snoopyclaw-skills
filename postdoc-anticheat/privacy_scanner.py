#!/usr/bin/env python3
"""
隐私风险扫描器
扫描文本/文件中的隐私泄露风险
"""

import sys
import re
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class RiskFinding:
    """风险发现"""
    category: str
    pattern: str
    matched: str
    line: int
    severity: str  # 高危/中危/低危
    suggestion: str


RISK_PATTERNS = [
    # 高危
    (r'\b\d{15,18}\b', "身份证号", "🔴高危", "立即脱敏，使用***替代"),
    (r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', "银行卡号", "🔴高危", "立即脱敏，勿在文档中出现"),
    (r'(?i)(password|pwd|密码)[\s:=]+\S+', "密码泄露", "🔴高危", "删除并重置相关账号"),
    (r'(?i)(api[_-]?key|secret|密钥)[\s:=]+\S+', "API密钥", "🔴高危", "立即轮换密钥，勿提交到仓库"),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "邮箱地址", "🔴高危", "替换为[邮箱]或泛化地址"),
    (r'\b1[3-9]\d{9}\b', "手机号", "🔴高危", "替换为[手机号]"),
    (r'\b\d{3}[-\s]?\d{4}[-\s]?\d{4}\b', "座机/短手机", "🟡中危", "检查是否为真实号码"),
    # 中危
    (r'(?i)(内部|保密|不对外|仅内部).{0,50}(公开|发布|共享)', "内部信息泄露意图", "🟡中危", "确认该信息是否可对外"),
    (r'(?i)(评估|判断|结论).{0,20}(不行|不合格|差|差劲)', "内部评价语", "🟡中危", "内部评价勿出现在交付文档中"),
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "IP地址", "🟡中危", "内网IP需脱敏，外网IP确认是否可公开"),
    (r'(?i)(真实|具体).(预算|工资|薪酬|收入|金额).{0,30}(元|万|%)', "财务数据", "🟡中危", "使用比例或范围替代具体数字"),
    (r'([\u4e00-\u9fa5]{2,4})[\s,，](博士|硕士|教授|研究员|工程师)', "真实人名+职称", "🟡中危", "替换为职称或代号"),
    # 低危
    (r'20\d{2}[-年]\d{1,2}[-月]\d{1,2}[日]?', "具体日期", "🟢低危", "日期一般可保留，视场景判断"),
    (r'(?i)(优势|劣势|缺点|问题).{0,20}(明显|突出)', "模糊评价语", "🟢低危", "评估是否构成内部信息"),
]


@dataclass
class ScanResult:
    file: str
    total_lines: int
    findings: List[RiskFinding] = field(default_factory=list)
    risk_level: str = "✅安全"
    
    def __post_init__(self):
        if self.findings:
            if any(f.severity == "🔴高危" for f in self.findings):
                self.risk_level = "🔴高危"
            elif any(f.severity == "🟡中危" for f in self.findings):
                self.risk_level = "🟡中危"
            else:
                self.risk_level = "🟢低危"


def scan_text(text: str, source_name: str = "文本") -> ScanResult:
    """扫描文本"""
    lines = text.split('\n')
    result = ScanResult(file=source_name, total_lines=len(lines))
    
    for line_num, line in enumerate(lines, 1):
        for pattern, desc, severity, suggestion in RISK_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                # 过滤一些误报
                matched_text = match.group()
                if desc == "具体日期" and "2026" in matched_text:
                    continue  # 年代太远，忽略
                if desc == "邮箱地址" and ("example" in matched_text or "test" in matched_text.lower()):
                    continue  # 测试邮箱忽略
                
                result.findings.append(RiskFinding(
                    category=desc,
                    pattern=pattern,
                    matched=matched_text[:50] + ("..." if len(matched_text) > 50 else ""),
                    line=line_num,
                    severity=severity,
                    suggestion=suggestion
                ))
    
    return result


def scan_file(filepath: str) -> ScanResult:
    """扫描文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return scan_text(content, filepath)
    except FileNotFoundError:
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        sys.exit(1)


def print_result(result: ScanResult, show_lines: bool = True):
    """打印扫描结果"""
    print("=" * 70)
    print(f"🔍 隐私风险扫描报告")
    print(f"   文件：{result.file}")
    print(f"   行数：{result.total_lines}")
    print(f"   风险等级：{result.risk_level}")
    print("=" * 70)
    
    if not result.findings:
        print("\n✅ 未发现隐私风险")
        return
    
    # 按严重程度分组
    by_severity = {"🔴高危": [], "🟡中危": [], "🟢低危": []}
    for f in result.findings:
        by_severity[f.severity].append(f)
    
    for severity in ["🔴高危", "🟡中危", "🟢低危"]:
        items = by_severity[severity]
        if not items:
            continue
        
        print(f"\n【{severity}】共 {len(items)} 项")
        print("-" * 70)
        
        for item in items:
            if show_lines:
                print(f"  📍 第{item.line}行：[{item.category}]")
            else:
                print(f"  📍 [{item.category}]")
            print(f"     内容：{item.matched}")
            print(f"     建议：{item.suggestion}")
    
    print("\n" + "=" * 70)
    print("处理建议：")
    print("  1. 高危：必须处理后再交付")
    print("  2. 中危：确认上下文，判断是否脱敏")
    print("  3. 低危：视场景决定，可保留")
    print("=" * 70)


def interactive_scan():
    """交互式扫描"""
    print("🔧 隐私风险扫描器 - 交互模式")
    print("-" * 40)
    
    filepath = input("文件路径：").strip()
    if not filepath:
        print("❌ 路径不能为空")
        return
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filepath}")
        return
    
    result = scan_file(filepath)
    print()
    print_result(result)


def desensitize_text(text: str) -> str:
    """简单的脱敏处理"""
    result = text
    
    # 手机号
    result = re.sub(r'\b1[3-9]\d{9}\b', '[手机号]', result)
    # 邮箱
    result = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[邮箱]', result)
    # 身份证号
    result = re.sub(r'\b\d{15,18}\b', '[身份证号]', result)
    # 银行卡号
    result = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[银行卡号]', result)
    # API Key
    result = re.sub(r'(?i)(api[_-]?key|secret)[\s:=]+\S+', r'\1:[API_KEY]', result)
    
    return result


def desensitize_file(filepath: str, output_path: str = None):
    """脱敏文件"""
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    desensitized = desensitize_text(content)
    
    if not output_path:
        output_path = filepath + ".desensitized"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(desensitized)
    
    print(f"✅ 脱敏版本已保存：{output_path}")
    return output_path


def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "--scan":
            if len(sys.argv) > 2:
                result = scan_file(sys.argv[2])
            else:
                interactive_scan()
                return
            print_result(result)
        
        elif cmd == "--scan-text":
            text = " ".join(sys.argv[2:])
            result = scan_text(text, "命令行输入")
            print_result(result)
        
        elif cmd == "--desensitize":
            if len(sys.argv) > 2:
                desensitize_file(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
            else:
                filepath = input("文件路径：").strip()
                desensitize_file(filepath)
        
        elif cmd == "--help":
            print("""用法：
  python3 privacy_scanner.py --scan <文件路径>     扫描文件
  python3 privacy_scanner.py --scan-text <文本>    扫描文本
  python3 privacy_scanner.py --desensitize <文件>  脱敏文件
  python3 privacy_scanner.py --interactive         交互模式""")
        else:
            interactive_scan()
    else:
        interactive_scan()


if __name__ == "__main__":
    main()
