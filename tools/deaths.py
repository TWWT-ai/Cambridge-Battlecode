"""Count a bot's champion deaths (SCOUT DEATH lines) per opponent in a league run.

Usage: python tools/deaths.py <league dir> <bot>
"""
import glob
import os
import sys
import zipfile
from collections import defaultdict

folder, bot = sys.argv[1], sys.argv[2]
per = defaultdict(lambda: [0, 0])
for f in glob.glob(os.path.join(folder, "*.repl26a")):
    a, b = os.path.basename(f)[4:].rsplit("-", 1)[0].split("-vs-")
    side, opp = ("a", b) if a == bot else ("b", a)
    text = zipfile.ZipFile(f).read(f"team-{side}.stdout").decode("utf-8", "replace")
    per[opp][0] += text.count("SCOUT DEATH")
    per[opp][1] += 1
total = sum(d for d, _ in per.values())
print(f"{bot}: {total} deaths in {sum(n for _, n in per.values())} games")
for opp, (d, n) in sorted(per.items(), key=lambda kv: -kv[1][0])[:8]:
    print(f"  {opp:18} {d / n:5.1f} per game")
