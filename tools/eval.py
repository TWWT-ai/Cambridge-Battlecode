"""Play a bot against an opponent on every map, from both sides, and summarise.

Usage: python tools/eval.py my-bot starter-cpp [map ...]
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAMBC = ROOT / "cambc.exe"
# A fresh folder per run, so tools/errors.py can check just this run's replays.
OUT = ROOT / "matches" / "eval" / time.strftime("%Y%m%d-%H%M%S")


def play(bot_a, bot_b, map_name):
    OUT.mkdir(parents=True, exist_ok=True)
    stats = OUT / f"{bot_a}-vs-{bot_b}-{map_name}.json"
    stats.unlink(missing_ok=True)
    proc = subprocess.run(
        [str(CAMBC), "run", bot_a, bot_b, "--map", map_name,
         "--statistics", str(stats), "-o", str(OUT)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not stats.exists():
        sys.exit(f"match failed ({bot_a} vs {bot_b} on {map_name}):\n{proc.stdout}\n{proc.stderr}")
    return json.loads(stats.read_text())


def main():
    bot, opponent, *maps = sys.argv[1:]
    maps = maps or sorted(p.stem for p in (ROOT / "maps").glob("*.map26a"))
    wins = gems = opp_gems = faults = deaths = 0
    rows = []
    for map_name in maps:
        for side in (0, 1):
            a, b = (bot, opponent) if side == 0 else (opponent, bot)
            s = play(a, b, map_name)
            won = s["outcome"] == ("teamA" if side == 0 else "teamB")
            mine, theirs = s["teams"][side]["submittedGems"], s["teams"][1 - side]["submittedGems"]
            wins += won
            gems += mine
            opp_gems += theirs
            faults += s["botFaults"][side]
            deaths += sum(c["deaths"] for c in s["champions"] if c["team"] == side)
            rows.append(f"{map_name:10} {'A' if side == 0 else 'B'}  {'WIN ' if won else 'loss'}"
                        f"  {mine:5} vs {theirs:5}  round {s['round']}")
    n = len(rows)
    print("\n".join(rows))
    print(f"\n{bot} vs {opponent}: {wins}/{n} wins, avg gems {gems / n:.0f} vs {opp_gems / n:.0f}, "
          f"avg deaths {deaths / n:.1f}, bot faults {faults}")
    print(f"replays: {OUT}")


if __name__ == "__main__":
    main()
