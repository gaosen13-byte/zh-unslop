#!/usr/bin/env python3
"""Heuristic checker for common Chinese AI-writing patterns; stdlib only."""

import argparse
import re
import sys
from pathlib import Path

RULES = [
    ("不是…而是…式转折", re.compile(r"不是[^。！？\n]{0,80}而是"), 2),
    ("三连排比", re.compile(r"[^，。！？\n]{1,12}[，、][^，。！？\n]{1,12}[，、][^，。！？\n]{1,12}[。！？]"), 1),
    ("总结套话", re.compile(r"总之|综上所述|总的来说"), 1),
    ("提示套话", re.compile(r"值得一提的是|值得关注的是|令人瞩目的是"), 1),
    ("空泛号召", re.compile(r"让我们"), 1),
    ("空洞升华", re.compile(r"开启(?:了)?无限可能|新的篇章|全新旅程|美好未来|更美好的明天"), 2),
    ("emoji 使用偏多", re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"), 1),
    ("破折号使用偏多", re.compile(r"[—]{1,}|(?:--+)"), 1),
    ("常见职场黑话：赋能", re.compile(r"赋能"), 1),
    ("常见职场黑话：闭环", re.compile(r"闭环"), 1),
    ("常见职场黑话：抓手", re.compile(r"抓手"), 1),
    ("生态/矩阵/布局堆词", re.compile(r"(?:生态|矩阵|布局)"), 1),
    ("空泛程度修饰词", re.compile(r"全面提升|深度(?:分析|融合|挖掘)|系统性地|全方位"), 1),
    ("绕行表达", re.compile(r"在.{1,12}方面(?:有所|得到|实现)?(?:提升|改善|优化)"), 1),
    ("泛化时代开场", re.compile(r"随着.{0,20}(?:不断发展|快速发展|日新月异)"), 1),
    ("替读者下结论", re.compile(r"显而易见|毋庸置疑|不言而喻"), 1),
    ("自我评价式套话", re.compile(r"值得关注|令人瞩目|取得(?:了)?(?:显著|巨大)成就"), 1),
    ("机械列举", re.compile(r"首先.{0,60}其次.{0,60}(?:最后|最终)"), 1),
    ("不说明结果的空泛动词", re.compile(r"助力(?:业务|发展|增长)|推动(?:高质量)?发展|促进(?:业务|发展)"), 1),
]


def sentences(text):
    return [part.strip() for part in re.split(r"(?<=[。！？!?；;])|[\r\n]+", text) if part.strip()]


def main():
    parser = argparse.ArgumentParser(description="检查中文文本中的常见 AI 腔表达（启发式评分）")
    parser.add_argument("file", nargs="?", help="文本文件路径；不填则从 stdin 读取")
    args = parser.parse_args()
    try:
        content = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))

    hits = []
    points = 0
    for sentence in sentences(content):
        reasons = [(label, weight) for label, pattern, weight in RULES if pattern.search(sentence)]
        if reasons:
            hits.append((sentence, reasons))
            points += sum(weight for _, weight in reasons)

    if hits:
        print("命中：")
        for sentence, reasons in hits:
            labels = "、".join(label for label, _ in reasons)
            print(f"- [{labels}] {sentence}")
    else:
        print("未发现常见模式。")
    score = min(100, points * 10)
    print(f"AI 味：{score}/100（启发式估分，越高表示命中越多）")


if __name__ == "__main__":
    main()
