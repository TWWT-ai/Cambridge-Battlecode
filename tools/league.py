"""Play one bot against a league of opponents on every map from both sides.

Usage:
  python tools/league.py tungtungsahur [--opps a,b,c] [--maps m1,m2] [--jobs 16] [--tag note]

Uses `cambc run-batch` (builds each bot once, then runs matches in parallel).
Wins come from run-batch's result lines; final gems come from the candidate's
"SCORE round ours theirs" trace in its stdout (written every 5 rounds).
Each run is saved under matches/league/<timestamp>/ and summarised in
matches/league/history.csv.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import time
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAMBC = ROOT / "cambc.exe"
OFFICIAL_MAPS = ["ambush", "collision", "contest", "corners", "eight", "elkring", "expanse",
                 "fragment", "interlock", "lanes", "monolith", "packs", "pilgrimage", "rows",
                 "rushbait_v2", "stampede", "swirl"]
MAP_FILE_SLUGS = {"rushbait_v2": "rushbait-v2"}
DEFAULT_OPPS = ["Faisal-bot", "opp-fai-melee", "opp-fai-ranged", "opp-fai-mirror",
                "opp-fai-heal", "opp-fai-bruiser", "opp-fai-casters", "opp-fai-vesper",
                "tralalerotrarala", "opp-tts-v2", "opp-tts-v3", "opp-tts-v4", "opp-tts-v5", "opp-tts-locker", "opp-tts-aggro",
                "tungtungsahur-v1", "my-bot", "my-bot-v2", "my-bot-v3", "starter-cpp"]
RESULT = re.compile(r"TEAM ([AB]) WIN \((.+?)\)\s+(\S+) vs (\S+)\s+(\S+)\s+Round (\d+)")
SCORE = re.compile(r"SCORE (\d+) (\d+) (\d+)")


def last_score(bundle: Path, side: str):
    try:
        with zipfile.ZipFile(bundle) as z:
            text = z.read(f"team-{side}.stdout").decode("utf-8", "replace")
    except (KeyError, zipfile.BadZipFile, FileNotFoundError):
        return None
    found = SCORE.findall(text)
    if not found:
        return None
    _, ours, theirs = found[-1]
    return int(ours), int(theirs)


def resolve_map(name: str) -> Path:
    """Resolve a published pool name, including cambc's ID-suffixed filenames."""
    exact = ROOT / "maps" / f"{name}.map26a"
    if exact.is_file():
        return exact
    slug = MAP_FILE_SLUGS.get(name, name)
    slug_exact = ROOT / "maps" / f"{slug}.map26a"
    if slug_exact.is_file():
        return slug_exact
    matches = list((ROOT / "maps").glob(f"{slug}-*.map26a"))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"no local map file found for {name!r}")
    raise RuntimeError(f"multiple local map files found for {name!r}: {matches}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bot")
    ap.add_argument("--opps", default=",".join(DEFAULT_OPPS))
    ap.add_argument("--maps", default=",".join(OFFICIAL_MAPS))
    ap.add_argument("--jobs", type=int, default=18)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    bot, opps, maps = args.bot, args.opps.split(","), args.maps.split(",")

    out = ROOT / "matches" / "league" / (time.strftime("%Y%m%d-%H%M%S") + "-" + bot)
    out.mkdir(parents=True, exist_ok=True)
    matches = []
    lines = []
    map_output_names = {}
    for opp in opps:
        for m in maps:
            map_path = resolve_map(m)
            map_output_names[map_path.stem] = m
            map_output_names[m] = m
            for side in ("a", "b"):
                a, b = (bot, opp) if side == "a" else (opp, bot)
                name = f"{len(matches):03d}-{a}-vs-{b}-{m}.repl26a"
                matches.append({"opp": opp, "map": m, "side": side, "bundle": out / name})
                lines.append(f"../../../bots/{a} ../../../bots/{b} ../../../maps/{map_path.name} {name}")
    manifest = out / "manifest.txt"
    manifest.write_text("\n".join(lines) + "\n")

    # Build every bot first: run-batch's own compile step fails on this machine
    # ("unable to open output file") whenever a source changed.
    def up_to_date(name):
        wasm = ROOT / "bots" / name / ".cambc" / "build" / "bot-injected.wasm"
        if not wasm.exists():
            return False
        newest = max(f.stat().st_mtime for f in (ROOT / "bots" / name / "src").rglob("*") if f.is_file())
        return newest < wasm.stat().st_mtime

    # Opponents that are already built are skipped, so two leagues can run at
    # once without rebuilding the same bot concurrently.
    for name in [bot] + [o for o in opps if not up_to_date(o)]:
        b = subprocess.run([str(CAMBC), "build", name], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if b.returncode != 0:
            print(f"build failed for {name}:")
            for l in [l for l in (b.stdout + b.stderr).splitlines() if "error" in l.lower()][:20]:
                print(l)
            sys.exit(1)

    t0 = time.time()
    output = []
    batch_log = out / "run-batch.log"
    for attempt in range(3):  # Windows sometimes locks a build output for a moment
        output = []
        mode = "w" if attempt == 0 else "a"
        with batch_log.open(mode, encoding="utf-8") as log:
            proc = subprocess.Popen(
                [str(CAMBC), "run-batch", str(manifest), "--jobs", str(args.jobs), "--color", "never"],
                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", bufsize=1)
            completed = 0
            assert proc.stdout is not None
            for line in proc.stdout:
                log.write(line)
                log.flush()  # Keep completed match records if this run is interrupted.
                output.append(line)
                if RESULT.search(line):
                    completed += 1
                    if completed % 250 == 0:
                        print(f"run-batch progress: {completed}/{len(matches)} matches", flush=True)
            proc.wait()
        stdout = "".join(output)
        if RESULT.search(stdout) or "unable to open output file" not in stdout:
            break
        time.sleep(5)
    if "error" in stdout.lower() and not RESULT.search(stdout):
        print("run-batch failed (build error?):")
        for l in [l for l in stdout.splitlines() if "error" in l.lower()][:20]:
            print(l)
        sys.exit(1)
    results = {}
    for r in RESULT.finditer(stdout):
        team, winner, a, b, raw_map, rnd = r.groups()
        m = map_output_names.get(raw_map, raw_map)
        results.setdefault((a, b, m), []).append((winner, int(rnd)))

    per_opp = defaultdict(lambda: {"wins": 0, "games": 0, "ours": 0, "theirs": 0, "scored": 0, "losses": [], "win_rounds": []})
    failed = 0
    games = []
    for mt in matches:
        a, b = (bot, mt["opp"]) if mt["side"] == "a" else (mt["opp"], bot)
        key = (a, b, mt["map"])
        if not results.get(key):
            failed += 1
            continue
        winner, rnd = results[key].pop(0)
        st = per_opp[mt["opp"]]
        st["games"] += 1
        won = winner == bot and (a != b)
        st["wins"] += won
        if won:
            st["win_rounds"].append(rnd)
        score = last_score(mt["bundle"], mt["side"])
        if score:
            st["ours"] += score[0]
            st["theirs"] += score[1]
            st["scored"] += 1
        games.append({"opp": mt["opp"], "map": mt["map"], "side": mt["side"], "won": bool(won), "round": rnd,
                      "score": score})
        if not won:
            st["losses"].append(f"{mt['map']}:{mt['side'].upper()}")

    total_w = sum(s["wins"] for s in per_opp.values())
    total_g = sum(s["games"] for s in per_opp.values())
    print(f"{bot} league ({time.time() - t0:.0f}s, {total_g} games, {failed} failed): {total_w}/{total_g} wins")
    for opp in opps:
        s = per_opp[opp]
        gems = (f"{s['ours'] / s['scored']:.0f} vs {s['theirs'] / s['scored']:.0f}" if s["scored"] else "n/a")
        wr = s["win_rounds"]
        speed = f"win rd {sum(wr) / len(wr):4.0f}" if wr else "win rd  n/a"
        print(f"  {opp:18} {s['wins']:2}/{s['games']:<2}  gems {gems:12}  {speed}  losses: {' '.join(s['losses'])}")
    fam = [o for o in opps if o == "Faisal-bot" or o.startswith("opp-fai")]
    if fam:
        fw = sum(per_opp[o]["wins"] for o in fam)
        fg = sum(per_opp[o]["games"] for o in fam)
        fo = sum(per_opp[o]["ours"] for o in fam)
        ft = sum(per_opp[o]["theirs"] for o in fam)
        fs = sum(per_opp[o]["scored"] for o in fam) or 1
        print(f"  FAISAL FAMILY      {fw}/{fg}  gems {fo / fs:.0f} vs {ft / fs:.0f}")
    summary = {"bot": bot, "tag": args.tag, "dir": str(out), "wins": total_w, "games": total_g,
               "per_opp": {k: {kk: vv for kk, vv in v.items()} for k, v in per_opp.items()}, "game_list": games}
    (out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    hist = ROOT / "matches" / "league" / "history.csv"
    new = not hist.exists()
    with hist.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "bot", "tag", "wins", "games"] + [f"{o}" for o in DEFAULT_OPPS])
        w.writerow([time.strftime("%H:%M:%S"), bot, args.tag, total_w, total_g]
                   + [f"{per_opp[o]['wins']}/{per_opp[o]['games']}" if o in per_opp else "" for o in DEFAULT_OPPS])


if __name__ == "__main__":
    main()
