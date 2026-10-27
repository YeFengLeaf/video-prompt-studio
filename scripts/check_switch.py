#!/usr/bin/env python3
"""check_switch.py — verify story-layer verbatim identity across a model switch.

Compares two production-package .md files (8-section contract):
  §2 事实层 and §3 分镜表 must be identical;
  §4 提示词 and §6 参数节 are execution-layer and are IGNORED
  (their difference is the expected result of a switch).

Comparison rule: text is normalized only for line endings (CRLF -> LF)
and trailing whitespace per line. Any other difference is a failure.
This mirrors Skill check_package.py's section handling; it does not
invent checks the Skill does not perform.

Usage:
    python3 scripts/check_switch.py <package-A.md> <package-B.md>

Exit codes: 0 = PASS, 1 = story layer differs, 2 = file/section error.
Standard library only.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

HEADING_RE = re.compile(r"^## (\d+)\.\s", re.MULTILINE)


def read_sections(path: Path) -> dict[int, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    matches = list(HEADING_RE.finditer(text))
    sections: dict[int, str] = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[match.end():end]
    return sections


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n"))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify §2/§3 story-layer identity across a model switch."
    )
    parser.add_argument("package_a", type=Path)
    parser.add_argument("package_b", type=Path)
    args = parser.parse_args(argv)

    for path in (args.package_a, args.package_b):
        if not path.is_file():
            print(f"ERROR: not a file: {path}", file=sys.stderr)
            return 2

    sa = read_sections(args.package_a)
    sb = read_sections(args.package_b)
    missing = [n for n in (2, 3) if n not in sa or n not in sb]
    if missing:
        print(f"ERROR: missing §2/§3 in one of the packages (sections found: "
              f"A={sorted(sa)}, B={sorted(sb)})", file=sys.stderr)
        return 2

    ok = True
    for num, name in ((2, "事实层"), (3, "分镜表")):
        raw_a, raw_b = sa[num], sb[num]
        norm_a, norm_b = normalize(raw_a), normalize(raw_b)
        if norm_a == norm_b:
            raw_note = "（逐字相同，含空白）" if raw_a == raw_b else "（内容相同，仅行尾空白/换行符差异）"
            print(f"§{num} {name}：IDENTICAL{raw_note}")
        else:
            ok = False
            print(f"§{num} {name}：DIFFERENT — 故事层不一致：")
            a_lines, b_lines = norm_a.split("\n"), norm_b.split("\n")
            for i, (la, lb) in enumerate(zip(a_lines, b_lines)):
                if la != lb:
                    print(f"  行 {i + 1} A: {la!r}")
                    print(f"  行 {i + 1} B: {lb!r}")
            if len(a_lines) != len(b_lines):
                print(f"  行数不同：A={len(a_lines)} B={len(b_lines)}")

    # §4 difference is expected (execution layer recompiled); report only.
    if 4 in sa and 4 in sb:
        same_prompt = normalize(sa[4]) == normalize(sb[4])
        print(f"§4 提示词：{'IDENTICAL（未重编译，请核查）' if same_prompt else 'DIFFERENT（预期内，执行层已重编译）'}")

    if ok:
        print("结论：PASS — 故事层逐字一致，切换验收第 1 条通过")
        return 0
    print("结论：FAIL — 故事层不一致，切换验收第 1 条未通过", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
