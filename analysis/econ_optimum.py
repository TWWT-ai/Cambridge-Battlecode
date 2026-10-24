"""Rough theoretical optimum for the econ race (no enemy), per map.

Usage: python analysis/econ_optimum.py <league dir containing prof-tts vs zz-idle games>

Map geometry comes from the zz-idle MAPDUMP inside the replays (see econ_profile.py).
Model (deliberately simple, an upper bound on what a farming plan could reach):
- Our draft in pick order: Ryth, Cassi&Issac (2 bodies), Stellar, Tavi, Prism; the first
  team_size bodies play.
- Camp DPS per champion, base stats, no items (basic attack every turn + damage spells
  every 8 turns, one cast per turn):
    Ryth 50+50/8+100/8 = 69, Issac 40+40/8 = 45, Cassi 30+140/8 = 48,
    Stellar 35+(200+140)/8 = 78, Tavi 35+35/8+220/8 = 67, Prism 35+(120+80)/8 = 60.
- Walking = 8-way BFS steps (walls, holes, altars, enemy spawn blocked).
- A unit (1 or 2 champions) clears a group in ceil(hp / dps) turns and takes the camps'
  strength every turn they are alive (strongest camp killed first); if that would drop the
  unit below 30% health it first recalls (5 turns) and walks from spawn; if the group would
  take more than 70% of the unit's health it is never attempted.
- Capture = 6 rounds after the kill. Respawn timer starts at capture.
- Immediate banking: after each capture walk to the nearest altar (BFS) and tribute
  max(1, ceil(bag/10)) + 1 turns; or 'batched': bank only once the bag reaches 48 gems.
- Greedy: each unit picks the group with the best gems / (wait-or-walk + clear + capture + bank)
  that no other unit is working on.
- Modes: 'full' = whole map (what zz-idle allows); 'half' = only groups at least as close
  to our spawn as to theirs (what a contested game realistically allows).
"""
import heapq
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ_profile as E  # noqa: E402

HP = {"W": 1350, "E": 2400, "G": 500, "O": 500, "M": 20000}
STR = {"W": 20, "E": 60, "G": 0, "O": 0, "M": 200}
BODIES = [("ryth", 69, 1200), ("cassi", 48, 700), ("issac", 45, 900), ("stellar", 78, 750),
          ("tavi", 67, 750), ("prism", 60, 700)]


def group_damage(kinds, dps):
    camps = sorted(((HP[k], STR[k]) for k in kinds), key=lambda c: -c[1] / c[0])
    alive = sum(s for _, s in camps)
    dmg = 0.0
    for hp, s in camps:
        dmg += alive * hp / dps
        alive -= s
    return dmg


def tables(mp):
    sp = mp.bfs(mp.our_spawn)
    other = mp.bfs(mp.their_spawn) if mp.their_spawn else {}
    G = len(mp.groups)
    gb = [mp.bfs(list(gr["tiles"])) for gr in mp.groups]
    # per altar: BFS from its stand tiles
    stands = []
    for ax, ay in mp.altars:
        st = [(ax + dx, ay + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if not mp.blocked(ax + dx, ay + dy)]
        stands.append(mp.bfs(st))
    tb = {"g_alt": [], "g_alt_i": [], "sp_g": [], "sp_g_other": [], "gg": [[0] * G for _ in range(G)],
          "alt_g": [[0] * G for _ in range(len(mp.altars))]}
    for i, gr in enumerate(mp.groups):
        best = min(range(len(stands)), key=lambda a: min(stands[a].get(t, 10 ** 6) for t in gr["tiles"]))
        tb["g_alt_i"].append(best)
        tb["g_alt"].append(min(stands[best].get(t, 10 ** 6) for t in gr["tiles"]))
        tb["sp_g"].append(min(sp.get(t, 10 ** 6) for t in gr["tiles"]))
        tb["sp_g_other"].append(min(other.get(t, 10 ** 6) for t in gr["tiles"]) if other else 10 ** 6)
        for j, gr2 in enumerate(mp.groups):
            tb["gg"][i][j] = min(gb[i].get(t, 10 ** 6) for t in gr2["tiles"])
        for a in range(len(stands)):
            tb["alt_g"][a][i] = min(stands[a].get(t, 10 ** 6) for t in gr["tiles"])
    return tb


def simulate(mp, tb, units, eligible, batch=0, horizon=2000, dps_mul=1.0, dmg_mul=1.0):
    G = len(mp.groups)
    ready = [0] * G
    busy = [False] * G
    st = []
    for u in units:
        dps = sum(b[1] for b in u) * dps_mul
        hp = sum(b[2] for b in u)
        st.append({"dps": dps, "hpmax": hp, "hp": hp, "loc": ("S", None), "bag": 0, "n": len(u)})
    heap = [(0, i) for i in range(len(st))]
    pending = []
    tributed = 0
    stats = {"caps": 0, "walk": 0, "bank_walk": 0, "trib": 0, "clear": 0, "recalls": 0}

    def dist_to(loc, g):
        if loc[0] == "S":
            return tb["sp_g"][g]
        if loc[0] == "G":
            return tb["gg"][loc[1]][g]
        return tb["alt_g"][loc[1]][g]  # ("A", altar index)

    while heap:
        t, i = heapq.heappop(heap)
        while pending and pending[0][0] <= t:
            tt, gm = heapq.heappop(pending)
            tributed += gm
            if tributed >= 1000:
                return tt, stats
        if t > horizon:
            return None, stats
        s = st[i]
        if s["loc"][0] == "G":
            busy[s["loc"][1]] = False
        # bank
        if s["bag"] > 0 and s["bag"] >= batch and s["loc"][0] == "G":
            g = s["loc"][1]
            d = tb["g_alt"][g]
            dur = max(1, math.ceil(s["bag"] / s["n"] / 10)) + 1
            heapq.heappush(pending, (t + d + dur, s["bag"]))
            stats["bank_walk"] += d * s["n"]
            stats["trib"] += dur * s["n"]
            s["bag"] = 0
            s["loc"] = ("A", tb["g_alt_i"][g])
            heapq.heappush(heap, (t + d + dur, i))
            continue
        best = None
        for g in eligible:
            if busy[g]:
                continue
            gr = mp.groups[g]
            walk = dist_to(s["loc"], g)
            if walk >= 10 ** 5:
                continue
            hpk = sum(HP[k] for k in gr["kinds"])
            clear = math.ceil(hpk / s["dps"])
            dmg = group_damage(gr["kinds"], s["dps"]) * dmg_mul
            if dmg > 0.7 * s["hpmax"]:
                continue
            recall = False
            start = max(t + walk, ready[g])
            if s["hp"] - dmg < 0.3 * s["hpmax"]:
                recall = True
                start = max(t + 5 + tb["sp_g"][g], ready[g])
            finish = start + clear + 6
            cost = finish - t + (tb["g_alt"][g] if batch == 0 else tb["g_alt"][g] * 0.3)
            val = gr["gems"] / cost
            if best is None or val > best[0]:
                best = (val, g, start, finish, dmg, recall, clear, walk)
        if best is None:
            if s["bag"] > 0 and s["loc"][0] == "G":
                g = s["loc"][1]
                d = tb["g_alt"][g]
                dur = max(1, math.ceil(s["bag"] / s["n"] / 10)) + 1
                heapq.heappush(pending, (t + d + dur, s["bag"]))
                s["bag"] = 0
                s["loc"] = ("A", tb["g_alt_i"][g])
                heapq.heappush(heap, (t + d + dur, i))
            else:
                heapq.heappush(heap, (t + 5, i))
            continue
        _, g, start, finish, dmg, recall, clear, walk = best
        if recall:
            s["hp"] = s["hpmax"]
            stats["recalls"] += 1
        s["hp"] -= dmg
        s["bag"] += mp.groups[g]["gems"]
        s["loc"] = ("G", g)
        busy[g] = True
        ready[g] = finish + mp.groups[g]["respawn"]
        stats["caps"] += 1
        stats["walk"] += walk * s["n"]
        stats["clear"] += clear * s["n"]
        heapq.heappush(heap, (finish, i))
    return None, stats


def eligible_groups(mp, tb, mode):
    out = []
    for g, gr in enumerate(mp.groups):
        if gr["gems"] == 0 or "M" in gr["kinds"]:
            continue
        if mode == "half" and tb["sp_g"][g] > tb["sp_g_other"][g]:
            continue
        out.append(g)
    return out


def plans(n):
    b = BODIES[:n]
    out = {"solo": [[x] for x in b],
           "pairs": [b[i:i + 2] for i in range(0, n, 2)],
           "one team": [b]}
    if n >= 4:
        out["tank+caster pair, rest solo"] = [[b[0], b[3]]] + [[x] for k, x in enumerate(b) if k not in (0, 3)]
    if n >= 5:
        out["trio + pair/solo"] = [[b[0], b[3], b[4]], [b[1], b[2]] + ([b[5]] if n > 5 else [])]
        out["trio + solos"] = [[b[0], b[3], b[4]]] + [[x] for k, x in enumerate(b) if k not in (0, 3, 4)]
    return out


def optimum(mp, n):
    """Best (fewest rounds) over squad plans, for each (map mode, item level, banking rule)."""
    tb = tables(mp)
    res = {}
    for mode in ("full", "half"):
        elig = eligible_groups(mp, tb, mode)
        for items, (dm, hm) in {"base": (1.0, 1.0), "items": (1.3, 0.7)}.items():
            for batch in (0, 48):
                best = None
                for name, units in plans(n).items():
                    r, stats = simulate(mp, tb, units, elig, batch, dps_mul=dm, dmg_mul=hm)
                    if r is not None and (best is None or r < best[0]):
                        best = (r, name, stats)
                res[(mode, items, batch)] = best
    return res


def main():
    games, maps = E.load_games(sys.argv[1])
    out = {}
    for name in E.MAPS:
        mp = maps.get(name)
        if not mp:
            continue
        res = optimum(mp, mp.size)
        out[name] = {f"{k[0]}/{k[1]}/{'bank48' if k[2] else 'banknow'}": (v[0], v[1], v[2]["caps"]) if v else None
                     for k, v in res.items()}
        print(f"== {name} ({mp.size} bodies)")
        for k, v in out[name].items():
            print(f"   {k:28} {v}")
    if "--json" in sys.argv:
        import json
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
