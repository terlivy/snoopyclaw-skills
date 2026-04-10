#!/usr/bin/env python3
"""
patent_disclosure_generator.py - 专利交底书自动生成器
版本: v1.0
日期: 2026-04-10

用途：
  - 基于用户提供的技术方案描述，自动生成符合标准格式的专利交底书
  - 输出格式：Markdown（可直接转为 Word/PDF）

使用方法：
  python3 patent_disclosure_generator.py "技术方案描述"
  或交互式输入：python3 patent_disclosure_generator.py --interactive
"""

import sys
import re
from datetime import datetime
from pathlib import Path

VERSION = "v1.0"
OUTPUT_PATH = Path.home() / "SC-Workspace/MyTasks/知识产权转化-专利撰写"


def parse_args():
    for i, arg in enumerate(sys.argv):
        if arg == "--interactive":
            return None
        if not arg.startswith("-"):
            return " ".join(sys.argv[i:])
    return None


class PatentDisclosureGenerator:
    """专利交底书生成器"""

    def __init__(self, invention_name="", tech_domain="", bg_tech="",
                 tech_scheme="", beneficial="", drawings="", impl=""):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.invention_name = invention_name
        self.tech_domain = tech_domain
        self.bg_tech = bg_tech
        self.tech_scheme = tech_scheme
        self.beneficial = beneficial
        self.drawings = drawings
        self.impl = impl

    def generate(self) -> str:
        name = self.invention_name or "（发明名称待填写）"
        domain = self.tech_domain or "（技术领域待填写）"
        bg = self.bg_tech or "（背景技术待填写）"
        scheme = self.tech_scheme or "（技术方案待填写）"
        beneficial = self.beneficial or "（有益效果待填写）"
        drawings = self.drawings or "（附图说明待填写）"
        impl = self.impl or "（具体实施方式待填写）"

        claims = self._generate_claims(scheme, name)

        return f"""# 专利交底书

**生成日期**：{self.date}  
**版本**：{VERSION}  
**状态**：初稿（待技术专家审核）

---

## 1. 发明名称

{name}

---

## 2. 技术领域

{domain}

---

## 3. 背景技术（现有技术及其不足）

{bg}

---

## 4. 发明内容

### 4.1 发明目的

（待填写：本发明旨在解决……）

### 4.2 技术方案（核心创新点）

{scheme}

### 4.3 有益效果

{beneficial}

---

## 5. 附图说明

{drawings}

**图1**：整体流程示意图  
**图2**：核心算法/方法步骤图  
**图3**：系统架构图（如有）

---

## 6. 具体实施方式

{impl}

---

## 7. 权利要求书（初稿）

### 独立权利要求

{claims}

### 从属权利要求

（待补充）

---

## 填写说明

| 章节 | 填写要求 | 注意事项 |
|------|---------|---------|
| 发明名称 | ≤26字，简明扼要，体现发明点 | 避免功能性描述 |
| 技术领域 | 具体到二级分类 | 如"人工智能/教育信息化" |
| 背景技术 | 引用最接近现有技术，分析其不足 | 需有针对性 |
| 技术方案 | 需清楚、完整地描述发明 | 覆盖所有实施例 |
| 有益效果 | 定性+定量描述 | 与背景技术不足对应 |
| 权利要求 | 独立+从属结构 | 保护范围层层递进 |

---

_本交底书由 patent_disclosure_generator.py {VERSION} 自动生成_
"""

    def _generate_claims(self, scheme: str, name: str) -> str:
        """从技术方案中提取关键词，生成初步权利要求"""
        features = [f.strip() for f in scheme.split("。") if len(f.strip()) > 10]
        if not features:
            return "(待技术专家根据技术方案撰写)"

        lines = [f"**权利要求1**（独立）：一种{name}，其特征在于：", ""]
        for i, f in enumerate(features[:5], 1):
            lines.append(f"{i}. " + f)
        return "\n".join(lines)


def interactive_mode():
    """交互式收集技术方案信息"""
    print("=" * 50)
    print("专利交底书生成器 - 交互模式")
    print("=" * 50)

    questions = [
        ("发明名称", "invention_name"),
        ("技术领域", "tech_domain"),
        ("背景技术（现有技术及不足）", "bg_tech"),
        ("技术方案（核心创新点）", "tech_scheme"),
        ("有益效果", "beneficial"),
        ("附图说明（可选，直接回车跳过）", "drawings"),
        ("具体实施方式", "impl"),
    ]

    answers = {}
    for question, key in questions:
        print(f"\n【{question}】")
        if key == "drawings":
            print("（直接回车跳过）")
        user_input = input("> ").strip()
        answers[key] = user_input

    return answers


def main():
    desc = parse_args()

    if not desc:
        answers = interactive_mode()
        generator = PatentDisclosureGenerator(**answers)
    else:
        generator = PatentDisclosureGenerator(tech_scheme=desc)

    output = generator.generate()
    print("\n" + "=" * 50)
    print("生成的交底书：")
    print("=" * 50)
    print(output)

    try:
        save = input("\n是否保存到文件？(y/n): ").strip().lower()
        if save == "y":
            OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_file = OUTPUT_PATH / f"交底书_{ts}.md"
            out_file.write_text(output, encoding="utf-8")
            print(f"已保存到：{out_file}")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
