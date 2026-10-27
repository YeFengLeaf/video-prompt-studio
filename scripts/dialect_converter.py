#!/usr/bin/env python3
"""dialect_converter.py: neutral prompt -> target-model dialect (stdlib only).

Rules (see references/03 section 13, five-step conversion engine):
- The story core (input text) is kept verbatim; facts, actions, dialogue untouched.
- Only mechanical transforms: structure reorder, reference-syntax replacement,
  parameter-position annotation.
- Any parameter absent from the input and without a fixed evidenced value is
  emitted as a [UNVERIFIED: to fill in] placeholder; values are never invented.
- Every output section carries an evidence-grade annotation (A/B/C/D + record
  numbers); C/D sections are marked UNVERIFIED.

Usage:
    python3 dialect_converter.py --input neutral.txt --model runway
    python3 dialect_converter.py --input neutral.txt --all --out-dir out/
    python3 dialect_converter.py --list-models
"""

import argparse
import re
import sys
from pathlib import Path

MODELS = {
    "seedance-2.0": {
        "grade": "B",
        "records": "Skill references/03 (migrated)",
        "ref_syntax": "@Image1 / @Video1 / @Audio1",
        "structure": "goal -> reference map -> subject/scene anchor -> timed action -> camera plan -> light/material/style anchor -> sound plan",
        "notes": [
            "Timeline in 0-3s segments; segmentation strongly advised above 10s.",
            "Every @ reference must state its purpose; parameters stay OUT of the prompt.",
        ],
    },
    "seedance-2.5": {
        "grade": "B",
        "records": "Skill references/03 (migrated, platform-dependent)",
        "ref_syntax": "@Image1 / @Video1 / @Audio1",
        "structure": "As 2.0; 30s split by information points, max 3-4; supports edit / extend.",
        "notes": [
            "Extend: state which state to continue from; do not restate finished action.",
            "fal platform values only after the platform is confirmed.",
        ],
    },
    "veo": {
        "grade": "A",
        "records": "Skill references/03 (migrated, Google Cloud guide)",
        "ref_syntax": "natural language reference description",
        "structure": "[camera] + [subject] + [action] + [environment] + [style and mood]",
        "notes": [
            "Negative constraints rephrased as 'describing what is absent', not abstract negation.",
            "Single-clip duration 4/6/8s (Veo 3.1); 8s required with reference images, 1080p or 4K (Google Cloud guide + Gemini API docs, 2026-10-27).",
        ],
    },
    "minimax-h3": {
        "grade": "A",
        "records": "Skill references/03 (migrated, MiniMax official GitHub prompt Skill, 2026-10-27)",
        "ref_syntax": "<Picture 1> with [Shot N] + timecode",
        "structure": "Three fields: integrated_multimodal_description / overall_soundscape / non_diegetic_music; timecodes two decimals, strictly increasing",
        "notes": [
            "The only 'parameters inside the prompt' exception: timecodes go in the prompt.",
            "Cut only when a new subject / space / state / viewpoint / time appears.",
        ],
    },
    "kling": {
        "grade": "A",
        "records": "Kling official 4.0 user guide (2026-10-27)",
        "ref_syntax": "@Image1 / @Video1 / @Element1 (capital E)",
        "structure": "natural language; references numbered in upload order, each with a stated purpose; parameters outside the prompt",
        "notes": [
            "Single clip 3-30s (default 10s); resolutions 720p/1080p/4K; aspects 21:9/16:9/1:1/9:16/Auto.",
            "References: <=10 images / <=5 videos / <=7 elements (<=3 video elements) / <=3 voice profiles / <=15 total; native stereo audio.",
            "Confirm the version before delivery: pre-4.0 parameters differ.",
        ],
    },
    "runway": {
        "grade": "A",
        "records": "REC_041/042/043/044/045; REC_046 is C UNVERIFIED",
        "ref_syntax": "natural language + panels (no @ syntax)",
        "structure": "[shot size] + [angle] + [movement + direction + speed] + [subject and action] + [lens/look] + [lighting/mood] + [what the shot reveals]",
        "notes": [
            "Every movement word must carry a speed or duration modifier; one reliable movement per shot (REC_041).",
            "Speed blacklist: quickly / rapidly / fast / suddenly are banned; use slow / gradually / gently / steadily / deliberately (REC_044).",
            "Double-directing: panel + prompt must not both direct camera movement (REC_043).",
            "Camera Motion panel items: [UNVERIFIED: REC_046, C-grade third-party tutorial].",
        ],
    },
    "pika": {
        "grade": "B",
        "records": "REC_047-051 (official reprint; domain not cross-verified)",
        "ref_syntax": "natural language + negative prompts listed separately",
        "structure": "A [subject] [action] in [setting], [style/lighting], [camera move], [look], [resolution tier], negative prompts",
        "notes": [
            "One subject per clip; negative prompts commonly: no morphing, no extra limbs, no blurry faces (REC_048).",
            "Picture must be textless (subtitles added in post); Pika 2.5 generates no audio (REC_050).",
            "Duration / resolution / aspect tiers: verify against the in-product values (REC_047, B-grade reprint).",
        ],
    },
    "sora": {
        "grade": "A",
        "records": "REC_052-054 (OpenAI official pages; product discontinued 2026-04-26, Videos API closed 2026-09-24: HISTORICAL ONLY)",
        "ref_syntax": "natural-language shot-list sections (no @ syntax)",
        "structure": "Primary Target & Visuals -> Format & Look -> Lenses & Filtration -> Grade/Palette -> Lighting & Atmosphere -> Location & Framing -> Sound -> Optimized Shot List",
        "notes": [
            "HISTORICAL ONLY: Sora 2 must not be used for current delivery; API resolutions were 720p only.",
            "Format & Look writes duration / shutter / aspect directly (REC_054); this converter fills no numbers: [UNVERIFIED: to fill in].",
            "No long compound precise camera trajectories; use single shots. Real-person likeness needs the person's own authorization (REC_053/054).",
        ],
    },
    "wan": {
        "grade": "A",
        "records": "REC_055-058 (official repo README, open-source inference)",
        "ref_syntax": "natural-language body text + command-line parameters outside the prompt",
        "structure": "natural-language prompt body, optionally expanded by prompt extension, + CLI flags (--task / --size / --ckpt_dir / --offload_model ...)",
        "notes": [
            "Size tiers (A): A14B 1280*720; TI2V-5B fixed 1280*704 / 704*1280; I2V --size is area, ratio follows input image; S2V 1024*704 (REC_055). No task is pre-selected: [UNVERIFIED: to fill in].",
            "A14B 1280*720, S2V-14B 1024*704 and prompt-extension details were not individually confirmed on the official model-card page (2026-10-27); verify before delivery.",
            "Wan-Animate tasks must not mount Wan2.2-series LoRA (REC_058).",
        ],
    },
    "ltx": {
        "grade": "A",
        "records": "REC_059-062 (official docs + repo README)",
        "ref_syntax": "natural-language six-element flowing paragraph (no @ syntax)",
        "structure": "Six elements, single flowing paragraph, present tense, 4-8 sentences: Establish the Shot -> Set the Scene -> Describe the Action -> Define Characters -> Identify Camera Movement(s) -> Describe the Audio",
        "notes": [
            "Emotion expressed through body action, never abstract labels such as sad (REC_059).",
            "Open-source bounds: resolution divisible by 32, frame count 8n+1, guidance 3-3.5, steps 40+ / 20-30 (REC_060); values are not pre-selected: [UNVERIFIED: to fill in].",
        ],
    },
    "generic": {
        "grade": "D",
        "records": "derived (D-grade)",
        "ref_syntax": "natural language ('reference image 1 is responsible for ...')",
        "structure": "natural language; no @Image1 / [Shot 2] style platform syntax",
        "notes": [
            "Plan within 15 seconds; all parameters outside the prompt, marked 'fill in per your platform'.",
        ],
    },
}

SPEED_BLACKLIST = ["quickly", "rapidly", "fast", "suddenly"]

def _map_refs(core, model):
    """Mechanical reference-syntax mapping only; returns (mapped_text, changed)."""
    mapped = core
    if model == "minimax-h3":
        mapped = re.sub(r"@Image(\d+)", r"<Picture \1>", mapped)
        mapped = re.sub(r"@Video(\d+)", r"<Video \1>", mapped)
        mapped = re.sub(r"@Audio(\d+)", r"<Audio \1>", mapped)
    elif model in ("seedance-2.0", "seedance-2.5"):
        mapped = re.sub(r"<Picture (\d+)>", r"@Image\1", mapped)
        mapped = re.sub(r"@Element(\d+)", r"@Image\1", mapped)
        mapped = re.sub(r"@element(\d+)", r"@Image\1", mapped)
    elif model == "kling":
        mapped = re.sub(r"<Picture (\d+)>", r"@Image\1", mapped)
        mapped = re.sub(r"@Image(\d+)", r"@Element\1", mapped)
    return mapped, mapped != core


def convert(text, model):
    """Return the target-model version with evidence annotations.

    The input text is kept verbatim inside the story-core section.
    """
    if model not in MODELS:
        raise ValueError("Unknown model: %s (available: %s)" % (model, ", ".join(sorted(MODELS))))
    m = MODELS[model]
    core = text.strip("\n")
    out = []
    out.append("# Dialect conversion output - %s" % model)
    out.append("")
    out.append("> Converter: `scripts/dialect_converter.py` (stdlib only). "
               "Story core kept verbatim; facts / actions / dialogue untouched. "
               "Evidence grade %s; sources: %s." % (m["grade"], m["records"]))
    if m["grade"] in ("C", "D"):
        out.append("> **UNVERIFIED**: this model profile is grade %s; "
                   "mark UNVERIFIED in the parameter section at delivery." % m["grade"])
    out.append("")
    out.append("## Story core (kept verbatim, do not edit)")
    out.append("")
    out.append(core)
    out.append("")
    out.append("## Target-model structure")
    out.append("")
    out.append(m["structure"])
    out.append("")
    out.append("Reorder the section-4 prompt paragraphs into the order above; "
               "story-core content does not change, only paragraph order.")
    out.append("")
    out.append("## Reference-syntax handling")
    out.append("")
    out.append("Target syntax: %s." % m["ref_syntax"])
    out.append("")
    mapped, changed = _map_refs(core, model)
    has_markers = re.search(r"@Image\d|@Video\d|@Audio\d|@Element\d|@element\d|<Picture \d+>", core)
    if changed:
        out.append("Mapped references (mechanical replacement only, same referents):")
        out.append("")
        out.append("```text")
        out.append(mapped)
        out.append("```")
    elif has_markers:
        out.append("Reference markers ARE present in the input, but this target model "
                   "uses natural language for references: rewrite each marker as "
                   "natural language (e.g. 'reference image 1 is responsible for ...'); "
                   "do not copy @ / <Picture> syntax into the prompt.")
    else:
        out.append("No reference markers (@Image / <Picture> / @element) detected in the input; "
                   "nothing to map. When assets exist, write them in the target syntax; "
                   "asset duties follow production-package section 5.")
    out.append("")
    out.append("## Rules and notes")
    out.append("")
    for note in m["notes"]:
        out.append("- " + note)
    if model == "runway":
        hits = [w for w in SPEED_BLACKLIST if re.search(r"\b%s\b" % w, core, re.I)]
        if hits:
            out.append("- **Speed blacklist HIT**: story core contains banned speed word(s) %s "
                       "(REC_044, A); rewrite with slow / gradually / gently / steadily / "
                       "deliberately; do not deliver verbatim." % ", ".join(hits))
        else:
            out.append("- Speed blacklist check: no quickly / rapidly / fast / suddenly "
                       "in the story core (REC_044).")
    out.append("")
    out.append("## Parameter section (all outside the prompt; values to fill in)")
    out.append("")
    out.append("| Item | Value | Evidence grade | Verification date |")
    out.append("|---|---|---|---|")
    out.append("| Duration | [UNVERIFIED: to fill in] | %s | UNVERIFIED | Fill per target-model tier |" % m["grade"])
    out.append("| Aspect | [UNVERIFIED: to fill in] | %s | UNVERIFIED | Fill per platform |" % m["grade"])
    out.append("| Resolution | [UNVERIFIED: to fill in] | %s | UNVERIFIED | Fill per platform |" % m["grade"])
    out.append("")
    out.append("The converter invented no parameter values; the three items above "
               "must be filled in by a human per platform before delivery.")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Neutral prompt -> target-model dialect (story core kept verbatim)")
    ap.add_argument("--input", help="neutral prompt plain-text file")
    ap.add_argument("--model", help="target model (see --list-models)")
    ap.add_argument("--all", action="store_true", help="emit all model versions into --out-dir")
    ap.add_argument("--out-dir", default=None, help="output directory for --all")
    ap.add_argument("--output", default=None, help="output file for a single model (default: stdout)")
    ap.add_argument("--list-models", action="store_true", help="list supported models with evidence grades")
    args = ap.parse_args(argv)
    if args.list_models:
        for name in sorted(MODELS):
            print("%-14s grade %s - %s" % (name, MODELS[name]["grade"], MODELS[name]["records"]))
        return 0
    if not args.input:
        ap.error("--input is required (except with --list-models)")
    text = Path(args.input).read_text(encoding="utf-8")
    if args.all:
        out_dir = Path(args.out_dir or "dialect_out")
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(MODELS):
            (out_dir / ("%s.md" % name)).write_text(convert(text, name), encoding="utf-8")
        print("Wrote %d model versions to %s" % (len(MODELS), out_dir))
        return 0
    if not args.model:
        ap.error("--model is required (or use --all)")
    rendered = convert(text, args.model)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
