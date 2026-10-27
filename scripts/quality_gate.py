#!/usr/bin/env python3
"""quality_gate.py: prompt quality gate, three tiers BLOCKED / WARN / PASS.

Executable rules (stdlib only). Checks, on a prompt text (or a production
package's section-4 prompt block, extracted the same way check_package.py
does it when --package is used):

  Q1 STYLE LOCK presence      - BLOCKED when no STYLE LOCK / style-lock marker.
  Q2 anchor-role overlap      - BLOCKED on conflicting duties for one reference;
                                WARN when references carry no duty words at all.
  Q3 emotion adjectives       - WARN on 1-2 bare emotion adjectives;
                                BLOCKED on >= 3 distinct ones.
  Q4 parameter leakage        - BLOCKED when resolution / aspect / fps tokens
                                appear inside the prompt (shot-timeline
                                segments such as "0-5s:" are NOT leakage).
  Q5 de-ai countermeasure coverage - counts how many of the B/01 eight defect
                                classes have at least one countermeasure
                                keyword present; WARN when <= 3 covered.

Tier rule (documented, no hidden weights):
  BLOCKED if any of Q1 / Q2-conflict / Q3>=3 / Q4 fires;
  else WARN if Q5 coverage <= 3, or Q2-no-duty, or Q3 1-2 hits;
  else PASS (coverage >= 4 and no other warning).

Usage:
    python3 quality_gate.py --prompt prompt.txt [--json]
    python3 quality_gate.py --package package.md [--json]
    python3 quality_gate.py --cases scripts/fixtures/quality_gate_cases.md
The --cases mode parses the case file format (see that file) and prints the
per-case tier, the expected tier, and the agreement rate.
"""

import argparse
import json
import re
import sys
from pathlib import Path

STYLE_LOCK_MARKERS = [
    r"STYLE\s*LOCK", r"Style\s*Lock", r"style\s*lock",
    r"风格锁", r"风格锁定", r"风格锚", r"视觉锚",
]

# Bare emotion adjectives (B/03 banned list + close equivalents). A hit counts
# only when the word stands alone as an emotion label; FACS / body-action
# phrasing (e.g. "嘴角单侧上扬") is NOT in this list on purpose.
EMOTION_ADJECTIVES = [
    "happy", "sad", "excited", "angry", "fearful", "nervous",
    "开心", "难过", "悲伤", "兴奋", "愤怒", "恐惧", "紧张", "快乐",
]

# Parameter tokens that must NOT appear inside the prompt body. Timeline
# segments (e.g. "0-5s:") are stripped before matching.
PARAM_TOKENS = [
    r"\b\d{3,4}p\b", r"\b4K\b", r"\b8K\b", r"\b16:9\b", r"\b9:16\b",
    r"\b\d+\s*fps\b", r"\b\d+\s*FPS\b",
]
TIMELINE_RE = re.compile(r"\d+\s*[–—-]\s*\d+\s*s\s*[：:]", re.I)

# B/01 eight defect classes: countermeasure keywords (at least one hit per
# class counts the class as covered). Keywords are taken from B/01's own
# countermeasure wording; see references/09_去AI感策略库.md.
CLASS_KEYWORDS = {
    "class1_style_stacking": ["拆四层", "四层", "分步叠加", "主体保护", "色彩调色层", "虚化词"],
    "class2_motion": ["生物力学", "时间弧", "节拍", "减词", "动作按节拍"],
    "class3_face": ["FACS", "微表情", "单元素", "皮肤", "纹理词", "降强度"],
    "class4_negation": ["正面状态", "先写", "静止状态", "负面清单", "改正面"],
    "class5_dialogue": ["Dialogue:", "标点", "短句", "口型", "呼吸", "分轮"],
    "class6_light_physics": ["光源方向", "光影", "投影", "物理", "重量", "跟随光源"],
    "class7_identity_refs": ["来源身份", "作用域", "character sheet", "不得传递", "负责"],
    "class8_post_edit": ["后期", "剪辑", "字幕后期", "饱和", "颗粒叠加", "混编"],
}

DUTY_WORDS = ["负责", "锚定", "提供", "不得传递", "只负责"]

def _find_refs(text):
    return sorted(set(re.findall(r"@Image\d+|@Video\d+|@Audio\d+|@Element\d+|@element\d+|<Picture \d+>", text)))


def _duty_conflicts(text):
    """Map each reference token to the duties stated for it in its clause.

    Clauses are split on 。；; and newlines. A clause counts as a duty
    statement for a token when it contains the token AND 负责; the duty is
    the text after 负责 up to the clause end. Two distinct duties for one
    token = conflict.
    """
    duties = {}
    for clause in re.split(r"[。；;\n]", text):
        tokens = re.findall(r"@Image\d+|@Video\d+|@Audio\d+|@Element\d+|@element\d+|<Picture \d+>", clause)
        m = re.search(r"负责\s*(.+)$", clause)
        if tokens and m:
            duty = m.group(1).strip(" ，,、")
            for tok in tokens:
                duties.setdefault(tok, set()).add(duty)
    return {tok: sorted(ds) for tok, ds in duties.items() if len(ds) > 1}


def gate(text):
    """Return (tier, checks) where checks is a list of dicts."""
    checks = []

    # Q1 STYLE LOCK
    if any(re.search(p, text) for p in STYLE_LOCK_MARKERS):
        checks.append({"id": "Q1", "status": "PASS", "detail": "STYLE LOCK marker present"})
        q1_blocked = False
    else:
        checks.append({"id": "Q1", "status": "BLOCKED", "detail": "no STYLE LOCK / style-lock marker"})
        q1_blocked = True

    # Q2 anchor-role overlap
    refs = _find_refs(text)
    conflicts = _duty_conflicts(text)
    if conflicts:
        detail = "; ".join("%s: %s" % (tok, " / ".join(ds)) for tok, ds in conflicts.items())
        checks.append({"id": "Q2", "status": "BLOCKED", "detail": "conflicting duties: " + detail})
        q2 = "BLOCKED"
    elif refs and not any(w in text for w in DUTY_WORDS):
        checks.append({"id": "Q2", "status": "WARN",
                       "detail": "%d reference(s) with no duty words (%s)" % (len(refs), ", ".join(refs))})
        q2 = "WARN"
    elif refs:
        checks.append({"id": "Q2", "status": "PASS", "detail": "%d reference(s), duties stated" % len(refs)})
        q2 = "PASS"
    else:
        checks.append({"id": "Q2", "status": "PASS", "detail": "no references in prompt"})
        q2 = "PASS"

    # Q3 emotion adjectives
    hits = []
    for word in EMOTION_ADJECTIVES:
        if word in text:
            hits.append(word)
    if len(hits) >= 3:
        checks.append({"id": "Q3", "status": "BLOCKED", "detail": ">=3 emotion adjectives: %s" % ", ".join(hits)})
        q3 = "BLOCKED"
    elif hits:
        checks.append({"id": "Q3", "status": "WARN", "detail": "emotion adjective(s): %s (rewrite as FACS / body action)" % ", ".join(hits)})
        q3 = "WARN"
    else:
        checks.append({"id": "Q3", "status": "PASS", "detail": "no bare emotion adjectives"})
        q3 = "PASS"

    # Q4 parameter leakage (timeline segments stripped first)
    scrubbed = TIMELINE_RE.sub("", text)
    leaks = sorted(set(m for pat in PARAM_TOKENS for m in re.findall(pat, scrubbed)))
    if leaks:
        checks.append({"id": "Q4", "status": "BLOCKED", "detail": "parameter token(s) inside prompt: %s" % ", ".join(leaks)})
        q4_blocked = True
    else:
        checks.append({"id": "Q4", "status": "PASS", "detail": "no parameter leakage (timeline segments excluded)"})
        q4_blocked = False

    # Q5 de-ai coverage
    covered = [name for name, kws in CLASS_KEYWORDS.items() if any(kw in text for kw in kws)]
    checks.append({"id": "Q5", "status": "PASS" if len(covered) >= 4 else "WARN",
                   "detail": "%d/8 defect classes covered: %s" % (len(covered), ", ".join(covered) or "none")})
    coverage = len(covered)

    if q1_blocked or q2 == "BLOCKED" or q3 == "BLOCKED" or q4_blocked:
        tier = "BLOCKED"
    elif coverage <= 3 or q2 == "WARN" or q3 == "WARN":
        tier = "WARN"
    else:
        tier = "PASS"
    return tier, checks


def _extract_package_prompt(text):
    """Extract the section-4 prompt block the way check_package.py does."""
    m = re.search(r"```(?:text|txt)?\s*\n(.*?)```", text, re.S | re.I)
    return m.group(1) if m else text


CASE_RE = re.compile(
    r"<!--\s*CASE\s+(\d+)\s+EXPECTED[=:]\s*(BLOCKED|WARN|PASS)\s*-->\s*\n```text\n(.*?)```",
    re.S,
)


def run_cases(path):
    """Parse the cases file, run the gate, print per-case results + agreement."""
    text = Path(path).read_text(encoding="utf-8")
    cases = CASE_RE.findall(text)
    if not cases:
        print("no cases found in %s (expected <!-- CASE N EXPECTED=TIER --> + ```text blocks)" % path, file=sys.stderr)
        return 2
    agree = 0
    for num, expected, prompt in cases:
        tier, checks = gate(prompt)
        ok = tier == expected
        agree += ok
        print("case %s: gate=%s expected=%s %s | %s" % (
            num, tier, expected, "AGREE" if ok else "MISMATCH",
            "; ".join("%s:%s" % (c["id"], c["status"]) for c in checks)))
    print("agreement: %d/%d = %.1f%%" % (agree, len(cases), 100.0 * agree / len(cases)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Prompt quality gate: BLOCKED / WARN / PASS")
    ap.add_argument("--prompt", help="prompt plain-text file")
    ap.add_argument("--package", help="production-package Markdown file (section-4 block is gated)")
    ap.add_argument("--cases", help="cases file (see scripts/fixtures/quality_gate_cases.md)")
    ap.add_argument("--json", action="store_true", help="JSON output (single prompt/package mode)")
    args = ap.parse_args(argv)
    if args.cases:
        return run_cases(args.cases)
    if args.prompt:
        text = Path(args.prompt).read_text(encoding="utf-8")
    elif args.package:
        text = _extract_package_prompt(Path(args.package).read_text(encoding="utf-8"))
    else:
        ap.error("one of --prompt / --package / --cases is required")
    tier, checks = gate(text)
    if args.json:
        print(json.dumps({"tier": tier, "checks": checks}, ensure_ascii=False, indent=2))
    else:
        print("tier: %s" % tier)
        for c in checks:
            print("%s %s: %s" % (c["id"], c["status"], c["detail"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
