"""Extra per-map analysis for analysis/maps.md (built on map_layout.py + farm_sim.py).

python analysis/maps_extra.py [section ...]   sections: zones plans util rules gank altars monolith (default all)

- zones:    camp groups classified by walking margin (enemy walk - our walk): home >= 10, near 3..9,
            contested -2..2, enemy <= -3; gems in each class; supply cap per class.
- plans:    best plan per map at D=100 and D=60 (half map), both sides (A and B mirror check).
- util:     champion-turn breakdown of the best D100 plan (walk/wait/clear/capture/bank).
- rules:    simple deployable rules evaluated on every map (fixed squad split + bank rule).
- gank:     camps the ENEMY's best plan farms with a solo champion that are close to our own farm loop.
- altars:   which altars each side banks at in its best plan, and walking distance for the other side.
- monolith: rough cost/benefit of monolith groups.
"""
import math
import sys
from collections import defaultdict
import farm_sim as fs
from map_layout import Map, tables, OFFICIAL

SECTIONS = sys.argv[1:] or ["zones", "plans", "util", "rules", "gank", "altars", "monolith"]
D = 100


def zone(margin):
    if margin >= 10:
        return "home"
    if margin >= 3:
        return "near"
    if margin >= -2:
        return "contested"
    return "enemy"


def cache_best():
    out = {}
    for name in OFFICIAL:
        m = Map(name)
        tbA, tbB = tables(m, "A"), tables(m, "B")
        n = m.picks + 1
        out[name] = (m, tbA, tbB, n,
                     fs.best_plan(m, tbA, n, D, "half"),
                     fs.best_plan(m, tbB, n, D, "half"))
    return out


BEST = cache_best()


def visits_by_squad(st, cfg):
    res = defaultdict(lambda: defaultdict(int))
    for (s, g), v in st["visits"].items():
        res[s][g] += v
    return res


if "zones" in SECTIONS:
    print("## zones (A side; B is the mirror)")
    print("| map | size | picks/bodies | altars (A walk) | home | near | contested | enemy-side | supply cap gems/round home+near / +contested |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name in OFFICIAL:
        m, tb, _, n, _, _ = BEST[name]
        cls = defaultdict(list)
        for g, gr in enumerate(m.groups):
            if gr["gems"] == 0:
                continue
            cls[zone(tb["sp_g_other"][g] - tb["sp_g"][g])].append(g)

        def desc(lst):
            if not lst:
                return "-"
            gems = sum(m.groups[g]["gems"] for g in lst)
            kinds = defaultdict(int)
            for g in lst:
                kinds[m.groups[g]["kinds"]] += 1
            return f"{len(lst)} grp/{gems}g ({', '.join(f'{c}x{k}' for k, c in sorted(kinds.items()))})"

        def cap(lst):
            r = 0.0
            for g in lst:
                gr = m.groups[g]
                if "M" in gr["kinds"]:
                    continue
                r += gr["gems"] / (gr["respawn"] + fs.CAP + math.ceil(gr["hp"] / (n * D)))
            return r
        alts = sorted(tb["sp_alt"])
        alt_s = f"{len(m.altars)} ({', '.join(str(a) if a < 10 ** 8 else 'x' for a in alts[:4])}{'...' if len(alts) > 4 else ''})"
        c1 = cap(cls["home"] + cls["near"])
        c2 = c1 + cap(cls["contested"])
        print(f"| {name} | {m.W}x{m.H} | {m.picks}/{n} | {alt_s} | {desc(cls['home'])} | {desc(cls['near'])} | "
              f"{desc(cls['contested'])} | {desc(cls['enemy'])} | {c1:.2f} / {c2:.2f} |")
    print()

if "plans" in SECTIONS:
    print("## theoretical rounds to 1000 (half map), best split/bank per cell; D100 / D60")
    print("| map | bodies(tts) | n=3 | n=4 | n=5 | n=6 | best plan for tts bodies (D100) | A/B mirror |")
    print("|---|---|---|---|---|---|---|---|")
    for name in OFFICIAL:
        m, tbA, tbB, n, bA, bB = BEST[name]
        cells = []
        for k in (3, 4, 5, 6):
            b1 = fs.best_plan(m, tbA, k, 100, "half")
            b2 = fs.best_plan(m, tbA, k, 60, "half")
            cells.append(f"{b1[0] if b1 else '-'} / {b2[0] if b2 else '-'}")
        plan = (f"{bA[0]} r, split {'/'.join(map(str, bA[1]))}, T={bA[2]}{', beta' if bA[3] else ''}"
                if bA else "none (no eligible non-monolith camps)")
        mirror = f"{bA[0]} / {bB[0]}" if bA and bB else "none / none"
        print(f"| {name} | {n} | " + " | ".join(cells) + f" | {plan} | {mirror} |")
    print()

if "util" in SECTIONS:
    print("## champion-turn breakdown of the best D100 plan (share of champion-turns)")
    keys = ["walk_camp", "wait_respawn", "clear", "capture", "walk_altar", "tribute", "recall", "idle"]
    print("| map | " + " | ".join(keys) + " | gems per champion-turn |")
    print("|---|" + "---|" * (len(keys) + 1))
    for name in OFFICIAL:
        m, tb, _, n, b, _ = BEST[name]
        if not b:
            print(f"| {name} | " + " | ".join("-" for _ in keys) + " | n/a |")
            continue
        a = b[4]["acct"]
        tot = sum(a.values())
        print(f"| {name} | " + " | ".join(f"{100 * a.get(k, 0) / tot:.0f}%" for k in keys) +
              f" | {1000 / (b[0] * n):.2f} |")
    print()

if "rules" in SECTIONS:
    print("## simple rules on every map (D100, half map). Cells = rounds to 1000 (ratio to per-map best).")
    rule_sets = {
        "2 squads, bank at once (tts-like)": dict(split="two", T=1, Y=-1),
        "2 squads, T100": dict(split="two", T=100, Y=-1),
        "map best split, bank at once": dict(split="best", T=1, Y=-1),
        "map best split, T50": dict(split="best", T=50, Y=-1),
        "map best split, T100": dict(split="best", T=100, Y=-1),
        "map best split, T100 or altar<=6": dict(split="best", T=100, Y=6),
        "pair + solos, T100": dict(split="pair", T=100, Y=-1),
        "auto split, bank at once": dict(split="auto", T=1, Y=-1),
        "auto split, T50": dict(split="auto", T=50, Y=-1),
        "auto split, T100": dict(split="auto", T=100, Y=-1),
        "auto split, T150": dict(split="auto", T=150, Y=-1),
    }

    def auto_split(m, tb, n):
        """Type-aware split: solos for groups that hit for <= 20 (clusters, single wolves),
        one or two squads (>= the size the heaviest reachable group needs) for the rest."""
        elig = fs.eligible_groups(m, tb, "half")
        light = [g for g in elig if m.groups[g]["str"] <= 20]
        heavy = [g for g in elig if m.groups[g]["str"] > 20]
        if not heavy:
            return tuple([1] * n)
        need = 2
        for g in heavy:
            gr = m.groups[g]
            for k in (2, 3, 4, 5, 6):
                if fs.group_damage(gr, k * D) <= 0.7 * k * fs.HP_BODY:
                    break
            need = max(need, k)
        need = min(need, n)
        solos = max(0, min(n - need, len(light) // 2))
        rest = n - solos
        squads = [rest - rest // 2, rest // 2] if rest >= 2 * need else [rest]
        return tuple(sorted(squads, reverse=True) + [1] * solos)

    def split(kind, n, best_cfg):
        if kind == "two":
            return (math.ceil(n / 2), n // 2)
        if kind == "pair":
            return tuple([2] + [1] * (n - 2))
        if kind == "trio":
            return tuple([3] + [1] * (n - 3))
        if kind == "solo":
            return tuple([1] * n)
        if kind == "auto":
            return None
        return best_cfg

    hdr = "| rule | " + " | ".join(OFFICIAL) + " | sum | mean ratio |"
    print(hdr)
    print("|---|" + "---|" * (len(OFFICIAL) + 2))
    for label, rs in rule_sets.items():
        cells, tot, ratios = [], 0, []
        for name in OFFICIAL:
            m, tb, _, n, b, _ = BEST[name]
            cfg = split(rs["split"], n, b[1] if b else (n,)) or auto_split(m, tb, n)
            elig = fs.eligible_groups(m, tb, "half")
            r, _ = fs.simulate(m, tb, cfg, D, rs["T"], 0, elig, Y=rs["Y"],
                               free_bank=rs["split"] != "two" or rs["T"] > 1)
            if r is None:
                cells.append("none")
                tot += 2000
                if b:
                    ratios.append(2000 / b[0])
                continue
            cells.append(f"{r} ({r / b[0]:.2f})" if b else "n/a")
            tot += r
            if b:
                ratios.append(r / b[0])
        mean = f"{sum(ratios) / len(ratios):.2f}" if ratios else "n/a"
        print(f"| {label} | " + " | ".join(cells) + f" | {tot} | {mean} |")
    print()
    print("auto split per map: " + ", ".join(
        f"{name} {'/'.join(map(str, auto_split(BEST[name][0], BEST[name][1], BEST[name][3])))}" for name in OFFICIAL))
    print("best split per map: " + ", ".join(
        f"{name} {'/'.join(map(str, BEST[name][4][1])) if BEST[name][4] else 'none'}" for name in OFFICIAL))
    print()

if "gank" in SECTIONS:
    print("## gank spots: groups the enemy's best plan farms SOLO, with our walking distance")
    print("| map | enemy solo group | kind | gems | enemy visits | our walk from spawn | from our nearest plan camp | enemy altar walk |")
    print("|---|---|---|---|---|---|---|---|")
    for name in OFFICIAL:
        m, tbA, tbB, n, bA, bB = BEST[name]
        if not bA or not bB:
            continue
        vb = visits_by_squad(bB[4], bB[1])
        va = visits_by_squad(bA[4], bA[1])
        ours = {g for s in va for g in va[s]}
        rows = []
        for s, gs in vb.items():
            if bB[1][s] != 1:
                continue
            for g, v in gs.items():
                near = min(tbA["gg"][o][g] for o in ours) if ours else 10 ** 9
                rows.append((near, g, v))
        seen = set()
        for near, g, v in sorted(rows):
            if g in seen:
                continue
            seen.add(g)
            gr = m.groups[g]
            print(f"| {name} | g{g} {gr['tiles'][0]} | {gr['kinds']} | {gr['gems']} | {v} | {tbA['sp_g'][g]} | {near} | "
                  f"{tbB['g_alt'][g]} to {m.altars[tbB['g_alt_i'][g]]} |")
    print()

if "altars" in SECTIONS:
    print("## altars used by each side's best plan (banks), walking distance from each spawn")
    print("| map | altar | A banks | B banks | A spawn walk | B spawn walk | free sides |")
    print("|---|---|---|---|---|---|---|")
    for name in OFFICIAL:
        m, tbA, tbB, n, bA, bB = BEST[name]
        if not bA or not bB:
            continue
        ca, cb = defaultdict(int), defaultdict(int)
        for b in bA[4]["banks"]:
            ca[b[2]] += 1
        for b in bB[4]["banks"]:
            cb[b[2]] += 1
        for a in sorted(set(ca) | set(cb)):
            zone_tiles = len(m.altar_zone(m.altars[a], "A"))
            print(f"| {name} | {m.altars[a]} | {ca[a]} | {cb[a]} | {tbA['sp_alt'][a]} | {tbB['sp_alt'][a]} | {zone_tiles}/8 |")
    print()

if "monolith" in SECTIONS:
    print("## monolith groups: cost to take with the whole team (no enemy), vs the team's farm rate")
    print("| map | group | gems | hp | our walk | ->altar | D | team dps | hit turns | dmg taken | heal trips | rounds | gems/round | farm rate (best plan) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name in OFFICIAL:
        m, tb, _, n, b, _ = BEST[name]
        for g, gr in enumerate(m.groups):
            if "M" not in gr["kinds"]:
                continue
            for d in (60, 100, 150):
                dps = n * d
                mono_hp = sum(fs.CAMP_HP[k] for k, _, _ in gr["camps"] if k == "M")
                rest_hp = gr["hp"] - mono_hp
                str_ = gr["str"]
                hit = math.ceil(mono_hp / dps)
                dmg = hit * str_
                pool = 0.7 * n * fs.HP_BODY  # spend at most 70% of the team's health per trip
                trips = max(0, math.ceil(dmg / pool) - 1)
                walk = tb["sp_g"][g]
                rounds = walk + hit + math.ceil(rest_hp / dps) + fs.CAP + trips * (5 + walk) + \
                    tb["g_alt"][g] + math.ceil(gr["gems"] / n / 10) + 1
                rate = gr["gems"] / rounds
                farm_rate = f"{1000 / b[0]:.2f}" if b else "n/a"
                print(f"| {name} | g{g} {gr['tiles'][0]} {gr['kinds']} | {gr['gems']} | {gr['hp']} | {walk} | {tb['g_alt'][g]} | {d} | {dps} | "
                      f"{hit} | {dmg} | {trips} | {rounds} | {rate:.2f} | {farm_rate} |")
    print()
