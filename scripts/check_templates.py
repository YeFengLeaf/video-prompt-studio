#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_templates.py — 校验 templates/ 三层模板的结构与占位符完整性。

用法：python check_templates.py [--root <skill 根目录>]
退出码：0 = 全部通过；1 = 有问题。
兼容 Python 3.9+，仅标准库。
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\{\{([a-z0-9_]+)\}\}")
LAYERS = {"base", "styles", "shots"}


def parse_front(text):
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def check_template(path, root):
    errs, warns = [], []
    text = path.read_text("utf-8")
    fm = parse_front(text)
    rel = path.relative_to(root).as_posix()

    for key in ("id", "layer", "useWhen", "models"):
        if not fm.get(key):
            errs.append("frontmatter 缺 %s" % key)

    layer = path.parent.name
    if layer not in LAYERS:
        errs.append("目录层级非法：%s（只允许 base/styles/shots）" % layer)
    if fm.get("layer") and fm["layer"] != layer:
        errs.append("frontmatter layer=%s 与目录 %s 不一致" % (fm["layer"], layer))
    if fm.get("id") and not fm["id"].startswith(layer + "/"):
        errs.append("id 应以 %s/ 开头" % layer)

    blocks = re.findall(r"```text\s*\n(.*?)```", text, re.S)
    if not blocks:
        errs.append("缺少 ```text 提示词骨架")
    else:
        # 取占位符最多的那个块：文首可能还有「结构示意」代码块
        skeleton = max(blocks, key=lambda b: len(PLACEHOLDER_RE.findall(b)))
        found = PLACEHOLDER_RE.findall(skeleton)
        if len(found) < 2:
            errs.append("骨架里的 {{占位符}} 少于 2 个")
        stray = skeleton.replace("{{", "").replace("}}", "")
        if "{" in stray or "}" in stray:
            errs.append("骨架里有不成对的单花括号")
        dup = sorted({x for x in found if found.count(x) > 3})
        if dup:
            warns.append("同一占位符出现超过 3 次：%s" % "、".join(dup))

    if "失败" not in text and "禁止" not in text:
        warns.append("没有「失败风险」或「禁止」段")

    if len(text.splitlines()) < 25:
        warns.append("模板过短（%d 行），可能缺填写规则" % len(text.splitlines()))

    return rel, errs, warns, len(PLACEHOLDER_RE.findall(text))


def run(root):
    root = Path(root)
    tdir = root / "templates"
    if not tdir.exists():
        print("找不到 templates/：%s" % tdir)
        return 2, []
    files = sorted(tdir.rglob("*.md"))
    total_err = total_warn = 0
    total_ph = 0
    by_layer = {}
    print("模板校验：%s\n" % root)
    for f in files:
        rel, errs, warns, ph = check_template(f, root)
        total_ph += ph
        by_layer[f.parent.name] = by_layer.get(f.parent.name, 0) + 1
        status = "FAIL" if errs else ("WARN" if warns else "PASS")
        print("%-4s %-28s 占位符 %2d" % (status, rel, ph))
        for e in errs:
            print("       ✗ %s" % e)
        for w in warns:
            print("       ! %s" % w)
        total_err += len(errs)
        total_warn += len(warns)
    print("\n共 %d 个模板（%s），占位符 %d 个" % (
        len(files), " / ".join("%s %d" % (k, v) for k, v in sorted(by_layer.items())), total_ph))
    print("汇总：错误 %d · 警告 %d" % (total_err, total_warn))
    return (1 if total_err else 0), files


def main(argv=None):
    ap = argparse.ArgumentParser(description="校验模板结构与占位符")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args(argv)
    code, _ = run(args.root)
    return code


if __name__ == "__main__":
    sys.exit(main())
