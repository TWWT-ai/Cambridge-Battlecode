"""Economy/combat profile of ming_bot from bots/mingstudy-trace replays (ming-study).

Usage: python analysis/ming_trace.py <league dir with mingstudy-trace games> [--per-slot]

mingstudy-trace = ming_bot + passive stdout instrumentation (bots/mingstudy-trace/src/bot.cpp):
  SCORE r ours theirs                         (slot 0, every 5 rounds)
  PSLOT slot champ role: C<g>/<gems>[o] A<a>   (compiled draft route, printed at round 6)
  MCAP r slot gain group                       (gem gain while standing on a camp tile)
  MGAIN r slot gain                            (gem gain elsewhere = a champion kill)
  MTRIB r slot amount                          (bag emptied while alive = tribute)
  MDEATH r slot bag_lost
  MSUM r slot champ c_boot c_channel c_tactic c_pitstop c_bank c_travel c_clear c_capture c_haul c_idle c_dead | ...
"""
import glob
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

NAMES = {0: "Ryth", 1: "Vesper", 2: "Vendetta", 3: "Cassi", 4: "Issac", 5: "Stellar", 6: "Prism",
         7: "Marcella", 8: "Willow", 9: "Ren", 10: "Varg", 11: "Tavi"}
STATES = ["boot", "channel", "tactic", "pitstop", "bank", "travel", "clear", "capture", "haul", "idle", "dead"]
BOT = "mingstudy-trace"


def parse(path):
    base = os.path.basename(path)[:-len(".repl26a")]
    m = re.match(r"\d+-(.+)-vs-(.+)-(\w+)$", base)
    a, b, mp = m.groups()
    side = "a" if a == BOT else "b"
    opp = b if side == "a" else a
    z = zipfile.ZipFile(path)
    text = z.read(f"team-{side}.stdout").decode("utf-8", "replace").replace("\x00", "")
    g = dict(map=mp, side=side.upper(), opp=opp, score=None, slots={}, caps=[], tribs=[], deaths=[], kills=[])
    # Champion processes share stdout, so lines can interleave: match tokens, not lines.
    for m in re.finditer(r"SCORE (\d+) (\d+) (\d+)", text):
        g["score"] = tuple(map(int, m.groups()))
    for m in re.finditer(r"PSLOT (\d+) (-?\d+) (\d+):((?: [CA]\d+(?:/\d+o?)?)*)", text):
        s = g["slots"].setdefault(int(m.group(1)), {})
        s["route"] = m.group(4).split()
        s["champ"] = NAMES.get(int(m.group(2)), m.group(2))
    for m in re.finditer(r"MCAP (\d+) (\d+) (\d+) (\d+)", text):
        g["caps"].append(tuple(map(int, m.groups())))
    for m in re.finditer(r"MGAIN (\d+) (\d+) (\d+)", text):
        g["kills"].append(tuple(map(int, m.groups())))
    for m in re.finditer(r"MTRIB (\d+) (\d+) (\d+)", text):
        g["tribs"].append(tuple(map(int, m.groups())))
    for m in re.finditer(r"MDEATH (\d+) (\d+) (\d+)", text):
        g["deaths"].append(tuple(map(int, m.groups())))
    for m in re.finditer(r"MSUM (\d+) (\d+) (\d+)((?: \d+){11}) \|((?: \d+){9})", text):
        s = g["slots"].setdefault(int(m.group(2)), {})
        s["champ"] = NAMES.get(int(m.group(3)), m.group(3))
        s["counts"] = list(map(int, m.group(4).split()))
        s["sum"] = list(map(int, m.group(5).split()))
    return g


def summarise(g, per_slot=False):
    out = []
    sc = g["score"] or (0, 0, 0)
    tribs = g["tribs"]
    first = min((t[0] for t in tribs), default=0)
    avg_bag = sum(t[2] for t in tribs) / len(tribs) if tribs else 0
    # capture sharing: (round, group) -> number of our bodies paid
    share = Counter(Counter((c[0], c[3]) for c in g["caps"]).values())
    lost = sum(d[2] for d in g["deaths"])
    stolen = sum(k[2] for k in g["kills"])
    tot = Counter()
    for s in g["slots"].values():
        for i, c in enumerate(s.get("counts", [])):
            tot[STATES[i]] += c
    turns = sum(tot.values()) or 1
    frac = ", ".join(f"{k} {100 * v / turns:.0f}%" for k, v in tot.most_common(7))
    # distinct camp groups captured per 100 rounds (team parallelism proxy)
    events = len(set((c[0], c[3]) for c in g["caps"]))
    rate = 100 * events / max(1, sc[0])
    out.append(f"{g['map']:<10} {g['side']} vs {g['opp']:<14} end {sc[0]:>4} {sc[1]:>4}-{sc[2]:<4} "
               f"1st trib r{first:<4} tribs {len(tribs):>3} avg bag {avg_bag:4.1f} caps {events:>3} "
               f"({rate:4.1f}/100r) shares {dict(sorted(share.items()))} deaths {len(g['deaths'])} "
               f"lost {lost} stolen {stolen} | {frac}")
    if per_slot:
        for slot in sorted(g["slots"]):
            s = g["slots"][slot]
            c = s.get("counts", [0] * 11)
            n = sum(c) or 1
            sm = s.get("sum", [0] * 9)
            route = " ".join(s.get("route", []))
            out.append(f"    slot {slot} {s.get('champ', '?'):<8} caps {sm[0]:>2} ({sm[1]:>3}g) tribs {sm[4]:>2} "
                       f"({sm[5]:>3}g) deaths {sm[6]} first {sm[8]:>3} | "
                       + " ".join(f"{STATES[i][:5]} {100 * c[i] / n:.0f}" for i in range(11) if c[i])
                       + f" | route {route}")
    return out


def main():
    d = sys.argv[1]
    per_slot = "--per-slot" in sys.argv
    games = [parse(f) for f in sorted(glob.glob(os.path.join(d, "*.repl26a")))]
    games.sort(key=lambda g: (g["opp"], g["map"], g["side"]))
    for g in games:
        print("\n".join(summarise(g, per_slot)))
    # aggregate vs idle
    agg = defaultdict(Counter)
    for g in games:
        for s in g["slots"].values():
            for i, c in enumerate(s.get("counts", [])):
                agg[g["opp"]][STATES[i]] += c
    for opp, c in agg.items():
        n = sum(c.values())
        print(f"ALL vs {opp}: " + ", ".join(f"{k} {100 * v / n:.1f}%" for k, v in c.most_common()))


if __name__ == "__main__":
    main()
