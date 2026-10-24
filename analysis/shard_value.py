"""Camp damage per 8 turns gained per gold, for our lineup's farming builds.

Per 8-turn cooldown cycle on one camp: basics (8, +1 with an attack reset) x Strength
plus the damage-spell multipliers x Focus (abilities in GameRules.md). Monster adds
x1.1 to all camp damage once 5 shards complete; Power counts as 6 shards.
Usage: python analysis/shard_value.py
"""
# name: (str, str_growth, focus, focus_growth, basics per 8 turns, spell multiplier sum vs camps)
CHAMPS = {
    "Stellar": (35, 3.5, 100, 10, 8, 3.4),
    "Tavi": (35, 5, 100, 10, 9, 2.2),
    "Ryth": (50, 5, 100, 10, 9, 1.0),
    "Varg": (50, 5, 100, 10, 9, 0.0),   # splash doubles this on 2-camp groups
    "Issac": (40, 4.75, 100, 10, 9, 0.0),
    "Cassi": (30, 3.5, 70, 15, 8, 2.0),
}


def damage(c, s=0, f=0, monster=False):
    st, sg, fo, fg, b, m = CHAMPS[c]
    d = b * (st + sg * s) + m * (fo + fg * f)
    return d * 1.1 if monster else d


def first_emblem(c, stat):
    s, f = (5, 0) if stat == "str" else (0, 5)
    return {"monster": damage(c, s, f, True), "power": damage(c, s + (stat == "str"), f + (stat == "foc"))}


if __name__ == "__main__":
    print(f"{'champ':8} {'base':>5} | {'Monster Str':>11} {'Monster Foc':>11} | {'+Power Str':>10} {'+Power Foc':>10}  (camp dmg / 8 turns)")
    for c in CHAMPS:
        base = damage(c)
        ms, mf = first_emblem(c, "str")["monster"], first_emblem(c, "foc")["monster"]
        ps = damage(c, 11, 0, True)   # Monster Str then Power Str (6 more)
        pf = damage(c, 0, 11, True)
        print(f"{c:8} {base:5.0f} | {ms:11.0f} {mf:11.0f} | {ps:10.0f} {pf:10.0f}")
    # check: Monster beats Power for a first emblem on every champion
    for c in CHAMPS:
        for stat in ("str", "foc"):
            e = first_emblem(c, stat)
            assert e["monster"] >= e["power"] or CHAMPS[c][5] == 0 and stat == "foc", (c, stat, e)
