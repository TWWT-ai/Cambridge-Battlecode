"""Forensics of the 5 lost platform matches against the top player (see analysis/forensics.md).

Usage: python analysis/forensics.py [section ...]
Sections: platform, mapid, decomp, pace, ming, v4diag (default: all but v4diag)

Inputs
- matches/platform-logs/<id>/team-a.stdout   our old bot's SCORE trace (team A), every 5 rounds
- matches/forensics/run1/*.repl26a           opp-tts-v2 / opp-tts-v4 (platform-era versions) as team A
                                              vs ming_bot / Faisal-bot / starter-cpp on the 10 official maps
- matches/league/20261015-085651-tungtungsahur ming_bot vs current tungtungsahur, both sides, 10 maps
- matches/forensics/v4diag/*.repl26a          fx-v4diag (opp-tts-v4 + DIAG trace) as team A (optional)
- analysis/map-dumps/<map>.txt               camp groups (gems per group) and team size per map

A tribute "event" is a change of a team's tributed total between two SCORE samples (5 rounds),
so one event can be the sum of several champions' tributes.
"""
import glob
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = ["collect", "collision", "corners", "elkring", "expanse", "interlock", "lanes", "monolith", "packs", "rows"]
PLATFORM = ["069a8cb7", "1ab06080", "2be0e2c1", "51e36018", "e8446c17"]
SCORE = re.compile(r"SCORE (\d+) (\d+) (\d+)")


# ---------------------------------------------------------------- loading
def parse_stdout(text):
    """-> (trace [(round, ours, theirs)], errors [(after_round, msg)], diag lines)"""
    text = text.replace("\x00", "")
    tr, errs, diag = [], [], []
    last = 0
    for line in text.splitlines():
        line = line.strip()
        m = SCORE.match(line)
        if m:
            last = int(m.group(1))
            tr.append((last, int(m.group(2)), int(m.group(3))))
        elif line.startswith("bot error"):
            errs.append((last, line))
        elif line.startswith("DIAG"):
            diag.append(line)
    return tr, errs, diag


def load_platform():
    out = {}
    for d in sorted(glob.glob(os.path.join(ROOT, "matches", "platform-logs", "*"))):
        if not os.path.isdir(d):
            continue
        key = os.path.basename(d)[:8]
        text = open(os.path.join(d, "team-a.stdout"), "rb").read().decode("utf-8", "replace")
        out[key] = parse_stdout(text)
    return out


def load_replay(path, side="a"):
    with zipfile.ZipFile(path) as z:
        return parse_stdout(z.read(f"team-{side}.stdout").decode("utf-8", "replace"))


def events(tr, idx):
    """idx 0 = ours, 1 = theirs -> [(round, gain)]"""
    ev, prev = [], 0
    for r, *v in tr:
        if v[idx] != prev:
            ev.append((r, v[idx] - prev))
            prev = v[idx]
    return ev


def load_local_old():
    """{(version, opp, map): trace} for opp-tts-v2 / v4 as team A."""
    runs = {}
    for f in glob.glob(os.path.join(ROOT, "matches", "forensics", "run1", "*.repl26a")):
        m = re.match(r"(opp-tts-v\d)-vs-(.+)-(\w+)\.repl26a", os.path.basename(f))
        if m:
            runs[(m.group(1), m.group(2), m.group(3))] = load_replay(f)[0]
    return runs


def load_map(name):
    groups, picks = [], 0
    for line in open(os.path.join(ROOT, "analysis", "map-dumps", name + ".txt"), encoding="utf-8"):
        p = line.split()
        if p and p[0] == "MAP":
            picks = int(p[6])
        elif p and p[0] == "GROUP":
            kinds = "".join(t[0] for t in p[8:])
            groups.append((kinds, int(p[3])))
    return picks, groups


# ---------------------------------------------------------------- helpers
def shares(name, max_split):
    """Gem amounts one champion can receive from one capture on this map."""
    picks, groups = load_map(name)
    s = set()
    for kinds, g in groups:
        if g <= 0:
            continue
        for k in range(1, min(max_split, picks) + 1):
            s.add(g // k)
            s.add(g // k + g % k)
    return sorted(s)


def min_coins(d, coins, cap=6):
    best = [0] + [99] * d
    for v in range(1, d + 1):
        for c in coins:
            if c <= v and best[v - c] + 1 < best[v]:
                best[v] = best[v - c] + 1
    return best[d] if best[d] <= cap else None


def decompositions(d, coins, max_terms=3):
    """All multisets (sorted tuples) of <= max_terms coins that sum to d."""
    res = set()

    def rec(rem, start, cur):
        if rem == 0:
            res.add(tuple(cur))
            return
        if len(cur) == max_terms:
            return
        for i in range(start, len(coins)):
            if coins[i] <= rem:
                rec(rem - coins[i], i, cur + [coins[i]])

    rec(d, 0, [])
    return sorted(res, key=len)


def at_round(tr, r, idx):
    v = 0
    for rr, *x in tr:
        if rr > r:
            break
        v = x[idx]
    return v


def first_round_reaching(tr, idx, target):
    for r, *x in tr:
        if x[idx] >= target:
            return r
    return None


def fmt_ev(ev):
    return " ".join(f"r{r}:+{d}" for r, d in ev)


# ---------------------------------------------------------------- sections
def sec_platform(P):
    print("## Platform matches (team A = our old bot)\n")
    print("| match | end | ours | theirs | our 1st trib | their 1st trib | our events | their events | errors |")
    print("|---|---|---|---|---|---|---|---|---|")
    for k in PLATFORM:
        tr, errs, _ = P[k]
        eo, et = events(tr, 0), events(tr, 1)
        ec = Counter(re.sub(r"\d+", "N", e[1]) for e in errs)
        er = f"{len(errs)} (r{errs[0][0]}-r{errs[-1][0]})" if errs else "0"
        print(f"| {k} | {tr[-1][0]} | {tr[-1][1]} | {tr[-1][2]} | {eo[0][0] if eo else '-'} | {et[0][0]} | "
              f"{len(eo)} | {len(et)} | {er} |")
    print()
    for k in PLATFORM:
        tr, errs, _ = P[k]
        if errs:
            per = Counter(e[0] for e in errs)
            print(f"{k} errors per 5-round window: " + " ".join(f"r{r}:{n}" for r, n in sorted(per.items())))
    print()


def sec_mapid(P, L):
    print("## Map identification\n")
    print("Score columns per map: `pre` = longest common prefix of OUR (round, gain) events with any local old-bot run "
          "on that map (rounds within +-5); `oursOK`/`theirOK` = share of platform events explainable as <=2 "
          "single-capture shares on that map (split <=2); `1st` = |our first tribute - closest local first tribute|; "
          "`set` = share of our platform gain values seen in local runs on that map.\n")
    for k in PLATFORM:
        tr = P[k][0]
        eo, et = events(tr, 0), events(tr, 1)
        rows = []
        for m in MAPS:
            coins = shares(m, 2)
            ok_o = sum(1 for _, d in eo if (min_coins(d, coins) or 9) <= 2) / max(1, len(eo))
            ok_t = sum(1 for _, d in et if (min_coins(d, coins) or 9) <= 2) / max(1, len(et))
            best_pre, best_first, vals = 0, 999, set()
            best_run = ""
            for (ver, opp, mm), ltr in L.items():
                if mm != m:
                    continue
                le = events(ltr, 0)
                vals |= {d for _, d in le}
                pre = 0
                for (r1, d1), (r2, d2) in zip(eo, le):
                    if d1 == d2 and abs(r1 - r2) <= 5:
                        pre += 1
                    else:
                        break
                if pre > best_pre:
                    best_pre, best_run = pre, f"{ver} vs {opp}"
                if eo and le:
                    best_first = min(best_first, abs(eo[0][0] - le[0][0]))
            setok = sum(1 for _, d in eo if d in vals) / max(1, len(eo))
            picks, groups = load_map(m)
            whole = {g for _, g in groups if g > 0}
            exact1 = sum(1 for _, d in eo + et if d in whole) / max(1, len(eo) + len(et))
            score = 2 * best_pre + 3 * ok_o + 3 * ok_t + 2 * setok + 6 * exact1 - best_first / 50
            rows.append((score, m, picks, best_pre, best_run, ok_o, ok_t, best_first, setok, exact1))
        rows.sort(reverse=True)
        print(f"### {k}: ours {fmt_ev(eo)}\n")
        print("| map | picks | pre | best prefix run | oursOK | theirOK | 1st | set | exact1 | score |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for score, m, picks, pre, run, oo, ot, fi, so, ex in rows[:5]:
            print(f"| {m} | {picks} | {pre} | {run} | {oo:.2f} | {ot:.2f} | {fi} | {so:.2f} | {ex:.2f} | {score:.1f} |")
        print()


GUESS = {"069a8cb7": "corners", "1ab06080": "packs", "2be0e2c1": "interlock",
         "51e36018": "lanes", "e8446c17": "expanse"}


def sec_decomp(P):
    print("## Their tribute events decomposed into capture shares (on the guessed map)\n")
    for k in PLATFORM:
        m = GUESS[k]
        picks, groups = load_map(m)
        whole = sorted({g for _, g in groups if g > 0})
        tr = P[k][0]
        et, eo = events(tr, 1), events(tr, 0)
        print(f"### {k} on {m} ({picks} picks; whole-group gems {whole})\n")
        print("| round | their gain | fewest whole-group captures | our total then | our gain within +-10 rounds |")
        print("|---|---|---|---|---|")
        for r, d in et:
            dec = decompositions(d, whole, 4)
            ds = " or ".join("+".join(map(str, x)) for x in dec[:2]) if dec else "NOT a sum of <=4 whole groups"
            near = [f"r{r2}:+{d2}" for r2, d2 in eo if abs(r2 - r) <= 10]
            print(f"| {r} | {d} | {ds} | {at_round(tr, r, 0)} | {' '.join(near) or '-'} |")
        sizes = [d for _, d in et]
        print(f"\nevents {len(sizes)}, mean {sum(sizes) / len(sizes):.1f}, median {sorted(sizes)[len(sizes) // 2]}, "
              f"single-group events {sum(1 for d in sizes if d in whole)}/{len(sizes)}\n")


def pace_row(tr, idx):
    ev = events(tr, idx)
    if not ev:
        return None
    end = tr[-1][0]
    w = [at_round(tr, 100, idx), at_round(tr, 200, idx) - at_round(tr, 100, idx),
         at_round(tr, 300, idx) - at_round(tr, 200, idx), tr[-1][1 + idx] - at_round(tr, 300, idx)]
    gaps = [b[0] - a[0] for a, b in zip(ev, ev[1:])]
    mg = sum(gaps) / len(gaps) if gaps else 0
    sd = (sum((g - mg) ** 2 for g in gaps) / len(gaps)) ** 0.5 if gaps else 0
    # steady-state rate between the 2nd event and the last one
    rate = tr[-1][1 + idx] / max(1, end - ev[0][0] + 5)
    return {"first": ev[0][0], "w": w, "end": end, "total": tr[-1][1 + idx], "n": len(ev),
            "meangap": mg, "cv": sd / mg if mg else 0, "rate": rate,
            "r500": first_round_reaching(tr, idx, 500), "maxgap": max(gaps) if gaps else 0}


def sec_pace(P):
    print("## Pace of the top player (theirs) and of us (ours)\n")
    print("| match | map | side | 1st trib | 0-100 | 100-200 | 200-300 | 300-end | end | total | gems/round from 1st trib to end | events | mean gap | gap CV | max gap | r@500 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k in PLATFORM:
        tr = P[k][0]
        for idx, side in ((1, "top"), (0, "us")):
            p = pace_row(tr, idx)
            if not p:
                print(f"| {k} | {GUESS[k]} | {side} | - | 0 | 0 | 0 | 0 | {tr[-1][0]} | 0 | | | | | | |")
                continue
            w = p["w"]
            print(f"| {k} | {GUESS[k]} | {side} | {p['first']} | {w[0]} | {w[1]} | {w[2]} | {w[3]} | {p['end']} | "
                  f"{p['total']} | {p['rate']:.2f} | {p['n']} | {p['meangap']:.1f} | {p['cv']:.2f} | {p['maxgap']} | {p['r500']} |")
    print()


def sec_ming(P, L):
    print("## ming_bot as a proxy: ming's tributed total in our SCORE traces vs the top player\n")
    d = os.path.join(ROOT, "matches", "league", "20261015-085651-tungtungsahur")
    rows = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(d, "*.repl26a"))):
        b = os.path.basename(f)
        m = re.match(r"\d+-(\S+?)-vs-(\S+?)-(\w+)\.repl26a", b)
        a_bot, b_bot, mp = m.group(1), m.group(2), m.group(3)
        side = "a" if a_bot == "tungtungsahur" else "b"
        tr = load_replay(f, side)[0]
        rows[mp].append(("cur-tts", "B" if side == "a" else "A", tr))
    for (ver, opp, mp), tr in L.items():
        if opp == "ming_bot":
            rows[mp].append((ver, "B", tr))
    print("ming's total at r100/200/300/400 (theirs column of the tts trace), first tribute, round reaching 500, "
          "final; one line per game.\n")
    print("| map | vs | ming side | ming 1st | @100 | @200 | @300 | @400 | r@500 | end | ming final | tts final |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for mp in MAPS:
        for who, mside, tr in rows[mp]:
            et = events(tr, 1)
            print(f"| {mp} | {who} | {mside} | {et[0][0] if et else '-'} | {at_round(tr, 100, 1)} | {at_round(tr, 200, 1)} | "
                  f"{at_round(tr, 300, 1)} | {at_round(tr, 400, 1)} | {first_round_reaching(tr, 1, 500)} | {tr[-1][0]} | "
                  f"{tr[-1][2]} | {tr[-1][1]} |")
        for k in PLATFORM:
            if GUESS[k] == mp:
                tr = P[k][0]
                et = events(tr, 1)
                print(f"| **{mp}** | **TOP PLAYER {k}** | B | {et[0][0]} | {at_round(tr, 100, 1)} | {at_round(tr, 200, 1)} | "
                      f"{at_round(tr, 300, 1)} | {at_round(tr, 400, 1)} | {first_round_reaching(tr, 1, 500)} | {tr[-1][0]} | "
                      f"{tr[-1][2]} | {tr[-1][1]} |")
    print()


def sec_local_old(L):
    print("## Local old-bot (team A) results on the guessed maps\n")
    print("| map | version | opp | our 1st | ours@100 | ours@200 | ours@300 | end | ours | theirs | opp 1st |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for m in sorted(set(GUESS.values())):
        for (ver, opp, mm), tr in sorted(L.items()):
            if mm != m:
                continue
            eo, et = events(tr, 0), events(tr, 1)
            print(f"| {m} | {ver} | {opp} | {eo[0][0] if eo else '-'} | {at_round(tr, 100, 0)} | {at_round(tr, 200, 0)} | "
                  f"{at_round(tr, 300, 0)} | {tr[-1][0]} | {tr[-1][1]} | {tr[-1][2]} | {et[0][0] if et else '-'} |")
    print()


def sec_v4diag():
    """Deaths / gem losses / lock trouble of the old bot (fx-v4diag DIAG lines, team A)."""
    d = os.path.join(ROOT, "matches", "forensics", "v4diag")
    print("## fx-v4diag (opp-tts-v4 + DIAG trace) as team A\n")
    print("| game | end | ours-theirs | our 1st trib | captures by r200 | deaths by r200 | deaths total | gems lost on death | "
          "error 42 (first round) | enemy locks seen (status lines) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for f in sorted(glob.glob(os.path.join(d, "*.repl26a"))):
        tr, errs, diag = load_replay(f, "a")
        rnd = lambda l: int(l.split()[1][1:])
        deaths = [l for l in diag if " DIED " in l]
        lost = sum(int(re.search(r"gems_before=(\d+)", l).group(1)) for l in deaths)
        caps = [l for l in diag if " gems " in l and rnd(l) <= 200
                and int(re.search(r"gems (\d+)->(\d+)", l).group(2)) > int(re.search(r"gems (\d+)->", l).group(1))]
        e42 = [e for e in errs if "visible enemy or neutral camp" in e[1]]
        en_locks = [l for l in diag if "LOCKSEEN" in l and "ally=0" in l]
        eo = events(tr, 0)
        name = os.path.basename(f)[len("fx-v4diag-vs-"):-len(".repl26a")]
        print(f"| {name} | {tr[-1][0]} | {tr[-1][1]}-{tr[-1][2]} | {eo[0][0] if eo else '-'} | {len(caps)} | "
              f"{sum(1 for l in deaths if rnd(l) <= 200)} | {len(deaths)} | {lost} | "
              f"{len(e42)}{' (r' + str(e42[0][0]) + ')' if e42 else ''} | {len(en_locks)} |")
    print()


def main():
    want = set(sys.argv[1:]) or {"platform", "mapid", "decomp", "pace", "ming", "local"}
    P = load_platform()
    L = load_local_old() if want & {"mapid", "ming", "local"} else {}
    if "platform" in want:
        sec_platform(P)
    if "mapid" in want:
        sec_mapid(P, L)
    if "local" in want:
        sec_local_old(L)
    if "decomp" in want:
        sec_decomp(P)
    if "pace" in want:
        sec_pace(P)
    if "ming" in want:
        sec_ming(P, L)
    if "v4diag" in want:
        sec_v4diag()


if __name__ == "__main__":
    main()
