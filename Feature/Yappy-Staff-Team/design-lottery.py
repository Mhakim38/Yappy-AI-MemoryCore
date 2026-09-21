#!/usr/bin/env python3
"""Design Concept Lottery - random design direction for Mira (and the design team).

Read-only: reads ~/.claude/skills/ui-ux-pro-max/data/*.csv, prints a draw. Writes nothing.

  design-lottery.py --mode explore            # new concept: style + palette + fonts + lens + constraint
  design-lottery.py --mode locked             # existing brand identity: craft lens + constraint only
  design-lottery.py --mode explore --variants 3   # 3 different draws for A/B/C exploration
  design-lottery.py --seed 42 ...             # reproducible draw
  design-lottery.py --platform native ...     # allow the React Native / Expo lens

Yappy runs this automatically before briefing Mira on any design task, and quotes the
printed line to Hakim. See Feature/Yappy-Staff-Team/SKILL.md "Design Concept Lottery".
"""
import argparse
import csv
import os
import random
import sys

SKILLS = os.path.expanduser("~/.claude/skills")
DATA = os.path.join(SKILLS, "ui-ux-pro-max", "data")

# Opt-in skills (disable-model-invocation): the staff READS the SKILL.md as a lens,
# it is not auto-triggered. name -> (what it pushes, needs native platform?)
EXPLORE_LENSES = {
    "antislop-ui": ("anti-generic discipline: earn every gradient/card/badge", False),
    "doodle-icons": ("hand-drawn, self-drawing playful iconography", False),
    "emil-design-eng": ("motion + micro-interaction craft", False),
    "antislop-layoutmobile": ("mobile reflow: tap targets, overflow, bottom nav", False),
    "appllama-app-design-skill": ("native-feeling mobile screens (Expo/RN only)", True),
}
# Identity is locked (e.g. ONDW Crystal White Glass): only craft lenses that do not touch look-and-feel.
LOCKED_LENSES = {
    "emil-design-eng": "motion + micro-interaction craft",
    "mobile-native": "installed-PWA feel: safe-area, dvh, tap, hover fixes",
    "antislop-human": "contrast, focus, keyboard, states",
    "review-animations": "strict review of existing motion",
}
CONSTRAINTS = [
    "one dominant shape language, no mixing",
    "type-led: typography does the heavy lifting, minimal decoration",
    "asymmetric layout, avoid centred-everything",
    "motion only on the single primary action",
    "no gradients at all",
    "one accent colour, used at most three times per screen",
    "generous whitespace, half the usual number of elements",
    "dense and information-rich, but with a clear scan path",
    "illustration-free, let photography or data lead",
    "every empty/loading/error state designed first",
    "thumb-zone first: primary actions bottom-reachable",
    "high-contrast surfaces, borders over shadows",
]


def rows(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def pick(rng, items):
    return rng.choice(items) if items else None


def draw(rng, mode, platform, lens_name, constraint):
    out = {"mode": mode}
    if mode == "explore":
        style = pick(rng, rows("styles.csv"))
        pal = pick(rng, rows("colors.csv"))
        typo = pick(rng, rows("typography.csv"))
        if style:
            out["style"] = f"#{style.get('No')} {style.get('Style Category')}"
        if pal:
            out["palette"] = f"#{pal.get('No')} {pal.get('Product Type')} (primary {pal.get('Primary')}, accent {pal.get('Accent')})"
        if typo:
            out["fonts"] = f"#{typo.get('No')} {typo.get('Font Pairing Name')}: {typo.get('Heading Font')} / {typo.get('Body Font')}"
        pool = {k: v for k, v in EXPLORE_LENSES.items() if platform == "native" or not v[1]}
        name = lens_name
        out["lens"] = f"{name} - {pool[name][0]} -> read {SKILLS}/{name}/SKILL.md"
    else:
        name = lens_name
        out["lens"] = f"{name} - {LOCKED_LENSES[name]} -> read {SKILLS}/{name}/SKILL.md"
        out["identity"] = "LOCKED: keep the project's existing look; lens is craft-only"
    out["constraint"] = constraint
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["explore", "locked"], default="explore")
    ap.add_argument("--variants", type=int, default=1)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--platform", choices=["web", "native"], default="web")
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 10**6)
    rng = random.Random(seed)
    if a.mode == "explore" and not os.path.isdir(DATA):
        print("note: ui-ux-pro-max data not found, style/palette/fonts skipped", file=sys.stderr)
    print(f"seed={seed} mode={a.mode} platform={a.platform}")
    n = max(1, a.variants)
    if a.mode == "explore":
        names = sorted(k for k, v in EXPLORE_LENSES.items() if a.platform == "native" or not v[1])
    else:
        names = sorted(LOCKED_LENSES)
    lenses = rng.sample(names, len(names))      # shuffled, so variants get different lenses
    cons = rng.sample(CONSTRAINTS, len(CONSTRAINTS))
    for i in range(n):
        d = draw(rng, a.mode, a.platform, lenses[i % len(lenses)], cons[i % len(cons)])
        label = f"variant {chr(65 + i)}" if a.variants > 1 else "draw"
        print(f"\n[{label}]")
        for k, v in d.items():
            if k != "mode":
                print(f"  {k:10} {v}")


if __name__ == "__main__":
    main()
