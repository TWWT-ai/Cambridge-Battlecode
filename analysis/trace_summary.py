"""Summarise mp-trace TRACE lines: share of champion turns per activity, per map (both sides pooled)."""
import zipfile, re, sys, glob, os
from collections import defaultdict
NAMES = {0: "Ryth", 1: "Vesper", 2: "Vendetta", 3: "Cassi", 4: "Issac", 5: "Stellar", 6: "Prism", 7: "Marcella", 8: "Willow", 9: "Ren", 10: "Varg", 11: "Tavi"}
CATS = ["hit-camp", "walk-farm", "wait-camp", "capture", "walk-capture", "follow", "idle", "bank", "tribute", "recall", "shoptrip", "survive", "fight", "dead"]
d = sys.argv[1]
bot = sys.argv[2] if len(sys.argv) > 2 else "mp-trace"
per_map = defaultdict(lambda: defaultdict(int))
per_champ = defaultdict(lambda: defaultdict(int))
caps = defaultdict(int)
deaths = defaultdict(int)
for f in sorted(glob.glob(os.path.join(d, "*.repl26a"))):
    base = os.path.basename(f)
    side = "a" if base.startswith("A-") else "b"
    m = base[2:].replace(".repl26a", "")
    z = zipfile.ZipFile(f)
    t = z.read(f"team-{side}.stdout").decode("utf-8", "replace").replace("\x00", "")
    last = {}
    for line in t.splitlines():
        if line.startswith("TRACE"):
            p = line.split()
            last[int(p[2])] = p
    for ch, p in last.items():
        caps[m] += int(p[4]); deaths[m] += int(p[6])
        for kv in p[7:]:
            k, v = kv.split("=")
            per_map[m][k] += int(v)
            per_champ[(m, NAMES.get(ch, ch))][k] += int(v)
print("map        " + " ".join(f"{c[:9]:>9}" for c in CATS) + "   captured deaths")
for m in sorted(per_map):
    tot = sum(per_map[m].values())
    print(f"{m:10} " + " ".join(f"{100 * per_map[m][c] / tot:8.1f}%" for c in CATS) + f"   {caps[m]:6} {deaths[m]}")
tot_all = defaultdict(int)
for m in per_map:
    for k, v in per_map[m].items():
        tot_all[k] += v
T = sum(tot_all.values())
print(f"{'ALL':10} " + " ".join(f"{100 * tot_all[c] / T:8.1f}%" for c in CATS))
print()
print("per champion (all maps):")
pc = defaultdict(lambda: defaultdict(int))
for (m, ch), dct in per_champ.items():
    for k, v in dct.items():
        pc[ch][k] += v
for ch in sorted(pc):
    tot = sum(pc[ch].values())
    print(f"{ch:10} " + " ".join(f"{100 * pc[ch][c] / tot:8.1f}%" for c in CATS))
