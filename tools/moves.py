"""Summarise SCOUT MOVE step logs (bots/tts-moves) over a league run.

Usage: python tools/moves.py <league dir> <bot>
Per champion and per map: tiles walked per game by purpose, camps captured,
and tiles walked per capture (camp + capture steps / captures).
"""
import glob
import os
import re
import sys
import zipfile
from collections import defaultdict

PURPOSES = ["camp", "capture", "altar", "home", "fight", "follow", "other"]
LINE = re.compile(r"SCOUT MOVE (\d+) (\S+) " + " ".join(rf"{p} (\d+)" for p in PURPOSES)
                  + r" captures (\d+) gems (\d+) gold (\d+)(?: trips((?: \d+/\d+){7}))?")
TRIPS = re.compile(r"(\d+)/(\d+)")


def games(folder, bot):
    for f in glob.glob(os.path.join(folder, "*.repl26a")):
        a, b = os.path.basename(f)[4:].rsplit("-", 1)[0].split("-vs-")
        game_map = os.path.basename(f).rsplit("-", 1)[1][:-8]
        side = "a" if a == bot else "b"
        text = zipfile.ZipFile(f).read(f"team-{side}.stdout").decode("utf-8", "replace")
        last, trips = {}, {}
        for m in LINE.finditer(text):
            last[m.group(2)] = [int(x) for x in m.groups()[2:12]]
            if m.group(13):
                trips[m.group(2)] = [(int(a), int(b)) for a, b in TRIPS.findall(m.group(13))]
        yield game_map, last, trips


def table(title, rows):
    print(f"\n{title}")
    print(f"  {'':10}" + "".join(f"{p:>8}" for p in PURPOSES) + f"{'total':>8}{'captures':>9}{'gems':>6}{'gold':>6}{'tiles/capture':>14}")
    for key, (n, sums) in sorted(rows.items()):
        avg = [s / n for s in sums]
        walk = avg[0] + avg[1]
        per = walk / avg[7] if avg[7] else 0
        print(f"  {key:10}" + "".join(f"{v:8.0f}" for v in avg[:7]) + f"{sum(avg[:7]):8.0f}{avg[7]:9.1f}{avg[8]:6.0f}{avg[9]:6.0f}{per:14.1f}")


def main():
    folder, bot = sys.argv[1], sys.argv[2]
    by_champ = defaultdict(lambda: [0, [0] * 10])
    by_map = defaultdict(lambda: [0, [0] * 10])
    walk = defaultdict(lambda: [[0, 0] for _ in PURPOSES])
    games_per = defaultdict(int)
    for game_map, last, trips in games(folder, bot):
        for champ, t in trips.items():
            games_per[champ] += 1
            for i, (a, b) in enumerate(t):
                walk[champ][i][0] += a
                walk[champ][i][1] += b
        team = [0] * 10
        for champ, vals in last.items():
            row = by_champ[champ]
            row[0] += 1
            row[1] = [x + y for x, y in zip(row[1], vals)]
            team = [x + y for x, y in zip(team, vals)]
        if last:
            by_map[game_map][0] += 1
            by_map[game_map][1] = [x + y for x, y in zip(by_map[game_map][1], team)]
    table("Per champion, average per game (tiles walked by purpose)", by_champ)
    table("Per map, whole team, average per game", by_map)
    if walk:
        print("\nTiles walked vs shortest terrain path for the same trips (actual / shortest per game, extra %)")
        print(f"  {'':10}" + "".join(f"{p:>16}" for p in PURPOSES[:6]) + f"{'all':>16}")
        for champ, rows in sorted(walk.items()):
            n = games_per[champ]
            cells = rows[:6] + [[sum(r[0] for r in rows), sum(r[1] for r in rows)]]
            print(f"  {champ:10}" + "".join(
                f"{a / n:6.0f}/{b / n:4.0f} {100 * (a - b) / b if b else 0:3.0f}%" for a, b in cells))


if __name__ == "__main__":
    main()
