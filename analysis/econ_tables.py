"""Markdown tables for analysis/econ-profile.md from econ_profile.py's JSON.

Usage:
  python analysis/econ_profile.py <league dir> --json prof.json
  python analysis/econ_tables.py prof.json
"""
import json
import sys
from collections import Counter, defaultdict

MAPS = ["corners", "collect", "lanes", "interlock", "expanse", "packs", "elkring", "monolith", "rows", "collision"]
CHAMPS = ["ryth", "issac", "cassi", "stellar", "tavi", "prism"]
# Buckets grouped for the turn breakdown table.
GROUPS = [
    ("walk camp", ["walk_camp"]),
    ("hit camp", ["hit_camp"]),
    ("capture", ["capture", "capture_walk"]),
    ("join cap", ["join_capture"]),
    ("resp wait", ["respawn_wait"]),
    ("walk altar", ["walk_altar"]),
    ("tribute", ["tribute"]),
    ("shop", ["shop_recall"]),
    ("retreat", ["retreat_heal"]),
    ("fight", ["fight", "fight_spawn", "fallback", "hunt"]),
    ("follow", ["follow", "follow_idle", "idle"]),
    ("dead", ["dead"]),
    ("exc/fuel", ["exception", "fuel", "other"]),
]


def pct(d, keys, n):
    return 100.0 * sum(d.get(k, 0) for k in keys) / max(1, n)


def team_turns(r):
    tt = Counter()
    for c, v in r["turns"].items():
        tt.update(v)
    return tt


def main():
    D = json.load(open(sys.argv[1]))
    by = defaultdict(list)
    for r in D:
        by[(r["map"], r["opp"])].append(r)

    for opp in ["zz-idle", "ming_bot"]:
        print(f"\n## vs {opp}: headline economy per map (A / B side)\n")
        print("| map | end round | gems/rd | first trib | caps | bag avg | BWALK turns/trib | cap->altar BFS | shared gem caps | share-waste turns | follow % | block turns | fuel-susp |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for m in MAPS:
            rs = sorted(by.get((m, opp), []), key=lambda r: r["side"])
            if not rs:
                continue
            def f(fn, fmt="{:.0f}"):
                return " / ".join(fmt.format(fn(r)) for r in rs)
            def gpr(r):
                return r["ours"] / max(1, r["end"])
            def first(r):
                return min(r["first_trib"].values()) if r["first_trib"] else 0
            def shared(r):
                n = sum(r["share_hist"].values())
                s = sum(v for k, v in r["share_hist"].items() if int(k) > 1)
                return 100.0 * s / max(1, n)
            def follow(r):
                tt = team_turns(r)
                return pct(tt, ["follow", "follow_idle"], sum(tt.values()))
            print(f"| {m} | {f(lambda r: r['end'])} | {f(gpr, '{:.2f}')} | {f(first)} | {f(lambda r: r['n_caps'])} | "
                  f"{f(lambda r: r['bag_avg'], '{:.1f}')} | {f(lambda r: r['walk_turns_avg'], '{:.1f}')} | "
                  f"{f(lambda r: r.get('cap_altar_bfs_avg', 0), '{:.1f}')} | {f(shared)}% | {f(lambda r: r['shared_waste'])} | "
                  f"{f(follow)} | {f(lambda r: r['block_turns'])} | {f(lambda r: r['fuel_susp'])} |")

        print(f"\n## vs {opp}: team turn breakdown, % of champion turns (both sides pooled)\n")
        print("| map | " + " | ".join(g for g, _ in GROUPS) + " |")
        print("|---|" + "---|" * len(GROUPS))
        tot_all = Counter()
        for m in MAPS:
            rs = by.get((m, opp), [])
            if opp == "zz-idle":
                rs = [r for r in rs if not (r["end"] >= 2000)]  # drop the deadlocked game
            tt = Counter()
            for r in rs:
                tt.update(team_turns(r))
            tot_all.update(tt)
            n = sum(tt.values())
            print(f"| {m} | " + " | ".join(f"{pct(tt, ks, n):.0f}" for _, ks in GROUPS) + " |")
        n = sum(tot_all.values())
        print("| **all** | " + " | ".join(f"**{pct(tot_all, ks, n):.0f}**" for _, ks in GROUPS) + " |")

    # per champion vs idle
    print("\n## vs zz-idle: per-champion gems tributed and turn use (mean of both sides)\n")
    print("| map | champ | gems | share % | first trib | hit % | walk camp % | capture+join % | walk altar+trib % | follow % | other top |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for m in MAPS:
        rs = [r for r in by.get((m, "zz-idle"), []) if r["end"] < 2000]
        if not rs:
            continue
        gems = Counter()
        first = defaultdict(list)
        turns = defaultdict(Counter)
        for r in rs:
            for c, v in r["trib_by_champ"].items():
                gems[c] += v / len(rs)
            for c, v in r["first_trib"].items():
                first[c].append(v)
            for c, v in r["turns"].items():
                turns[c].update(v)
        total = sum(gems.values())
        for c in CHAMPS:
            if c not in turns:
                continue
            t = turns[c]
            n = sum(t.values())
            other = Counter({k: v for k, v in t.items() if k not in (
                "hit_camp", "walk_camp", "capture", "capture_walk", "join_capture", "walk_altar", "tribute", "follow", "follow_idle")})
            ot = ", ".join(f"{k} {100 * v / n:.0f}" for k, v in other.most_common(2) if v / n >= 0.03)
            fr = "/".join(str(x) for x in first[c]) if first[c] else "-"
            print(f"| {m} | {c} | {gems[c]:.0f} | {100 * gems[c] / max(1, total):.0f} | {fr} | {pct(t, ['hit_camp'], n):.0f} | "
                  f"{pct(t, ['walk_camp'], n):.0f} | {pct(t, ['capture', 'capture_walk', 'join_capture'], n):.0f} | "
                  f"{pct(t, ['walk_altar', 'tribute'], n):.0f} | {pct(t, ['follow', 'follow_idle'], n):.0f} | {ot} |")

    print("\n## vs zz-idle: camp availability (gem groups, excl. monolith; only valid with an idle opponent)\n")
    print("| map | gem groups (our half) | avail groups/rd | idle (alive, untargeted) groups/rd | idle in our half/rd | idle gems/rd (our half) | respawn->capture latency | never captured (our half count) |")
    print("|---|---|---|---|---|---|---|---|")
    for m in MAPS:
        rs = sorted([r for r in by.get((m, "zz-idle"), []) if r["end"] < 2000], key=lambda r: r["side"])
        if not rs:
            continue
        def f(fn, fmt="{:.1f}"):
            return " / ".join(fmt.format(fn(r)) for r in rs)
        print(f"| {m} | {rs[0]['n_gem_groups']} ({rs[0]['n_half_groups']}) | {f(lambda r: r['avail_group_rounds_avg'])} | "
              f"{f(lambda r: r['idle_group_rounds_avg'])} | {f(lambda r: r['idle_half_avg'])} | {f(lambda r: r['idle_half_gems_avg'], '{:.0f}')} | "
              f"{f(lambda r: r['respawn_to_capture_latency_avg'], '{:.0f}')} | {f(lambda r: len(r['never_captured']), '{:.0f}')} |")

    print("\n## vs zz-idle: bag-size histogram at tribute start, and futile camp work\n")
    print("| map | tributes | bag sizes (count) | futile turns (failed camp attempts + recovery) | shop-trip turns | deaths |")
    print("|---|---|---|---|---|---|")
    for m in MAPS:
        rs = sorted([r for r in by.get((m, "zz-idle"), []) if r["end"] < 2000], key=lambda r: r["side"])
        if not rs:
            continue
        h = Counter()
        for r in rs:
            h.update({int(k): v for k, v in r["bag_hist"].items()})
        hs = ", ".join(f"{k}:{v}" for k, v in sorted(h.items()))
        print(f"| {m} | {' / '.join(str(r['n_trib']) for r in rs)} | {hs} | {' / '.join(str(r['futile_total']) for r in rs)} | "
              f"{' / '.join(str(r['shop_cost']) for r in rs)} | {' / '.join(str(r['deaths']) for r in rs)} |")


if __name__ == "__main__":
    main()
