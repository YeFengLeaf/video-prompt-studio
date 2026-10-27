#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest.py — 回归自测：模板 + 样例 + 方言隔离 + 占位符。

用法：python selftest.py
退出码：0 = 全通过；1 = 有失败。
兼容 Python 3.9+，仅标准库。
"""
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import check_package  # noqa: E402
import check_templates  # noqa: E402

RESULT = []


def record(name, ok, detail=""):
    RESULT.append((name, ok, detail))
    print("%-4s %-42s %s" % ("PASS" if ok else "FAIL", name, detail))


def test_templates():
    code, files = check_templates.run(ROOT)
    record("模板结构与占位符", code == 0, "%d 个模板" % len(files))


def test_examples():
    ex_dir = ROOT / "assets" / "examples"
    outputs = sorted(ex_dir.glob("*/output*.md"))
    if not outputs:
        record("样例存在", False, "没有 assets/examples/*/output.md")
        return
    for out in outputs:
        text = out.read_text("utf-8")
        model = check_package.parse_model(text, None)
        r = check_package.check(text, model)
        fails = [i for i in r.items if i[1] == "FAIL"]
        record("样例 %s" % out.parent.name, not fails,
               "%s · PASS %d / WARN %d" % (model, r.count("PASS"), r.count("WARN")))
        for cid, _, detail in fails:
            print("       ✗ %s %s" % (cid, detail))


def test_syntax_isolation():
    """把 Seedance 样例按 Veo 校验，应报 S-08。"""
    sample = ROOT / "assets" / "examples" / "01_single_story" / "output.md"
    if not sample.exists():
        record("方言隔离（负向）", False, "缺样例 01")
        return
    text = sample.read_text("utf-8")
    r = check_package.check(text, "veo")
    ids = [i for i in r.items if i[0] == "S-08" and i[1] == "FAIL"]
    record("方言隔离（负向）", bool(ids), "Veo 校验应拒绝 @ImageN")


def test_placeholder_guard():
    """含未填占位符的包必须被 S-10 拦下。"""
    sample = ROOT / "assets" / "examples" / "01_single_story" / "output.md"
    if not sample.exists():
        record("占位符拦截（负向）", False, "缺样例 01")
        return
    text = sample.read_text("utf-8")
    text = text.replace("声音：", "声音：{{unfilled_slot}}", 1)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        tmp = Path(f.name)
    try:
        r = check_package.check(tmp.read_text("utf-8"), "seedance-2.0")
        ids = [i for i in r.items if i[0] == "S-10" and i[1] == "FAIL"]
        record("占位符拦截（负向）", bool(ids), "残留 {{…}} 应 FAIL")
    finally:
        tmp.unlink(missing_ok=True)


def test_model_switch_keeps_story():
    """同一分镜换模型：事实层与分镜表不变，只改执行层。"""
    a = ROOT / "assets" / "examples" / "01_single_story" / "output.md"
    d = ROOT / "assets" / "examples" / "04_model_switch"
    candidates = sorted(d.glob("output-*.md")) if d.exists() else []
    if not (a.exists() and candidates):
        record("换模型只改执行层", False, "缺 01 或 04 样例")
        return
    b = candidates[0]
    ta, tb = a.read_text("utf-8"), b.read_text("utf-8")
    sa, sb = check_package.section_map(ta), check_package.section_map(tb)

    def norm(s):
        return re.sub(r"\s+", "", s or "")

    def shot_rows(sec):
        return [norm(line) for line in (sec or "").splitlines() if line.strip().startswith("| S")]

    same_facts = norm(sa.get(2, "")) == norm(sb.get(2, ""))
    same_shots = shot_rows(sa.get(3)) == shot_rows(sb.get(3))
    prompt_a = check_package.extract_prompt_block(sa.get(4, ""))
    prompt_b = check_package.extract_prompt_block(sb.get(4, ""))
    different_prompt = bool(prompt_a and prompt_b and prompt_a != prompt_b)
    ok = same_facts and same_shots and different_prompt
    record("换模型只改执行层", ok,
           "事实层同=%s 分镜同=%s 提示词异=%s（%s）" % (
               same_facts, same_shots, different_prompt, b.name))


def test_negative_cases():
    """负向：只测 check_package.py 实际执行的检查，不虚构它没有的检查。

    - MiniMax H3：脚本不校验时间码格式，只豁免 S-09（时间码可进提示词）；
      但 S-08 语法隔离仍然适用，提示词里出现 @Image1 必须 FAIL。
    - Seedance 2.5：脚本不执行 30s 模型上限，只校验分镜合计 = 参数节标称
      （S-03）；35s 分镜配 30s 标称必须 FAIL，上限本身靠人工复核。
    """
    # MiniMax：取 04 样例，只把提示词块里的 <Picture 1> 换成 @Image1
    mm = (ROOT / "assets" / "examples" / "04_model_switch" / "output-minimax.md").read_text("utf-8")
    mm_bad = mm.replace("<Picture 1> 提供女孩身份", "@Image1 提供女孩身份", 1)
    r = check_package.check(mm_bad, "minimax-h3")
    s08 = [(s, d) for i, s, d in r.items if i == "S-08"]
    record("MiniMax 时间码不豁免语法隔离（负向）",
           bool(s08) and s08[0][0] == "FAIL" and mm_bad != mm,
           s08[0][1] if s08 else "?")

    # Seedance 2.5：分镜合计 35s，参数节标称 30s
    base = (ROOT / "assets" / "examples" / "01_single_story" / "output.md").read_text("utf-8")
    over = base.replace("目标模型：Seedance 2.0", "目标模型：Seedance 2.5", 1)
    over = over.replace("| S01-01 | 0–5s |", "| S01-01 | 0–12s |")
    over = over.replace("| S01-02 | 5–10s |", "| S01-02 | 12–24s |")
    over = over.replace("| S01-03 | 10–15s |", "| S01-03 | 24–35s |")
    over = over.replace("| 时长 | 15s |", "| 时长 | 30s |")
    r2 = check_package.check(over, "seedance-2.5")
    s03 = [(s, d) for i, s, d in r2.items if i == "S-03"]
    record("Seedance 2.5 超长未对账（负向）",
           bool(s03) and s03[0][0] == "FAIL",
           s03[0][1] if s03 else "?")


def test_checker_regressions():
    """QC 回归：多段、重复引用、块外占位符、错误镜号、5 列台词表。"""
    base = (ROOT / "assets" / "examples" / "01_single_story" / "output.md").read_text("utf-8")

    def one(text, cid, model="seedance-2.0"):
        r = check_package.check(text, model)
        return [(s, d) for i, s, d in r.items if i == cid]

    # 多段：S02 从 0s 重新开始，不应被判成断点
    multi = base.replace("| 时长 | 15s |", "| 时长 | 25s |")
    multi = multi.replace("\n\n## 4. 提示词", "\n"
                          "| S02-01 | 0–5s | 全景 | 平视 | 35mm | 固定 | 第二段建立 | — | 雨声 | 街道空 → 人入画 |\n"
                          "| S02-02 | 5–10s | 近景 | 平视 | 85mm | 固定 | 第二段落点 | — | 雨声 | 人入画 → 停住 |\n\n"
                          "## 4. 提示词", 1)
    s02 = one(multi, "S-02")
    s03 = one(multi, "S-03")
    record("多段包时间轴", bool(s02) and s02[0][0] == "PASS" and s03[0][0] == "PASS",
           "%s / %s" % (s02[0][0] if s02 else "?", s03[0][0] if s03 else "?"))

    # 同一素材引用两次，不应被算成两份资产
    dup = base.replace("，不传递背景。", "；@Image1 提供雨衣轮廓。", 1)
    s07 = one(dup, "S-07")
    record("重复引用不误判", bool(s07) and s07[0][0] == "PASS", s07[0][1] if s07 else "?")

    # 第 1 节残留占位符，必须 FAIL
    ph = base.replace("- 时长 15s：", "- 时长 {{duration}}：", 1)
    s10 = one(ph, "S-10")
    record("块外占位符拦截", bool(s10) and s10[0][0] == "FAIL", s10[0][1] if s10 else "?")

    # 作用镜头写了不存在的镜号，必须 FAIL
    bad = base.replace("| 全部 | 背景、光线 | @Image1 |", "| S09-99 | 背景、光线 | @Image1 |")
    s11 = one(bad, "S-11")
    record("错误作用镜头拦截", bool(s11) and s11[0][0] == "FAIL", s11[0][1] if s11 else "?")

    # 5 列台词表（没有“结论”列）仍应识别台词
    t3 = (ROOT / "assets" / "examples" / "03_script_dialogue" / "output.md").read_text("utf-8")
    t3 = t3.replace("| 说话人 | 原文（逐字） | 语气 | 字数 | 预算秒数 | 结论 |",
                    "| 说话人 | 原文（逐字） | 语气 | 字数 | 预算秒数 |")
    t3 = t3.replace("|---|---|---|---|---:|---:|---|", "|---|---|---|---|---:|")
    t3 = t3.replace("| 11 | 2.5 | 可执行 |", "| 11 | 2.5 |")
    t3 = t3.replace("| 6 | 1.5 | 可执行 |", "| 6 | 1.5 |")
    s05 = one(t3, "S-05", "seedance-2.5")
    record("5 列台词表", bool(s05) and s05[0][0] == "PASS" and "2 条台词" in s05[0][1],
           s05[0][1] if s05 else "?")


def test_check_switch():
    """check_switch.py：故事层逐字一致判 PASS，§2 改一字判 FAIL。"""
    import subprocess
    a = ROOT / "assets" / "examples" / "01_single_story" / "output.md"
    b = ROOT / "assets" / "examples" / "04_model_switch" / "output-minimax.md"
    if not (a.exists() and b.exists()):
        record("切换验收脚本", False, "缺 01 或 04 样例")
        return
    r = subprocess.run([sys.executable, str(HERE / "check_switch.py"), str(a), str(b)],
                       capture_output=True, text=True, encoding="utf-8")
    ok_pair = r.returncode == 0
    text = a.read_text("utf-8")
    if "## 2. 事实层" not in text:
        record("切换验收脚本", False, "01 样例无 §2 标题")
        return
    text = text.replace("## 2. 事实层", "## 2. 事实层\n- 多余事实：切换验收负向用例", 1)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        tmp = Path(f.name)
    try:
        r2 = subprocess.run([sys.executable, str(HERE / "check_switch.py"), str(tmp), str(b)],
                            capture_output=True, text=True, encoding="utf-8")
        ok_neg = r2.returncode == 1
    finally:
        tmp.unlink(missing_ok=True)
    record("切换验收脚本", ok_pair and ok_neg,
           "正例 exit %d · 改 §2 后 exit %d" % (r.returncode, r2.returncode))


def test_quality_gate_cases():
    """quality_gate.py --cases：20 例一致率 ≥19/20（case 09 已知未调）。"""
    import subprocess
    cases = HERE / "fixtures" / "quality_gate_cases.md"
    if not cases.exists():
        record("质量门禁 20 例", False, "缺 fixtures/quality_gate_cases.md")
        return
    r = subprocess.run([sys.executable, str(HERE / "quality_gate.py"), "--cases", str(cases)],
                       capture_output=True, text=True, encoding="utf-8")
    m = re.search(r"agreement: (\d+)/(\d+)", r.stdout)
    ok = r.returncode == 0 and bool(m) and int(m.group(1)) >= 19 and m.group(2) == "20"
    record("质量门禁 20 例", ok, m.group(0) if m else (r.stdout + r.stderr)[-160:])


def test_dialect_converter_core():
    """dialect_converter：全部模型故事核逐字保留 + 未填参数一律占位符。"""
    import dialect_converter
    core = "女孩站在便利店门口，@Image1 负责女孩身份。\n她把车票折成纸鹤。"
    ok = True
    bad = ""
    for name in sorted(dialect_converter.MODELS):
        out = dialect_converter.convert(core, name)
        m = re.search(r"## Story core \(kept verbatim, do not edit\)\n\n(.*?)\n\n## Target-model structure",
                      out, re.S)
        kept = bool(m) and m.group(1) == core
        placeholders = "[UNVERIFIED: to fill in]" in out
        if not (kept and placeholders):
            ok = False
            bad = name
            break
    record("方言转换故事核逐字", ok,
           "%d 个模型" % len(dialect_converter.MODELS) if ok else "失败于 %s" % bad)


def main():
    print("=" * 68)
    print("video-prompt-studio 自测")
    print("=" * 68)
    test_templates()
    test_examples()
    test_syntax_isolation()
    test_placeholder_guard()
    test_model_switch_keeps_story()
    test_checker_regressions()
    test_negative_cases()
    test_check_switch()
    test_quality_gate_cases()
    test_dialect_converter_core()
    fails = [r for r in RESULT if not r[1]]
    print("\n汇总：%d 项，失败 %d 项" % (len(RESULT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
