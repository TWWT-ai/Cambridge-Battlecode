"""Waste attribution per map: share of champion turns lost to each economy inefficiency.

Usage: python analysis/econ_waste.py <league dir with prof-* games> [bot name, default prof-tts] [opp, default zz-idle]

Categories (a turn can fall in more than one of the first two, the rest are disjoint turn classes):
  futile    camp work since the last capture/tribute that ended in a retreat or death, plus the recovery
            (econ_profile.extra_metrics; an upper bound: includes the walk to the abandoned camp)
  solo-hit  leader (Ryth/Issac) HIT turns on a wolf/elk group with no ally within 4 tiles
  follow    FOLLOW + FIDLE (back-liner shadowing its leader, not hitting)
  spawnfight FSPAWN + FALLB (engaged by enemies standing on their own spawn; vs an idle opponent all waste)
  capwaste  CAPW/JOINW/CAPS/JOINS streaks that did not end in a reward for this champion
  bank      BWALK + TRIB + CTRIB + BLOCK (walk to altar and tribute channel)
  shop      SHOP + CRECs (recall to shop)
  dead/ret  DEAD + RETR + HEAL + CRECr
  block     turns standing on a camp spawn tile while not capturing (delays that group's respawn)
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ_profile as E  # noqa: E402

MAPS = ["corners", "collect", "lanes", "interlock", "expanse", "packs", "elkring", "monolith", "rows", "collision"]


def load(d, bot):
    # econ_profile.load_games assumes the bot is called prof-tts; patch the name test.
    import re
    d = Path(d)
    log = (d / "run-batch.log").read_text(encoding="utf-8", errors="replace")
    results = defaultdict(list)
    for r in E.RESULT.finditer(log):
        team, winner, a, b, m, rnd = r.groups()
        results[(a, b, m)].append((winner, int(rnd)))
    games, maps = [], {}
    for f in sorted(d.glob("*.repl26a")):
        m = re.match(r"\d+-(.+)-vs-(.+)-([a-z]+)\.repl26a", f.name)
        a, b, mapname = m.groups()
        side = "a" if a == bot or (bot == "prof-*" and a.startswith("prof-")) else "b"
        opp = b if side == "a" else a
        winner, rnd = results[(a, b, mapname)].pop(0)
        g = E.Game(f, side, opp, mapname, (winner == bot, rnd))
        if opp == "zz-idle" and mapname not in maps:
            maps[mapname] = E.MapInfo(g.opp_text, "b" if side == "a" else "a")
        games.append(g)
    return games, maps


def waste(g, mp):
    gmap = E.group_index_map(g, mp)
    caps = E.capture_events(g, mp)
    n = len(g.turns)
    out = Counter()
    ex = E.extra_metrics(g, mp, caps)
    out["futile"] = ex["futile_total"]
    byr = defaultdict(dict)
    for t in g.turns:
        byr[t[0]][t[1]] = t
    for t in g.turns:
        c = t[2]
        if c in ("FOLLOW", "FIDLE"):
            out["follow"] += 1
        elif c in ("FSPAWN", "FALLB"):
            out["spawnfight"] += 1
        elif c in ("BWALK", "TRIB", "CTRIB", "BLOCK", "BWAIT"):
            out["bank"] += 1
        elif c in ("SHOP", "CRECs"):
            out["shop"] += 1
        elif c in ("DEAD", "RETR", "HEAL", "CRECr"):
            out["dead/ret"] += 1
        if c == "HIT" and t[1] in (0, 4):
            di = gmap.get(t[7], -1)
            if di >= 0 and not set(mp.groups[di]["kinds"]) <= set("GO"):
                near = sum(1 for cid, u in byr[t[0]].items() if cid != t[1] and u[2] != "DEAD"
                           and max(abs(u[3] - t[3]), abs(u[4] - t[4])) <= 4)
                if near == 0:
                    out["solo-hit"] += 1
    # capture streaks that earned nothing
    capr = set((c[0], c[1]) for c in g.caps)
    by = defaultdict(list)
    for t in g.turns:
        by[t[1]].append(t)
    for cid, ts in by.items():
        i = 0
        while i < len(ts):
            if ts[i][2] in ("JOINW", "JOINS", "CAPW", "CAPS"):
                j = i
                while j < len(ts) and ts[j][2] in ("JOINW", "JOINS", "CAPW", "CAPS") and ts[j][7] == ts[i][7]:
                    j += 1
                got = any((ts[x][0], cid) in capr for x in range(i, min(j + 1, len(ts))))
                if not got:
                    out["capwaste"] += j - i
                i = j
            else:
                i += 1
    out["block"] = E.blocking_turns(g, mp, gmap, caps)
    return out, n


def main():
    d = sys.argv[1]
    bot = sys.argv[2] if len(sys.argv) > 2 else "prof-tts"
    opp = sys.argv[3] if len(sys.argv) > 3 else "zz-idle"
    games, maps = load(d, bot)
    cats = ["futile", "solo-hit", "follow", "spawnfight", "capwaste", "bank", "shop", "dead/ret", "block"]
    print(f"### {bot} vs {opp}: % of champion turns per waste category (both sides pooled)\n")
    print("| map | end A / B | " + " | ".join(cats) + " |")
    print("|---|---|" + "---|" * len(cats))
    tot, totn = Counter(), 0
    for m in MAPS:
        gs = [g for g in games if g.map == m and g.opp == opp]
        if not gs:
            continue
        mp = maps.get(m)
        if mp is None:
            continue
        agg, nn = Counter(), 0
        for g in gs:
            if g.end_round >= 2000 and opp == "zz-idle":
                continue
            w, n = waste(g, mp)
            agg.update(w)
            nn += n
        tot.update(agg)
        totn += nn
        ends = " / ".join(str(g.end_round) for g in sorted(gs, key=lambda g: g.side))
        print(f"| {m} | {ends} | " + " | ".join(f"{100 * agg[c] / max(1, nn):.0f}" for c in cats) + " |")
    print("| **all** | | " + " | ".join(f"**{100 * tot[c] / max(1, totn):.0f}**" for c in cats) + " |")


if __name__ == "__main__":
    main()
