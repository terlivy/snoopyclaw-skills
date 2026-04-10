#!/usr/bin/env python3
"""
novelty_checker.py - 专利新颖性/创造性辅助判断工具
版本: v1.0
日期: 2026-04-10

用途：
  - 对用户提供的技术方案进行新颖性/创造性初步分析
  - 基于结构化问题引导，帮助识别创新点和潜在风险
  - 提示常见的对比文件检索方向

使用方式：
  python3 novelty_checker.py --interactive
  python3 novelty_checker.py "技术方案描述"
"""

import sys
from datetime import datetime

VERSION = "v1.0"


def parse_args():
    for i, arg in enumerate(sys.argv):
        if not arg.startswith("-"):
            return " ".join(sys.argv[i:])
    return None


NOVELTY_QUESTIONS = [
    {
        "id": 1,
        "question": "该方案要解决的技术问题是什么？",
        "purpose": "明确技术问题有助于判断创造性",
    },
    {
        "id": 2,
        "question": "该方案的核心创新点（即区别于现有技术的特征）是什么？",
        "purpose": "识别创造性贡献点",
    },
    {
        "id": 3,
        "question": "该技术特征是否在现有技术中被公开过？（自行检索或凭知识判断）",
        "purpose": "新颖性初步判断",
    },
    {
        "id": 4,
        "question": "该技术特征是否属于本领域技术人员的公知常识？",
        "purpose": "排除公知常识性特征",
    },
    {
        "id": 5,
        "question": "该方案是否产生了预料不到的技术效果？",
        "purpose": "创造性提升的重要指标",
    },
]

CREATIVITY_SCORES = {
    "问题": {"描述": "技术问题的新颖程度", "权重": 0.15},
    "创新点清晰度": {"描述": "核心创新点是否明确可辨", "权重": 0.25},
    "非显而易见性": {"描述": "是否非显而易见", "权重": 0.30},
    "技术效果": {"描述": "技术效果的显著性", "权重": 0.20},
    "可专利性": {"描述": "整体可专利性评估", "权重": 0.10},
}


def evaluate_novelty(scheme_desc: str = "") -> str:
    """生成新颖性/创造性分析报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = [
        f"# 专利新颖性/创造性分析报告",
        f"**生成时间**：{now}",
        f"**版本**：{VERSION}",
        "",
        "---",
        "",
        "## 一、新颖性分析",
        "",
        "### 判断标准",
        "根据《专利法》第22条，新颖性是指该发明或实用新型不属于现有技术。",
        "",
        "### 分析要点",
        "1. **现有技术检索**：需在专利数据库（CPRS、CNKI、Google Patents等）进行检索",
        "2. **单独对比原则**：每项权利要求需与单篇对比文件进行比较",
        "3. **下位对比**：具体方案落入上位概念时，仍可评述新颖性",
        "",
        "### 初步检索建议",
        "| 检索方向 | 关键词 | 分类号 |",
        "|---------|--------|--------|",
        "| 中文专利 | 技术领域核心词 + 关键技术特征 | IPC主分类 |",
        "| 英文专利 | English keywords + technical features | CPC分类 |",
        "| 论文 | 核心概念 + 应用场景 | CNKI/Google Scholar |",
        "",
        "---",
        "",
        "## 二、创造性分析",
        "",
        "### 判断标准（三步法）",
        "1. 确定最接近的现有技术",
        "2. 识别区别技术特征及其实际解决的技术问题",
        "3. 判断是否显而易见",
        "",
        "### 创造性提升要素",
        "| 要素 | 说明 | 加分 |",
        "|------|------|------|",
        "| 预料不到的技术效果 | 效果超出预期 | +2 |",
        "| 解决了长期未解决的技术问题 | 技术偏见被克服 | +1.5 |",
        "| 多个非显而易见特征的组合 | 1+1>2 | +1 |",
        "| 商业上的成功 | 由技术特征直接导致 | +0.5 |",
        "",
        "---",
        "",
        "## 三、风险提示",
        "",
        "⚠️ **本分析为辅助判断工具，不能替代专业专利检索和专利代理人审核**",
        "",
        "常见驳回理由：",
        "- 区别特征被最接近对比文件公开（缺乏新颖性）",
        "- 区别特征属于公知常识（显而易见）",
        "- 技术效果未在说明书中充分证实",
        "",
        "---",
        "",
        "## 四、建议",
        "",
        "1. **建议进行正式专利检索**后再提交申请",
        "2. **保留研发过程中的实验数据**，用于证明有益效果",
        "3. **技术交底书应详细描述每个技术特征的作用**，便于审查员理解",
        "4. **咨询专利代理人**，获取专业评估意见",
        "",
        f"---\n_本报告由 novelty_checker.py {VERSION} 自动生成_",
    ]

    return "\n".join(report)


def interactive_evaluation():
    """交互式新颖性评估"""
    print("=" * 50)
    print("专利新颖性/创造性辅助评估 - 交互模式")
    print("=" * 50)

    answers = {}
    for q in NOVELTY_QUESTIONS:
        print(f"\n【问题{q['id']}】{q['question']}")
        print(f"目的：{q['purpose']}")
        answers[q['id']] = input("> ").strip()

    return answers


def main():
    desc = parse_args()

    if desc:
        print(f"技术方案：{desc}\n")

    report = evaluate_novelty(desc)
    print(report)

    try:
        save = input("\n是否保存报告？(y/n): ").strip().lower()
        if save == "y":
            from pathlib import Path
            OUTPUT_DIR = Path.home() / "SC-Workspace/MyTasks/知识产权转化-专利撰写"
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_file = OUTPUT_DIR / f"新颖性分析报告_{ts}.md"
            out_file.write_text(report, encoding="utf-8")
            print(f"已保存到：{out_file}")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
