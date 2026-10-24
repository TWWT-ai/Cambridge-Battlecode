"""Pure econ-race farming simulator on top of map_layout.py (no enemy interference).

Model (assumptions are restated in analysis/maps.md):
- N bodies split into squads; a squad moves as one unit (dps = size*D, health pool = size*HP_BODY).
- Walking = BFS steps (8-way, walls/holes/altars/enemy spawn blocked). Clear time = ceil(hp / squad dps).
  Capture = 6 rounds after the kill (5-round timer starts at the next capture phase).
  The respawn timer starts when the reward is claimed.
- Camps hit back: each living camp deals its strength per turn until it dies (hardest hitter per hp first).
  A squad starts a camp only if it keeps >=30% health afterwards; otherwise it recalls first
  (5 turns, full heal at spawn) and walks from spawn.
- Banking: walk to the nearest altar (BFS from the camp), tribute ceil(bag_per_member/10) turns + 1.
  Bank when bag >= T, when nothing is available, when tributed+carried >= 1000, or for free while the
  next camp is still respawning (detour fits inside the wait).
- Greedy target choice: max gems / (walk + respawn wait + clear + capture + beta*walk(camp->altar)).
- Monolith groups excluded (see monolith section of maps.md).
- Modes: 'safe' = groups at least 3 steps closer to our spawn than to theirs; 'half' = ties included;
  'all' = the whole map (enemy absent).
"""
import math
import sys
import heapq
from collections import defaultdict
from map_layout import Map, tables, OFFICIAL, HP as CAMP_HP, STR as CAMP_STR

HP_BODY = 850
CAP = 6


def group_damage(g, dps):
    hps = sorted(((CAMP_HP[k], CAMP_STR[k]) for k, _, _ in g["camps"]), key=lambda c: -c[1] / c[0])
    alive_str = sum(s for _, s in hps)
    dmg = 0.0
    for hp, s in hps:
        dmg += alive_str * hp / dps
        alive_str -= s
    return dmg


def simulate(m, tb, squads, D, T, beta, eligible, horizon=2000, trace=False, free_bank=True, cheb_choice=False, Y=-1):
    """Y >= 0: also bank any non-empty bag when the nearest altar is within Y steps of the current camp."""
    G = len(m.groups)
    ready = [0] * G
    claimed = [False] * G
    sq = [{"size": s, "loc": ("S", None), "bag": 0, "hp": s * HP_BODY} for s in squads]
    pending = []
    tributed = 0
    committed = [0]
    heap = [(0, i) for i in range(len(sq))]
    heapq.heapify(heap)
    stats = {"visits": defaultdict(int), "banks": [], "timeline": {}, "recalls": 0, "first_bank": None, "log": [],
             "acct": defaultdict(int)}  # champion-turns per activity (squad size weighted)
    acct = stats["acct"]

    def d_to_group(loc, g):
        if loc[0] == "S":
            return tb["sp_g"][g]
        if loc[0] == "G":
            return tb["gg"][loc[1]][g]
        return tb["alt_g"][loc[1]][g]

    def c_to_group(loc, g):
        if loc[0] == "S":
            return tb["cheb_g"][g]
        if loc[0] == "G":
            return tb["gg_cheb"][loc[1]][g]
        return tb["alt_g_cheb"][loc[1]][g]

    def d_to_altar(loc):
        if loc[0] == "S":
            i = min(range(len(m.altars)), key=lambda a: tb["sp_alt"][a])
            return tb["sp_alt"][i], i
        if loc[0] == "G":
            return tb["g_alt"][loc[1]], tb["g_alt_i"][loc[1]]
        return 0, loc[1]

    while heap:
        t, i = heapq.heappop(heap)
        if t > horizon:
            return None, stats
        while pending and pending[0][0] <= t:
            tt, gm = heapq.heappop(pending)
            tributed += gm
            for mark in (250, 500, 750, 1000):
                if tributed >= mark and mark not in stats["timeline"]:
                    stats["timeline"][mark] = tt
            if tributed >= 1000:
                return tt, stats
        s = sq[i]
        if s["loc"][0] == "G":
            claimed[s["loc"][1]] = False
        carried = sum(x["bag"] for x in sq)
        size = s["size"]
        pool = size * HP_BODY

        def bank():
            dist, a = d_to_altar(s["loc"])
            dur = max(1, math.ceil(s["bag"] / size / 10)) + 1
            done = t + dist + dur
            heapq.heappush(pending, (done, s["bag"]))
            stats["banks"].append((i, s["bag"], a, dist))
            if stats["first_bank"] is None:
                stats["first_bank"] = done
            if trace:
                stats["log"].append(f"t{t} sq{i} bank {s['bag']} at {m.altars[a]} walk {dist} done {done}")
            committed[0] += s["bag"]
            acct["walk_altar"] += dist * size
            acct["tribute"] += dur * size
            s["bag"] = 0
            s["loc"] = ("A", a)
            heapq.heappush(heap, (done, i))

        near = Y >= 0 and s["loc"][0] == "G" and tb["g_alt"][s["loc"][1]] <= Y
        if s["bag"] > 0 and (s["bag"] >= T or near or committed[0] + carried >= 1000):
            bank()
            continue
        best = None
        for g in eligible:
            if claimed[g]:
                continue
            gr = m.groups[g]
            dps = size * D
            walk = d_to_group(s["loc"], g)
            if walk >= 10 ** 8:
                continue
            start = max(t + walk, ready[g])
            if cheb_choice:  # value judged on straight-line distance (like choose_camp), travel is real
                cw = c_to_group(s["loc"], g)
                cstart = max(t + cw, ready[g])
            clear = math.ceil(gr["hp"] / dps)
            dmg = group_damage(gr, dps)
            recall = 0
            if s["hp"] - dmg < 0.3 * pool:
                if dmg > 0.7 * pool:
                    continue
                recall = 5
                start = max(t + recall + tb["sp_g"][g], ready[g])
            finish = start + clear + CAP
            cost = finish - t + beta * tb["g_alt"][g]
            if cheb_choice and not recall:
                cost = cstart + clear + CAP - t + beta * tb["g_alt"][g]
            val = gr["gems"] / cost
            if best is None or val > best[0]:
                best = (val, g, finish, dmg, recall, start)
        if best is None:
            if s["bag"] > 0:
                bank()
            else:
                acct["idle"] += 5 * size
                heapq.heappush(heap, (t + 5, i))
            continue
        _, g, finish, dmg, recall, start = best
        # Free bank: the detour via the altar fits inside the respawn wait.
        if free_bank and s["bag"] > 0 and not recall:
            da, a = d_to_altar(s["loc"])
            dur = max(1, math.ceil(s["bag"] / size / 10)) + 1
            if t + da + dur + tb["alt_g"][a][g] <= start:
                bank()
                continue
        clear_t = math.ceil(m.groups[g]["hp"] / (size * D))
        if recall:
            s["hp"] = pool
            stats["recalls"] += 1
            acct["recall"] += 5 * size
            acct["walk_camp"] += tb["sp_g"][g] * size
            acct["wait_respawn"] += (start - t - 5 - tb["sp_g"][g]) * size
        else:
            w = d_to_group(s["loc"], g)
            acct["walk_camp"] += w * size
            acct["wait_respawn"] += (start - t - w) * size
        acct["clear"] += clear_t * size
        acct["capture"] += CAP * size
        s["hp"] -= dmg
        s["bag"] += m.groups[g]["gems"]
        s["loc"] = ("G", g)
        claimed[g] = True
        ready[g] = finish + m.groups[g]["respawn"]
        stats["visits"][(i, g)] += 1
        if trace:
            stats["log"].append(
                f"t{t} sq{i} -> grp{g} {m.groups[g]['kinds']}{m.groups[g]['tiles'][0]} "
                f"{'(recall) ' if recall else ''}done {finish} bag {s['bag']}")
        heapq.heappush(heap, (finish, i))
    return None, stats


def configs(n):
    out = {tuple([1] * n), tuple([n])}
    if n >= 3:
        out.add(tuple([2] + [1] * (n - 2)))
        out.add(tuple([3] + [1] * (n - 3)))
    if n >= 4:
        out.add(tuple([2, 2] + [1] * (n - 4)))
        out.add(tuple([2] * (n // 2) + [1] * (n % 2)))
    if n >= 5:
        out.add((3, n - 3))
        out.add(tuple([3, 2] + [1] * (n - 5)))
    if n >= 6:
        out.add((3, 3))
        out.add((4, 1, 1))
        out.add((2, 2, 2))
    return sorted(out)


def eligible_groups(m, tb, mode):
    out = []
    for g, gr in enumerate(m.groups):
        if gr["gems"] == 0 or "M" in gr["kinds"]:
            continue
        margin = tb["sp_g_other"][g] - tb["sp_g"][g]
        if mode == "half" and margin < 0:
            continue
        if mode == "safe" and margin < 3:
            continue
        out.append(g)
    return out


THRESHOLDS = (1, 25, 50, 75, 100, 150, 250)


def best_plan(m, tb, n, D, mode, cfgs=None, thresholds=THRESHOLDS, betas=(0, 1), free_bank=True, cheb_choice=False, Ys=(-1,)):
    elig = eligible_groups(m, tb, mode)
    best = None
    for cfg in (cfgs or configs(n)):
        for T in thresholds:
            for beta in betas:
                for Y in Ys:
                    r, st = simulate(m, tb, cfg, D, T, beta, elig, free_bank=free_bank, cheb_choice=cheb_choice, Y=Y)
                    if r is not None and (best is None or r < best[0]):
                        best = (r, cfg, T, beta, st)
                        st["Y"] = Y
    return best


def supply_bound(m, tb, D, n, mode):
    elig = eligible_groups(m, tb, mode)
    rate = 0.0
    for g in elig:
        gr = m.groups[g]
        clear = math.ceil(gr["hp"] / (n * D))
        rate += gr["gems"] / (gr["respawn"] + CAP + clear)
    return rate, len(elig)


def fmt(b):
    if not b:
        return "none"
    return f"{b[0]} {'/'.join(map(str, b[1]))} T{b[2]}{'b' if b[3] else ''}"


if __name__ == "__main__":
    maps = sys.argv[1:] or OFFICIAL
    for name in maps:
        m = Map(name)
        tb = tables(m, "A")
        n_tts = m.picks + 1
        print(f"== {name} picks {m.picks} (tungtungsahur fields {n_tts} bodies)")
        for mode in ("safe", "half", "all"):
            sr, ne = supply_bound(m, tb, 100, n_tts, mode)
            bound = f">= {1000 / sr:.0f} rounds" if sr > 0 else "no modeled gem supply"
            print(f"  [{mode}] {ne} gem groups, supply cap {sr:.2f} gems/round ({bound})")
            for D in (60, 100):
                row = []
                for n in (3, 4, 5, 6):
                    b = best_plan(m, tb, n, D, mode)
                    row.append(f"n{n}: {fmt(b)}")
                print(f"    D{D}  " + " | ".join(row))
