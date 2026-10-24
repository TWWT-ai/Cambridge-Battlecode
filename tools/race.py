"""Compare rounds-to-win per map between league runs (e.g. vs zz-idle).

Usage: python tools/race.py <summary.json or league dir> [more ...]
Prints, per map and side, the round each run won (or LOST/-), plus the total.
"""
import json
import sys
from pathlib import Path

runs = []
for arg in sys.argv[1:]:
    p = Path(arg)
    if p.is_dir():
        p = p / "summary.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    runs.append((d["bot"] + (f"[{d['tag']}]" if d.get("tag") else ""), {(g["opp"], g["map"], g["side"]): g for g in d.get("game_list") or d["games"]}))

keys = sorted(set().union(*[set(r[1]) for r in runs]))
print(f"{'opp/map/side':34}" + "".join(f"{name[:16]:>17}" for name, _ in runs))
totals = [0] * len(runs)
for k in keys:
    row = f"{'/'.join(k):34}"
    for i, (_, gs) in enumerate(runs):
        g = gs.get(k)
        cell = "-" if not g else (str(g["round"]) if g["won"] else f"LOST{g['round']}")
        totals[i] += g["round"] if g and g["won"] else 2000
        row += f"{cell:>17}"
    print(row)
print(f"{'TOTAL (loss = 2000)':34}" + "".join(f"{t:>17}" for t in totals))
