"""Solo camp-clear and gank-burst calculator for every CAMBC 2026a champion.

python analysis/mechanics_calc.py            # markdown tables (used in analysis/mechanics.md)

Numbers come from GameRules.md / sdk/cpp/cambc.h and were checked with bots/mx-probe-{a,b,c}
against bots/mx-idle on corners (see analysis/mechanics.md, "Verified by experiment"):
- basic attack = Strength; melee may walk and attack, ranged may not; an attack reset gives a 2nd basic.
- one successful cast per turn; each slot recasts every 8 turns; "excludes walking" spells only if not moved.
- a damaging spell and a basic attack can share a turn (ranged too, if it did not move).
- camps hit the nearest champion once per round (strength), starting the round after the first hit;
  a 1-round stun on the camp skips one camp attack. Camps never heal.
- Monster emblem (5 Monster shards): x1.1 to ALL damage vs camps (basic and spells).
- Jungle emblem: x0.7 camp damage taken; Durability: x0.9 all damage taken.
- Varg shield 2.5F for 5 turns absorbs camp hits; Ren retaliates 0.2F per hit taken (also vs camps).
- Vendetta: any kill (camps too) resets both cooldowns.
Model: champion starts in range, all cooldowns ready, full health, no walking during the fight.
"""
import math

# name: (hp, str, foc, hp_g, str_g, foc_g, ranged, kit)
# kit entries: (kind, mult) kinds: dmg (single), aoe (radius 1), stun (single dmg+stun), aoestun,
#              reset, dash, shield, heal, stunonly, enh_reset (reset whose next basic stuns)
CH = {
    "Ryth":     (1200, 50, 100, 100, 5, 10, False, [("aoestun", 1.0), ("reset", 0)]),
    "Vesper":   (900, 45, 100, 100, 5, 10, True, [("reset", 0), ("dash", 0)]),
    "Vendetta": (800, 70, 100, 100, 5, 10, False, [("reset", 0), ("dash", 0)]),
    "Cassi":    (700, 30, 70, 71.25, 3.5, 15, True, [("dmg", 2.0), ("stunonly", 0)]),
    "Issac":    (900, 40, 100, 95, 4.75, 10, False, [("reset", 0), ("dash", 0)]),
    "Stellar":  (750, 35, 100, 75, 3.5, 10, True, [("dmg", 2.0), ("aoe", 1.4)]),
    "Prism":    (700, 35, 80, 75, 3.5, 10, True, [("stun", 1.5), ("aoe", 1.0)]),
    "Marcella": (1200, 45, 50, 100, 5, 10, False, [("enh_reset", 0), ("dmg", 2.0)]),
    "Tavi":     (750, 35, 100, 75, 5, 10, True, [("reset", 0), ("stun", 2.2)]),
    "Willow":   (700, 45, 105, 50, 3, 5, True, [("heal", 3.0), ("reset", 0)]),
    "Ren":      (900, 40, 100, 100, 5, 10, False, [("stun", 1.25), ("dash", 0)]),
    "Varg":     (1000, 50, 100, 100, 5, 10, False, [("reset", 0), ("shield", 2.5)]),
}
CAMPS = {  # name: (hp per camp, str per camp, camps in group, gems, gold, respawn)
    "G": (500, 0, 1, 24, 0, 50),
    "GG": (500, 0, 2, 48, 0, 50),
    "W": (1350, 20, 1, 22, 90, 40),
    "E": (2400, 60, 1, 36, 160, 60),
    "M": (20000, 200, 1, 200, 300, 150),
}


def stats(name, shards):
    hp, s, f, hg, sg, fg, ranged, kit = CH[name]
    hp += hg * shards.get("hp", 0)
    s += sg * shards.get("str", 0)
    f += fg * shards.get("foc", 0)
    if name == "Ryth":
        s += 0.01 * (hp - CH[name][0])
    return hp, s, f, ranged, kit


def solo(name, camp, shards=None, monster=False, jungle=False, limit=400):
    """Turn-by-turn solo fight. Returns (turns, hp_lost, dmg_dealt_by_spells_share)."""
    shards = shards or {}
    hp, s, f, ranged, kit = stats(name, shards)
    chp, cstr, n, *_ = CAMPS[camp]
    camps = [chp] * n
    mult = 1.1 if monster else 1.0
    taken_mult = 0.7 if jungle else 1.0
    cd = [0, 0]
    shield = 0.0
    shield_t = 0
    awake = False
    stunned = False
    enh = False
    lost = 0.0
    turn = 0
    while any(c > 0 for c in camps) and turn < limit:
        turn += 1
        # camp phase: awake camps hit (single target = us); skipped if stunned last turn
        if awake:
            if stunned:
                stunned = False
            else:
                hits = sum(1 for c in camps if c > 0)
                for _ in range(hits):
                    d = cstr * taken_mult
                    a = min(shield, d)
                    shield -= a
                    d -= a
                    lost += d
                    if name == "Ren" and cstr > 0:
                        hit(camps, 0.2 * f * mult, aoe=False)
        if shield_t > 0:
            shield_t -= 1
            if shield_t == 0:
                shield = 0
        # our turn: one cast (best damage spell, else shield if threatened, else reset)
        killed_before = sum(1 for c in camps if c <= 0)
        cast = None
        best = None
        for i, (k, m) in enumerate(kit):
            if cd[i] > 0:
                continue
            if k in ("dmg", "stun") and best is None:
                best = i
            elif k in ("aoe", "aoestun") and best is None:
                best = i
        # prefer the larger damage spell when several are ready
        ready = [i for i, (k, m) in enumerate(kit) if cd[i] == 0 and k in ("dmg", "stun", "aoe", "aoestun")]
        if ready:
            best = max(ready, key=lambda i: kit[i][1] * (min(n, sum(1 for c in camps if c > 0)) if kit[i][0] in ("aoe", "aoestun") else 1))
            k, m = kit[best]
            if k in ("aoe", "aoestun"):
                hit(camps, m * f * mult, aoe=True)
            else:
                hit(camps, m * f * mult, aoe=False)
            if k in ("stun", "aoestun") and cstr > 0:
                stunned = True
            cast = best
        elif name == "Varg" and cstr > 0 and cd[1] == 0:
            shield = 2.5 * f
            shield_t = 5
            cast = 1
        elif name == "Cassi" and cstr > 0 and cd[1] == 0 and awake:
            stunned = True
            cast = 1
        # basic attack(s)
        if any(c > 0 for c in camps):
            basic(camps, s * mult, name)
            awake = True
        if cast is None:
            for i, (k, m) in enumerate(kit):
                if k in ("reset", "enh_reset") and cd[i] == 0 and any(c > 0 for c in camps):
                    basic(camps, s * mult, name)
                    if k == "enh_reset" and cstr > 0:
                        stunned = True
                    cast = i
                    break
        if cast is not None:
            cd[cast] = 8
        awake = True
        # Vendetta: a kill resets both cooldowns
        if name == "Vendetta" and sum(1 for c in camps if c <= 0) > killed_before:
            cd = [0, 0]
        cd = [max(0, c - 1) for c in cd]
    return turn, lost


def hit(camps, dmg, aoe):
    if aoe:
        for i, c in enumerate(camps):
            if c > 0:
                camps[i] = c - dmg
    else:
        for i, c in enumerate(camps):
            if c > 0:
                camps[i] = c - dmg
                return


def basic(camps, dmg, name):
    for i, c in enumerate(camps):
        if c > 0:
            camps[i] = c - dmg
            if name == "Varg":  # splash onto the adjacent camp of the group
                for j, d in enumerate(camps):
                    if j != i and d > 0:
                        camps[j] = d - dmg
                        break
            return


BUILDS = {
    "base": ({}, False, False),
    "+5 Monster(best stat)": (None, True, False),
    "+5 Jungle HP": ({"hp": 5}, False, True),
}


def monster_stat(name):
    # pick the stat whose 5 shards clear a wolf fastest
    best = None
    for st in ("str", "foc"):
        t, _ = solo(name, "W", {st: 5}, monster=True)
        if best is None or t < best[0]:
            best = (t, st)
    return best[1]


def table():
    out = []
    out.append("| champion | HP/Str/Foc | G (500) | GG (1000) | W (1350, str 20) | E (2400, str 60) | M (20000, str 200) |")
    out.append("|---|---|---|---|---|---|---|")
    for name in CH:
        hp, s, f, *_ = stats(name, {})
        cells = []
        for camp in ("G", "GG", "W", "E", "M"):
            t, lost = solo(name, camp)
            dead = lost >= hp
            if camp in ("G", "GG"):
                cells.append(f"{t}")
            else:
                cells.append(f"{t} t, -{lost:.0f} hp" + (" **DIES**" if dead else f" ({lost / hp:.0%})"))
        out.append(f"| {name} | {hp:.0f}/{s:.0f}/{f:.0f} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def build_table():
    out = []
    out.append("| champion | build | GG turns | W turns, hp lost | E turns, hp lost (of max) | wolves per full HP |")
    out.append("|---|---|---|---|---|---|")
    for name in CH:
        for label, (sh, mon, jun) in BUILDS.items():
            if sh is None:
                st = monster_stat(name)
                sh = {st: 5}
                label = f"+5 Monster {st}"
            hp, *_ = stats(name, sh)
            tg, _ = solo(name, "GG", sh, mon, jun)
            tw, lw = solo(name, "W", sh, mon, jun)
            te, le = solo(name, "E", sh, mon, jun)
            per = "inf" if lw <= 0 else f"{hp / lw:.1f}"
            out.append(f"| {name} | {label} | {tg} | {tw}, -{lw:.0f} | {te}, -{le:.0f} of {hp:.0f}{' DIES' if le >= hp else ''} | {per} |")
    # combined builds for the best elk soloists
    for name, sh in (("Ryth", {"hp": 5}), ("Ryth", {"hp": 10}), ("Varg", {"str": 5, "hp": 5}), ("Vendetta", {"str": 5, "hp": 5}),
                     ("Marcella", {"hp": 5, "str": 5})):
        hp, *_ = stats(name, sh)
        te, le = solo(name, "E", sh, monster="str" in sh, jungle=True)
        tw, lw = solo(name, "W", sh, monster="str" in sh, jungle=True)
        out.append(f"| {name} | {sh} jungle{'+monster' if 'str' in sh else ''} | - | {tw}, -{lw:.0f} | {te}, -{le:.0f} of {hp:.0f}{' DIES' if le >= hp else ''} | {'inf' if lw <= 0 else f'{hp / lw:.1f}'} |")
    return "\n".join(out)


def burst():
    """Damage to a champion from full cooldowns, standing in range, over 1/2/3/8 turns."""
    out = ["| champion | turn 1 | 2 turns | 3 turns | 8 turns | stuns in 8 turns |", "|---|---|---|---|---|---|"]
    for name in CH:
        hp, s, f, ranged, kit = stats(name, {})
        cd = [0, 0]
        tot = 0
        rows = []
        stuns = 0
        for t in range(8):
            ready = [i for i, (k, m) in enumerate(kit) if cd[i] == 0 and k in ("dmg", "stun", "aoe", "aoestun")]
            cast = None
            dmg = 0
            if ready:
                i = max(ready, key=lambda i: kit[i][1])
                dmg += kit[i][1] * f
                stuns += kit[i][0] in ("stun", "aoestun")
                cast = i
            elif any(cd[i] == 0 and k == "stunonly" for i, (k, m) in enumerate(kit)):
                cast = [i for i, (k, m) in enumerate(kit) if k == "stunonly"][0]
                stuns += 1
            dmg += s
            if cast is None:
                for i, (k, m) in enumerate(kit):
                    if k in ("reset", "enh_reset") and cd[i] == 0:
                        dmg += s
                        stuns += k == "enh_reset"
                        cast = i
                        break
            if cast is not None:
                cd[cast] = 8
            cd = [max(0, c - 1) for c in cd]
            tot += dmg
            rows.append(tot)
        out.append(f"| {name} | {rows[0]:.0f} | {rows[1]:.0f} | {rows[2]:.0f} | {rows[7]:.0f} | {stuns} |")
    return "\n".join(out)


if __name__ == "__main__":
    print("## Solo clear (turns from first hit to kill; HP lost)\n")
    print(table())
    print("\n## Builds\n")
    print(build_table())
    print("\n## Burst vs a champion (no Durability)\n")
    print(burst())
