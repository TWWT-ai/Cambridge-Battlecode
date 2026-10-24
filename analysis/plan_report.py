"""Per-map farm plans and policy sensitivity (uses farm_sim.py). Prints markdown.

python analysis/plan_report.py [map ...]
"""
import sys
import math
from collections import defaultdict
import farm_sim as fs
from map_layout import Map, tables, OFFICIAL, cheb

D = 100


def plan_details(m, tb, best):
    r, cfg, T, beta, st = best
    lines = [f"best: {r} rounds, squads {'/'.join(map(str, cfg))}, bank threshold T={T}, beta={beta}, "
             f"first tribute r{st['first_bank']}, 250/500/750 at {st['timeline'].get(250)}/{st['timeline'].get(500)}/"
             f"{st['timeline'].get(750)}, recalls {st['recalls']}"]
    for i, size in enumerate(cfg):
        visits = sorted(((v, g) for (s, g), v in st["visits"].items() if s == i), reverse=True)
        banks = [b for b in st["banks"] if b[0] == i]
        alts = defaultdict(int)
        for b in banks:
            alts[m.altars[b[2]]] += 1
        avg = sum(b[1] for b in banks) / len(banks) if banks else 0
        vs = ", ".join(f"g{g} {m.groups[g]['kinds']}{m.groups[g]['tiles'][0]} x{v}" for v, g in visits)
        lines.append(f"  squad {i} (size {size}): {vs}; banks {len(banks)} avg {avg:.0f} gems at "
                     + ", ".join(f"{a} x{c}" for a, c in alts.items()))
    return "\n".join(lines)


def sensitivity(m, tb, n, mode):
    elig = fs.eligible_groups(m, tb, mode)
    out = {}
    # threshold sweep with best config per threshold
    for T in fs.THRESHOLDS:
        b = fs.best_plan(m, tb, n, D, mode, thresholds=(T,))
        out[f"T{T}"] = b[0] if b else None
    b = fs.best_plan(m, tb, n, D, mode, cfgs=[tuple([1] * n)])
    out["all-solo"] = b[0] if b else None
    b = fs.best_plan(m, tb, n, D, mode, cfgs=[(n,)])
    out["one-blob"] = b[0] if b else None
    # two squads like tungtungsahur (3+rest), bank at once
    two = (math.ceil(n / 2), n // 2)
    b = fs.best_plan(m, tb, n, D, mode, cfgs=[two], thresholds=(1,), betas=(0,), free_bank=False)
    out["2 squads, bank at once"] = b[0] if b else None
    b = fs.best_plan(m, tb, n, D, mode, free_bank=False)
    out["no free-bank"] = b[0] if b else None
    b = fs.best_plan(m, tb, n, D, mode, cheb_choice=True)
    out["Chebyshev choice"] = b[0] if b else None
    b = fs.best_plan(m, tb, n, D, mode, cfgs=[two], thresholds=(1,), betas=(0,), free_bank=False, cheb_choice=True)
    out["tts-like (2 squads, T1, Chebyshev)"] = b[0] if b else None
    return out


if __name__ == "__main__":
    for name in (sys.argv[1:] or OFFICIAL):
        m = Map(name)
        tb = tables(m, "A")
        n = m.picks + 1
        print(f"### {name} ({n} bodies, D={D})")
        for mode in ("half", "safe"):
            b = fs.best_plan(m, tb, n, D, mode)
            print(f"[{mode}] " + plan_details(m, tb, b))
        s = sensitivity(m, tb, n, "half")
        print("sensitivity [half]: " + ", ".join(f"{k}={v}" for k, v in s.items()))
        print()
