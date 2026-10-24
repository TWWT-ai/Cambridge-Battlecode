"""Economy profile of tungtungsahur, from bots/prof-tts instrumentation.

Usage: python analysis/econ_profile.py <league dir with prof-tts games> [--json out.json]

Reads every .repl26a in the league directory, picks prof-tts's stdout (team a or b),
and the zz-idle map dump (MAPDUMP/ROW/GRP lines) from idle games.
Prints per-map tables used in analysis/econ-profile.md.

prof-tts stdout lines (see bots/prof-tts/src/prof.h):
  P round cid cls x y gems gold tgt src fuel_k onspawn [+fuelN]
  CAP round cid group dgems dgold group_gems group_gold x y
  TRIBSTART round cid bag ax ay walk_turns cheb_dist from(x*1000+y) bag_since
  TRIBDONE round cid amount / TRIBFAIL round cid amount
  INIT round cid name x y team_size / GIDX i x y gems gold / SCORE round ours theirs
"""
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict, deque
from pathlib import Path

NAMES = {0: "ryth", 3: "cassi", 4: "issac", 5: "stellar", 6: "prism", 11: "tavi"}
ORDER = [0, 4, 3, 5, 11, 6]
RESULT = re.compile(r"TEAM ([AB]) WIN \((.+?)\)\s+(\S+) vs (\S+)\s+(\S+)\s+Round (\d+)")
MAPS = ["collect", "collision", "corners", "elkring", "expanse", "interlock", "lanes", "monolith", "packs", "rows"]

# Turn class -> bucket used in the report.
BUCKET = {
    "CWALK": "walk_camp", "HIT": "hit_camp", "CAPS": "capture", "CAPW": "capture_walk",
    "JOINS": "join_capture", "JOINW": "join_capture", "RWAIT": "respawn_wait",
    "BWALK": "walk_altar", "BLOCK": "walk_altar", "BWAIT": "walk_altar",
    "TRIB": "tribute", "CTRIB": "tribute",
    "SHOP": "shop_recall", "CRECs": "shop_recall", "HEAL": "retreat_heal", "RETR": "retreat_heal",
    "CRECr": "retreat_heal", "CTP": "other",
    "FIGHT": "fight", "FSPAWN": "fight_spawn", "FALLB": "fallback",
    "FOLLOW": "follow", "FIDLE": "follow_idle", "HUNT": "hunt", "IDLE": "idle",
    "DEAD": "dead", "EXC": "exception", "FUEL": "fuel",
}
BUCKETS = ["walk_camp", "hit_camp", "capture", "capture_walk", "join_capture", "respawn_wait",
           "walk_altar", "tribute", "shop_recall", "retreat_heal", "fight", "fight_spawn", "fallback",
           "follow", "follow_idle", "hunt", "idle", "dead", "exception", "fuel", "other"]


def read_stdout(z, side):
    try:
        return z.read(f"team-{side}.stdout").decode("utf-8", "replace").replace("\x00", "")
    except KeyError:
        return ""


def lines(text):
    for l in text.splitlines():
        l = l.strip()
        if l:
            yield l


# ---------------------------------------------------------------- map dump

class MapInfo:
    def __init__(self, text, idle_side):
        self.rows = []
        self.groups = []
        for l in lines(text):
            p = l.split()
            if p[0] == "MAPDUMP":
                self.W, self.H, self.size = int(p[1]), int(p[2]), int(p[3])
            elif p[0] == "ROW":
                self.rows.append(p[2] if len(p) > 2 else "")
            elif p[0] == "GRP":
                tiles = [tuple(map(int, t.split(","))) for t in p[6].split(";")]
                self.groups.append({"i": int(p[1]), "kinds": p[2], "gems": int(p[3]), "gold": int(p[4]),
                                    "respawn": int(p[5]), "tiles": tiles})
        # 'S' = zz-idle's spawn, 'E' = prof-tts's spawn
        self.altars = [(x, y) for y, r in enumerate(self.rows) for x, c in enumerate(r) if c == "A"]
        self.our_spawn = [(x, y) for y, r in enumerate(self.rows) for x, c in enumerate(r) if c == "E"]
        self.their_spawn = [(x, y) for y, r in enumerate(self.rows) for x, c in enumerate(r) if c == "S"]
        self.by_tile = {}
        for g in self.groups:
            for t in g["tiles"]:
                self.by_tile[t] = g["i"]
        self._bfs = {}

    def blocked(self, x, y):
        if not (0 <= x < self.W and 0 <= y < self.H):
            return True
        c = self.rows[y][x]
        return c in "#oAS"

    def bfs(self, sources):
        key = tuple(sorted(sources))
        if key in self._bfs:
            return self._bfs[key]
        dist = {}
        q = deque()
        for s in sources:
            dist[s] = 0
            q.append(s)
        while q:
            x, y = q.popleft()
            d = dist[(x, y)]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    n = (x + dx, y + dy)
                    if n in dist or self.blocked(*n):
                        continue
                    dist[n] = d + 1
                    q.append(n)
        self._bfs[key] = dist
        return dist

    def altar_stand(self):
        out = set()
        for ax, ay in self.altars:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    t = (ax + dx, ay + dy)
                    if not self.blocked(*t):
                        out.add(t)
        return list(out)

    def dist_to_altar(self, tile):
        d = self.bfs(self.altar_stand())
        return d.get(tile)


# ---------------------------------------------------------------- one game

class Game:
    def __init__(self, path, side, opp, mapname, result):
        self.path, self.side, self.opp, self.map = path, side, opp, mapname
        self.winner_is_us, self.end_round = result
        z = zipfile.ZipFile(path)
        self.text = read_stdout(z, side)
        self.opp_text = read_stdout(z, "b" if side == "a" else "a")
        self.turns = []        # (round, cid, cls, x, y, gems, gold, tgt, src, fuel, onspawn, extra)
        self.caps = []
        self.trib_start = []
        self.trib_done = []
        self.trib_fail = []
        self.init = {}
        self.score = []
        self.errors = Counter()
        for l in lines(self.text):
            p = l.split()
            k = p[0]
            try:
                if k == "P":
                    extra = 0
                    if p[-1].startswith("+fuel"):
                        extra = int(p[-1][5:])
                        p = p[:-1]
                    self.turns.append((int(p[1]), int(p[2]), p[3], int(p[4]), int(p[5]), int(p[6]), int(p[7]),
                                       int(p[8]), p[9], int(p[10]), int(p[11]), extra))
                elif k == "CAP":
                    self.caps.append(tuple(int(v) for v in p[1:]))
                elif k == "TRIBSTART":
                    self.trib_start.append(tuple(int(v) for v in p[1:]))
                elif k == "TRIBDONE":
                    self.trib_done.append(tuple(int(v) for v in p[1:]))
                elif k == "TRIBFAIL":
                    self.trib_fail.append(tuple(int(v) for v in p[1:]))
                elif k == "INIT":
                    self.init[int(p[2])] = (p[3], int(p[4]), int(p[5]), int(p[6]))
                elif k == "SCORE":
                    self.score.append((int(p[1]), int(p[2]), int(p[3])))
                elif "error" in l:
                    self.errors[l[:80]] += 1
            except (ValueError, IndexError):
                self.errors["parse: " + l[:60]] += 1
        self.final_ours = self.score[-1][1] if self.score else 0
        self.final_theirs = self.score[-1][2] if self.score else 0
        tot = sum(t[2] for t in self.trib_done)
        if self.winner_is_us and self.end_round < 2000:
            self.final_ours = max(self.final_ours, 1000)
        self.trib_total = tot


def load_games(d):
    d = Path(d)
    log = (d / "run-batch.log").read_text(encoding="utf-8", errors="replace")
    results = defaultdict(list)
    for r in RESULT.finditer(log):
        team, winner, a, b, m, rnd = r.groups()
        results[(a, b, m)].append((winner, int(rnd)))
    games, maps = [], {}
    for f in sorted(d.glob("*.repl26a")):
        m = re.match(r"\d+-(.+)-vs-(.+)-([a-z]+)\.repl26a", f.name)
        a, b, mapname = m.groups()
        side = "a" if a.startswith("prof-") else "b"
        opp = b if side == "a" else a
        winner, rnd = results[(a, b, mapname)].pop(0)
        g = Game(f, side, opp, mapname, (winner == (a if side == "a" else b), rnd))
        if opp == "zz-idle" and mapname not in maps:
            maps[mapname] = MapInfo(g.opp_text, "b" if side == "a" else "a")
        games.append(g)
    return games, maps


# ---------------------------------------------------------------- metrics

def turn_breakdown(g):
    per = defaultdict(Counter)
    for t in g.turns:
        b = BUCKET.get(t[2], "other")
        per[t[1]][b] += 1
        if t[11]:
            per[t[1]]["fuel"] += t[11]
    return per


def capture_events(g, mp):
    """Deduplicate CAP lines into captures: (round, group) -> list of (cid, dgems, dgold)."""
    caps = defaultdict(list)
    for (r, cid, gi, dg, dgold, gg, ggold, x, y) in g.caps:
        if gi < 0:
            continue
        caps[(r, gi)].append((cid, dg, dgold, gg, ggold))
    return caps


def share_count(entries):
    cid, dg, dgold, gg, ggold = entries[0]
    if gg > 0 and dg > 0:
        return max(1, round(gg / dg))
    if ggold > 0 and dgold > 0:
        return max(1, round(ggold / dgold))
    return len(entries)


def group_index_map(g, mp):
    """prof-tts GIDX index -> map dump index (match by first spawn tile)."""
    out = {}
    for l in lines(g.text):
        p = l.split()
        if p[0] == "GIDX":
            t = (int(p[2]), int(p[3]))
            out[int(p[1])] = mp.by_tile.get(t, -1)
    return out


def analyse(g, mp):
    res = {"map": g.map, "opp": g.opp, "side": g.side, "won": g.winner_is_us, "end": g.end_round,
           "ours": g.final_ours, "theirs": g.final_theirs}
    gmap = group_index_map(g, mp) if mp else {}
    per = turn_breakdown(g)
    res["turns"] = {NAMES.get(c, str(c)): dict(v) for c, v in per.items()}
    # tributes
    starts = g.trib_start
    res["n_trib"] = len(starts)
    res["bag_avg"] = sum(s[2] for s in starts) / len(starts) if starts else 0
    res["bag_hist"] = Counter(s[2] for s in starts)
    res["walk_turns_avg"] = sum(s[5] for s in starts) / len(starts) if starts else 0
    res["walk_dist_avg"] = sum(s[6] for s in starts if s[7] >= 0) / max(1, sum(1 for s in starts if s[7] >= 0))
    # bag age: rounds from first gem to tribute start
    ages = [s[0] - s[8] for s in starts if s[8] > 0]
    res["bag_age_avg"] = sum(ages) / len(ages) if ages else 0
    res["trib_by_champ"] = Counter()
    for (r, cid, amt) in g.trib_done:
        res["trib_by_champ"][NAMES.get(cid, str(cid))] += amt
    res["trib_fail"] = len(g.trib_fail)
    res["first_trib"] = {}
    for (r, cid, amt) in sorted(g.trib_done):
        res["first_trib"].setdefault(NAMES.get(cid, str(cid)), r)
    # captures
    caps = capture_events(g, mp)
    res["n_caps"] = len(caps)
    shares = Counter()
    by_kind = Counter()
    gems_by_kind = Counter()
    shared_gem_caps = 0
    capt_gems_by_champ = Counter()
    for (r, gi), ents in caps.items():
        n = share_count(ents)
        shares[n] += 1
        kind = mp.groups[gmap.get(gi, -1)]["kinds"] if mp and gmap.get(gi, -1) >= 0 else "?"
        by_kind[kind] += 1
        gems_by_kind[kind] += ents[0][3]
        if ents[0][3] > 0 and n > 1:
            shared_gem_caps += 1
        for e in ents:
            capt_gems_by_champ[NAMES.get(e[0], str(e[0]))] += e[1]
    res["share_hist"] = dict(shares)
    res["caps_by_kind"] = dict(by_kind)
    res["gems_by_kind"] = dict(gems_by_kind)
    res["shared_gem_caps"] = shared_gem_caps
    res["captured_by_champ"] = dict(capt_gems_by_champ)
    res["gold_total"] = sum(e[2] for ents in caps.values() for e in ents)
    # walking distance capture -> altar (BFS on the map) for captures that gave gems
    if mp:
        d_alt = []
        for (r, cid, gi, dg, dgold, gg, ggold, x, y) in g.caps:
            if dg > 0:
                d = mp.dist_to_altar((x, y))
                if d is not None:
                    d_alt.append(d)
        res["cap_altar_bfs_avg"] = sum(d_alt) / len(d_alt) if d_alt else 0
    # fuel
    fuels = [t[9] for t in g.turns if t[2] not in ("DEAD", "CTRIB", "CRECs", "CRECr")]
    res["fuel_avg_k"] = sum(fuels) / len(fuels) if fuels else 0
    res["fuel_susp"] = sum(t[11] for t in g.turns)
    res["errors"] = dict(g.errors)
    res.update(extra_metrics(g, mp, caps))
    # respawn blocking: standing on a spawn tile of a group that is not capturable now
    res["block_turns"] = blocking_turns(g, mp, gmap, caps) if mp else 0
    if g.opp == "zz-idle" and mp:
        res.update(idle_camp_time(g, mp, gmap, caps))
    return res


def extra_metrics(g, mp, caps):
    """Futile attack cycles, capture-walk per capture, shared-capture waste, shop-trip cost."""
    by_c = defaultdict(list)
    for t in g.turns:
        by_c[t[1]].append(t)
    cap_turns = defaultdict(set)
    for (r, cid, gi, dg, dgold, gg, ggold, x, y) in g.caps:
        cap_turns[cid].add(r)
    futile = Counter()
    futile_events = Counter()
    shop_cost = Counter()
    for cid, ts in by_c.items():
        buf = []
        i = 0
        while i < len(ts):
            t = ts[i]
            if t[0] in cap_turns[cid] or t[2] in ("TRIB", "CAPS", "JOINS"):
                buf = []
            if t[2] in ("RETR", "DEAD") and (i == 0 or ts[i - 1][2] not in ("RETR", "DEAD", "CRECr", "HEAL")):
                # failure: wasted = buffer (camp work since last success) + the recovery that follows
                camp_buf = [b for b in buf if b[2] in ("CWALK", "HIT", "RWAIT", "CAPW", "FOLLOW", "FIDLE", "FIGHT", "FALLB", "FSPAWN", "JOINW")]
                futile[cid] += len(camp_buf)
                j = i
                while j < len(ts) and ts[j][2] in ("RETR", "DEAD", "CRECr", "HEAL"):
                    j += 1
                futile[cid] += j - i
                futile_events[cid] += 1
                # walking back from spawn after the recovery
                k = j
                while k < len(ts) and ts[k][2] == "CWALK" and k - j < 80 and (k == j or ts[k][10] or True):
                    if ts[k][0] in cap_turns[cid] or ts[k][2] != "CWALK":
                        break
                    k += 1
                buf = []
                i = j
                continue
            if t[2] == "SHOP":
                # recall channel + walk-out from spawn until first non-walk turn
                j = i + 1
                while j < len(ts) and ts[j][2] == "CRECs":
                    j += 1
                k = j
                while k < len(ts) and ts[k][2] in ("CWALK", "FOLLOW", "FIDLE") and ts[k][10] == 1:
                    k += 1
                shop_cost[cid] += k - i
            buf.append(t)
            i += 1
    capw = sum(1 for t in g.turns if t[2] in ("CAPW", "JOINW"))
    shared_waste = 0
    for (r, gi), ents in caps.items():
        n = share_count(ents)
        shared_waste += (n - 1) * 6
    return {"futile_turns": {NAMES.get(c, str(c)): v for c, v in futile.items()},
            "futile_events": {NAMES.get(c, str(c)): v for c, v in futile_events.items()},
            "futile_total": sum(futile.values()), "capw_turns": capw,
            "capw_per_cap": capw / max(1, len(caps)), "shared_waste": shared_waste,
            "shop_cost": sum(shop_cost.values()), "n_turns": len(g.turns),
            "deaths": sum(1 for i, t in enumerate(g.turns) if t[2] == "DEAD" and
                          not any(u[1] == t[1] and u[0] == t[0] - 1 and u[2] == "DEAD" for u in g.turns[max(0, i - 12):i]))}


def blocking_turns(g, mp, gmap, caps):
    """Turns a champion stood on a camp spawn tile while NOT capturing (CWALK/RWAIT/FOLLOW/...).
    With nothing alive there, that delays the group's respawn."""
    n = 0
    for t in g.turns:
        if t[2] in ("CAPS", "JOINS", "CAPW", "JOINW", "HIT", "TRIB", "CTRIB", "DEAD"):
            continue
        if (t[3], t[4]) in mp.by_tile:
            n += 1
    return n


def idle_camp_time(g, mp, gmap, caps):
    """Reconstruct gem-group availability (only valid vs zz-idle: only we capture).
    Alive from round 1 until it is captured; respawns respawn rounds after the capture.
    'Assigned' = some champion's tgt (dump index) is that group this round."""
    end = g.end_round
    G = len(mp.groups)
    cap_rounds = defaultdict(list)
    for (r, gi) in caps:
        di = gmap.get(gi, -1)
        if di >= 0:
            cap_rounds[di].append(r)
    alive = [[False] * (end + 2) for _ in range(G)]
    for i, gr in enumerate(mp.groups):
        r0 = 1
        for c in sorted(cap_rounds[i]) + [end + 1]:
            # alive from r0 until it is cleared; clear time unknown -> alive until the
            # last turn someone targeted it before the capture, approximated by the capture round - 6
            for r in range(r0, min(c - 6, end + 1)):
                if r >= 1:
                    alive[i][r] = True
            r0 = c + gr["respawn"]
    targeted = defaultdict(set)
    for t in g.turns:
        di = gmap.get(t[7], -1)
        if di >= 0:
            targeted[t[0]].add(di)
    gem_groups = [i for i, gr in enumerate(mp.groups) if gr["gems"] > 0 and "M" not in gr["kinds"]]
    ours_d = mp.bfs(mp.our_spawn)
    theirs_d = mp.bfs(mp.their_spawn)
    half = [i for i in gem_groups
            if min(ours_d.get(t, 10 ** 6) for t in mp.groups[i]["tiles"]) <= min(theirs_d.get(t, 10 ** 6) for t in mp.groups[i]["tiles"])]
    idle_half = 0
    idle_half_gems = 0
    for r in range(1, end + 1):
        for i in half:
            if alive[i][r] and i not in targeted[r]:
                idle_half += 1
                idle_half_gems += mp.groups[i]["gems"]
    idle_rounds = 0      # sum over rounds of (#alive unassigned gem groups)
    idle_gem_rounds = 0  # weighted by gems
    avail_rounds = 0
    for r in range(1, end + 1):
        for i in gem_groups:
            if alive[i][r]:
                avail_rounds += 1
                if i not in targeted[r]:
                    idle_rounds += 1
                    idle_gem_rounds += mp.groups[i]["gems"]
    # time from respawn to next capture per group (latency), gem groups only
    lat = []
    for i in gem_groups:
        rs = sorted(cap_rounds[i])
        for a, b in zip(rs, rs[1:]):
            lat.append(b - a - mp.groups[i]["respawn"])
    caps_per_group = {mp.groups[i]["kinds"] + "@" + str(mp.groups[i]["tiles"][0]): len(cap_rounds[i]) for i in gem_groups}
    never = [mp.groups[i]["kinds"] + "@" + str(mp.groups[i]["tiles"][0]) for i in gem_groups if not cap_rounds[i]]
    half_caps = sum(len(cap_rounds[i]) for i in half)
    return {"n_half_groups": len(half), "idle_half_avg": idle_half / max(1, end),
            "idle_half_gems_avg": idle_half_gems / max(1, end), "half_caps": half_caps,
            "total_caps_gem": sum(len(cap_rounds[i]) for i in gem_groups),
            "idle_group_rounds_avg": idle_rounds / max(1, end), "idle_gem_rounds_avg": idle_gem_rounds / max(1, end),
            "avail_group_rounds_avg": avail_rounds / max(1, end),
            "respawn_to_capture_latency_avg": sum(lat) / len(lat) if lat else 0,
            "caps_per_group": caps_per_group, "never_captured": never,
            "n_gem_groups": len(gem_groups)}


def main():
    d = sys.argv[1]
    games, maps = load_games(d)
    out = []
    for g in games:
        out.append(analyse(g, maps.get(g.map)))
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, indent=1, default=str))
    # summary print
    for r in out:
        tt = Counter()
        for c, v in r["turns"].items():
            tt.update(v)
        n = sum(tt.values())
        top = ", ".join(f"{k} {100 * v / n:.0f}%" for k, v in tt.most_common(8))
        print(f"{r['map']:10} {r['opp']:8} {r['side']} won={int(r['won'])} end={r['end']:4} ours={r['ours']:4} "
              f"bag={r['bag_avg']:.1f} walk={r['walk_turns_avg']:.1f} caps={r['n_caps']} shares={r['share_hist']} "
              f"block={r['block_turns']} | {top}")


if __name__ == "__main__":
    main()
