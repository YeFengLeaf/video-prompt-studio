#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_package.py — 校验视频提示词生产包的结构不变量（S-01…S-14）。

只做确定性检查：不评价镜头好不好、文字美不美。
用法：
    python check_package.py <package.md> [--model seedance-2.0] [--json]

退出码：0 = 无 FAIL；1 = 有 FAIL；2 = 文件/参数错误。
兼容 Python 3.9+，仅标准库。
"""
import argparse
import json
import re
import sys
from pathlib import Path

CJK = r"\u4e00-\u9fff"
SECTION_RE = re.compile(r"^##\s*([1-8])[\.、]\s*(.+)$", re.M)
TIME_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[–\-~至]\s*(\d+(?:\.\d+)?)\s*s", re.I)
SHOT_ID_RE = re.compile(r"^S\d{2}-\d{2}$")
DIALOGUE_RE = re.compile(r"「([^」]*)」")
DIALOGUE_EN_RE = re.compile(r"[\"“]([^\"”\n]{2,})[\"”]")
REF_PATTERNS = {
    "seedance": re.compile(r"@(?:Image|Video|Audio)\s*\d+", re.I),
    "picture": re.compile(r"<Picture\s*\d+>", re.I),
    "refzh": re.compile(r"参考图\s*\d+"),
    "refen": re.compile(r"reference image\s*\d+", re.I),
    "element": re.compile(r"@element\s*\d+", re.I),
}
MODEL_ALIASES = {
    "seedance 2.0": "seedance-2.0", "seedance2.0": "seedance-2.0",
    "seedance-2.0": "seedance-2.0",
    "seedance 2.5": "seedance-2.5", "seedance2.5": "seedance-2.5",
    "seedance-2.5": "seedance-2.5",
    "veo": "veo", "veo 3": "veo", "veo3": "veo",
    "minimax": "minimax-h3", "minimax h3": "minimax-h3", "h3": "minimax-h3",
    "minimax-h3": "minimax-h3",
    "kling": "kling", "可灵": "kling", "即梦": "seedance-2.0",
}
FORBIDDEN_REFS = {
    "seedance-2.0": [("picture", "<Picture N>"), ("element", "@elementN")],
    "seedance-2.5": [("picture", "<Picture N>"), ("element", "@elementN")],
    "kling": [("seedance", "@ImageN"), ("picture", "<Picture N>")],
    "minimax-h3": [("seedance", "@ImageN"), ("element", "@elementN")],
    "veo": [("seedance", "@ImageN"), ("element", "@elementN"), ("picture", "<Picture N>")],
    "generic": [("seedance", "@ImageN"), ("picture", "<Picture N>"), ("element", "@elementN")],
}


class Result:
    def __init__(self):
        self.items = []  # (id, status, detail)

    def add(self, cid, status, detail):
        self.items.append((cid, status, detail))

    def count(self, status):
        return sum(1 for _, s, _ in self.items if s == status)

    @property
    def failed(self):
        return self.count("FAIL") > 0

    def render(self):
        out = []
        for cid, status, detail in self.items:
            out.append("%-5s %-4s %s" % (cid, status, detail))
        out.append("")
        out.append("汇总：PASS %d · WARN %d · FAIL %d" % (self.count("PASS"), self.count("WARN"), self.count("FAIL")))
        return "\n".join(out)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(cs):
    return bool(cs) and all(re.fullmatch(r":?-{2,}:?", c or "") for c in cs)


def table_rows(text):
    """返回表格数据行（跳过表头与分隔行）：[(cells, raw)]"""
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cs = cells(line)
        if is_sep(cs):
            continue
        rows.append(cs)
    return rows


def first_table_header(sec):
    """返回该节第一张表的数据首行（表头）。"""
    for line in (sec or "").splitlines():
        if line.strip().startswith("|"):
            cs = cells(line)
            if is_sep(cs):
                continue
            return cs
    return []


def strip_header_rows(rows):
    """去掉第一行表头（如果它看起来像表头）。"""
    if rows and any(k in rows[0][0] for k in ("镜号", "编号", "项", "说话人", "条")):
        return rows[1:]
    return rows


def parse_model(text, override):
    if override:
        return normalize_model(override)
    m = re.search(r"目标模型[：:]\s*\**([^\n*]+)", text)
    if m:
        return normalize_model(m.group(1))
    return "generic"


def normalize_model(name):
    key = name.strip().lower()
    if key in MODEL_ALIASES:
        return MODEL_ALIASES[key]
    key2 = re.sub(r"\s+", " ", key)
    if key2 in MODEL_ALIASES:
        return MODEL_ALIASES[key2]
    for k, v in MODEL_ALIASES.items():
        if k in key2:
            return v
    return "generic"


def section_map(text):
    marks = list(SECTION_RE.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(m.group(1))] = text[start:end]
    return out


def extract_prompt_block(sec):
    """取第 4 节第一个 ```text 代码块。"""
    m = re.search(r"```(?:text|txt)?\s*\n(.*?)```", sec, re.S | re.I)
    return m.group(1) if m else ""


def check(text, model):
    r = Result()
    secs = section_map(text)

    # S-01 八节齐全
    missing = [str(i) for i in range(1, 9) if i not in secs]
    if missing:
        r.add("S-01", "FAIL", "缺少第 %s 节" % "、".join(missing))
    else:
        empty = [str(i) for i, v in secs.items() if len(v.strip()) < 20]
        if empty:
            r.add("S-01", "WARN", "第 %s 节内容过少" % "、".join(empty))
        else:
            r.add("S-01", "PASS", "8 节齐全")

    # 代码块闭合
    fences = len(re.findall(r"^\s*```", text, re.M))
    if fences % 2:
        r.add("S-01", "FAIL", "代码块未闭合（``` 数量为奇数）")

    # S-01 表头必须能被解析（防止列错位后静默误判）
    h3 = first_table_header(secs.get(3, ""))
    if h3:
        need = [c for c in ("镜号", "时间", "主动作") if not any(c in x for x in h3)]
        if need:
            r.add("S-01", "FAIL", "分镜表表头缺列：%s" % "、".join(need))

    # S-02/S-03 时间轴
    shots = []
    if 3 in secs:
        for cs in strip_header_rows(table_rows(secs[3])):
            if len(cs) < 2:
                continue
            sid = cs[0].strip("` ")
            if not re.match(r"^S\d{2}-\d{2}", sid):
                continue
            m = TIME_RE.search(cs[1])
            if not m:
                r.add("S-02", "FAIL", "%s 时间格无法解析：%s" % (sid, cs[1]))
                continue
            t0, t1 = float(m.group(1)), float(m.group(2))
            shots.append((sid, t0, t1, cs))
    if not shots:
        r.add("S-02", "FAIL", "第 3 节没有可解析的分镜行（镜号形如 S01-01）")
    else:
        # 按段分组：每条视频各自从 0s 开始，不能跨段要求连续
        segs = {}
        for s in shots:
            segs.setdefault(s[0][:3], []).append(s)
        problems = []
        for seg, ss in segs.items():
            if abs(ss[0][1]) > 1e-6:
                problems.append("%s 不从 0s 开始" % seg)
            if any(abs(ss[i][2] - ss[i + 1][1]) > 1e-6 for i in range(len(ss) - 1)):
                problems.append("%s 镜间有断点/重叠" % seg)
            if any(x[1] >= x[2] for x in ss):
                problems.append("%s 存在 t0≥t1" % seg)
        if problems:
            r.add("S-02", "FAIL", "；".join(problems))
        else:
            r.add("S-02", "PASS", "%d 段 / %d 镜，每段从 0s 连续排到段尾" % (len(segs), len(shots)))

        total = None
        if 6 in secs:
            for cs in table_rows(secs[6]):
                if cs and "时长" in cs[0]:
                    m = re.search(r"(\d+(?:\.\d+)?)\s*s", cs[1] if len(cs) > 1 else "")
                    if m:
                        total = float(m.group(1))
                        break
        span = sum(s[2] - s[1] for s in shots)
        if total is None:
            r.add("S-03", "WARN", "第 6 节未写时长，无法对账（分镜合计 %ss）" % round(span, 1))
        elif abs(span - total) <= 0.5:
            r.add("S-03", "PASS", "分镜合计 %.1fs ≈ 标称 %ss" % (span, total))
        else:
            r.add("S-03", "FAIL", "分镜合计 %.1fs ≠ 标称 %ss" % (span, total))

    # S-04 每镜有主动作
    no_action = [s[0] for s in shots if len(s[3]) < 7 or not s[3][6].strip(" —-")]
    if no_action:
        r.add("S-04", "FAIL", "%s 缺主动作" % "、".join(no_action))
    elif shots:
        r.add("S-04", "PASS", "每镜都有动作格（是否只一个主动作需人工 R-11）")

    # S-05/S-06 台词
    dialogue_rows = []
    if 2 in secs:
        for cs in table_rows(secs[2]):
            if len(cs) >= 5 and cs[0] not in ("说话人",) and "---" not in cs[0]:
                if cs[1].strip(" —-") and cs[1].strip() not in ("无对白", "—", "-"):
                    dialogue_rows.append(cs)
    prompt = extract_prompt_block(secs.get(4, ""))
    if "```" not in secs.get(4, ""):
        r.add("S-05", "FAIL", "第 4 节没有代码块包裹的提示词")

    quoted = [q for q in DIALOGUE_RE.findall(prompt) if q.strip()]
    quoted += [q for q in DIALOGUE_EN_RE.findall(prompt) if q.strip()]
    table_texts = [cs[1].strip() for cs in dialogue_rows]
    missing_in_table = [q for q in quoted if not any(q in t or t in q for t in table_texts)]
    dropped = [t for t in table_texts if not any(t in q or q in t for q in quoted)]
    if missing_in_table and table_texts:
        r.add("S-05", "WARN", "提示词里有引号内容未进台词表：%s" % "；".join(missing_in_table)[:80])
    elif dropped:
        r.add("S-05", "FAIL", "台词表有台词未进入提示词：%s" % "；".join(dropped)[:80])
    elif dialogue_rows:
        r.add("S-05", "PASS", "%d 条台词逐字进出" % len(dialogue_rows))
    else:
        r.add("S-05", "PASS", "无台词（已明确）")

    budget_warn = []
    for cs in dialogue_rows:
        try:
            chars = int(re.sub(r"[^\d]", "", cs[3]) or "0")
            budget = float(re.sub(r"[^\d.]", "", cs[4]) or "0")
        except ValueError:
            continue
        if chars and budget and chars / 6.0 > budget + 0.6 and "超时" not in " ".join(cs):
            budget_warn.append("%s：%d字/%.1fs" % (cs[0], chars, budget))
    if budget_warn:
        r.add("S-06", "WARN", "字数按 6 字/秒仍超预算：%s" % "；".join(budget_warn)[:100])
    else:
        r.add("S-06", "PASS", "台词预算未触发硬超时")

    # S-07/S-13 素材
    asset_rows = []
    if 5 in secs:
        for cs in table_rows(secs[5]):
            if cs and re.match(r"^A\d{2}", cs[0]):
                asset_rows.append(cs)
    refs = []
    for kind, pat in REF_PATTERNS.items():
        for m in pat.findall(prompt):
            refs.append((kind, m))
    ref_tokens = {m.lower() for _, m in refs}
    if refs and not asset_rows:
        r.add("S-07", "FAIL", "提示词引用了素材，但第 5 节没有资产行")
    elif refs and len(ref_tokens) > len(asset_rows):
        r.add("S-07", "FAIL", "不同引用 %d 个 > 资产 %d 行" % (len(ref_tokens), len(asset_rows)))
    elif asset_rows and not refs:
        r.add("S-07", "WARN", "有 %d 份资产，但提示词没有绑定任何素材" % len(asset_rows))
    elif asset_rows:
        r.add("S-07", "PASS", "%d 份资产，%d 个不同引用（共 %d 处）" % (
            len(asset_rows), len(ref_tokens), len(refs)))
    else:
        r.add("S-07", "PASS", "无素材引用")

    no_owner = []
    for cs in asset_rows:
        role = cs[2] if len(cs) > 2 else ""
        must_not = cs[4] if len(cs) > 4 else ""
        if not role.strip(" —-") or not must_not.strip(" —-"):
            no_owner.append(cs[0])
    if no_owner:
        r.add("S-13", "WARN", "%s 未写主职责或「不得传递」" % "、".join(no_owner))
    elif asset_rows:
        r.add("S-13", "PASS", "每份资产都写了主职责与不得传递")

    # S-08 语法隔离
    bad = []
    for kind, label in FORBIDDEN_REFS.get(model, []):
        if REF_PATTERNS[kind].search(prompt):
            bad.append(label)
    if bad:
        r.add("S-08", "FAIL", "%s 方言里出现不该用的引用：%s" % (model, "、".join(bad)))
    else:
        r.add("S-08", "PASS", "引用语法与 %s 一致" % model)

    # S-09 参数泄漏
    leak = []
    if model != "minimax-h3":
        for pat in (r"--ar\b", r"--v\s", r"duration\s*=", r"resolution\s*="):
            if re.search(pat, prompt, re.I):
                leak.append(pat)
        for pat in (r"\b(?:16:9|9:16|1:1|4:3)\b", r"\b(?:480p|720p|1080p|4K)\b"):
            if re.search(pat, prompt, re.I):
                leak.append(pat)
    if leak:
        status = "FAIL" if any(p.startswith("--") or "=" in p for p in leak) else "WARN"
        r.add("S-09", status, "提示词内出现参数：%s" % "、".join(leak[:4]))
    else:
        r.add("S-09", "PASS", "参数未泄漏进提示词")

    # S-10 占位符：检查第 1–6 节，防止模板变量残留在决策/事实/分镜等位置
    ph_sections = [str(i) for i in range(1, 7)
                   if "{{" in secs.get(i, "") or "}}" in secs.get(i, "")]
    if ph_sections:
        r.add("S-10", "FAIL", "第 %s 节残留未填的 {{占位符}}" % "、".join(ph_sections))
    else:
        r.add("S-10", "PASS", "第 1–6 节无残留占位符")

    # S-11 作用镜头：写错的镜号必须阻断，空范围只警告
    bad_scope, warn_scope = [], []
    shot_ids = {s[0] for s in shots}
    for cs in asset_rows:
        scope = cs[3] if len(cs) > 3 else ""
        if not scope.strip(" —-"):
            warn_scope.append(cs[0])
            continue
        for sid in re.findall(r"S\d{2}-\d{2}", scope):
            if shots and sid not in shot_ids:
                bad_scope.append("%s→%s" % (cs[0], sid))
    if bad_scope:
        r.add("S-11", "FAIL", "作用镜头引用了不存在的镜号：%s" % "、".join(bad_scope))
    elif warn_scope:
        r.add("S-11", "WARN", "%s 未写作用镜头范围" % "、".join(warn_scope))
    elif asset_rows:
        r.add("S-11", "PASS", "作用镜头都能对上分镜")

    # S-12 镜号唯一
    ids = [s[0] for s in shots]
    if len(ids) != len(set(ids)):
        dup = sorted({x for x in ids if ids.count(x) > 1})
        r.add("S-12", "FAIL", "镜号重复：%s" % "、".join(dup))
    elif shots:
        r.add("S-12", "PASS", "镜号唯一")

    # S-14 提示词块内无解释
    chinese_explain = re.findall(r"^\s*(?:说明|注意|备注|解释)[：:]", prompt, re.M)
    if chinese_explain:
        r.add("S-14", "WARN", "提示词块内出现解释性行，复制会带进模型")
    else:
        r.add("S-14", "PASS", "提示词块内无解释行")

    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description="校验视频提示词生产包（结构不变量）")
    ap.add_argument("package", help="生产包 Markdown 路径")
    ap.add_argument("--model", default=None, help="覆盖模型：seedance-2.0/2.5, veo, minimax-h3, kling, generic")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)

    path = Path(args.package)
    if not path.exists():
        print("找不到文件：%s" % path, file=sys.stderr)
        return 2
    text = path.read_text("utf-8")
    model = parse_model(text, args.model)
    r = check(text, model)

    if args.json:
        print(json.dumps({
            "file": str(path), "model": model,
            "items": [{"id": a, "status": b, "detail": c} for a, b, c in r.items],
            "summary": {"pass": r.count("PASS"), "warn": r.count("WARN"), "fail": r.count("FAIL")},
        }, ensure_ascii=False, indent=2))
    else:
        print("文件：%s" % path)
        print("模型：%s\n" % model)
        print(r.render())
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main())
