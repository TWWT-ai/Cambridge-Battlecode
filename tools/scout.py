"""Summarise what tungtungsahur saw of its opponent in a match log.

Usage: python tools/scout.py <log.zip | team-x.stdout | .repl26a> [side a|b]

Reads the SCOUT lines (see scout() in bots/tungtungsahur/src/bot.cpp) and the
SCORE trace, and prints: both drafts, the score race, where each enemy
champion was seen and how much it carried, where enemies tributed, which of
our champions died (bag lost, enemies near), and enemy altar locks.
"""
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


def read_log(path: Path, side: str) -> str:
    if path.suffix in (".zip", ".repl26a"):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith(".stdout")]
            name = f"team-{side}.stdout" if f"team-{side}.stdout" in names else names[0]
            data = z.read(name)
    else:
        data = path.read_bytes()
    return data.decode("utf-8", "replace").replace("\x00", "")


def main():
    path = Path(sys.argv[1])
    side = sys.argv[2] if len(sys.argv) > 2 else "a"
    text = read_log(path, side)
    lines = [l.strip() for l in text.splitlines()]

    for l in lines:
        if l.startswith("SCOUT DRAFT"):
            print(l[len("SCOUT "):])
            break
    scores = [tuple(map(int, m)) for m in re.findall(r"SCORE (\d+) (\d+) (\d+)", text)]
    if scores:
        # The reporter logs its own ally total first, including when it plays B.
        marks = [s for s in scores if s[0] % 100 == 0] + [scores[-1]]
        print("score (round: ours-theirs): " + "  ".join(f"r{r}:{a}-{b}" for r, a, b in marks))

    seen = defaultdict(list)       # enemy name -> [(round, x, y, gems, hp, flags)]
    tributes = defaultdict(int)    # (x, y) of an enemy seen tributing -> count
    deaths = []
    locks = []
    enemy_re = re.compile(r"(\w+)@(-?\d+),(-?\d+):(\d+)/(\d+)([TR]*)")
    for l in lines:
        if l.startswith("SCOUT SEE"):
            head, _, rest = l.partition("|")
            r = int(head.split()[2])
            for name, x, y, gems, hp, flags in enemy_re.findall(rest):
                seen[name].append((r, int(x), int(y), int(gems), int(hp), flags))
                if "T" in flags:
                    tributes[(int(x), int(y))] += 1
        elif l.startswith("SCOUT DEATH"):
            head, _, rest = l.partition("|")
            p = head.split()
            deaths.append((int(p[2]), p[3], int(p[4]), rest.strip()))
        elif l.startswith("SCOUT LOCK"):
            p = l.split()
            locks.append((int(p[2]), p[3]))

    print("\nenemy champions seen (sightings, rounds, mean position, max bag, times tributing/recalling):")
    for name, s in sorted(seen.items(), key=lambda kv: -len(kv[1])):
        xs = sum(v[1] for v in s) / len(s)
        ys = sum(v[2] for v in s) / len(s)
        print(f"  {name:9} {len(s):4}  r{s[0][0]}-r{s[-1][0]}  ~({xs:.0f},{ys:.0f})  max bag {max(v[3] for v in s):3}"
              f"  T{sum('T' in v[5] for v in s)} R{sum('R' in v[5] for v in s)}")
    if tributes:
        print("enemy tribute positions:", ", ".join(f"{x},{y} x{n}" for (x, y), n in sorted(tributes.items(), key=lambda kv: -kv[1])))
    print(f"\nour deaths: {len(deaths)}, gems lost {sum(d[2] for d in deaths)}")
    for r, name, gems, near in deaths:
        print(f"  r{r:4} {name:8} bag {gems:3}  near: {near or '(no enemy in sight: camp or unseen)'}")
    if locks:
        print("\nenemy altar locks seen:", ", ".join(f"r{r} at {t}" for r, t in locks))


if __name__ == "__main__":
    main()
