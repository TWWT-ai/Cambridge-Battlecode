"""Map layout analysis for CAMBC 2026a (reads analysis/map-dumps/<map>.txt written by bots/mp-probe).

Usage: python analysis/map_layout.py [map ...]
Prints, per map: size, picks, spawns, altars, every camp group with BFS walking
distances (8-way moves, walls/holes/altars/enemy spawn blocked) from each spawn,
Chebyshev distance from our spawn, and the walk to the nearest altar.
"""
import sys, math, os
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
DUMPS = os.path.join(HERE, "map-dumps")
# Current published pool (2026-10-17). Keep local-only legacy maps out of the
# default report; their dumps remain available by passing a map name directly.
OFFICIAL = ["ambush", "collision", "contest", "corners", "eight", "elkring", "expanse",
            "fragment", "interlock", "lanes", "monolith", "packs", "pilgrimage", "rows",
            "rushbait_v2", "stampede", "swirl"]
HP = {"W": 1350, "E": 2400, "G": 500, "O": 500, "M": 20000}
STR = {"W": 20, "E": 60, "G": 0, "O": 0, "M": 200}
DIRS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


class Map:
    def __init__(self, name):
        self.name = name
        self.rows, self.groups = [], []
        for line in open(os.path.join(DUMPS, name + ".txt"), encoding="utf-8"):
            line = line.rstrip("\n")
            if line.startswith("MAP"):
                p = line.split()
                self.W, self.H = int(p[1]), int(p[2])
                self.bodies, self.picks, self.sym = int(p[4]), int(p[6]), int(p[8])
            elif line.startswith("ROW"):
                self.rows.append(line.split(" ", 2)[2])
            elif line.startswith("GROUP"):
                p = line.split()
                camps = []
                for tok in p[8:]:
                    k, x, y = tok.split(",")
                    camps.append((k, int(x), int(y)))
                self.groups.append({"id": int(p[1]), "gems": int(p[3]), "gold": int(p[5]),
                                    "respawn": int(p[7]), "camps": camps,
                                    "tiles": [(x, y) for _, x, y in camps],
                                    "kinds": "".join(sorted(k for k, _, _ in camps)),
                                    "hp": sum(HP[k] for k, _, _ in camps),
                                    "str": sum(STR[k] for k, _, _ in camps)})
        self.altars = [(x, y) for y in range(self.H) for x in range(self.W) if self.rows[y][x] == "A"]
        self.spawn = {"A": [(x, y) for y in range(self.H) for x in range(self.W) if self.rows[y][x] == "S"],
                      "B": [(x, y) for y in range(self.H) for x in range(self.W) if self.rows[y][x] == "T"]}
        self._bfs_cache = {}

    def walkable(self, x, y, team):
        if not (0 <= x < self.W and 0 <= y < self.H):
            return False
        c = self.rows[y][x]
        if c in "#oA":
            return False
        if team == "A" and c == "T":
            return False
        if team == "B" and c == "S":
            return False
        return True

    def bfs(self, sources, team):
        key = (tuple(sorted(sources)), team)
        if key in self._bfs_cache:
            return self._bfs_cache[key]
        INF = 10 ** 9
        d = [[INF] * self.W for _ in range(self.H)]
        q = deque()
        for (x, y) in sources:
            if self.walkable(x, y, team) and d[y][x] == INF:
                d[y][x] = 0
                q.append((x, y))
        while q:
            x, y = q.popleft()
            nd = d[y][x] + 1
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if self.walkable(nx, ny, team) and d[ny][nx] > nd:
                    d[ny][nx] = nd
                    q.append((nx, ny))
        self._bfs_cache[key] = d
        return d

    def altar_zone(self, a, team):
        ax, ay = a
        return [(ax + dx, ay + dy) for dx, dy in DIRS if self.walkable(ax + dx, ay + dy, team)]

    @staticmethod
    def dmin(d, tiles):
        return min(d[y][x] for x, y in tiles)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def tables(m, team):
    """Distances for one team: spawn->group, group->nearest altar (+which), group->group, altar->group."""
    other = "B" if team == "A" else "A"
    ds = m.bfs(m.spawn[team], team)
    do = m.bfs(m.spawn[other], other)
    zones = [m.altar_zone(a, team) for a in m.altars]
    g_alt, g_alt_i, gg = [], [], []
    for g in m.groups:
        dg = m.bfs(g["tiles"], team)
        best = min(range(len(m.altars)), key=lambda i: m.dmin(dg, zones[i]) if zones[i] else 10 ** 9)
        g_alt.append(m.dmin(dg, zones[best]))
        g_alt_i.append(best)
        gg.append([m.dmin(dg, h["tiles"]) for h in m.groups])
    alt_g = []
    for z in zones:
        dz = m.bfs(z, team) if z else None
        alt_g.append([m.dmin(dz, g["tiles"]) if dz else 10 ** 9 for g in m.groups])
    sp_g = [m.dmin(ds, g["tiles"]) for g in m.groups]
    sp_g_other = [m.dmin(do, g["tiles"]) for g in m.groups]
    sp_alt = [m.dmin(ds, z) if z else 10 ** 9 for z in zones]
    sp_alt_other = [m.dmin(do, z) if z else 10 ** 9 for z in m_altzones(m, other)]
    cheb_g = [min(cheb(s, t) for s in m.spawn[team] for t in g["tiles"]) for g in m.groups]
    gg_cheb = [[min(cheb(a, b) for a in g["tiles"] for b in h["tiles"]) for h in m.groups] for g in m.groups]
    alt_g_cheb = [[min(cheb(z, b) for z in m.altar_zone(a, team) for b in g["tiles"]) if m.altar_zone(a, team) else 10 ** 9
                   for g in m.groups] for a in m.altars]
    return dict(sp_g=sp_g, sp_g_other=sp_g_other, g_alt=g_alt, g_alt_i=g_alt_i, gg=gg, alt_g=alt_g,
                sp_alt=sp_alt, sp_alt_other=sp_alt_other, cheb_g=cheb_g, gg_cheb=gg_cheb, alt_g_cheb=alt_g_cheb)


def m_altzones(m, team):
    return [m.altar_zone(a, team) for a in m.altars]


def describe(name):
    m = Map(name)
    t = tables(m, "A")
    tb = tables(m, "B")
    out = []
    sym = {0: "horizontal mirror", 1: "vertical mirror", 2: "180 rotation"}[m.sym]
    sa, sb = m.spawn["A"], m.spawn["B"]
    out.append(f"## {name}: {m.W}x{m.H}, {m.picks} picks ({sym})")
    out.append(f"spawn A {sa[0]}-{sa[-1]}, spawn B {sb[0]}-{sb[-1]}; altars {len(m.altars)}: " +
               ", ".join(f"{a} (A {t['sp_alt'][i]}, B {tb['sp_alt'][i]})" for i, a in enumerate(m.altars)))
    out.append("| grp | kinds | at | gems | gold | hp | dps-in | resp | A walk | B walk | A cheb | ->altar | altar |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, g in enumerate(m.groups):
        out.append(f"| {i} | {g['kinds']} | {g['tiles'][0]} | {g['gems']} | {g['gold']} | {g['hp']} | {g['str']} | {g['respawn']} | "
                   f"{t['sp_g'][i]} | {t['sp_g_other'][i]} | {t['cheb_g'][i]} | {t['g_alt'][i]} | {m.altars[t['g_alt_i'][i]]} |")
    return "\n".join(out)


if __name__ == "__main__":
    for n in (sys.argv[1:] or OFFICIAL):
        print(describe(n))
        print()
