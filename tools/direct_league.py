"""Run a league by invoking cambc run once per match.

Use this on Windows when cambc run-batch's generated CMake paths fail to build.
Usage:
  python tools/direct_league.py BOT [--opps a,b] [--maps map-a,map-b] [--jobs 8] [--tag note]
"""
import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from league import DEFAULT_OPPS, OFFICIAL_MAPS, ROOT, resolve_map

CAMBC = ROOT / "cambc.exe"
WINNER_RE = re.compile(r"finished: round (\d+)/\d+ .*?team([AB])", re.IGNORECASE)
GEMS_RE = re.compile(r"^\s*([AB])\s+(\S+)\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+", re.MULTILINE)


def run_one(item):
    index, bot, opp, map_name, side, out_dir = item
    bot_a, bot_b = (bot, opp) if side == "a" else (opp, bot)
    map_path = resolve_map(map_name)
    tag = f"{index:03d}-{map_name}-{opp}-side-{side}"
    log_path = out_dir / f"{tag}.log"
    cmd = [str(CAMBC), "run", bot_a, bot_b, "--map", str(map_path), "--out-dir", str(out_dir)]
    try:
        attempts = []
        for attempt in range(3):
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=120)
            output = proc.stdout + proc.stderr
            attempts.append(f"--- attempt {attempt + 1} ---\n{output}")
            if proc.returncode == 0:
                break
            # Parallel cambc processes occasionally race while persisting a
            # temporary replay/input file on Windows. Retry only that transient.
            if "failed to persist temporary file" not in output or attempt == 2:
                log_path.write_text("\n".join(attempts), encoding="utf-8")
                return {"index": index, "bot": bot, "opponent": opp, "map": map_name,
                        "side": side, "ok": False, "error": f"exit {proc.returncode}", "log": str(log_path)}
            time.sleep(1)
        output = proc.stdout + proc.stderr
        log_path.write_text("\n".join(attempts), encoding="utf-8")
        winner_match = WINNER_RE.search(output)
        if not winner_match:
            return {"index": index, "bot": bot, "opponent": opp, "map": map_name,
                    "side": side, "ok": False, "error": "could not parse winner", "log": str(log_path)}
        winner_side = winner_match.group(2).lower()
        bot_side = "a" if bot_a == bot else "b"
        score_by_side = {m.group(1).lower(): int(m.group(3)) for m in GEMS_RE.finditer(output)}
        replay_match = re.search(r"replay bundle: (.+)", output)
        replay = replay_match.group(1).strip() if replay_match else None
        return {"index": index, "bot": bot, "opponent": opp, "map": map_name,
                "side": side, "ok": True, "won": winner_side == bot_side,
                "bot_gems": score_by_side.get(bot_side),
                "opponent_gems": score_by_side.get("b" if bot_side == "a" else "a"),
                "round": int(winner_match.group(1)), "replay": replay, "log": str(log_path)}
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") + (exc.stderr or "")
        log_path.write_text(str(output), encoding="utf-8")
        return {"index": index, "bot": bot, "opponent": opp, "map": map_name,
                "side": side, "ok": False, "error": "timeout after 120 seconds", "log": str(log_path)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bot")
    ap.add_argument("--opps", default=",".join(DEFAULT_OPPS))
    ap.add_argument("--maps", default=",".join(OFFICIAL_MAPS))
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    opponents = args.opps.split(",")
    maps = args.maps.split(",")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    suffix = f"-{args.tag}" if args.tag else ""
    out_dir = ROOT / "matches" / "league" / f"{stamp}-{args.bot}-direct{suffix}"
    out_dir.mkdir(parents=True, exist_ok=False)

    names = list(dict.fromkeys([args.bot] + opponents))
    for name in names:
        build = subprocess.run([str(CAMBC), "build", name], cwd=ROOT,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        if build.returncode:
            print(f"build failed for {name}:\n{build.stdout}\n{build.stderr}", file=sys.stderr)
            return 1

    matches = []
    for opp in opponents:
        for map_name in maps:
            resolve_map(map_name)
            for side in ("a", "b"):
                matches.append((len(matches) + 1, args.bot, opp, map_name, side, out_dir))

    results = []
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = [pool.submit(run_one, item) for item in matches]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            if completed % 25 == 0 or completed == len(matches):
                wins = sum(r.get("won", False) for r in results)
                failed = sum(not r.get("ok", False) for r in results)
                print(f"{completed}/{len(matches)} complete; {wins} wins, {failed} failed", flush=True)

    results.sort(key=lambda r: r["index"])
    totals = {}
    for r in results:
        state = totals.setdefault(r["opponent"], {"wins": 0, "games": 0, "losses": [], "gems": []})
        if r.get("ok"):
            state["games"] += 1
            state["wins"] += int(r.get("won", False))
            if not r.get("won", False):
                state["losses"].append(f"{r['map']}:{r['side']}")
            if r.get("bot_gems") is not None:
                state["gems"].append(r["bot_gems"])

    wins = sum(s["wins"] for s in totals.values())
    games = sum(s["games"] for s in totals.values())
    failed = sum(not r.get("ok", False) for r in results)
    summary = {"bot": args.bot, "tag": args.tag, "dir": str(out_dir), "wins": wins,
               "games": games, "failed": failed, "per_opp": totals, "results": results}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"{args.bot} direct league: {wins}/{games} wins, {failed} failed; {out_dir}")
    for opp in opponents:
        state = totals[opp]
        avg_gems = sum(state["gems"]) / len(state["gems"]) if state["gems"] else 0
        print(f"  {opp:20} {state['wins']:2}/{state['games']:<2} avg gems {avg_gems:5.0f} losses: {' '.join(state['losses'])}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
