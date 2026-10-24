# Map layouts and farm planning (tungtungsahur vs the top player)

Scope note: sections 1–7 preserve the earlier 10-map snapshot. The official pool and several map layouts
have since changed; use the 17-map refresh below for current map decisions. Historical scores and routes
must not be treated as current results.

> **Rules-version warning (21 October 2026):** The 17-map layouts and farm-rate tables were captured on
> 17 October with the older local rules. The 21 October handbook adds/changes camp and champion data,
> so map geometry is only a starting hypothesis; reward totals, clear times, and bank schedules must be
> recomputed from refreshed maps and the current runner. See
> [`game-update-20261021-strategy.md`](game-update-20261021-strategy.md).
Bot folders made for this report: `bots/mp-probe` (layout dump), `bots/mp-trace`, `bots/mp-bank50`,
`bots/mp-bank50h`, `bots/mp-fixspawn`, `bots/mp-proffix`, `bots/mp-solowolf`. No existing bot was modified.

## Current pool refresh (17 October 2026)

`cambc maps pull` refreshed the published pool to 17 maps. Complete layouts are in
`analysis/map-dumps/<map>.txt`; distances are in `analysis/map-layout-20261017.txt`; the summary table
below comes from `analysis/maps-extra-20261017.txt` and `analysis/farm-sim-20261017.txt`. Several maps
whose names stayed the same have different group counts and yields than the old snapshot above.

The zone cap is a theoretical gem supply rate at D100, excluding Monolith groups: home+near camps /
home+near plus contested camps. The plan column is a no-enemy simulation for the half-map, with 100
damage per body per round; it is not a match result and omits enemy pressure, heals, spells, items, and
Monoliths. `bodies` is the simulator's `picks + 1` count (Cassi & Issac count as two bodies).

| Map | Size | Picks / bodies | Zoned supply cap (gems/round) | Half-map D100 plan to 1000 |
|---|---:|---:|---:|---|
| ambush | 100x100 | 5 / 6 | 3.98 / 5.64 | 457 rounds, 3/3, bank at 250 |
| collision | 41x41 | 3 / 4 | 3.61 / 4.49 | 496 rounds, 2/1/1, bank at 250 |
| contest | 50x50 | 5 / 6 | 0.00 / 0.00 | none: only Monoliths award gems; excluded by this model |
| corners | 71x71 | 5 / 6 | 7.07 / 7.07 | 371 rounds, 4/1/1, bank at 150 |
| eight | 41x30 | 5 / 6 | 3.93 / 3.93 | 446 rounds, all 6 together, bank at 75 |
| elkring | 30x30 | 5 / 6 | 2.54 / 2.54 | 463 rounds, 3/3, bank at 150 |
| expanse | 80x80 | 3 / 4 | 7.09 / 7.09 | 547 rounds, 2/1/1, bank at 150 |
| fragment | 30x30 | 3 / 4 | 1.48 / 1.48 | 725 rounds, 2/2, bank at 25 |
| interlock | 40x40 | 4 / 5 | 2.29 / 4.19 | 467 rounds, 3/1/1, bank at 75 |
| lanes | 90x30 | 5 / 6 | 8.28 / 8.28 | 363 rounds, six solo routes, bank at 250 |
| monolith | 50x50 | 5 / 6 | 4.45 / 4.45 | 349 rounds, 2/2/1/1, bank at 150 |
| packs | 31x31 | 3 / 4 | 2.58 / 4.16 | 459 rounds, 3/1, bank at 250 |
| pilgrimage | 50x65 | 5 / 6 | 1.08 / 5.67 | 536 rounds, 2/2/2, bank at 100 |
| rows | 50x50 | 4 / 5 | 3.60 / 3.60 | 451 rounds, 3/2, bank at 150 |
| rushbait_v2 | 30x80 | 4 / 5 | 4.27 / 4.27 | 446 rounds, 2/1/1/1, bank at 250 |
| stampede | 60x50 | 5 / 6 | 0.00 / 3.79 | no feasible half-map plan under the camp-damage safety model |
| swirl | 45x30 | 4 / 5 | 0.00 / 22.94 | 412 rounds, 3/2, bank at 250 |

### Initial strategies for the added maps

- **Ambush:** the 100x100 map has a long approach and only 3 home/near gem groups (298 gems). Start with
  a 3/3 split for the two toughest camp routes; contest the two central gem clusters only with a safe
  return to an altar. Do not spread six bodies across distant empty lanes.
- **Contest:** both 200-gem Monoliths are the only gem sources; gold-only camps do not advance the win
  condition. The ordinary farming model cannot evaluate this map. Experiment 78's Prism / Stellar /
  Cassi & Issac / Ryth / Tavi draft scored 7/8 against four local proxies, versus main's 5/8; keep it
  isolated pending top-team validation. Focus the team on a protected Monolith clear and altar denial.
  Defensive-first items, early Monolith forcing, camp-damage emblems, and tank escort tests scored only
  5–6/8, so retain the candidate's current role builds while testing the next objective-control idea.
- **Eight:** one altar sits at the centre of the 41x30 map. The half-map model favors keeping all six
  bodies together; prioritize the three home-side gem groups, then cross as a group to deny a camp or
  protect a bank.
- **Fragment:** only three home/near gem groups supply 204 gems, so it is a slow economy map. The 2/2
  split with a low 25-gem bank threshold is the model's best route; avoid unsupported deep farming.
- **Pilgrimage:** only one 68-gem group is home, while 328 gems lie in contested groups. A 2/2/2 split
  is the modeled route, but teams should move together through the middle and avoid leaving a carry
  alone on a contested capture.
- **Rushbait v2:** nine home-side camps yield 254 gems, with two distant altars on the 30x80 map. Use
  several independent routes (2/1/1/1 in the model) and bank around 250 rather than making repeated
  small cross-map altar trips.
- **Stampede:** the entire 360-gem source is one contested camp with six elk and six gem clusters.
  The camp-damage model rejects every safe clear, so this map is a single contested objective;
  coordinate a full team clear and protect the carrier. Experiment 78's Prism / Stellar / Cassi & Issac /
  Ryth / Tavi draft scored 8/8 against four local proxies, versus main's 6/8. Keep the draft candidate
  isolated pending live validation.
- **Swirl:** all 18 gem groups (1,728 gems) are in the contested zone, and the two altars are close to
  central camp clusters. The model favors a 3/2 split with 250-gem banks; keep both squads close enough
  to reinforce instead of sending solo champions into the central camps.

The public Mite–Intercontinental Fish group (`dbad7f6f-421b-42a4-91e2-46b125d6e582`) included Packs,
Rows, Rushbait v2, Stampede, and Contest. Mite won Rows and Stampede; Fish won Packs and Rushbait v2.
Contest was reported as a Mite win after 2,000 rounds, but both sides had 0 gems, so exclude it as
evidence of map advantage. Mite drafted Prism / Stellar / Cassi & Issac / Ryth / Tavi on both Stampede
and Contest. These are single-match observations, not per-map win-rate estimates.

## TL;DR

1. **The top player is farming close to the theoretical econ optimum.** A pure econ-race simulator
   (no enemy, our side of the map only, 100 damage per champion per turn) needs 251-463 rounds to 1000
   gems depending on the map. The top player reached ~1000 in 335-475 rounds *while being contested*.
   tungtungsahur needs 1.3-1.8x the optimum even against an idle opponent (table in section 2).
2. **Most of the gap is how the team is split, not banking.** The simulator rebuilt tungtungsahur's
   structure (2 squads, bank right away). It is on average **1.40x** the per-map optimum. A map-aware split
   ("solo farmers on every group that hits for <= 20, squads only as big as the heaviest home camp needs")
   gets 1.21x with immediate banking, and **1.05x** with banking at >=150 gems per squad (section 5).
3. **A deadlock bug shows up on corners, a layout-driven bug.** Champions wait for the
   centre gem cluster to respawn *while standing on its tiles*, and an occupied tile stops the respawn.
   Five champions sat on (36,35)-(41,42) from round ~100 to 2000 (`prof-tts` corners A, 816 gems at r2000).
   A one-line fix (`bots/mp-fixspawn`, bot.cpp:457) gives **corners vs idle 427/463 -> 335/394 rounds**.
   The full league is unchanged at **362/400**. The platform corners loss (96 gems by r400, last tribute r185) fits this bug.
4. **The decisive area differs by map.** It is the corners centre (4 gem groups next to the centre altar), the
   collision single altar (27,20), the packs centre GGOO pair and the interlock altars either side of the
   hole band. Rows, expanse and lanes are pure races (there is little to contest).
5. **Monoliths are never worth it on rows or collect** (0.5-1.5 gems/round vs 2.2-4.0 from farming).
   On the monolith map they only break even at ~150 damage per champion. Use them for denial: one champion on a
   group tile resets the enemy's capture.

## 0. Method and assumptions

- Layout: `bots/mp-probe` (src/bot.cpp:7-50) prints the grid, spawns, altars and every camp group. The
  dumps are in `analysis/map-dumps/<map>.txt`. `analysis/map_layout.py` computes 8-way BFS walking
  distances (walls, holes, altars and the enemy spawn are blocked) from each spawn to each group, and from
  each group to the nearest altar's 8 neighbour tiles. Run `python analysis/map_layout.py` for the full
  per-group tables (all 10 maps, ~290 lines). The key rows are quoted below.
- Plans: `analysis/farm_sim.py`, an event simulator of a pure econ race.
  - Bodies = `team_size()+1`: our draft has Cassi & Issac as one pick and two bodies, so 3/4/5 picks
    mean 4/5/6 bodies.
  - A squad moves as one unit with dps = size x D. Clear time = ceil(hp/dps). Capture = 6 rounds
    (5-round timer + 1). The respawn timer starts at capture.
  - Camps hit back with their strength every turn until they die. A squad attacks only if it keeps >=30%
    health, otherwise it recalls first (5 turns, full heal).
  - Bank = walk to the nearest altar + ceil(bag per member / 10) + 1 turns.
  - Bank when the squad's bag >= T, for free when the altar detour fits inside the next camp's respawn
    wait, or when the bag finishes the game.
  - Greedy target: max gems / (walk + respawn wait + clear + capture).
  - "half" = only groups at least as close to our spawn as to theirs; "safe" = >=3 steps closer.
  - Monolith groups are excluded from the plans (see section 3.11).
- **Damage assumption D:** D100 = 100 damage per champion per turn (the task's baseline; roughly a
  champion with 3-5 shards). D60 = base stats with no items. `analysis/econ_optimum.py` derives these
  from the kits: Ryth 69, Issac 45, Cassi 48, Stellar 78, Tavi 67, Prism 60, average ~61.
  Real games move from D60 towards D100+ as gold is spent, so the truth lies between the two columns.
- Not modelled: enemies, vision (camp state is known), dash and teleport, gold. The simulator gives a
  lower bound for an uncontested half map.
- Sides: every map is symmetric. B's best plan equals A's within 4 rounds (collision 419/415, interlock
  397/400, the rest identical). One plan per map is enough.
- New scripts: `analysis/maps_extra.py` builds the tables in sections 1-5 (output in
  `analysis/extra_results.txt`; runtime ~45 s). `analysis/plan_report.py` writes the per-squad itineraries
  (`analysis/plan_results.txt`). `farm_sim.py` gained turn accounting and an optional "bank if the altar is
  within Y" rule. Its defaults and earlier results are unchanged.

## 1. Layouts at a glance

Zones are the enemy's walk minus our walk to a group: home >= 10, near 3..9, contested -2..2. The
supply cap is the sum of gems/(respawn+capture+clear) over those groups at D100 with tungtungsahur's body
count, so 1000/cap is a hard lower bound on rounds.

| map | size | picks/bodies | altars (our walks) | home | near | contested | supply cap: home+near / +contested (gems/round) |
|---|---|---|---|---|---|---|---|
| collect | 40x40 | 5/6 | 6 (3, 4, 5, 34..) | 11 grp/366g (3E, EE, 3G, GG, 3W) | 5 grp/154g | 6 grp/520g (2E, 2G, 2 monolith) | 8.37 / 10.24 |
| collision | 41x41 | 3/4 | **1 reachable** (27,20) at 21; (39,20) sealed | 6 grp/246g (2E, EGGG, 3W) | - | 2 W next to the altar | 3.74 / 4.62 |
| corners | 71x71 | 5/6 | 5 (19 centre, 31, 33, 53..) | 8 grp/282g (4E, EE, 3W) | EEG, W | **4 GG at the centre altar** | 6.11 / 9.42 |
| elkring | 30x30 | 5/6 | 2, both 23 from **both** spawns | 3 EO | 2 EO | - | 2.54 |
| expanse | 80x80 | 3/4 | 10 (7, 20, 32, 35..) | 9 grp/398g (E, EGGG, 3GG, 3W, WW) | 2 EGGG | - | 9.35 |
| interlock | 40x40 | 4/5 | 4 (17, 22, 33, 33) | GGG + 3W | E | 2E (29/29) | 3.07 / 4.09 |
| lanes | 90x30 | 5/6 | 18 (7, 8, 10, 15..) | 3E + 6G (x=36-39) | 9W (x=42-43) | - | 8.11 |
| monolith | 50x50 | 5/6 | 6 on the diagonal (25, 25, 32, 34..) | E, 3W, 2WW | WW + monolith group | - | 4.45 |
| packs | 31x31 | 3/4 | 6 (3, 12, 21, 25..) | 2 WW | WW | **2 GGOO (15 vs 16)** | 2.49 / 4.06 |
| rows | 50x50 | 4/5 | 2: ours (15,16) at 10, theirs at 62 | 3 WWW | - | GGMM (448 gems, 41k hp) | 3.60 |

Camp facts that drive every plan:
- Gem clusters (G, 500 hp, 0 damage) and single wolves (1350 hp, 20 damage) can be soloed. A solo at
  D100 takes 280 damage from a wolf; at D60, 460.
- Elk (2400 hp, 60 damage) needs >= 2 bodies: a solo at D100 takes 1440 damage. WW (2700/40) needs 2.
  WWW (4050/60) and EGGG (elk first) need 2-3. EE/EEG (4800-5300 hp, 120 damage) need 4.

## 2. Theoretical rounds to 1000 gems vs reality

Theoretical rounds (half map, best split and bank threshold per cell, D100 / D60) by number of bodies
farming in parallel:

| map | n=3 | n=4 | n=5 | n=6 | our bodies | **best plan, D100** (split, bank threshold T) |
|---|---|---|---|---|---|---|
| collect | 371 / 439 | 306 / 413 | 278 / 348 | 251 / 310 | 6 | **251** (2/1/1/1/1, T150) |
| collision | 555 / 785 | 419 / 585 | 371 / 487 | 339 / 414 | 4 | **419** (2/1/1, T75) |
| corners | 505 / 576 | 376 / 487 | 366 / 414 | 318 / 403 | 6 | **318** (3/1/1/1, T250) |
| elkring | 743 / 965 | 560 / 816 | 489 / 778 | 463 / 559 | 6 | **463** (3/3, T150) |
| expanse | 424 / 503 | 338 / 401 | 287 / 317 | 260 / 298 | 4 | **338** (3/1, T250) |
| interlock | 505 / 629 | 450 / 548 | 397 / 483 | 359 / 449 | 5 | **397** (3/1/1, T150) |
| lanes | 425 / 468 | 382 / 440 | 323 / 396 | 297 / 368 | 6 | **297** (2/1/1/1/1, T150) |
| monolith | 647 / 845 | 519 / 665 | 411 / 548 | 349 / 469 | 6 | **349** (2/2/1/1, T150) |
| packs | 545 / 699 | 431 / 552 | 394 / 475 | 368 / 425 | 4 | **431** (2/2, T250) |
| rows | 672 / 937 | 591 / 714 | 451 / 651 | 416 / 597 | 5 | **451** (3/2, T150) |

The whole map (enemy idle, every group allowed) is 10-25% faster on maps with many groups: collect
213, corners 240, lanes 249, expanse 247 at 6 bodies (`analysis/sim_results.txt`).

Rounds to 1000 in practice:

| map | plan D100 | plan D60 | sim "tts-like" (2 squads, bank at once) | **tts vs idle (A/B)** | tts vs weak (task) | tts + spawn fix vs idle | ming vs idle | **top player (platform)** |
|---|---|---|---|---|---|---|---|---|
| collect | 251 | 310 | 452 | 379/316 | ~366 | 372/316 | 315/324 | 335 or 355 (lanes or collect) |
| collision | 419 | 585 | 522 | 758/748 | ~750 | 758/748 | 568/590 | - |
| corners | 318 | 403 | 414 | 427/463 | ~360 | **335/394** | 341/390 | **~385** (match 069a) |
| elkring | 463 | 559 | 568 | 577/595 | ~571 | 577/594 | 651/589 | - |
| expanse | 338 | 401 | 403 | 469/484 | ~469 | 469/484 | 428/459 | - |
| interlock | 397 | 483 | 540 | 426/434 | ~448 | 426/434 | 431/408 | **~460** (match 2be0) |
| lanes | 297 | 368 | 508 | 438/433 | ~433 | 432/433 | 307/313 | 335 or 355 (lanes or collect) |
| monolith | 349 | 469 | 582 | 675/595 | ~628 | 675/595 | 745/767 | - |
| packs | 431 | 552 | 522 | 669/669 | ~531 | 669/(895*) | 754/724 | **~475** (match 1ab0) |
| rows | 451 | 651 | 571 | 872/679 | ~679 | 872/679 | 707/697 | - |

\* packs B vs idle is distorted by tungtungsahur attacking the idle enemy on its spawn (`fight_spawn`, 18-28% of
champion turns in `prof-tts`). The `mp-proffix` trace shows 3 champions parked at the idle team's spawn for
200 rounds. This is an artifact of the idle opponent, not of the fix.

How the platform maps were identified (only our stdout exists): each tribute jump in
`matches/platform-logs/timelines.txt` must be a sum of that map's group gem values.
- 1ab0: only +44/+48, i.e. packs WW 44 and GGOO 48.
- 2be0: +22/+36/+72/+94/+58, i.e. interlock W 22, E 36, GGG 72.
- 069a: +22/+36/+48/+96/+84, i.e. corners W, E, GG 48, EEG 96.
- 51e3 and e844: contain our own +24 tributes (single gem clusters), so lanes or collect.

The top player's first tribute came at r35 on packs and interlock and r50 on corners. Their pace is
between our D60 and D100 optima while being contested, so they farm almost without waste *and* win the fights.

Champion-turn use, plan vs tungtungsahur (vs idle):
- **Plan (D100):** clear 22-35%, walk to camps 27-41%, capture 10-19%, bank walk 4-15%,
  tribute 4-9%, respawn waits 0-21%, recall 1-5%. That is 0.36-0.74 gems per champion-turn.
- **tungtungsahur** (`analysis/econ_profile.py` on `matches/league/20261015-091619-prof-tts`):
  - hitting camps only 13-27% of turns;
  - following a leader (follow + follow_idle) 26% on collision, 28-31% on elkring, 39-46% on monolith,
    30-32% on rows;
  - 0.26-0.53 gems per champion-turn (rows 0.26, monolith 0.26, elkring 0.28, collision 0.33,
    lanes 0.38, expanse 0.53).
  - The lost time is mostly bodies that follow without farming, not slow killing.

## 3. Per-map plans and tactics (side A; side B is the mirror)

Format: "group (x,y) walk/to-altar". Walk = BFS steps from our spawn, to-altar = steps from the group to the
nearest altar. Squad itineraries come from `analysis/plan_results.txt`: Rn = rounds, xN = visits.

### 3.1 collect (40x40, 6 bodies, 180-degree rotation; spawn (1-3,1-3))
- **Layout:** home altars (7,1) (8,1) (9,1) are 3-5 steps from spawn. Many groups are close:
  - W (4,6) 3/4, E (9,8) 6/6, G (14,10) 11/8, GG (16,4) 13/6, G (16,6) 13/6, W (16,2) 13/6;
  - E (15,13) 12/11, EE (3,17) 14/15, G (19,14) 16/12, G (6,23) 20/21.
- **Contested:** E (16,24) 21 vs 20, E (23,15) 20 vs 21, G (30,10) 27 vs 26, G (9,29) 26 vs 27, and the two
  monoliths (38,1) and (1,38) at 35/35.
- **Plan (251 rounds, D60 310), split 2/1/1/1/1, T150:**
  - The pair loops W (16,2) x3, E (9,8) x3 and E (15,13).
  - Four solos rotate the gem clusters G (6,23), (14,10), (16,6), (19,14), (9,29), GG (16,4) and the wolves
    W (4,6), (24,2), (5,30).
  - Banks are at (7,1)/(9,1) with 63-188 gems each; the first tribute lands r43.
- **Gank spots:** the enemy's solo farmers on G (30,10) and W (34,9) are 8-10 steps from our loop, and
  G (20,25) is 11. The enemy banks 20-24 steps away at (9,1) from there, so they walk past our altars.
- **Monolith:** not worth it (0.8-1.5 gems/round for the whole team vs 4.0 farming; section 3.11).

### 3.2 collision (41x41, 4 bodies, vertical mirror; spawn (3-5,1-3))
- **Layout:** a bush belt plus a 3-row hole band (x<20, y 19-21) separates the halves on the west. The only
  connection is x 20-34.
- **One altar for both teams:** (27,20), 21 steps from each spawn. The second altar (39,20) sits in a
  sealed pocket: walls on rows 7 and 33 (x 23-40) and a 2-thick diagonal wall. BFS cannot reach it; a
  teleport crystal can (range 3, e.g. (34,20) -> (37,20), then 1 step to (38,20)).
- **Home groups:** W (10,5) 5/16, W (15,9) 10/11, W (19,13) 14/7, E (21,3) 16/16, E (29,3) 24/19,
  EGGG (37,3) 32/27 (108 gems, our biggest).
- **Contested:** W (24,18) and (24,22) at 19/19, **2 steps from the altar**.
- **Plan (419 rounds, D60 585), split 2/1/1, T75:**
  - The pair takes EGGG (37,3) x4 plus the mid wolves.
  - Two solos run the wolf chain (10,5) -> (15,9) -> (19,13) -> (24,18), which leads towards the altar.
  - Every bank is at (27,20). First tribute r92: every camp is 7-27 steps from the altar.
- **Choke:** all tributes of both teams end at (27,20). An altar lock there blocks every enemy tribute
  until 3 basic attacks; the enemy has no second walkable altar.
- **Gank spots:** the enemy's wolf farmer at (24,22) is 0 steps from our (24,18) loop; (19,27) is 5 and
  (15,31) is 9.
- **tungtungsahur:** 748-758 vs idle, the largest gap to the plan of any map. Its champions walk 25.6 tiles
  on average to bank, with 52 gems per bank.

### 3.3 corners (71x71, 6 bodies, horizontal mirror; spawn (13-15,33-35))
- **The centre:** 4 GG groups (48 gems, 1000 hp, 0 damage) at (34,32) and (34,36) (ours, 19 vs 21) and
  (36,32) and (36,36) (theirs), all **1 step from the centre altar (35,34)**, which is 19 from both spawns.
  Holding the whole centre is worth ~2.9 gems/round with no bank walking.
- **Home groups:** W (10,41) 6/24, E (18,22) 11/16, E (17,49) 14/17, E (12,16) 17/14, E (10,53) 18/15,
  EE (12,66) 31/9; near EEG (25,60) 24 vs 32, 22 to (1,69). The corner altars (1,1) and (1,69) are 31/33
  from spawn.
- **Plan (318 rounds, D60 403), split 3/1/1/1, T250:**
  - The trio does EEG (25,60) x3 and EE (12,66) x2, banking ~216 at (1,69).
  - **Two solos each own one centre GG** ((34,32) and (34,36), 6 visits each) and bank 48 at (35,34)
    every visit.
  - One solo farms W (10,41) and W (28,13).
- **Gank spots:** the enemy's centre GG farmers are 2 steps from ours. The centre is the fight. The top
  player's corners timeline (+48 every 10-20 rounds from r215 to r385) is centre control; we tributed 96
  in total.
- **Bug:** the respawn-squat deadlock (section 4) was found here: five champions stood on and next to
  group 3 (36,36)/(36,37) from r~100 to r2000.

### 3.4 elkring (30x30, 6 bodies, 180-degree rotation; spawn (0-2,0-2))
- **Layout:** 10 EO groups (elk + gold cluster: 2900 hp, 60 damage, 36 gems + 195 gold, respawn 60).
  The two altars (26,3) and (3,26) are 23 steps from *both* spawns, so both are shared.
- **Home groups:** EO (3,6) 4/18, (9,2) 7/15, (3,12) 10/12; near (19,2) 17/5 and (3,20) 17/5.
- **Supply:** the 5 own groups give 2.54 gems/round, so >= 394 rounds unless we take enemy groups.
- **Plan (463 rounds, D60 559), split 3/3, T150 (~4 banks per trio):** the trios alternate the 5 own
  groups and bank at whichever altar is next to their last group: (3,26) after (3,20), (26,3) after (19,2).
- **No solo farming is possible:** a solo takes 1440 damage per elk at D100. "Pair + solos" takes 1108
  rounds in the simulator.
- **Choke:** both altars sit 5 steps from our near groups and 5 from the enemy's, so every bank happens on
  shared ground. Carrying gems for long is deadly here: camp kills destroy carried gems. `mp-bank50` lost
  ~270 rounds on elkring A.

### 3.5 expanse (80x80, 4 bodies, 180-degree rotation; spawn (3-6,2-5))
- **Home groups:** W (5,12) 7/9, GG (11,18) 13/7, W (5,22) 17/7, GG (25,4) 19/10, E (25,15) 19/10,
  W (17,34) 29/7, GG (5,35) 30/8, WW (41,6) 40/9, EGGG (8,60) 53/10 and (8,67) 60/17 (108 gems each).
  Altars (14,4), (13,26), (12,47) are all on our side.
- **Pure race:** no contested group; the nearest enemy farm is 54+ steps from our loop.
- **Plan (338 rounds, D60 401), split 3/1, T250:**
  - The trio walks to EGGG (8,60)/(8,67) and banks ~232 at (12,47).
  - The solo loops GG (11,18), (5,35) and (25,4) and banks ~190 at (13,26).
  - Walking is 41% of champion-turns; the first tribute is r133.
- With 4 solos the whole-map optimum is 315. Every extra parallel farmer pays here.

### 3.6 interlock (40x40, 5 bodies, 180-degree rotation; spawn (0-2,0-2))
- **Layout:** altars (19,16) (ours, 17 vs 22) and (20,23) (theirs) sit on either side of the central hole
  band (x 16-23, y 19-20), only 7 tiles apart. (36,12) and (3,27) are 33 from both spawns.
- **Home groups:** W (5,8) 6, W (5,14) 12, **GGG (10,18) 16/6 (72 gems, 1500 hp, 0 damage)**, W (5,21) 19;
  near E (28,3) 26 vs 34. Contested: E (31,10) and E (8,29) at 29/29, 4 steps from (36,12) and (3,27).
- **Plan (397 rounds, D60 483), split 3/1/1, T150:**
  - The trio does the 3 elks (28,3), (31,10), (8,29) and banks at (3,27)/(19,16).
  - One solo owns GGG (10,18) (5 visits, banking 72 at (19,16) each time).
  - One solo loops the 3 wolves on x=5.
- **Gank spots:** the enemy's GGG (29,21) is 13 steps from our loop and their wolves on x=34 are 13-17. The
  centre (19-20, 16-23) is where both teams bank: the peel and altar-lock hot spot.

### 3.7 lanes (90x30, 6 bodies, horizontal mirror; spawn (2-4,12-14))
- **Layout:** 18 altars, ours at x 11-29. **Every camp is in the middle (x 36-53).**
  - Ours: 6 G at x=36 (32/6), 3 E at x=39 (35/9), 9 W at x=42-43 (38-39/12-13).
  - Theirs start at x=46.
- **Plan (297 rounds, D60 368), split 2/1/1/1/1, T150:**
  - Four solos rotate the six gem clusters at x=36 and the wolves at x=43.
  - The pair takes E (39,13) and the wolf chain.
  - Banks are at (29,4) and (29,13). The first tribute is r166 because of the 32-step walk in.
- **Contact line:** the enemy's solo wolves at x=46 are 3 steps from ours at x=43, and their G at x=53 is
  10 steps from our loop.

### 3.8 monolith (50x50, 6 bodies, 180-degree rotation; spawn (2-4,45-47))
- **Layout:** altars on the diagonal: (37,39) 32, (30,30) 25, (19,19) 25, (12,10) 34; corner altars (45,48)
  40 and (4,1) 43.
- **Home groups:** W (3,39) 6, W (15,46) 11, E (13,38) 13, W (3,31) 14, WW (9,24) 21, WW (29,46) 25.
  Near: WW (3,9) 36 vs 41, and the monolith group (48,48) at 43 vs 46 (M + 8 G = 392 gems, altar adjacent).
- **Plan (349 rounds, D60 469), split 2/2/1/1, T150:**
  - The pairs loop WW (3,9), (9,24), (29,46) and E (13,38).
  - The solos loop W (15,46), (3,31) and (3,39).
  - Banks are split between (12,10), (37,39), (30,30) and (19,19), all shared with the enemy (25-34 from
    both spawns).
- **tungtungsahur:** 41-46% of its champion turns are follow/follow_idle, the worst of any map. Many
  single wolves and pairs of wolves make this an ideal map for more independent units.

### 3.9 packs (31x31, 4 bodies, 180-degree rotation; spawn (0-2,0-2))
- **Home groups:** WW (8,2) 6/5 (to (2,6), 3 steps from spawn), WW (16,2) 14/11; near WW (24,3) 22 vs 25,
  3 to (28,6). **Contested centre: GGOO (12,18) 15 vs 16 and (18,12) 16 vs 15** (48 gems + 70 gold,
  2000 hp, 0 damage).
- **Supply:** our 3 WW give only 2.49 gems/round (>= 402 rounds). The centre pair adds 1.57/round and
  decides the race.
- **Plan (431 rounds, D60 552), split 2/2, T250:** both pairs rotate WW (16,2), (8,2) and (24,3) plus
  GGOO (12,18), and bank ~250 at (2,6) and (28,6).
- **Top player (match 1ab0):** first +44 at r35, which fits all champions on WW (8,2) and an immediate bank
  at (2,6). After that, +44/+48 every ~25 rounds, so they ran both centre GGOO.

### 3.10 rows (50x50, 5 bodies, 180-degree rotation; spawn (2-5,2-5))
- **Layout:** each side has one altar: ours (15,16) 10 steps away, theirs 62. Our three WWW (66 gems,
  4050 hp, 60 damage, respawn 40) are on the top lane: (18,5) 13/11, (31,5) 26/24, (42,5) 37/35. The
  centre GGMM (25,24) holds 448 gems in 41000 hp.
- **Pure race:** no gank spot (enemy camps are 73+ steps away), and altars cannot be contested cheaply.
- **Plan (451 rounds, D60 651), split 3/2, T150:**
  - The trio loops (31,5) x6 and (42,5) x3; the pair loops (18,5) x6 (a pair survives it at D100 only
    because it is next to home).
  - Bank about every 2 groups at (15,16).
  - Banking at once costs 120 rounds here (571 vs 451) because camps are 11-35 steps from the altar.
- **tungtungsahur:** 679-872 vs idle, the biggest absolute gap together with collision.

### 3.11 Monolith groups (whole team, no enemy; `maps_extra.py monolith`)

| map / group | gems | our walk | D100: rounds, gems/round | D150: gems/round | farming rate (best plan) |
|---|---|---|---|---|---|
| collect M (38,1) or (1,38) | 200 | 35 (28 to altar) | 148 rounds, 1.35 | 1.46 | 3.98 |
| monolith GGGGGGGGM (48,48) | 392 | 43 (altar adjacent) | 147 rounds, 2.67 | 2.93 | 2.87 |
| rows GGMM (25,24) | 448 | 36 (25 to altar) | 569 rounds, 0.79 | 1.07 | 2.22 |

The monolith deals 200 damage per turn: 6800 damage at D100 against a team pool of ~5100 health, so at
least 1 heal trip (5 + walk) is needed. tungtungsahur's 0.2 value penalty (bot.cpp:504) is right; rejected
experiment #35 agrees.
- **Denial:** a capture needs an uncontested group tile. If the enemy sinks ~150 rounds of 6 champions
  into the monolith, one of our champions stepping onto a group tile resets their capture.

## 4. Bug found through the layout: respawn-squat deadlock (corners)

- **Evidence:** in `matches/league/20261015-091619-prof-tts/002-prof-tts-vs-zz-idle-corners.repl26a`
  (team a stdout, `P` lines), Ryth, Stellar and Tavi stand at (36,35), (36,36) and (36,37), and Cassi and
  Prism at (40,42) and (41,42). All five are in state CWALK with target group 3 from r~100 to r2000.
  (36,36) and (36,37) are exactly group 3's tiles (centre GG). The game ends at r2000 with 816 gems
  against an idle opponent.
  - The same stall hit `mp-bank50h` corners B (600 gems at r405, still 792 at r1805, game to r2000)
    after an unrelated change. The bug is latent and triggered by small timing changes.
- **Mechanism (most likely):**
  - The rules say "Any occupied spawn tile delays the entire group".
  - `update_ledger` (bot.cpp:457) stores `ready = round + timer`. A group whose timer has reached 0 but
    which is held back by an occupied tile therefore looks ready (`ready == round`).
  - `farm_group` (bot.cpp:574-579) then walks onto its tiles (`goals = g->tiles`) instead of "one step off
    its tiles", which keeps the group from respawning, forever.
  - It needs a group next to where champions idle, such as the corners centre (4 GG one step from the
    centre altar).
- **Fix:** in `bots/mp-fixspawn/src/bot.cpp:456-460`, `ready[i] = round + std::max<int>(timer, 1)`. The
  waiting champions then stand off the tiles and the group respawns.
- **Results:**
  - corners vs idle 427/463 -> **335/394** (`matches/league/20261015-134312-mp-fixspawn`).
  - The instrumented copy (`mp-proffix`) does corners A in 360 instead of stalling to 2000.
  - All games vs ming_bot are identical to the baseline (12/20).
  - Full 400-game league: **362/400**, same as the current best (`matches/league/20261015-134428-mp-fixspawn`).
- **Platform:** match 069a (corners) shows our last tribute at r185 and 96 gems at r400. That is
  consistent with this deadlock (the platform version was older, but this code is unchanged).

## 5. General rules: what the simulator says and what the real bot did

Simulator, D100, half map, each rule applied unchanged to all 10 maps. Ratio = rounds / per-map optimum
(`maps_extra.py rules`).

| rule | collect | collision | corners | elkring | expanse | interlock | lanes | monolith | packs | rows | mean ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 squads, bank at once (tts-like) | 452 | 522 | 414 | 568 | 403 | 540 | 508 | 582 | 522 | 571 | 1.40 |
| 2 squads, bank at T100 | 343 | 525 | 365 | 497 | 398 | 483 | 402 | 504 | 452 | 536 | 1.23 |
| best split per map, bank at once | 301 | 480 | 372 | 568 | 399 | 460 | 342 | 455 | 522 | 571 | 1.20 |
| best split per map, T100 | 260 | 467 | 329 | 497 | 364 | 444 | 312 | 374 | 452 | 536 | 1.08 |
| best split per map, T100 or altar within 6 | 300 | 466 | 329 | 471 | 364 | 442 | 354 | 374 | 466 | 536 | 1.11 |
| "pair + solos" everywhere, T100 | 260 | 467 | 352 | 1108 | 356 | 439 | 312 | 535 | 579 | 1075 | 1.41 |
| **auto split**, bank at once | 337 | 480 | 372 | 568 | 342 | 460 | 342 | 506 | 522 | 571 | 1.21 |
| **auto split, T150** | 262 | 468 | 329 | 469 | 363 | 409 | **297** | 399 | 449 | **451** | **1.05** |

**Auto split rule:**
- Light groups are those that hit for <= 20 (gem/gold clusters, single wolves). Heavy groups hit harder.
- `need` = the smallest squad that clears the heaviest home group keeping >= 30% health. At D100 that is
  2 for E/WW/EO/EGGG and 3 for WWW.
- solos = min(n - need, floor(light/2)); the rest form 1 squad, or 2 if rest >= 2 x need.
- Resulting splits: collect 3/1/1/1, collision 2/1/1, corners 3/1/1/1, elkring 3/3, expanse 2/1/1,
  interlock 3/1/1, lanes 2/1/1/1/1, monolith 3/2/1, packs 2/2, rows 3/2.

Lessons from the simulator:
- The split is worth more than the bank threshold on gem/wolf maps: lanes 508 -> 342 from splitting, then
  -> 297 from banking; collect 452 -> 301 -> 251.
- The bank threshold is the only lever on rows and packs (571 -> 451 and 522 -> 431), where camps are far
  from altars.
- "Bank whenever an altar is within 6" is worse than a plain threshold (collect 260 -> 300, lanes 312 -> 354).
  The +1 tribute turn and the walk add up.

Real-bot checks (tungtungsahur + one change, 20 games each vs zz-idle and vs ming_bot; per-map rounds in
section 2 and below):

| variant | change | vs idle, sum of 20 end rounds (baseline 11106) | vs ming_bot | full league |
|---|---|---|---|---|
| `mp-bank50` (bot.cpp:905-915) | each champion keeps farming until its bag >= 50 unless an enemy is visible, an altar is within 2, or the bag wins | 10804: lanes 438/433 -> 362/400, rows 872/679 -> 635/614, packs 669 -> 565, but elkring A 577 -> 848, interlock and expanse +40 | 9/20 (baseline 12/20) | - |
| `mp-bank50h` | same, only at >= 70% health | 12682 (corners B stalled to 2000: section 4) | 10/20 | - |
| `mp-fixspawn` | respawn-squat fix | 11157 (corners -92/-69; packs B +226 is the idle-spawn artifact) | 12/20, identical games | **362/400** (= best) |
| `mp-solowolf` (fixspawn + bot.cpp:598) | back-liners at >= 80% health also solo single wolves within 16 | collision 758/748 -> **588/691**, corners 344/342, collect 342/382; interlock 426/434 -> 499/617, expanse +40/+94 | 13/20. Interlock wins faster (r605/570 vs 900/770); collect B becomes a win; **collision collapses (our gems 560/404 -> 242/176)** | 345/400 (loses 17 games, all to self-play variants) |

Conclusion: the simulator's levers are real but map-dependent in the real bot. Without protection, more
lone farmers lose fights against the aggressive tungtungsahur variants, and bigger bags die to camps on
elk maps. The rules below are therefore map-gated.

## 6. Recommendations (ranked by expected impact)

1. **Ship the respawn-squat fix** (bot.cpp:457, one line, already in `bots/mp-fixspawn`).
   - Corners vs idle is 70-90 rounds faster and the 2000-round deadlock is gone; league 362/400 is
     unchanged.
   - It probably cost the platform corners game outright (96 gems).
2. **Assign farming per map at round 1 (map-aware split), using the plans in section 3.** The simulator
   predicts 25% fewer rounds on average (sum 5082 -> 3896 at D100) and up to 40% on collect, lanes and
   monolith.
   - Solos own the light groups closest to their altar, 1-2 groups each:
     - corners: the 2 centre GG (34,32) and (34,36), banking at (35,34);
     - interlock: GGG (10,18), banking at (19,16);
     - lanes: the six G at x=36;
     - collect: G (14,10), (16,6), (19,14), GG (16,4);
     - expanse: GG (11,18), (5,35), (25,4).
   - Squads only for heavy groups, sized by `need` (section 5).
   - The squad leader no longer drags 1-3 followers around: follow + follow_idle is 26-46% of turns on
     collision, elkring, monolith and rows.
   - Do not switch on lone-wolf soloing everywhere. `mp-solowolf` sped up collision vs idle
     (758/748 -> 588/691), but against ming the collision lone farmers were picked off near the shared
     altar (our gems 560/404 -> 242/176), and it lost 17 league games to fight-heavy variants.
   - Solo loops must stay away from the enemy's paths: lanes x=36, collect home, interlock GGG, and the
     corners centre only with the squad within ~8. Solos fall back to the squad when an enemy has been seen
     within ~8 tiles in the last ~10 rounds.
3. **Corners centre control**, where the top player beat us.
   - Two champions farm the two own centre GG and bank 48 at (35,34) every visit; the cycle is 50 respawn
     + ~10 clear + 6 capture.
   - Steal (36,32) and (36,36) when the enemy is not within 8.
   - Put the altar lock on (35,34) when the enemy holds bags near it.
   - Ceiling: ~2.9 gems/round from the centre alone, which is 1000 gems in ~345 rounds even without any
     other farming.
4. **Collision: own the only altar.**
   - Fight for (27,20) and keep a lock on it when enemy bags approach. Every enemy tribute must happen
     there; they have no other walkable altar.
   - Farm the mid wolves (24,18)/(24,22) (2 steps from the altar) between banks.
   - Optional lock-proof bank: buy a 10-gold teleport crystal, cross the wall (34,20) -> (37,20) (3-turn
     channel; damage does not stop it), tribute at (39,20), then **recall** home (5 turns, cheaper than the
     21-step walk back). The enemy cannot lock that altar without teleporting too (locks need range 2;
     (34,20) is 5 away).
5. **Bank rule by situation, not one threshold:**
   - Solos on 0-damage loops (gem clusters) bank when the bag >= 48-72 *or* when the detour fits inside
     the next cluster's respawn wait.
   - On rows and packs (camps 11-35 from the altar) squads bank every 2 groups (bag >= ~130 per squad,
     ~45 per champion) while no enemy is visible.
   - Everywhere else, especially elkring and interlock, keep banking right away: `mp-bank50` lost 270
     rounds on elkring A and 9/20 vs ming.
6. **Monoliths:** never on rows or collect. On the monolith map, only use them as a denial target: stand
   on a group tile when the enemy is capturing.
7. **Don't fight enemies standing on their own spawn** (18-28% of turns wasted on packs vs idle, 12% on
   rows). They heal to full there; cap the chase at ~6 tiles from their spawn region.
8. **Pre-position before respawns:** the plan spends 0-21% of turns waiting at the next camp. Wait one step
   off the tiles (the fix guarantees that) instead of walking back to the leader.

## Files

- Layout dumps: `analysis/map-dumps/*.txt`; probe bot `bots/mp-probe/src/bot.cpp`.
- Distances and tables: `analysis/map_layout.py`.
- Simulator: `analysis/farm_sim.py`. Itineraries: `analysis/plan_report.py` -> `analysis/plan_results.txt`.
  Bounds per body count: `analysis/sim_results.txt`.
- This report's tables: `analysis/maps_extra.py` -> `analysis/extra_results.txt`.
- Experiments: `bots/mp-fixspawn`, `bots/mp-solowolf`, `bots/mp-bank50`, `bots/mp-bank50h`, `bots/mp-proffix`
  (instrumented fix). Leagues: `matches/league/20261015-1340*-mp-bank50`, `-134124-mp-bank50h`,
  `-134312-mp-fixspawn` (idle + ming), `-134428-mp-fixspawn` (full), `-134404-mp-proffix`,
  `-134902-mp-solowolf` (idle + ming), `-134935-mp-solowolf` (full).

## Collision follow-up (17 Oct 2026)

The proposed teleport-crystal route to altar `(39,20)` was tested against the four strong local
proxies. Buying it for bags of 100+ gems scored 4/8, equal in wins to main; triggering it for any
positive bag scored 2/8. Replay instrumentation confirms that the teleport route activated, but it
did not produce better match outcomes. Treat the route as rejected for general play rather than as
a reliable answer to the altar lock.

A map-only draft that takes Stellar / Cassi & Issac / Varg instead of Ryth scored 5/8 in two repeated
Collision runs, versus 4/8 for main. It gained one win against Xuanming but still lost both games to
Ming, who banked 968 and 924 gems. When combined with the Contest/Stampede Prism draft from
experiment 78, the full pool reached 109/136, with Collision 5/8, Contest 7/8, Stampede 8/8 and all
other map scores unchanged from experiment 78. This is the best current local candidate, but the
Collision response remains unproven against top teams. See experiment 85 and run paths in
`bots/tungtungsahur/PLAN.md`.

## Swirl follow-up (17 Oct 2026)

Swirl is 45x30 with four picks and 18 paired gem-bearing groups. The camps are dangerous: individual
groups hit for 40-240 damage per round, while the no-contact route model's best 5-body plan uses a
3/2 split, banks at 250 gems, and reaches 1000 in a theoretical 412 rounds. The current bot instead
uses its standard 2/2/1 assignment after the early phase, with Varg farming separately.

In the 17-map run, Swirl scored 4/8. Candidate 85 lost all four sampled games to Ming and Xuanming;
the losses recorded 47-70 deaths and 132-198 gems lost. One Ming-side game scored 352-990 by r1085;
the other scored 476-980 by r1045. The candidate also saw enemy altar locks at (21,19) and (23,10).

Experiment 88 tried Jungle Health first for Varg and the mage, then their regular damage builds. It
reduced deaths in the sampled strong-proxy games (Ming 55/47 -> 39/45; Xuanming 70/53 -> 47/39),
but scored only 3/8 and fell behind earlier against Xuanming. The added survival did not pay back
the lost camp damage. Do not retain this as a global or Swirl build. The prior whole-team opening
through round 600 tied the baseline at 4/8.

Experiment 89 kept Varg with Issac's squad objective after the opening, creating a 3+2 split rather
than a 2+2+1 split. It stayed at 4/8: gems improved against Ming but declined against Xuanming, and
both still won both sides. Experiment 90 delayed banks until 150 gems when no enemy was visible;
that dropped Swirl to 2/8. It lost 1,802 carried gems on deaths in the four Ming/Xuanming games,
versus 647 for the immediate-bank candidate. The theoretical T=250 route optimizes uncontested farm
time and is unsafe under these opponents' combat pressure. For now, keep immediate banking and
focus further Swirl work on a camp-specific 3+2 assignment that can preserve combat coverage.

## Expanse follow-up (17 Oct 2026)

The map-only C&I / Varg / Stellar draft order previously tested as experiment 72 now combines well
with experiment 85's Contest, Stampede, and Collision drafts. In the matched full-pool run, Expanse
rose from 5/8 for main to 8/8 for the candidate, which won both sides against each of Ming, Xuanming,
Faisal, and opp-racer. The full pool scored 112/136 versus 104/136 for main, with gains limited to
Collision 4/8 -> 5/8, Contest 5/8 -> 7/8, Expanse 5/8 -> 8/8, and Stampede 6/8 -> 8/8. No other
map regressed. This is the strongest local draft plan to carry into live testing; it is not yet
validated against top-50 teams in unranked matches.

## Pilgrimage and Lanes follow-up (17 Oct 2026)

Pilgrimage's simulator recommendation of a 2/2/2 split with a 100-gem threshold is only a no-contact
starting point. The map-specific T=100 rule (bank at once if an enemy is visible) scored 4/8, below
the current candidate's 5/8. Splitting from round 1 also stayed at 5/8: it beat Ming on both sides
instead of losing both, but lost both sides to Xuanming instead of taking one. A Vendetta-for-Ryth
draft dropped to 3/8 and lost all four sampled Ming/Xuanming games. For now, retain experiment 91's
Pilgrimage draft, role builds, bank logic, and grouped opening; use scouting to prioritize improving
the early altar race and the Xuanming matchup.

Lanes is an economy race with a strong side-B disadvantage in the current proxy set: all four
baseline side-B losses had no deaths, and the idle race is only 12 rounds slower from B than A.
Switching from the grouped opening to split squads at round 200 scored 3/8, below 4/8. A Lanes Ren
draft replacing Ryth scored 4/8 but lost both sides to Ming and Xuanming; replacing Tavi with Ren
scored 5/8 overall but only 1/4 against those two strongest proxies, versus 2/4 for experiment 91.
Treat Ren and earlier splitting as rejected for the top-team target. The current candidate's standard
draft, equipment, and farm pattern remain the better tested Lanes setup. Detailed run IDs and the
per-opponent outcomes are in `bots/tungtungsahur/PLAN.md`.


## Rushbait v2 follow-up (17 Oct 2026)

The 30x80 Rushbait v2 map benefits from entering the mid-game squad phase from the opening, on either side. The all-side rule won 7/8 in each of two targeted repeats. Added to the current map-specific candidate, the 17-map strong-proxy result rose from 112/136 to 113/136; Rushbait improved from 5/8 to 7/8, with Stampede moving from 8/8 to 7/8. In the expanded 680-game local pool, Rushbait rose from 35/40 to 39/40 and Swirl from 34/40 to 35/40, giving 592/680 versus 587/680 for the previous candidate and 577/680 for main. Keep the candidate’s existing map draft and equipment; only the Rushbait opening phase changes.

A side-specific Rushbait condition scored 3/8 and 4/8, but it failed to take its intended early branch, so discard those runs as an implementation failure rather than evidence against the all-side opening. A separate global movement fallback test regressed the broad pool by one win and produced a dangerous Bruiser Ambush loss; retain the current movement behavior. The candidate remains isolated pending live validation against ranked top-50 teams.


## Lanes side-B equipment follow-up (17 Oct 2026)

Lanes' side-B games remain an economy race; switching to the mid-game split from round 1 did not turn any of its four side-B losses into wins. Giving Tavi Monster Strength before Power Focus on both sides also failed to improve the map total and reduced the result against Ming/Xuanming from 2/4 to 1/4.

The side-B-only Tavi build is more promising: buy Monster Strength for the first emblem, then return to Power Focus. It scored 5/8 in two identical targeted runs, compared with 4/8 for the prior candidate. On the full strong-proxy pool it raised Lanes from 4/8 to 5/8 and total wins from 113/136 to 114/136 with no other map regressions. The 680-game local pool rose from 592/680 to 593/680; broad Lanes is 37/40 versus 36/40. Keep this as an isolated candidate at bots/cand-lanes-sideb-tavi-monster/src/bot.cpp while awaiting live validation. Ryth's Swirl Monster Strength first build scored 3/8 and is rejected; retain his current health-first build.


## Ambush recovery and remaining strong-proxy losses (17 Oct 2026)

The 100x100 no-movement fallback skips a camp group after 12 stalled movement turns. With source timestamps refreshed and distinct compiled WASM hashes verified, the matched broad run rose from 593/680 without recovery to 610/680 with recovery. Ambush improved from 21/40 to 40/40, converting 19 losses; Pilgrimage fell one net win (30/40 to 29/40) and Rushbait v2 fell one (39/40 to 38/40). Against the four strong proxies, the targeted Ambush result improved from 6/8 to 8/8. The candidate's strong league is 117/136 versus a fresh same-name main build at 104/136.

An earlier same-name source-swap comparison falsely showed identical results because copied source files retained timestamps older than the CMake objects. `tools/league.py` invokes an incremental `cambc build`, so it reused v104's old WASM. Those comparisons are invalid. Later tests touched each swapped source, built explicitly, and confirmed the WASM hashes changed before running.

Narrowing the extra group lookup to Ambush produced 611/680 broad but 116/136 strong (one below v104's 117/136); Ambush remained 40/40. At that point v104 led the strong proxy set; experiment #115 later superseded it by one strong-set and one broad-set win.

Replay analysis of v104's 11 losses to `ming_bot` shows several distinct failure types:

- Collision: both sides lost badly (416–968 and 254–924), with 22 and 14 deaths. Enemy altar locks repeatedly appeared at (27,20), and the enemy banked around (26,19).
- Swirl: both sides lost (352–990 and 476–980), with 55 and 47 deaths. Logs show repeated altar locks at (21,19) and (23,10), plus repeated enemy tributes.
- Pilgrimage: side A lost 596–924 with 11 deaths and 138 gems lost; the enemy Stellar carried up to 114. Side B lost 692–980 despite no carried gems lost, pointing to a farming/tribute pace gap as well as combat.
- Contest side B ended 200–200 at round 2000, and Stampede side A ended 900–900 at round 2000. These are tied-score games at the round cap; Stampede also recorded 49 deaths and 1,260 gems lost.

The current code already attacks visible enemy altar locks while banking. The remaining logs point to an earlier economy and survival problem: the enemy is gaining central altar control before our champions can bank enough, and on Collision/Swirl repeated deaths compound the gap. Test map-specific retreat/banking changes against those losses before changing the lock attack itself.

These remain local proxy results. The user has since supplied unranked group `4cf7ad87-2c52-452e-a9a3-59787c302e67`: Heavenly Court lost 0–5 to FRChronic, which was rank 58 around the match. The top-50 streak remains 0/10. TinyFish is installed, but browser actions are not exposed in this session; main source and submission ZIP remain unchanged.

Fresh controlled comparisons supersede earlier copied-source trials: after refreshing source timestamps and verifying distinct WASM hashes, v104 scored 610/680 on the broad pool versus 577/680 for a fresh main-source build (`20261017-192402-cand-ambush-stall-recovery`). V104 gained 19 Ambush, 6 Expanse, 4 Stampede, 3 Rushbait v2, 2 Contest, 1 Lanes, and 1 Swirl win, while losing 2 Collision and 1 Pilgrimage; other map totals were unchanged. Its strong-proxy result was 117/136 versus main's 104/136. A proposed Swirl-only late retreat check then scored 0/4 against Ming/Xuanming, and all four replay ZIP hashes matched the v104 controls exactly, so the change produced no observed action difference. Keep the v104 source as the isolated local leader; these are local results only.

Two more Swirl-specific survival checks confirmed the tradeoff. Recalling at 50% health reduced observed deaths but scored 3/8 (baseline 4/8), so the farming loss outweighed safer retreats. A 40% threshold tied the targeted 4/8 and scored 118/136 on the strong set, one above v104, but fell to 607/680 broad versus v104's 610/680; broad Swirl itself fell from 35/40 to 32/40. Reject both and keep the v104 30% tank / 35% other thresholds.

On Pilgrimage, Tavi's Monster Strength-first build scored 5/8 against the four strong proxies, below v104's 6/8 on that set (`20261017-194005-cand-ambush-stall-recovery` vs `20261017-175715-cand-ambush-stall-recovery`). Keep the existing build; the game's enemy Stellar already reached a 114-gem bag, but added camp damage on Tavi did not overcome the tribute/economy gap.

A second Pilgrimage test made champions break a nearby enemy lock on a home altar even while carrying no gems. It scored 5/8 in two identical runs (`20261017-194247` and `20261017-194304`), below v104's 6/8. It won one of two games against Ming but lost both to Xuanming. Keep the existing bank behavior; the extra basic attacks did not give a net strong-proxy improvement.

Collision has only one reachable altar, at (27,20), and v104's Ming replays show repeated enemy locks there. Attacking that lock while empty still scored 4/8 (`20261017-194508-cand-ambush-stall-recovery`), below v104's 5/8; it continued to lose all four Ming/Xuanming games. Keep the existing bank-only lock break.

Replacing Varg with Tavi in Collision's three-pick draft kept Stellar and C&I but remained 5/8, tied with v104, and still lost both Ming games (`20261017-194617-cand-ambush-stall-recovery`). The ranged damage did not turn the central camp contest; restore Varg.

On Swirl, Varg reinforcing Ryth instead of solo-farming improved the two Ming loss scores from 414 average gems to 631, but still lost all four games to Ming/Xuanming. Across the 20-opponent Swirl pool, it scored 34/40 versus v104's 35/40 (`20261017-194840-cand-ambush-stall-recovery`). Keep Varg solo; the higher scores against the strongest two proxies did not convert into extra wins.

## Latest isolated local candidate: Lanes shopping threshold (17 Oct 2026)

Experiment #115 raises the Lanes side-B recall-for-shopping threshold from 150 to 250 gold. Two targeted repeats each scored 6/8, versus 5/8 for a fresh v104 control. The full strong-proxy set scored 118/136 versus 117/136 for v104, and the 20-opponent broad pool scored 611/680 versus 610/680. Lanes improved from 5/8 to 6/8 in the strong set and from 37/40 to 38/40 in the broad Lanes subset; no other map total changed. Runs: `20261017-195019`, `20261017-195038`, `20261017-195109`, `20261017-195134`, `20261017-195154`, and `20261017-195236` under `matches/league/`.

The candidate is isolated at `bots/cand-ambush-stall-recovery/src/bot.cpp`, snapshot `candidate-source-v115-lanes-shoptrip250.cpp`. Main source and `submissions/tungtungsahur.zip` remain unchanged. These are local proxy results; the live top-50 streak remains 0/10. TinyFish now reports installed, but its browser actions are not exposed in this session.

A threshold sweep tested 200 and 300 gold. The 200-gold variant scored 5/8 in two identical Lanes strong-proxy runs (`20261017-195844` and `20261017-195930`); 300 gold scored 3/8 (`20261017-195907`) and lost both Faisal games. Reject both. Keep 250 as the best tested side-B threshold; it scored 6/8 in two targeted runs and improved integrated scores by one win.

## Swirl support draft check (17 Oct 2026)

Replacing Varg with Willow on Swirl tested whether support healing could offset the loss of Varg's solo farming. It tied the standard draft at 4/8 but lost all four games against Ming and Xuanming, ending at only 195 and 427 average gems against their 983 and 956. Keep Varg; Willow's healing did not compensate for the lost farm and damage. Run: `20261017-223244-cand-swirl-willow`.

## Collision role lineup checks (17 Oct 2026)

The requested Tank/Fighter/Marksman lineup (Ryth/Vendetta/Tavi) scored 2/8 and lost all six games against Ming, Xuanming, and Faisal (`20261017-223334-cand-collision-role-lineup`); its low gem totals show the three-body lineup cannot keep pace. Adding the C&I pair with Ryth and Tavi scored 1/8 (`20261017-223401-cand-collision-ryth-ci-tavi`). Replacing only Varg with Ryth while retaining Stellar and C&I scored 4/8 (`20261017-223428-cand-collision-ryth-for-varg`), below the current lineup's 5/8, and still lost all Ming/Xuanming games. Keep Stellar/C&I/Varg for Collision; in this map the camp and gem economy gains from that draft outweigh the role-based alternatives tested so far.

## Stampede follow-up after the live loss (17 Oct 2026)

The supplied group used the main standard draft on Stampede (Stellar/C&I/Ryth/Varg/Tavi) and scored 0 against FRChronic's Prism/Stellar/C&I/Ryth/Tavi. A fresh paired local run on both sides against Ming, Xuanming, Faisal, and opp-racer scored 6/8 for main versus 7/8 for isolated v115. The candidate's Prism lineup converted main's Xuanming side-A loss to a win; both still tied Ming at 900–900 on one side. Three equipment variants were screened: Monster Strength first on Tavi tied at 7/8, on Prism fell to 6/8, and on both fell to 5/8. Reject all three; keep current equipment and retain the map-specific Prism draft as the leading isolated candidate. This is local proxy evidence, not a top-50 win. Results are in `matches/league/20261017-2301-stampede-monster-screen/summary.json`.

### Stampede experiment #126: delay the squad split

The Stampede camp is the only gem source on the map, so a split team can leave it underpowered. Starting
from v115, #126 ignores the mid-game phase flag until Stellar's late-game flag, keeping the shared farm
behavior active for the transition. A fresh strong-proxy screen scored 8/8 versus 7/8 for v115. The
22-opponent Stampede pool scored 41/44 versus 36/44: six losses became wins and one win regressed. The
Ming side-A replay improved from 900–900 at the 2000-round cap (49 deaths, 1,260 gems lost) to 900–180
at r1695 (44 deaths, 180 gems lost). Build outputs had zero bot errors.

The v115 comparison is controlled on Stampede only; #115 remains the all-map validated candidate.
Extending the early/shared phase all the way to round 900 or 600 reduced the strong-proxy score to 7/8,
so reject both. A round-900 condition checked after the late flag was a no-op: it produced the exact
same Ming replay hash as #126, whose phase trace entered mid at r417 and late at r418. Keep the shorter
override as the leading Stampede branch at `bots/cand-stampede-team/src/bot.cpp`, isolated from main
until top-50 live validation. Run summaries are under `matches/league/20261017-230854-cand-stampede-team`,
`20261017-231001-cand-stampede-team`, `20261017-231150-cand-stampede-team900-active`, and
`20261017-231219-cand-stampede-team600-active`.
# Full-map check of the Stampede shared-farm change (17 Oct 2026)

The Stampede #126 phase change is no longer only a Stampede-specific candidate. In a same-name 17-map comparison it scored 119/136 against the four strong local proxies and 612/680 across the broad 20-opponent pool; #115 scored 118/136 and 611/680 respectively. The broad paired changes were Stampede +2 wins, Lanes +1, Pilgrimage -2.

Caching the map flag during initialization (#131) preserved all 136 strong-proxy outcomes and scored 614/680 in two exact broad repeats, versus #126's 612/680. Four broad outcomes changed: Stampede +1, Pilgrimage +2, Lanes -1. This is a repeatable but modest local result, so #131 remains isolated from the main bot pending live top-50 validation. The source and WASM hashes and run IDs are recorded in bots/tungtungsahur/PLAN.md.
# Elkring/Fragment draft split (18 Oct 2026)

Elkring and Fragment are both 30x30, but their pick counts differ: five picks on Elkring and three on Fragment. Applying Varg-before-Ryth to both maps improved Elkring by four broad games but reduced Fragment by three, so reject the combined rule. The loss was concentrated in local Fragment matchups against Faisal-bot and older tungtungsahur variants.

Experiment #133 identifies Elkring by its altar positions and changes only its pick order. The roster remains Stellar / Cassi & Issac / Varg / Ryth / Tavi there; Fragment retains the standard three picks, Stellar / Cassi & Issac / Ryth. #133 scored 120/136 against four strong proxies and 618/680 in two exact broad repeats, versus #131's 119/136 and 614/680. All four broad gains were on Elkring; other map totals were unchanged. Keep this draft isolated pending live top-50 validation. Run IDs and source/build hashes are in bots/tungtungsahur/PLAN.md.
# Pilgrimage pick-order and frontline screens (18 Oct 2026)

On Pilgrimage, putting Varg before Ryth improved average carried gems against Ming (644 to 932) but still lost both games and dropped the targeted result from 6/8 to 5/8. Replacing Tavi with Ren scored 5/8, winning one Ming side but losing both Xuanming sides. Keep #133's existing Pilgrimage draft; neither targeted variant passed the strong-proxy gate.
# Swirl Varg-order screen (18 Oct 2026)

Moving Varg before Ryth while keeping the four-pick Swirl roster fell to 3/8 from #133's 4/8. Ming and Xuanming still won both sides, and opp-racer gained a win. Keep the original draft. This was a targeted screen only.

### Swirl strategy screen #143

A counter-draft check restricts Swirl's earlier retreat to the four-pick Cassi & Issac / Varg / Stellar / Vendetta enemy composition used by Ming and Xuanming. This preserved #141's strong-proxy result (121/136, repeated) and restored its broad result to 618/680, repeated exactly, matching #133's map totals. It is an isolated candidate and has not yet been tested against a live top-50 roster.

# Pilgrimage high-bag banking follow-up (#145, 18 Oct 2026)

On the 50x65 Pilgrimage map, the #143 Faisal-bot side-B replay showed Tavi dying at (12,60) with 144 gems while travelling toward the west altar; the enemy Stellar collected the bag. Across that game, deaths dropped 236 gems and the score ended 676-988. #145 adds a 40-turn path-cost penalty to altars in the enemy half when a champion carries at least 100 gems. It leaves smaller bags and every other map unchanged.

The direct-runner Pilgrimage pool scored 31/40 in two identical #145 runs, compared with a fresh same-runner #143 control at 29/40. The two new wins were one side against Faisal-bot and one against opp-tts-aggro; other per-opponent map totals matched. The exact four strong proxies remained 6/8, equal to the #133 control. On the targeted Faisal-bot side-B game, #145 won 1004-820, had 16 deaths, and lost no gems on deaths. See `matches/league/145-direct-broad-pilgrimage-20261018`, its repeat, and `matches/league/143-direct-broad-pilgrimage-control-20261018` for replay bundles and summaries. This remains local proxy evidence; live top-50 progress is still 0/10.

## Full-map check of #145 and Collision follow-ups (#146–147, 18 Oct 2026)

Because `cambc run-batch` still fails on generated Windows CMake object paths, the 680-game run used the direct runner. It completed all games after two sequential retries for temporary-file access errors. #145 scored 620/680 versus the same-runner #143 control at 618/680. The difference is only Pilgrimage; all other map totals match exactly:

| Map | #145 | #143 | Change |
|---|---:|---:|---:|
| Ambush | 40/40 | 40/40 | — |
| Collision | 37/40 | 37/40 | — |
| Contest | 32/40 | 32/40 | — |
| Corners | 34/40 | 34/40 | — |
| Eight | 39/40 | 39/40 | — |
| Elkring | 38/40 | 38/40 | — |
| Expanse | 40/40 | 40/40 | — |
| Fragment | 37/40 | 37/40 | — |
| Interlock | 36/40 | 36/40 | — |
| Lanes | 38/40 | 38/40 | — |
| Monolith | 36/40 | 36/40 | — |
| Packs | 34/40 | 34/40 | — |
| Pilgrimage | 31/40 | 29/40 | +2 |
| Rows | 39/40 | 39/40 | — |
| Rushbait v2 | 38/40 | 38/40 | — |
| Stampede | 36/40 | 36/40 | — |
| Swirl | 35/40 | 35/40 | — |

The four strong local proxies also repeated #143's 121/136 exactly by map. Ming scored 26/34, with eight losses: Collision both sides, Pilgrimage both sides, Swirl both sides, Contest side B, and Rushbait v2 side B. On Collision, Ming repeatedly tributed near (26,19) and locked the central altar at (27,20); our team died 22 and 14 times but dropped only 110 and 66 gems, indicating altar economy/control is more important than the death bags there. On Swirl, our teams died 47 and 34 times and dropped 98 and 242 gems. On Pilgrimage, the two losses ended 596–1016 and 692–1072; only side A lost gems to deaths (138), so the route fix does not close the broader farming gap.

Two isolated Collision checks failed to improve the 5/8 strong-proxy baseline. #146 kept the four champions on one shared objective through the mid-game and scored 4/8, losing both games to Ming and Xuanming. #147 put Varg's Power Strength emblem before Monster Strength; it stayed 5/8 and lowered its Ming-game gem average from 335 to 192. Keep the #145 draft and split schedule. Run folders are recorded in `bots/tungtungsahur/PLAN.md`. These proxies are not verified current top-50 matches.

On Swirl, #148 attempted to break an enemy altar lock with an unloaded champion while no enemy was visible. It scored 4/8 versus #145's 5/8 across Ming, Xuanming, faisal-orig, and opp-racer. It won all four weaker-proxy games but lost both sides against Ming and Xuanming; do not promote it. Preserve the #145 Swirl behavior.

## Swirl and Collision screens (#149–152, 18 Oct 2026)

Replacing Ryth with Tavi on Swirl tied the 5/8 v27 baseline but lowered the average gem total against Ming from 484 to 275. A 40% recall threshold limited to the exact Swirl counterdraft fell to 4/8 and still lost both sides to Ming and Xuanming. Keep v27's roster and recall thresholds.

Two Collision opening changes were also rejected. Varg solo-farming from round one scored 4/8 versus the fresh v27 control at 5/8, with Ming-game gems falling from 335 to 205 on average. A two-pair split (Stellar/Varg and Issac/Cassi) also scored 4/8; in its Ming games we submitted 66 and 132 gems versus 416 and 254 for v27. The results support a broader route-quality gap against Ming's coordinated camp planner; neither simple solo nor paired farming is enough. Run folders and full results are in `bots/tungtungsahur/PLAN.md`.

## Collision elite-camp avoidance (#153, 18 Oct 2026)

The v27 Collision opening diagnostic showed all four champions walking toward the same enemy-side camp group with three elks: 108 gems, 7,200 total health, and 180 damage per turn. The champions repeatedly died and retried this camp. #153 gates a rule to Collision's 41×41 map with altar (27,20), excluding groups whose combined camp damage exceeds 100 per turn from farming targets.

Against Ming, Xuanming, Faisal-bot, and opp-racer on both sides, #153 scored 6/8 versus a fresh v27 control at 5/8. It flipped both side-A losses against Ming and Xuanming to wins, but flipped Xuanming side B from a win to a loss. On the full 20-opponent Collision pool, #153 tied v27 at 37/40: it gained side-A wins against opp-tts-aggro and opp-tts-v5, and lost side-B wins against opp-tts-v3 and opp-tts-v4. Keep it as a Collision-specific candidate for further testing; do not treat the broad tie as an overall league improvement. Full run paths and hashes are in `bots/tungtungsahur/PLAN.md`.

On the exact strong-proxy set, a full 17-map run tied v27 at 121/136. Collision rose 5/8→6/8, while Lanes fell 6/8→5/8; all other map totals matched. Keep v27 as the verified full-map baseline; #153 does not improve the aggregate result in this sample.

The rule is map-gated: on Swirl, #153 matched the fresh v27 control exactly at 5/8 with identical per-opponent gem totals (`20261018-014231` vs `20261018-014237`).

## Pilgrimage squad follow-ups (#154–155, 18 Oct 2026)

A balanced 3/3 opening split moved Varg to Cassi & Issac's squad but scored 5/8 versus v27's fresh 6/8. It won both Ming games and lost both Xuanming games. Returning to one shared objective only during the fight alarm also scored 5/8 (Ming 1/2, Xuanming 0/2). Keep the standard Pilgrimage behavior; both splits traded away wins against a strong proxy. Run details are in `bots/tungtungsahur/PLAN.md`.

## Pilgrimage: five-pick combat order (#156–158, 18 Oct 2026)

Static mage-first improved the four-strong-proxy Pilgrimage screen from 6/8 to 8/8, but lost 2 wins in the 20-opponent Pilgrimage pool (29/40 versus v27's 31/40). Gating the change to Pilgrimage tied the full strong-map aggregate at 121/136; it did not improve the broad result. Raising mage priority only during a fight alarm scored 5/8 versus v27's 6/8. Keep the original action order. Details and replays are listed in `bots/tungtungsahur/PLAN.md`.

## Collision full-pool follow-up (#153/v28)

Across all maps and 20 local opponents, v28 scored 622/680 against v27's 620/680, but the difference is not attributable to the Collision rule: Collision win flips balanced two-for-two, and Lanes changed by two wins despite no Lanes code change. With no seed control in `cambc run`, keep the result marked inconclusive; the Collision-only pool itself remains tied at 37/40. See `bots/tungtungsahur/PLAN.md` for run IDs.

## Collision: threshold refinement (#160, 18 Oct 2026)

Skipping only camps above 150 damage/turn scored 6/8 against the four strong proxies, tied #153/v28 on the full Collision pool at 37/40, and tied v27 across all maps at 121/136. No broad or strong-set gain; keep the v27 farming baseline and reserve v28 for live validation.

## Contest: Willow for Ryth counter-draft (#161, 18 Oct 2026)

Replacing Ryth with Willow on Contest tied v27 at 7/12 on a six-opponent targeted screen, but shifted results away from the four strong proxies (4/8 vs 7/8) toward opp-fai-casters (2/2 vs 0/2) and opp-tts-locker (1/2 vs 0/2). The full 20-opponent pool scored 21/40 versus a fresh v27 control at 32/40 (the earlier v27 Contest pool also scored 32/40). Reject the swap and retain v27's Contest draft. See bots/tungtungsahur/PLAN.md for run IDs and hashes.

## Contest: reduced early gold weight (#165, 18 Oct 2026)

Contest only awards gems from its two Monoliths, but gold camps still fund equipment. Removing their early value or keeping the whole team in the early phase regressed against the four strong proxies (3/8, 4/8, and 6/8). Keeping the usual phase split and lowering the early gold weight from 2.0 to 0.25 performed better: 8/8 against the selected strong Contest proxies, 33/40 twice against the full 20-opponent Contest pool versus v27's 32/40, and 122/136 across all maps versus v27's 121/136. The full-pool improvement came from opp-fai-casters side A; the all-map strong gain came from Ming Contest side B. Keep the 0.25 rule isolated for live testing. It is uploaded as separate test submission v29 but has not been verified against current top-50 teams. See bots/tungtungsahur/PLAN.md for all run IDs and hashes.

### Contest rule cross-map broad check

The full local pool scored 619/680 for v29 and 620/680 for a fresh v27. Contest remained 33/40 versus 32/40; Pilgrimage shifted by two wins against v29 even though this rule is Contest-gated, while the other maps matched. Since the runner does not pair seeds, the all-map total is inconclusive. The repeated Contest-specific improvement is the reason to keep v29 isolated for live testing; it is not evidence of an overall full-pool gain.

## Pilgrimage bank-route follow-ups (#166–167, 18 Oct 2026)

A 68-gem threshold for the allied-half route penalty tied v27 at 31/40 in the full map pool but fell from 6/8 to 5/8 on the strong proxies. The 92-gem Ryth death replay was byte-identical because the survival retreat returns before the bank routine. Trying the safe bank route before retreat for low-health 68+ gem carriers tied the strong set at 6/8 but fell to 30/40 in the full pool, losing one opp-tts-v2 and one locker side while gaining my-bot side A. Reject both changes and retain v27's current banking and survival order.

### Follow-up screens (#168–170, 18 Oct 2026)

Adding a 40-point surcharge for locked altars (#168) tied v27 at 6/8 strong and 31/40 on the full Pilgrimage pool; it did not prevent Ryth or Varg from dying with 92 gems. Moving banking before combat burst actions (#169) tied at 6/8 strong and scored 28/40 in an unpaired full-pool run, versus v27's recent 31/40. Raising the health retreat threshold to 55% for carriers with at least 68 gems (#170) also tied at 6/8 strong and lost both sides against opp-tts-v3; Ryth still died with 92 gems, one round later. Reject all three and keep v27's current Pilgrimage bank and retreat behavior. Run IDs and hashes are in bots/tungtungsahur/PLAN.md.

## Contest gold-weight refinement (#171–172, 18 Oct 2026)

Varying v29's Contest-only early gold weight from 0.25 to 0.5 or 0.1 reduced the strong-proxy result from 8/8 to 7/8 for each variant. Reject both; retain 0.25 as the strongest tested Contest setting, pending live top-50 validation. The variants were not run on the full pool; see bots/tungtungsahur/PLAN.md for hashes and run IDs.

### Contest altar-lock response (#173)

Sending an empty-handed Tank to clear an enemy altar lock when an ally carried gems nearby and no enemy was within five tiles tied a fresh v29 control at 3/8 against the four targeted locker/caster proxies. Both runs had 267 team deaths. Reject the diversion and keep the current Tank farming/defense behavior. Run details are in bots/tungtungsahur/PLAN.md.

### Corners opening split (#174)

On Corners, bypass the shared early team-farm objective and let role-based objectives split from the start. The full 20-opponent map pool improved 34/40→36/40 in two candidate runs; the six-opponent targeted screen improved 6/12→9/12. In an unseeded 680-game comparison, all-map scores tied at 620/680, with Corners +2 and Pilgrimage -2 even though the change is Corners-gated. Keep this as a map-specific candidate and do not claim an all-map gain.

### Contest + Corners combination (#175)

Combining #174 with Contest's tested 0.25 early-gold weight scored 69/80 across the full Contest and Corners pools on two identical runs: 33/40 Contest and 36/40 Corners. v27 scored 66/80 on those maps (32/40 and 34/40). Submission version 30 is available for unranked validation; live top-50 streak remains 0/10.

### Contest high-DPS camp avoidance (#176)

On Contest, avoid farming groups above 100 damage per turn until late game. This scored 39/40 on two full 20-opponent pool runs versus #175's 33/40. Repeat-loss replays showed much lower death counts and earlier gem tributes, including 68→31 deaths vs opp-tts-v4 and 77→24 vs opp-tts-locker. The 680-game comparison was 628/680 versus #175 at 621/680; Contest improved by six wins and the all-map result's unrelated Lanes and Stampede changes were +2 and -1. The only Contest loss tied at 600 gems and lost the lifetime-gold tiebreak.

Mid/late Contest gold values of 0.25 and 0.05 scored 38/40 and 37/40. The 0.25 variant lost both my-bot-v2 games without submitting gems. Keep #176's safer camp rule and do not add mid/late gold weighting. Test versions 31 and 32 contain identical #176 builds; neither is the production submission.

### Remaining v31 local-proxy loss pattern

opp-tts-v5 scored 25/34: its Swirl win involved 66 of our deaths, 1,050 gems lost, repeated tributes near (22,18), and locks around (21,19)/(23,10); both Collision sides also lost with locks at (27,20). opp-tts-v3 scored 28/34 and won both Pilgrimage sides (136–1004 and 884–1036); side B lost 92 gems on deaths, while the opponent locked altars at (14,3) and (35,3). opp-tts-v4 scored 28/34 and, with v5, won both Packs sides. These are local proxy traces, not live top-50 evidence.

### Swirl follow-ups (#179–180, 18 Oct 2026)

Extending #176's high-damage camp avoidance to Swirl scored 34/40 versus a fresh #176 control at 35/40. Broadening the parity-retreat draft trigger to Ryth/Cassi & Issac/Stellar/Tavi scored 30/40; it fixed both opp-tts-v5 sides but regressed other opponents, including opp-tts-locker. Reject both and preserve #176's Contest-only camp avoidance and existing Swirl trigger. Run IDs and source/WASM hashes are recorded in `bots/tungtungsahur/PLAN.md`.

## Packs opening split (#184, 18 Oct 2026)

The loss replays pointed to slow gem farming: version 31 scored its first 44 gems around round 100, while the top local replay scored 44 by round 35. Letting the existing role-specific objective phase start on round 1 split the team into two farming pairs (Ryth/Stellar and Issac/Cassi). This scored 38/40 in two full Packs-pool runs against a fresh version 31 control at 34/40, and won all four targeted Packs games against opp-tts-v4 and opp-tts-v5. In the unseeded 680-game all-map comparison, it scored 632/680 versus 628/680 for version 31; Packs was the only map total that changed (34/40→38/40). Keep #184 as the best local candidate for Packs, pending live validation. Full run IDs, replay recovery, and hashes are in `bots/tungtungsahur/PLAN.md`.

Candidate #184 is uploaded separately as test submission version 33. The supplied group URL is still the finished 17 Oct FRChronic 0–5 group with null submission versions, so it does not test version 33. Live top-50 streak remains 0/10.

### Packs combat leash (#185, 18 Oct 2026)

Keep #184's opening split, but restrict Packs enemy engagement to normal attack range until round 600. Against Faisal-bot and opp-tts-locker this won 4/4 versus a fresh #184 control at 2/4, converting both of #184's side-A losses. The full 20-opponent Packs pool remained 38/40 in two candidate runs, tied with a fresh #184 control at 38/40; the two losses shifted to opp-tts-v4 and opp-tts-v5 while the control lost to Faisal-bot and opp-tts-locker. Retain #184 as the strongest measured local all-map candidate; #185 is an unuploaded alternative, not a pool-wide improvement. See `bots/tungtungsahur/PLAN.md` for replay IDs and hashes.

### Pilgrimage role split and early leash (#186, 18 Oct 2026)

The v3 replay showed an early farming deficit (zero gems on our side by round 700 versus 796 for the enemy). Starting Pilgrimage's role-objective split on round 1 and keeping early engagement at attack range scored 34/40 twice, versus a fresh #184 control at 29/40. On the same-runner 17-map comparison it scored 636/680 twice versus 632/680 for #184; Pilgrimage gained five wins, Lanes lost one, and the other 15 maps matched. The focused strong-proxy screen tied overall at 6/10, while the four-strong subset regressed 4/8 to 6/8 because the v3 gains came with two Xuanming losses. Favor this opening as the best local all-map candidate, but seek live validation and monitor Xuanming. The verified bundle was uploaded separately as test submission v34; it has not yet been selected in a fresh match group. Run IDs and hashes are in `bots/tungtungsahur/PLAN.md`.

## Top-50 replay update (18 Oct 2026)

After test candidate #189/v35, live groups against ranks 1–3 showed that the old local map scores do not transfer reliably. The detailed results and replay links are in `analysis/live-top50-match-review-20261018.md`.

- **Swirl, Collision, Pilgrimage, Contest:** all four lost to both ranks 1 and 2. Swirl had zero gems and 24/26 deaths; Collision banked only 22 against rank 2; Pilgrimage banked 388 against 1,112; Contest had zero gems and 67/97 deaths. The rank-2 enemy's repeated draft core was Ren/Stellar/C&I/Ryth/Varg. A Pilgrimage trigger broadened to that core regressed its local screen (#190); a Swirl Ren-for-Varg draft also regressed (#191).
- **Lanes and Expanse:** both lost to rank 3 with zero kills and at most two HC deaths, so these are farming-tempo losses. Mite dealt 66.1k/62.7k monster damage versus HC's 40.8k on Lanes/Expanse and banked about 1,000 gems on each.
- **Stampede:** the rank-2 result was a win, but rank 3 beat the same Prism/Stellar/C&I/Ryth/Tavi lineup 1,080–0. The replay recorded HC's first camp clear at round 329 versus Mite's round 32. Investigate the opening path and contested-camp arrival timing before changing the draft or equipment again.

The current production build remains unchanged. Live top-50 consecutive wins remain 0/10.

### Stampede opening follow-up (#192–193, 18 Oct 2026)

#192 avoids Stampede camp groups above 100 damage per turn until round 150, allowing the team to clear safer side camps first. It kept the four-strong-proxy 17-map score at 120/136, tied with a fresh #189 control. On the full Stampede pool it scored 36/40 versus 35/40 for a fresh control; the change traded two `my-bot-v2` wins for two `Faisal-bot` wins. It was uploaded separately as test version 36. The Mite rematch still lost Stampede 0–1080: side-camp clears began at round 35 and continued through round 146, while Mite reached the gem camp by round 124. Deaths dropped from 14 to 9, but our team submitted no gems. #193 forced gem-camp-only routing after round 100 and fell to 8/10 on the five-strong-proxy Stampede screen, below #192's 10/10. Keep #193 rejected; the next experiment should make the side-camp-to-gem-camp transition sooner without discarding #192's local gain.

### Procless #4 replay update (18 Oct 2026)

The new live five-map group against Procless lost 0–5 without bot faults. Collision exposed a large route delay: our first gem collection/bank was r79/r84, compared with Procless r21/r36. On Lanes and Pilgrimage, initial collection was within four and two rounds respectively, but our monster damage was lower by 27.8k and 55.6k. Swirl and Contest remained combat failures: 17 deaths/2 kills and 58 deaths/7 kills, versus Procless 3/12 and 11/45. See `analysis/live-top50-match-review-20261018.md` for the full table and exact summaries.

Stampede route experiments #194–196 did not beat the fresh #192 control (8/10, 7/10, and 9/10 versus 10/10). Burst-before-retreat #197 also regressed on Swirl/Collision/Contest (17/30 versus 20/30). Keep all four isolated and reject them.

### Collision opening candidate #198

The Procless replay showed two early deaths to camp damage before the first gem collection, at r79 versus the enemy's r21. Adding the Collision-specific >100 damage-per-turn camp exclusion to #192 scored 7/10 twice on the five-proxy Collision screen versus fresh #192 at 5/10 twice. Across all 17 maps against five strong proxies it scored 142/170 versus 140/170, with Collision improving 5/10→7/10 and every other map unchanged. The 680-game broad pool was 637/680 versus 636/680, but the only aggregate map gain was an unseeded Pilgrimage flip, not Collision. This is promising targeted evidence, but live confirmation is needed.

The verified candidate was uploaded separately as test version 37; the Procless re-test is group `4a2bd4ac-4623-4896-8e3f-d8d026845e71` and finished 0–5. The opening fix transferred: our first Collision camp clear, gem collection, and bank moved to rounds 10/19/41, versus Procless at 14/21/61. It still ended 22–1,002 with 14 deaths, 0 kills, and 204 gems lost; Procless had 0 deaths and 10 kills. The replay therefore isolates the remaining issue to surviving the fight and protecting collected gems, rather than reaching the first camp.

Collision-only earlier retreat variants (#199 parity and #200 1.15× strength) scored 5/10 and 6/10 on the five-proxy map screen, below #198's 7/10. Reject both. See `bots/tungtungsahur/PLAN.md` for source hash, ZIP hash, and run folders.

## Rank-5 live map results and Fragment draft test (18 Oct 2026)

The rank-5 new team(4) groups used Ambush, Corners, Eight, Fragment, and Rushbait v2. The first group, likely test v37, lost all five. Four maps showed roughly half the opponent's monster damage; Fragment was worse (20.5k vs 74.6k), with 22 deaths to 4 and 4 kills to 14. Ambush was a pure economy race: no deaths either side, but 28.4k monster damage and 404 submitted gems for us versus 49.5k and 1,024 for the opponent. Earlier first banks on Ambush, Fragment, and Rushbait did not compensate for lower ongoing camp income.

Candidate #201 let Varg solo safe camps during the early phase. It scored 113/136 on the 17-map strong-proxy set versus #198's 120/135 (one control run failed); Collision dropped 6/8 to 4/8 and Pilgrimage 8/8 to 5/8. Reject it; soloing Varg early is not a safe global fix.

Candidate #202 copies the top-5 Fragment draft Varg / Stellar / Ryth, replacing the standard four-body Stellar / Cassi & Issac / Ryth roster only on Fragment. The repeated 16-opponent local screen improved 28/32 versus 23/32 twice; the 17-map strong screen improved Fragment 7/8 to 8/8 and had no completed-map regressions. In the v38 live re-test, the same draft still lost Fragment 215–1,001. It had 12 deaths and 0 kills against 0 and 11, and dealt 22.9k monster damage against 66.5k. Treat the lineup as a promising local draft, not a solution to Fragment's live farm and combat gap. Full run IDs and source/package hashes are in bots/tungtungsahur/PLAN.md.

## AlphaSlop rank-6 map results (18 Oct 2026)

The v38 test build lost on all five maps against AlphaSlop: Packs 188–1,028, Monolith 534–1,026, Rows 528–1,056, Ambush 404–1,024, Fragment 259–1,045. In Rows and Ambush no champions died or fought; our monster damage was 39.4k/26.3k against 68.9k/55.0k. Packs and Fragment also had heavy deaths. Candidate #202's Varg / Stellar / Ryth Fragment lineup still lost to AlphaSlop's four-body C&I / Ryth / Stellar roster. See the live review and PLAN log for per-map stats and group ID.

## Rank-7 live map results (18 Oct 2026)

Against Sneaky Bush Campers, the bot lost 0–5. Stampede accumulated 1,080 gems but banked zero after 23 deaths; the opponent submitted 1,080 with 10 deaths. Expanse (518–1,014) and Lanes (524–1,002) were mostly farm races with no more than three HC deaths. Interlock (364–1,032) and Elkring (450–1,026) also had large combat gaps, with HC deaths/kills 18/1 and 16/2 versus 2/12 and 3/13. Monster damage was lower for HC on every map. Detailed group records are in the live top-50 review.


## Ambush: v39 and round-150 follow-up

The corrected round-150 split scored 40/40 wins on the local 20-opponent Ambush screen and 6 deaths, versus a fresh round-1 split control at 37/40 and 28 deaths. The integrated version with the Fragment draft scored 120/136 on four strong proxies across all 17 maps, below the fresh Fragment control at 122/136; both scored 8/8 on Ambush in this small set.

Against rank 5, v39 first banked 72 gems at r99, ahead of the opponent's first r120 bank. It reached 178 at r144, then Cassi and Issac died to monsters at r145. The score stayed at 178 until r404; Issac later died carrying 106 gems. Against queue-time ranks 5, 6, 9, and 10, v39 submitted 596, 476, 702, and 462 Ambush gems and lost all four matches. Ranks 11–15 also lost their Ambush matches after repeating the r100 first deposit. Better opening timing did not become sustained farming against stronger opponents.

Avoiding all Ambush camps above 100 strength (#210) regressed to 34/40 with 49 deaths versus v39's 40/40 and 6 deaths. Do not use that broad camp exclusion. The unresolved Ambush problem is sustained gem production against stronger teams, alongside safe farming and survival.

## Live combat gaps on ranks 9–10

Rank-9 Boost's Swirl match ended 0–1,068 with 29 HC deaths, 1 kill, and 4.5k monster damage versus 84.4k. Rank-10 Univardisty of Shingtonwash's Contest match ended 0–1,000 with 86 deaths, 5 kills, and 15.6k monster damage versus 205.4k. These are combat collapses as well as economy gaps.


## Fragment: first v39 live wins

The Varg / Stellar / Ryth Fragment draft produced the first two v39 live wins, both on Fragment: 1,014–276 against Ad Astra (#26) and 1,006–598 against 剑桥夜爬者 (#29). The first had 8 kills to 7 and 53.1k monster damage to 51.2k; the second had 14 kills each and 61.1k monster damage to 63.4k. Both had zero platform-reported bot faults. The v39 live campaign now has 2 wins in 110 completed matches; both wins were separated by losses, so the maximum consecutive streak is one and the current streak is zero.

The following rank-30 KKB group (`45c52751-c4fa-4377-8db3-11f8fa2958a0`) lost on Fragment, 483–1,013, despite the Varg / Stellar / Ryth draft. HC had 6 kills to 14 and 52.3k monster damage to 66.7k. The other four maps also had less HC monster damage, with 2, 8, 14, and 18 deaths respectively on Ambush, Corners, Eight, and Rushbait v2. The two Fragment wins have not yet generalized to this nearby rank-30 opponent.

KKB used Ren / Cassi & Issac / Stellar on Fragment; Ren made 8 kills and Stellar 6. A local Fragment draft replacing Varg with Vendetta/Ren reached 23/32, below Varg / Stellar / Ryth at 28/32, so the live matchup suggests a future counterdraft experiment but does not justify replacing the general lineup.


## Rank #31 map check — umamusume

The latest group (rank #31) also lost all five maps. Farm damage was lower on each: Fragment 42.2k vs 65.7k; Ambush 42.1k vs 86.9k; Packs 15.9k vs 54.5k; Monolith 32.6k vs 64.3k; Rows 39.4k vs 77.0k. Packs and Fragment also had 17 and 20 deaths. This keeps sustained camp output as a shared issue across both open farm maps and combat maps.

The #31 Ambush replay suggests an item question, but the isolated Ryth damage build (#213) tied the local control at 31/32 and lost 9.6 gems per game on average. Keep the v39 health build for now; improving one champion's camp damage was insufficient.

## Rank #31 Master of Betas map check

Master of Betas won all five tested maps, with monster damage exceeding ours on each. Swirl (36–1,058, 29 deaths, 12.3k vs 81.2k monster damage) and Stampede (0–1,080 despite 18 deaths) were the sharpest failures. This adds more evidence that gem collection without survival and deposit timing is not enough, and that Swirl needs a substantially different combat plan.

## Rank #33 Memory? map check

Memory? won 0–5. Contest ran to round 2,000 with no gems collected or submitted; the normal timer tiebreak went to Memory? on lifetime gold (11,775–575), with kills 99–1 and deaths 1–121. This was a fight/survival failure, not a different map win condition. On Fragment and Collision our kills were 0/14 and 1/10 respectively; all five maps had lower HC monster damage.

The #33 Memory? Contest replay exposed a first-contact collapse: first deaths were at r42 (Ryth) and r48 (Prism, Cassi, Issac), all to the opponent's Ryth; by r57 another two champions fell to Varg. A Contest draft swapping Prism for Vendetta/Ren scored 6/8 versus 7/8 for v39. Swapping Prism for Varg tied 7/8 but submitted 1,000 fewer gems and traded the losing matchup. Keep the v39 lineup; the opponent-mirror response was not locally supported.

Contest candidate #216 applies the parity retreat trigger whenever the active map is Contest. It scored 40/40 against the full local pool versus a fresh v39 control's 39/40; its only flipped result was a win over a control-side 600–600 tie. On four stronger local proxies, both builds went 8/8 on Contest, but #216 deposited 7,600 gems versus 7,200. Across all 17 maps and those same proxies, overall wins were tied 125/136, and every map's win count matched. Uploaded as test version 40 for live validation; local screens do not count as top-50 wins.

The first live test against queue-time #26 Cabbage (group `8da6a23e-ca78-4e29-bf01-61152c1bd182`) lost 0–5. Contest was still a wipe: the enemy group was visible by r30, Cassi and Issac died at r42, and the team finished 0 banked gems with 93 deaths and 4 kills. Swirl lost 36–1,034 with 31 deaths; Fragment lost 124–1,020 with 18 deaths; Stampede lost 120–1,320 and only cleared 28.5k monster damage to 73.9k; Ambush banked 928 vs 1,086 with no deaths. The retreat adjustment is not enough against a top-50 early engage. Revisit Contest's opening and farming split; keep v40 out of production.

Replacing Prism with Varg on Contest (#217) scored 36/40 versus v40's 40/40 on the full local Contest pool; reject. A move-retry patch (#218) that replans around a newly occupied destination tied v40 at 40/40 on local Ambush but was lower on the four-proxy all-map screen (123/136 vs 125/136), with losses on Elkring and Stampede. It did not reproduce the Ambush movement error locally, so keep it unuploaded pending better evidence.

Queue-time #29 Still Testing (group `bd89f7c3-e3df-4103-97bd-e012f1570c80`) lost 0–5 on Corners, Eight, Pilgrimage, Rows, and Rushbait v2. Monster damage lagged on all five. Rows was a farm-only loss: 528/1,056 submitted gems, no deaths or kills, and 38.7k/71.9k monster damage. Corners and Pilgrimage combined weak farming with losses in combat. Continue prioritizing farming pace and reducing time spent away from gem camps.

Queue-time #34 EggsAfter11AM (group `e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1`) also beat us 0–5. Monster damage and earned gold were lower on all five maps. Monolith and Lanes were mostly farm races; Elkring, Interlock, and Collision added heavy combat losses. Elkring finished 216/1,044 submitted gems with 18 deaths and 1 kill; Interlock 292/1,010 with 17 deaths and no kills; Collision 102/1,002 with 16 deaths and 1 kill. Enemy champions commonly bought damage emblems and then Durability Health; some also completed Jungle Health. This is an opponent-build correlation, not a proven cause. Issac's one-champion Durability second-emblem experiment (#137) tied the previous local control, so it does not support a broad change. A targeted new build needs controlled local evidence.

Queue-time #15 Zarzorki (group `deec6df3-1b7f-438d-9221-70e00a5a4591`) beat the v40-likely test 0–5. Ambush and Rows again showed a farm ceiling without contact: 702/1,092 and 528/1,056 submitted gems, zero deaths, but monster damage was 41.9k/80.6k and 38.7k/74.3k respectively. Contest parity retreat did not transfer: our first deaths were Ryth r40, Stellar r48, Issac and Cassi r50, and Prism r56; final totals were 77/5 deaths, 3/64 kills, and 3.7k/187.0k monster damage. Elkring's 23/3 deaths and 90/1,062 banked gems show both combat and gem-retention problems. Fragment's Varg / Stellar / Ryth draft lost 204/1,048 with 10/20 kills, so that draft is not a general solution against top teams. Prioritize a new Contest opening and sustained monster damage; do not treat local wins as top-team validation.

Queue-time #31 SilverSamurai (group `bfadbe71-52dd-41fc-9d3f-3fda1e00e13d`) beat the v40-likely test 0–5, again with less monster damage on all five maps. Expanse (518/1,106), Lanes (648/1,010), and Monolith (548/1,062) were no-contact farm losses with 2, 3, and 6 HC deaths respectively. Packs (396/1,032, 17/7 deaths, 4/12 kills) and Swirl (72/1,078, 25/10 deaths, 2/18 kills) also collapsed in combat. This repeats the cross-map issue: the bot does not sustain camp damage and gem income long enough, while bad fights make the gap worse on compact maps.

Queue-time #35 conqueror_of_openai (group `a40b7063-19c9-47f9-af57-a7420f12bd3f`) beat the v40-likely test 0–5. Monster damage was lower on every map. Corners was the closest match (666/1,014 gems, 5/4 deaths, 4/4 kills, 50.9k/68.9k damage); Pilgrimage banked every collected gem but had a 27.2k/78.7k monster-damage gap. Eight, Interlock, and Collision added heavy combat and gem-loss problems. This suggests fights worsen the deficit, but are not its only source: even when champion trades and banking were controlled, the bot lost the farm race.
 
## Recent top-50 replay follow-up — open-map farming and Contest collapse

Three additional live groups against hello (#26), Ad Astra (#28), and 剑桥夜爬者 (#27) add 15 maps of evidence. The match-group interface does not provide timeline summaries, so the values here are captured team-A scoreboard snapshots and observed death events from the downloaded stdout logs. Expanse against Ad Astra ended 518–988 with only two captured deaths; Lanes against 剑桥夜爬者 ended 584–942 with three. These point to route throughput rather than combat as the main deficit on those matches. Candidate #219's round-1 generic role split lost its local paired screen 22/24 to v40's 23/24 and had slightly lower average gems on all three tested maps, so it does not fix this.

Contest remains a separate acute failure: hello killed 121 captured times, starting at rounds 31–35; 剑桥夜爬者 killed 67 times, starting at round 33. Both matches finished 0 score against 800. The parity-retreat candidate's local Contest score is not transferring to top-50 fights. Investigate the opening and early survival behavior before reusing the same retreat threshold. Ad Astra's Fragment match was a strong exception: our last logged score was 992–276, giving one win in that 1–4 group.
 
## Rank-35 and rank-36 follow-up

Two more top-50 groups continued the same pattern. Rank-35 Trzy Kwaterki beat us on Ambush 688–928 and Monolith 504–946 with only five and three captured deaths; Corners was 526–976 with seven. Rank 36 beat us on Ambush 476–914 with eight deaths, Corners 402–966 with seven, and Monolith 548–968 with seven. These are mostly farm-output losses. Elkring and Collision/Pilgrimage had more deaths and combined the farm deficit with combat losses.

Three isolated hypotheses were locally rejected: generic early role split (#219: 22/24 vs 23/24), Expanse Stellar Monster Strength first (#220: 8/8 tied wins but fewer gems), and safer open-map split with early combat preserved (#221: 21/24 vs 23/24). Contest's one-enemy-margin retreat (#222) scored 39/40 vs v40's 40/40. A better direction is needed before changing production.

## Valenki live follow-up — rank #38

Group `e67a83d6-499e-4ab2-bb85-30b776ae3fff` confirms the open-map farming gap with full match summaries: on Expanse and Rows, HC banked all the gems it collected and had only two and one deaths, yet monster damage was roughly half the opponent's (36.96k/72.85k and 41.39k/72.90k). Earned gold was also less than half, so these were route/clear-throughput losses rather than fight collapses. Lanes showed the same damage/gold deficit with five deaths and no kills.

Contest is a different failure mode: zero gems collected, 45 deaths to 19, 10 kills to 33, and 26.6k/171.9k monster damage. The first Cassi/Issac deaths happened at r109, followed by the rest of the team dying repeatedly. Fragment combined both issues: 482 collected but only 344 submitted, 12/7 deaths, and 33.1k/71.2k monster damage. No bot faults occurred. The prior user-roster candidate #223 remains below v40 locally (28/40 vs 39/40), so continue improving it in isolation rather than uploading it unchanged.

## EvilMangohh live follow-up — rank #39

Group `ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b` shows that low monster damage persists on Stampede, Ambush, and Pilgrimage even without many deaths. HC damage was 34.3k/81.3k on Stampede (6/0 deaths; all 360 gems banked), 33.6k/66.1k on Ambush (7/1 deaths), and 26.9k/76.8k on Pilgrimage (12/3 deaths). Gold earnings lagged by 3.1k–4.2k. These are route, target uptime, itemization, or camp-damage problems beyond survival.

Swirl and Packs were combat collapses: 33/13 deaths and 20.0k/92.5k monster damage on Swirl; 20/0 deaths, 0/14 kills, and 14.9k/60.4k damage on Packs. On Swirl the first deaths were Ryth r22, Stellar r36, and Cassi/Issac r38. The opponent drafted Cassi & Issac, Stellar, Ryth, and Ren, which does not match the current narrow Swirl counterdraft condition. This is a specific matchup for the next local counterdraft screen. No bot faults occurred.

## Isolated follow-ups after the Valenki/EvilMangohh replays

The Swirl retreat extension for EvilMangohh's C&I / Stellar / Ryth / Ren composition (#224) tied its v40 control 8/14 against seven local opponents and earned fewer gems versus `opp-swirl-meta-core`; reject. A balanced fixed-roster shopping queue (#225) tied the #223 baseline at 28/40. Moving Vendetta's Power Strength ahead of her Health purchase (#226) improved the fixed-roster screen to 30/40, especially on Lanes and Rows, but average gems remained flat and it was still below v40's 39/40. These are isolated candidates only; do not upload them.

## Fixed-roster v41 live result against 天使 (#46)

The v41-like fixed-roster group `112d14b4-4b01-4ef0-b1fd-011dd07c8f6b` lost 0–5. 天使 selected Cassi & Issac on all five maps, giving the opponent one more active body on every map. The lineup disadvantage was compounded by distinct failures: Expanse and Rows had near-zero combat but about half the opponent's monster damage and gold; Contest ended 0–1,000 with 71/3 deaths and only 2/71 kills; Fragment banked only 168 of 212 collected gems and had 0/10 kills. No bot faults were reported. Full data is in the live review and replay folder.

Candidate #227 preserves a ready Willow heal when an ally is below 30%, preventing generic burst from spending her one ability cast first. It tied #226's 30/40 local result, so this behavior did not change local proxy outcomes; it is nevertheless the more faithful implementation of the requested support priority. Its OneTap (#47) test, group `83c42928-b082-4ca7-a423-aadb3ce617ae`, lost 0–5.

OneTap's Expanse (24.8k vs 69.2k monster damage) and Rows (28.4k vs 68.9k) replays show the same farm-throughput deficit with only three and zero deaths. Lanes also lost its monster-damage race (36.1k vs 71.4k). Contest and Fragment add combat collapses (32/5 and 14/2 deaths; 2/32 and 1/13 kills). Cassi & Issac provided an extra opposing body on four maps, but that does not explain the low-death Expanse/Rows gap. Review the downloaded summaries/replays in `matches/live/83c42928-b082-4ca7-a423-aadb3ce617ae/`.

## Contest: prioritize its only gem camps

The v43-likely group against E=mc²+AI³ (`cfe10790-872f-4df1-9664-863139501d2d`) lost Contest 0–1,000 with 25 deaths and 50.8k/121.6k monster damage. Replay inspection found that we cleared gold-only groups #3/#4/#2 repeatedly and never attacked either of the two Monolith groups. The map dump confirms each Monolith group yields 200 gems; all other camps yield zero gems. Existing logic favors gold-only camps early, reduces Monolith value to 20%, and blocks >100-strength groups until late. The opponent cleared the two Monoliths near rounds 387 and 675 and banked at round 431. The next local test should let the team select Monolith as the shared objective while keeping gold-only camps low priority and checking whether a full-party clear survives; immediately opening all strong camps (#234) scored only 18/40, and late-only changes (#235/#239) did not work. Full replay is in `matches/live/cfe10790-872f-4df1-9664-863139501d2d/`.

## Contest vs WHIM: opening survival still dominates

The v44-likely fixed-roster test against queue-time rank-50 WHIM (`a5faf63f-bd4e-400c-8eaa-8da44f2d77c3`) lost Contest 0–1,000 with 64 deaths to 6. The first Ryth death was at round 34 to a camp, followed by Willow at 54, Vendetta at 68, and Prism at 71. This happened well before the candidate's round-450 Monolith switch. WHIM's Cassi & Issac / Stellar / Ren / Varg / Ryth lineup cleared the two Monolith routes and dealt 230.3k monster damage to our 12.4k; our side earned only 445 gold to 14,060. The delayed objective choice cannot compensate for losing the opening camp race and frontline.

#245 gained local Contest gems (820 mean vs #233's 645) but lost local wins (31/40 vs 33/40) and the top-50 group ended 0–5. #246 reached 32/40 local Contest but was below baseline on the integrated five-map screen (28/40 vs 31/40). These should remain rejected. Re-test the opening and equipment under the prior multi-body meta draft before trying another live Contest variant.


## Rank #47 WHIM — five-map replay follow-up

The v45-likely meta-control submission lost 0–5 to WHIM's C&I / Stellar / Ren / Varg / Ryth drafts. Contest collapsed at the first central fight: Ryth died at r30, followed by 98 team deaths and 19 kills; WHIM finished with 28 deaths and 79 kills. We collected 400 gems but banked none. Monster damage was 12.6k vs 256.9k. On Expanse, Rows, Lanes, and Fragment the same throughput deficit persisted: our monster damage ranged 22.8k–43.4k, against 65.8k–76.9k for WHIM. Rows had just two deaths, pointing to slow camp clearing even without combat collapse. Replays and raw summaries are in `matches/live/c559fb26-1c62-44cf-b7ea-32116ca9acdb/`.

The current Contest draft (Prism / Stellar / C&I / Ryth / Tavi) gives up the opposing team's Varg and Ren roles. Draft-only local substitutions did not beat the 40/40 control: WHIM's full lineup 36/40, Varg-only 36/40, and Ren-only 37/40. Immediate Monolith access plus that draft scored 21/40. Next isolate survival under a central early engage and improve damage uptime before revisiting gem-camp aggression.


A Contest-only one-enemy retreat check on the fixed user roster (#253, based on the round-400 objective variant) scored 30/40 vs its #245 baseline at 31/40, so the more cautious trigger alone did not improve proxy results. The off-roster Ren draft with that trigger tied at 37/40 (#252) and also remains rejected.


Two follow-ups also failed to improve local results: #254 copied WHIM's lineup on all five maps and scored 188/200 vs #248's 197/200; #255 gave Ryth a Durability Health emblem before Jungle Health and scored 29/40 Contest vs #245's 31/40. Keep the existing draft and tank build for the next fixed-roster test.


## Please — fixed roster vs map-size counterdraft

The rank-50 Please match confirms a large throughput gap. Fixed-roster v46 lost 0–5. On Expanse and Rows it had zero or two deaths and no kills but dealt 28.2k and 28.4k monster damage versus 62.4k and 68.9k. Contest reached the 2,000-round cap without gem submissions; HC had 79 deaths and 7.2k camp damage to Please's 11 and 183.8k.

The v47 map-size counterdraft used C&I / Stellar / Ren / Varg / Ryth and won Fragment, banking 1,014 vs 842 gems with 74.7k vs 63.2k camp damage and 30 vs 23 kills. It still lost Contest 0–1,000 on kills/farming (107 deaths, 4 kills, 22.0k monster damage vs 7, 71, 177.5k); Expanse, Rows, and Lanes also lost their gem races. This is one positive Fragment matchup, not a general strategy win. Detailed evidence is in the two group folders and the live review.


### Candidate #256 local follow-up

The exact map-size counterdraft with a Contest-only one-enemy retreat scored 185/200 on the five-map local pool, below #254 at 188/200. Reject the retreat change; retain #254 as the reference while testing item queues.


The v48 counterdraft item test (Power Strength -> Durability Health -> Power Strength for Varg/fighter/Issac) lost 0–5 to Please. It also lost Fragment, where v47 had won: 284/284 gems vs 1,020/1,020, 28 vs 8 deaths, 6 vs 20 kills, and 33.3k vs 65.0k camp damage. On Contest damage was 8.5k vs v47's 22.0k. Taking 5 Power shards before switching to defense still delayed too much damage for this team's income; next test keeps buying Power Strength continuously.


## Memory? — C&I and early combat

v49's top-50 Contest loss had 123 deaths / 2 kills vs Memory?'s 2 / 102, with 0 gems banked by either side. Memory drafted five independent units (Varg / Stellar / Ren / Ryth / Tavi); our C&I pair shared a death link, so one kill removes two bodies. On Expanse, Rows, and Lanes, no-death stats still show our camp damage below theirs: 33.6k vs 65.1k, 52.7k vs 68.9k, and 37.4k vs 65.7k. Fragment lost both the fight and farm race (433 vs 1,026 gems banked, 9 vs 16 kills, 32.1k vs 74.2k monster damage). Test the no-C&I lineup on Contest, but investigate camp-clearing throughput separately. Replay folder: `matches/live/0ab66a47-d3d9-4f88-92ad-5854b979e29e/`.


The Contest single-body lineup (Varg / Stellar / Ren / Ryth / Tavi) scored 37/40 vs 36/40 for the C&I / Stellar / Ren / Varg / Ryth lineup. V50 was tested against Memory? in group `3cbf32fc-50b9-4021-a59a-f06ed40fdfd9` and lost 0–5; the mirror draft still suffered 102 deaths / 6 kills and failed to farm. Detailed follow-up appears below.


## Rank-1 and rank-2 farm-throughput review

V50 lost 0–5 to Intercontinental Fish in group `39ffefa6-4fc3-447f-b6f2-00779d0c1616`. Expanse and Rows were low-contact gem races (0 deaths on Expanse; 2 on Rows), yet HC cleared 7/10 camps and dealt 33.0k/40.5k monster damage to Fish's 46/17 and 74.7k/68.9k. Contest and Fragment added severe combat failures. In Contest HC cleared 8 camps, dealt 8.0k monster damage and banked 0 gems; Fish cleared 81, dealt 194.0k, banked 1,000, and killed 55 champions while losing 3.

V51's Contest hold opening reduced HC deaths from 55 to 50 but also reduced camp clears 8 to 2 and monster damage 8.0k to 6.3k; it did not change the 0–5 result. Do not hold Ryth stationary. V52 changed Expanse's third draft pick from Ren to Varg; its single live Expanse sample increased HC camp clears from 7 to 17 and damage from 33.0k to 35.4k, but remained far below 46 / 74.7k and lost the gem race 584 to 1,016. Keep this as an experiment, not a proven map strategy.

V52 lost 0–5 to Mite (current rank 2). On Contest, both teams drafted Varg / Stellar / Ren / Ryth / Tavi; Mite's farm loop still cleared 128 camps vs HC's 1, produced 191.2k vs 2.3k monster damage, and ended with 116 kills to 0 while losing no champions. Mite banked no gems either; it won on the round-limit gold tiebreak. This confirms that draft matching alone does not address the Contest execution/farming bottleneck. Current top-50 campaign is 4/275 maps, max consecutive streak 1, current 0/10. Summary files and replays: `matches/live/39ffefa6-4fc3-447f-b6f2-00779d0c1616/`, `matches/live/dc38a306-c22c-416f-899a-a6d1eaabc880/`, `matches/live/d38357a2-8edb-4aa4-b6bf-5450b985c1cb/`, `matches/live/729a4de9-1426-4694-94c6-d10335409c67/`.

## Replay fuel diagnosis and open-map follow-up — 18 Oct 2026

The official v54–v56 likely replays show repeated `fuelExhausted` events while the match summaries still report zero `botFaults`. This is a lost/suspended action, not a crashing bot. Expanse (80×80) and Lanes (90×30) are the clearest cases: official farm damage stayed well below the opponents even with few deaths.

An instrumented local c275 build traced the opening path. Camp-group setup used roughly 69k of the initial 200k fuel on Expanse and 95k on Lanes; the map had 24 and 42 groups respectively. Ranking objectives then repeatedly invoked `deep_group`, which recomputed the nearest distance to each side's spawn region. Replacing only spawn-position extraction from the group bitboard had negligible Expanse impact and saved about 8k on Lanes. Sorting groups by theoretical value was rejected because sorting itself cost about 27k fuel on Lanes.

Candidate c276 preserves the original spawn bitboards and camp scoring. It caches exact Chebyshev distance for rectangular spawn regions (with an exact point-scan fallback for irregular regions) and checks the expensive enemy-side rule only after inexpensive scoring shows a camp can beat the current best. This candidate scored 30/30 against the local Faisal-bot, opp-fai-mirror, and opp-tts-v5 proxies over Contest, Expanse, Rows, Lanes, and Fragment. It scored 5/10 against c272 head-to-head, so it is a live test candidate, not a proven promotion. It was uploaded as separate test v57. Official results are pending the user's fresh group.

Live campaign at this checkpoint: **4/305 top-50 maps**, maximum streak 1, current streak **0/10**. Keep `bots/tungtungsahur/src/bot.cpp` and its ZIP unchanged until the user-defined 10-win streak is achieved.

### Full-pool control check after v57 upload

On the full 17-map pool against Faisal-bot, opp-fai-mirror, and opp-tts-v5, c276 scored 80/102 while the identical-pool c272 control scored 82/102. The candidate did not improve the aggregate, although it gained one win against Faisal-bot and one against opp-fai-mirror while losing two against opp-tts-v5. c277's representative-spawn shortcut tied at 80/102 and was rejected as less exact. v57 remains a test-only submission awaiting official evidence.


## Rank-5 top-50 result and c279 draft screen (18 Oct 2026)

The v57-likely group `79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f` lost 0–5. On Expanse, Rows, and Lanes the body counts matched, but our monster damage was 30.85k/44.55k/32.663k vs 62.45k/66.924k/63.745k and submitted gems were 398/660/444 vs 1,014/990/1,002. Contest had five bodies against six, followed by 69 deaths. Fragment had four against three yet suffered 22 deaths. Treat farm throughput and survival/fighting as the priorities.

`fuelExhausted` events were exactly one per champion on both sides and every map, also matching v55/v56; there were zero bot faults. This roster-sized event is not a useful optimization target by itself.

Draft-only c279 mirrors the exposed top-5 lineups on Contest, Rows, Lanes, and Fragment. Its local screen scored 28/30 across three proxies/five maps, with both losses on Lanes vs opp-fai-mirror; direct c279 vs c276 scored 6/10 and averaged 849 vs 761 submitted gems. Results are mixed; do not promote without an official result. See `analysis/live-top50-match-review-20261018.md`.


## c279/c281 candidate screen

c279 (v58) mirrored the rank-5 lineup on four maps; its local screen was 28/30 and direct result vs c276 was 6/10. c280's all-map Issac strength build was also 28/30 and reduced gem output, so reject that general rule. c281 (v59) used the strength build only on Rows and Lanes: 29/30 on the five-map screen and 7/10 vs c279, including all four Rows/Lanes head-to-head wins. The wider 17-map screen was 79/102 (c276:80/102, c272:82/102), so c281 is only a targeted live test candidate. No production changes.


## c282 / v60 equipment test

On Expanse, Rows, and Lanes, c282 gives Stellar Monster Focus shards first for the 10% camp damage emblem, then Power Focus. The five-map score remained 29/30, with lower opponent gem totals than c281; direct head-to-head was 8/10, 878 vs 788 average submitted gems, and c282 won both sides on all three farm maps. Full 17-map score remained 79/102, so keep it as a targeted official test, not a general upgrade. Uploaded separately as v60; no official group result yet.


## Equipment A/B result

Keep Monster Focus on Stellar only for Expanse / Rows / Lanes (v60/c282). Extending it to Cassi and Tavi (c283) kept 29/30 proxy wins but yielded more opponent gems and lost 4/10 vs c282. Replacing Monster Focus with Treasure Focus on Stellar (c284) also kept 29/30 but yielded still more opponent gems and lost 2/10. The item bonus choice matters: prioritize Monster Emblem's camp damage over Treasure Emblem's gold on these maps.


## Rows/Lanes Ryth item check

c285 changed Ryth to Monster/Power Strength on Rows and Lanes. It won both Lanes sides vs c282 but lost both Lanes sides to opp-fai-mirror, fell from 29/30 to 28/30 on the proxy screen, and had worse average gems head-to-head. Reject the Ryth strength build; keep v60's Ryth health equipment and Issac fighter equipment for these maps.


## Cassi/Tavi item isolates

Monster Focus on Cassi only (c286) and Tavi on both Lanes sides (c287) each swept their 30-game proxy screens but did not beat v60 head-to-head: 4/10 (813:829 gems) and 5/10 (809:825 gems), respectively. Do not expand Stellar's Monster Focus equipment. v60/c282 remains the best supported farm-map build.


## Rows / Lanes tank equipment follow-up: c288

Giving Ryth Monster Health then Power Health on Rows/Lanes preserved his tank health build and added the monster emblem. c288 converted c282's Lanes side-A proxy loss and scored 30/30 on the five-map screen. The 17-map result improved from 79/102 to 80/102, with the entire gain confined to Lanes (5/6 to 6/6). The direct c288/c282 10-game matchup was a side-B sweep, 5–5 overall, so it is inconclusive on the item effect. The candidate package is verified and uploaded separately as v61; keep the change isolated until live results. The v60-likely group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is already recorded in the Rows review; the user re-sent the same link on 18 Oct.

c289 swapped Ryth's second five health shards to Jungle Health, while c290 used Monster Health for both five-shard sets. Each stayed 30/30 on the five-map proxy screen but allowed more opponent gems than c288, with no additional wins. Reject both; retain Monster Health + Power Health for the local Lanes candidate.


## Rows live farm review (18 Oct 2026)

In the rank-5 group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34`, Rows was a zero-combat loss: 594 vs 1,056 banked gems, 38.854k vs 66.924k monster damage, and 9 vs 16 camp clears, with no deaths or champion damage. The next group `a96043a5-af65-4a93-a9af-971d34b1a879` repeated the exact Rows stats.

The replay event coordinates show the route difference. Our north-side team repeatedly cleared groups 0 and 2 (x=18 and x=31) but did not clear group 4. The south-side opponent farmed groups 1 and 3 plus group 5 (x=7). Each group is worth 66 gems; our side's multiple gem-collection entries often represent that reward split across allies. The throughput gap is the number of cleared groups, not the gem value of the groups selected.

The bot's leader/follower farming is organized around two objectives, and Varg's solo selector excludes multi-wolf packs. Rows follow-up c296 (Cassi Monster Focus), c297 (remove target stickiness), and c298 (healthy Varg solo wolf-pack exception) did not improve the control screen; all are local-only rejects. Test a third independent route or quantify pathing/target selection before revisiting equipment.

Debug trace c299 found that Ryth and Varg select group 4 but produce no camp-clear event there; Ryth was stationary at (38,9) on a sampled turn while still targeting that group. c300 applied Ambush's 12-turn no-progress target recovery to Rows, but did not improve the local screen or gem output. The remaining question is whether the camp is invisible, still respawning, or unreachable from the chosen approach; do not treat the trace alone as proof of a pathfinding bug.

Follow-up confirms group 4 was visible and partially damaged (three wolves at round 70, two at round 90), but never fully cleared. c301 skipping it regressed; c302 stronger target commitment tied control; c303 area-target optimization regressed. Keep the route available and investigate damage/retreat/target switching. None of these candidates was uploaded.

## Rank-1 group by map (18 Oct 2026)

Against Intercontinental Fish, Ambush banked 582/1,024 with no deaths but only 6/12 camp clears and half the monster damage; treat as a route/throughput problem. Corners banked 374/1,002 with 5/0 deaths, 13/41 clears, and 0/4 kills, combining farm and combat gaps. Expanse had 4/0 deaths but only 17/46 clears and 584/1,016 banked gems, another clean farm deficit. Fragment had 14/1 deaths and 10/24 clears, so both survival and farm need work.

Contest had the largest collapse: 0/1,000 gems, 76/2 deaths, 0/62 kills, 6.3k/200.7k monster damage, and 2/95 camp clears. Our roster had six physical bodies but no Willow; Fish's lineup had six bodies and two ranged carries plus Prism, with C&I and Ren. The first death at round 41 triggered a snowball. The late Focus-emblem discrepancy followed the gold gap; the first fix should be a safer opening and better survival, not assuming late-game shopping alone wins fights.

c306's map-specific Contest draft drops C&I and adds Willow, retaining Varg, Ryth, Stellar, and Tavi. It kept five independent bodies, swept c291 and three proxies on Contest (8/8), and tied the c291 full-pool score at 82/102. Uploaded as v63 for a targeted Fish test; result group 350cf6e4-a539-4b50-b612-63f2086b91d9 is queued.


## Contest and Expanse: latest Fish replay (18 Oct 2026)

Across v63–v65-likely groups, Fish won all five selected maps each time. Contest's v65 three-tile opening response converted some early pressure into 2 kills, but did not open farm space: 0:1,000 gems, 4:78 camp-clear event entries, 8.696k:188.144k monster damage, and 59:6 deaths. Keep the 3-tile response as a test candidate only; the 4- and 5-tile versions regressed local Contest screens.

Expanse is a direct route/economy comparison because both teams drafted Cassi & Issac / Stellar / Varg and dealt zero champion damage. Our team banked 584 vs Fish's 1,016 gems, cleared 17 vs 46 camp entries, and our first logged clear was at round 28 versus Fish's round 15. The side-A route repeatedly cleared the nearby groups at (5,12) and (5,22); Fish spread clears across its mirrored area. Investigate side-A camp arrival timing, target switching, and whether C&I/Issac spend too long on low-return camps before changing their item build.

Ambush remains a route deficit (582:1,024 gems and 6:12 clears, no deaths). Corners combines farming and combat gaps (374:1,002, 13:41, deaths 5:0, kills 0:4). Fragment combines both as well (102:1,020, 10:24, deaths 14:1, kills 0:14). All maps were fault-free.

c307, c308, c309, and c311 are rejected local variants. c310 is the only new tactical trial worth tracking: 8/8 Contest proxies, 82/102 all-map proxies (same count as c306), uploaded separately as v65, live group 0–5. Do not promote it.

## Rank-5 custom-map follow-up (18 Oct 2026)

The current v65-likely bot lost 0-5 to rank-5 new team (4) across rushbait_v2, rows, lanes, eight, and interlock. The same maps had already been tested with the earlier v60-likely build; the newer draft helped one opening but did not close the economy gap.

| Map | Banked gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 300:1,020 | 19:36 | 33.316k:54.768k | 3:0 | 0:2 |
| rows | 594:1,056 | 9:16 | 38.854k:66.924k | 0:0 | 0:0 |
| lanes | 538:1,008 | 19:46 | 35.860k:67.174k | 3:0 | 0:2 |
| eight | 132:1,008 | 7:19 | 27.481k:53.971k | 19:2 | 2:11 |
| interlock | 386:1,004 | 15:32 | 30.742k:62.578k | 13:4 | 3:9 |

Rows is the cleanest farming diagnosis: no champion damage or deaths, with our team clearing groups 0 and 2 while the opponent clears mirrored groups 1, 3, and 5. Gold was 2,430:4,320, so the equipment gap comes from clearing fewer camps, not an observed shortage of item choices. Rushbait improved from 212 to 300 gems and 9 to 3 deaths after the counterdraft. Eight includes Tavi, yet still had 19 deaths and only 132:1,008 gems. Interlock had 13:4 deaths and 386:1,004 gems.

Local c316 split-route scored 4/8 on Rows, 0/2 versus c310 and 0/2 versus c291; reject. Logging-only c317 confirms c310 has one shared early objective; local targets rotate group 0 to 2 to 4. The live Rows trace shows only groups 0 and 2 cleared, so arrival/readiness/path completion still needs diagnosis. Production and upload remain unchanged after v65.

## v66 Rows route test

Group 05465728-a486-48f7-8439-41b56bc27724 tested v66-likely against rank-5 new team (4) on the same five maps. It lost 0-5, and all map metrics exactly matched v65-likely. Rows remained 594:1,056 gems, 9:16 clear entries, and zero champion damage or deaths. The 3x preference for a damaged Rows wolf pack did not change the route; reject c318/v66. A stricter finish commitment needs a progress escape so the bot cannot remain stuck on an unreachable or stalled camp.

## v67 Rows lock test and follow-up (18 Oct 2026)

The c320 hard lock on a damaged Rows wolf group was uploaded as v67 and tested against rank-5 new team (4) in group [955faf23-97fb-4f5f-b405-8944957190c7](https://2026a.battlecode.co.uk/game/match-groups/955faf23-97fb-4f5f-b405-8944957190c7). The group lost 0-5 without bot faults. Rows fell to 528:1,056 gems and 9:16 clear entries; Team A cleared groups 0, 2, and 4, while Team B kept clearing 1, 3, and 5. Team A dealt 37.846k monster damage and had no deaths. The v65/v66/v67 Rows replays share the same seed and draft: v65/v66 cleared groups 0 and 2 and banked 594:1,056, so the paired route change cost 66 gems. The other four map metrics matched. Reject c320/v67: its 6/8 local screen and 1,006 average local gems did not transfer to this top-5 group.

c321 set early Rows gold weighting to zero and remained 6/8 locally at 974 average gems; reject. The next Rows work should measure per-champion travel, arrival, camp readiness, and damage time to explain why our nine camp clears lag the opponent's sixteen. Do not change item priorities or production until that route gap is understood. Campaign: **4 wins / 370 completed top-50 maps**, maximum streak 1, current 0/10.

## v68–v71 follow-ups

The four groups against rank-5 new team (4) all lost 0-5 with no bot faults: [v68](https://2026a.battlecode.co.uk/game/match-groups/1f420eff-95d4-47cf-adf2-1181a8dfc274), [v69](https://2026a.battlecode.co.uk/game/match-groups/b9ee15a5-adc4-41a8-8912-9e82789b30d4), [v70](https://2026a.battlecode.co.uk/game/match-groups/0c22b4fb-111d-407d-bb96-e84a2f9bc336), [v71](https://2026a.battlecode.co.uk/game/match-groups/47ff93c4-2182-4c8d-9b2a-61961476fd63). They reuse the same map seeds and drafts.

v68's 30% retreat did not change the eight loss: 19:2 deaths, the same early deaths, and 132:1,008 submitted gems. v69's Cassi Monster Focus order raised Rows damage to 44.550k and clears to 11:16, but banked gems stayed at 594:1,056; the two additional clears were at rounds 382 and 385. v70's Ryth Strength gear added no further clear or gem gain. v71's 1.0 current-target bonus matched the baseline at 9:16 clears and 594:1,056. c328's Varg solo-safe-camp route tied the Rows baseline locally at 6/8 and 974 average gems. No change won a map. Keep c324's Rows gear as a test lead only; reject c323 and the additional c326/c327/c328 changes. Continue looking for early route throughput, since late extra clears do not bank before the opponent wins. Campaign: **4 wins / 390 completed top-50 maps**, max streak 1, current 0/10.

## Current top-5 comparison (18 Oct 2026)

The later group [2c01edc0-7f92-468f-9838-0337a2d12c8f](https://2026a.battlecode.co.uk/game/match-groups/2c01edc0-7f92-468f-9838-0337a2d12c8f) against #5 Sneaky Bush Campers was 0-5, likely v71, with no platform faults. The opponent banked 1,016–1,032 gems on every map while our team banked 366–792. Rows was a clean farm-rate loss (792:1,023 gems; 13:19 camp clears; no champion damage or deaths). Eight and Interlock show a separate fight/survival issue: 36:2 deaths and 1:25 kills combined. The older user-supplied URL `dbdcc65c-...` is a different, previously reviewed v60-likely group.


## Rank-5 map diagnostics: v73-likely group (18 Oct 2026)

Group b4117649-1de1-4564-b0c4-4f633cb53371 finished 0–5 against Sneaky Bush Campers. c332/v73 attribution is by upload timing; the API does not show pinned versions.

| Map | Gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Primary issue |
|---|---:|---:|---:|---:|---|
| Interlock | 536:1,004 | 13:33 | 27.429k:76.532k | 18:2 | First clear at r44 vs r9; opponent Stellar had 11 kills. Draft change transferred but did not address camp tempo or carry survival. |
| Eight | 366:1,032 | 9:18 | 29.632k:64.429k | 17:2 | First clear at r42 vs r13; combat collapse. |
| Rows | 792:1,023 | 13:19 | 52.958k:74.400k | 0:0 | Pure camp-throughput loss; first clear r25 vs r28, then opponent cleared 6 more camps. |
| Lanes | 546:1,016 | 24:44 | 38.922k:69.965k | 5:1 | Nearly equal first clear timing, then opponent sustained far more clears. |
| Rushbait v2 | 488:1,022 | 17:46 | 34.150k:68.284k | 14:9 | Opponent first clear r20 vs r25; both farming and fight deficit. |

The exact lineups are in the replay scout logs. Interlock used our Tavi / Cassi & Issac / Ryth / Stellar draft against Stellar / Ren / Tavi / Prism. The updated fixed-roster local candidates c333/c334 were below c327 on both the targeted maps and full map pool, so do not treat the user-requested roster as a measured upgrade yet. The next map work should target early clear cadence and identify what keeps enemy Stellar alive long enough to snowball.


## Local Interlock follow-ups

The v73 Interlock Tavi-first draft lost 536:1,004 with 18:2 deaths; the opponent's Stellar reached 11 kills. c335 tried Varg / Ryth / Tavi / Willow, and c336 tried Tavi / Cassi & Issac / Ryth / Willow. Both scored 3/10 locally against five proxies, below c327's 6/10. Do not use either as an Interlock counterdraft.

c338 let Vendetta pursue safe multi-wolf camps in the early phase. On Interlock / Eight / Rows it scored 8/30 versus c327's 23/30. The added wolf range did not close the farming deficit.

## Rows side-route follow-up (18 Oct 2026)

The queue-time rank-50 test in group [9de98fb4-1737-4b66-b7b4-0859bfc0096d](https://2026a.battlecode.co.uk/game/match-groups/9de98fb4-1737-4b66-b7b4-0859bfc0096d) lost Rows 528:1,056 gems and 9:17 camp clears without combat. First clears were nearly simultaneous (round 25 vs 26); the opponent then cleared eight more camps. This confirms that early arrival alone is not the bottleneck.

Own-side route isolates c339-c343 failed to beat c327's 10/10 local Rows screen. c341's immediate Varg route to own group 4 scored 8/10; the midgame route c343 scored 6/10. c342 never activated because Rows had already left the early phase before round 60. Do not force Varg onto a solo wolf route: the split/travel cost outweighed any extra clears. The next useful investigation is when the standard squad leaves groups 0/2 and why its late group-4 clears fail to bank before match end.

c345 tested having the Fighter squad avoid camps within 5 tiles of Ryth's Rows anchor, to split the two squad routes. It tied c327 at 10/10 against the same five local proxies, but opponents banked 768.9 gems on average versus 732.6 against c327, and c345 won 13 rounds later on average. Reject the spacing rule; it remains local in `bots/c345` and was not uploaded. The result reinforces that route separation alone is not improving Rows throughput.

The rank-50 Rows replay cleared group 0/2 five/four times on our side and did not touch group 4; the winner cleared mirrored groups 1/3/5 seven/five/five times. First clear timing was round 25 vs 26, so the loss (528:1,056 banked gems) comes from repeated route coverage after the opener. c346 tested the opposing Varg / Cassi & Issac / Tavi / Stellar draft, with Stellar leading the former Tank squad. It scored 4/10 against c327's 10/10 on the same proxies after fixing the early leader handoff. Reject the no-Tank draft; final artifacts are under `matches/league/20261018-130520-c346/`.

c347 put Varg on Ryth's route during midgame; it scored 5/10 vs c327's 10/10, so reject. c348 changed Ryth's Rows build from Health to Strength shards; it tied c327 at 10/10 on proxies but scored 5–5 head-to-head, winning only on side A and losing only on side B. Reject the side-dependent build and keep the production Health setup. The proxy screen is `matches/league/20261018-130908-c348/`; head-to-head logs are in `matches/league/20261018-130938-c348-direct-rows-ryth-strength-vs-base/`.

The submitted-gem deficit extends beyond Rows: the same rank-50 group lost all five maps, and camp clears were below the opponent on every map. See `analysis/live-top50-match-review-20261018.md` for the complete table.


## Fresh rank-1 map comparison (18 Oct 2026)

Group [794748d5-1c1f-42c5-a937-9f82e1a5fb75](https://2026a.battlecode.co.uk/game/match-groups/794748d5-1c1f-42c5-a937-9f82e1a5fb75) against Intercontinental Fish finished 0–5 (likely v73/c332 by queue timing; exact version is not exposed). Interlock was an opening-tempo collapse: Fish cleared at round 9, we first cleared at round 44, then finished 29:9 camp-clear entries and 1,010:110 submitted gems. Eight and Rushbait combined severe death gaps with under-farming. Lanes and Rows had no meaningful fight; both exposed slower sustained farming, with 23:41 and 9:17 clears respectively.

Rows gives the cleanest route signal: our three north-side groups at (18,3), (18,5), and (31,3) produced 9 clear entries; the opponent's south-side groups at (7,46), (18,46), and (31,46) produced 17. Neither team dealt champion damage or lost a champion. First clear was round 25 vs 21, so the later deficit comes from repeat coverage and camp throughput, not solely opening arrival. Interlock's Team-A stdout also recorded two caught `Champion cannot act` errors and Eight's recorded four; neither match had an API-reported bot fault. Diagnose these action failures, but the larger route gap remains visible on maps without combat. Keep the current candidate test-only; prioritize opening travel on Interlock and route coverage/repeated clears on Rows/Lanes before adjusting equipment.


## v74 Interlock draft test and local follow-ups (18 Oct 2026)

The v74-likely test group [9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3](https://2026a.battlecode.co.uk/game/match-groups/9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3) against #1 Intercontinental Fish finished 0–5. Ren-first replaced Tavi on Interlock and produced 182:1,010 gems, 7:30 camp clears, and 18:0 deaths, versus the paired Tavi-first result of 110:1,010, 9:29 clears, and 15:0 deaths. It did not deny Fish Ren because both teams can draft the same champion. The 72-gem gain came with more deaths and fewer clears; keep v74 unpromoted. The other four maps exactly repeated the previous group. Full metrics are in the live review.

Local isolates do not yet provide a Rows or combat upgrade: c349 Varg priority scored 4/10 vs c332 and lost both Rows games; c351 early retreat scored 1/6; c352 mirrored the no-Tank Rows draft but lost 0/2 to c332; c353's Power-before-Monster Varg build tied but was slower and yielded more opponent gems; c355's stricter outmatched threshold tied 3/6 while banking fewer gems. Reject all five. Continue investigating how to raise sustained camp damage/clear frequency without fragmenting the working squad routes.

c356 forced Rows into the mid-game split at round 35. It went 9/10 on local proxies but lost both direct games to c332, took 15 rounds longer to win on average, and yielded 759 Faisal-family opponent gems vs c332's 710. Reject the early split; wait for stronger route evidence before changing the timing.

## New top-1 samples: Ambush, Expanse, Packs, Fragment, Collision

Fresh v74-likely group [e6b3ee2b-077f-4d25-91b7-f2f5c71fce91](https://2026a.battlecode.co.uk/game/match-groups/e6b3ee2b-077f-4d25-91b7-f2f5c71fce91) lost all five maps to Intercontinental Fish. Ambush and Expanse had no combat and showed the largest repeat-clear gap (6:12 and 17:46 camp clears). Packs, Fragment, and Collision had 19, 14, and 15 deaths on our side, with 0 kills; the opponent recorded 14, 14, and 11 kills. None had API bot faults. This confirms the strategy needs different work by map family: route throughput on Ambush/Expanse, survival and focus fire on Packs/Fragment/Collision.

Packs' telemetry showed a relevant equipment timing difference: opponent Issac bought Power Strength at r24, while our Issac first bought Jungle Health at r47. c358 tested the damage build on Packs and Collision, but it scored 11/20 against proxies versus c332's 12/20 and let the Faisal-family bots bank 583 gems versus 472. Do not generalize the offensive build from this one observation.

c359 enabled the Ambush split at the mid-game shard trigger or r100 rather than r150. The local Ambush proxy screen tied at 10/10 and was faster, but the live test [7250aac0-ed63-4984-bed9-7a9fb1d685a1](https://2026a.battlecode.co.uk/game/match-groups/7250aac0-ed63-4984-bed9-7a9fb1d685a1) reduced Ambush submitted gems 582→404, increased deaths 0→2, and added one camp clear. Reject the timing change; local proxies did not predict the top-1 outcome. Other maps repeated the v74 baseline exactly.

Rows c357 delayed the Varg solo side route until r35 but still lost both direct matches to c332 (792:990 gems). Keep the existing squad route. All these candidates remain separate from production; v75/c359 is the newest test upload, but it is rejected pending better live evidence.

Expanse follow-ups did not transfer from the top-1 telemetry: c360 gave Issac Monster/Power Strength and c361 split the team at r35. Both tied the 10/10 proxy win rate but were slower and yielded less own gem totals than c332; c361 lost one direct game, c360 both. Reject them. The opponent's earlier item timing is likely a symptom of clearing and earning gold sooner, not evidence that Issac's defensive build is the main cause. Keep Expanse work focused on the first-to-second-camp route and repeated target selection.
## Rank-2 Mite live sample and Packs interpretation (18 Oct 2026)

Group [e29257b6-18d9-49aa-b952-43a426e1ab2d](https://2026a.battlecode.co.uk/game/match-groups/e29257b6-18d9-49aa-b952-43a426e1ab2d), with latest test v77/c363 likely, lost all five maps to current #2 Mite with no platform faults. Ambush (356:1,024 gems) and Expanse (540:1,116) show broad camp-output gaps without major combat deaths. Packs (208:1,014), Fragment (300:1,048), and Collision (154:1,002) also had 13, 14, and 13 Team-A deaths and 0, 4, and 0 kills.

Packs is a mirrored C&I / Stellar / Ren matchup. Mite Stellar got 7 kills, zero deaths, and 5.9k champion damage; our Stellar got 3 deaths and 2.1k champion damage. Our Cassi and Issac died at rounds 52–53. Mite Issac bought Strength gear; our Issac bought Health gear, while our Ren had only 35 gold and could not buy his role-specific tank items. Against Fish, c363's Ren tank build improved Packs farming to 344 gems and 11 clear entries, but against Mite it yielded 208 gems and seven entries. The durability gain is opponent-dependent; the next useful test should address the first fight and C&I survival rather than add more Tank Health.

c364b's Monster Strength-first Issac build and c366's Power Strength-first build both tied c363 at 6/10 on the same five Packs proxies and lost both direct games. c365's attack-range leash scored 5/10 and won only one of two direct games. Keep all three unuploaded. Campaign is 4 wins / 450 maps, current consecutive streak 0/10.
## v78–v80 Packs candidate results

The Mite comparison showed mixed transfer for the Packs ideas:

- c367 gave Issac Durability Strength then Jungle Strength, matching Mite's observed Strength item family. It tied c363 at 6/10 locally but only delivered 184 gems and five clears against Mite, below v77's 208 gems and seven clears.
- c368 retreated when nearby enemy strength reached parity. Against Mite it raised submitted gems 208→232 and lowered deaths 13→12, but cleared one fewer camp and dealt less monster damage. Against Fish it scored 256 versus v77's 344 gems and kept the same 14 deaths, so this was not a transferable gain.
- c369 prioritized the enemy with the highest raw damage stats. It tied c363 at 7/10 locally but lost to Mite at 140 gems and five clears, below v77's 208 gems and seven clears.

All three candidates lost their five-map live groups. Keep c368 as an isolated research lead only; do not promote these changes. The main remaining Packs issue is surviving the first fight while still maintaining camp throughput. Ambush and Expanse continue to show mostly farming deficits.

## v81 Expanse split test

v81/c373 starts Expanse in its mid-game route at round 1, keeps Stellar with the Cassi/Issac trio, assigns Varg a separate safe camp, and uses 0.75 gold weighting for the leader. It improved Expanse against both top opponents without deaths or bot faults:

- Mite: 636:1,116 gems, 20:32 clears, first clear r14:r11; v77 was 540:1,116 with 16:32 clears and first clear r28.
- Intercontinental Fish: 778:1,016 gems, 22:46 clears, first clear r14:r15; v77 was 584:1,016 with 17:46 clears and first clear r28.

The opening now matches the near-side wolf loop and transfers across opponents. Repeat throughput remains low: 20–22 clears against 32–46. Ambush, Packs, Fragment, and Collision stayed unchanged. Keep v81 test-only; the next Expanse experiment should address midgame target switching and camp-clearing cadence. Production remains gated on a verified 10-win streak.

## User-created v60 test: Rows, Lanes, Eight, Interlock, Rushbait_v2

Against ladder #5, v60 lost all five maps without bot faults. Rows banked 594 vs 1,056 gems (9 vs 16 clears) with no deaths, showing a pure route-throughput deficit. Lanes banked 560 vs 1,038 (20 vs 47 clears). Rushbait_v2 banked 212 vs 1,004 (17 vs 35 clears) and had 9 deaths. Eight was the clearest collapse: 154 vs 1,024 gems, 6 vs 19 clears, 19 vs 5 deaths. Interlock reached 596 vs 1,032, with 15 vs 36 clears and 17 vs 6 deaths.

Prioritize map-specific routing for Rows and Lanes, and safe opening/retreat behavior on Eight and Interlock. The top-50 coverage set now includes ten of the 17 published maps; Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, and Swirl remain untested live. Group: https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34. A v83 same-map comparison against #5 is pending in group bd1c7f28-ab38-464c-aa27-74c0325737d6.

## Latest-upload test against #5 on the added map set

The follow-up group [bd1c7f28-ab38-464c-aa27-74c0325737d6](https://2026a.battlecode.co.uk/game/match-groups/bd1c7f28-ab38-464c-aa27-74c0325737d6), queued after v83/c376, also lost 0–5 with zero bot faults. Results: Rushbait_v2 300:1,020 gems (19:36 clears, 3:0 deaths); Rows 594:1,056 (9:16, 0:0); Lanes 538:1,008 (19:46, 3:0); Eight 132:1,008 (7:19, 19:2); Interlock 182:1,054 (10:30, 15:0). The submission number is not exposed in the match summary, so call this the latest-upload group.

Compared with the separate v60 group, Rushbait_v2 improved; Rows was identical; Lanes/Eight stayed near the same; Interlock differed sharply. Drafts and seeds differed, so do not attribute these differences to the Expanse-only code change. Focus experiments on safe camp tempo on Eight and Interlock, and a higher clear rate on Rows/Lanes. Seven published maps still need top-50 results (Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, Swirl).
# Interlock follow-up against Intercontinental Fish (18 Oct 2026)

Across v88–v91, the best Interlock sample came from v90/c391: it switched to the split farming phase on round 1 while retaining the c388 dynamic draft (Tavi/Ren/Stellar/Cassi & Issac). That map banked 204 gems, made 9 camp-clear entries, and had 13 deaths; its first clear was round 11. v91/c392 used the split with the mirrored Fish lineup and fell to 88 gems, 10 clear entries, 16 deaths, and a round-28 first clear. The lineup/role interaction is a plausible explanation, but these are single-map samples; retain as a hypothesis, not a confirmed cause. Both games still lost heavily to Fish. Keep map-specific split research separate from production.

## Latest map evidence: v92 coverage and v93–v94 Contest tests (18 Oct 2026)

v92/c395 added live top-50 evidence on all previously untested maps. It lost every game against #1 Intercontinental Fish and #2 Mite. Contest remains the sharpest combat collapse (Mite: 0 gems, 94 death events, 94 kills conceded, 1.5k vs 190.5k monster damage). Swirl had 27 deaths, 0 gems, and 7.37k vs 88.98k monster damage. Rows lost as a no-death farming race (528:1,012 gems; 37.668k:64.8k monster damage). Interlock was variable between 276 and 480 gems across two different teams/seeds, with 11–14 deaths.

The v93-likely/c397 Contest counterdraft selected six bodies (Varg / C&I / Ryth / Stellar / Tavi) after Mite exposed a six-body lineup, but still lost the [Mite group](https://2026a.battlecode.co.uk/game/match-groups/eba1da49-7ea6-4711-ac74-11972535abd3) 0–5. Contest reached round 2,000 with no gems and 140 Team-A death events; first deaths were Cassi r37, Issac r38, Tavi r41, Ryth r47, Stellar r50, and Varg r57. The draft is not the main blocker. Current Contest logic blocks camps over 100 strength until late, while our team engages around center before depositing gems. Next investigate safer opening movement, damage uptime under stuns, and early access to the two 200-gem camps. c398 remains local-only; c399 was tested live as v94.

c399 retained Willow while adding C&I and dropping Varg, then was uploaded as v94 for a focused Mite test. The [group](https://2026a.battlecode.co.uk/game/match-groups/528af232-c8fa-42e7-9375-240ff909d1a9) also lost 0–5. On Contest, this six-body lineup still banked 0 gems and recorded 132 Team-A death events; Cassi and Issac died at r29. It is fewer events than v93's 140 but more than v92's 94 on different seeds, so it does not establish a survival gain. The remaining score snapshots (Swirl 0:976, Interlock 480:998, Rows 528:990, Eight 198:876) leave the farm deficit unchanged outside Interlock.

The v92 Contest item timeline shows the spending gap follows income: our five champions earned 105 gold total and bought only three Monster Strength shards for Varg at r69; Mite's six champions earned 21.4k gold, spent 19.7k, and started buying Treasure shards between r50 and r136. Local Treasure-first test #138 lost four wins, so do not copy that purchase order without new evidence. c400 (move burst before Contest survival) matched c395 exactly on the proxy screen and had no stable direct edge; c401 (prioritize the highest raw-damage target in burst ties) fell to 10/12 proxy wins versus c395's 12/12. Neither was uploaded.

Live map coverage is now **17/17**, but the campaign remains **4 wins / 590 top-50 maps**, maximum streak 1, current 0/10. Latest upload v94 is rejected for production. Keep production hashes unchanged and continue testing toward the ten-win streak.

## Contest follow-ups: Willow heal, back-line farming, and Prism mirror (18 Oct 2026)

The v94-likely Mite replay shows first contact around round 22; Cassi and Issac died by round 29 before our team deposited gems. c402 increased Willow's Contest heal trigger from 30% to 50% while enemies were visible. It tied the c399 control at 7/8 and 3,200 aggregate gems on four strong proxies. c403 let only the front line respond to early Contest contact while the back line retained farm movement; it fell to 4/8. Reject both.

c404 changed only Contest's lineup to Prism / Stellar / Cassi & Issac / Ryth / Tavi, mirroring Mite's six bodies instead of taking Willow. It tied c399 at 38/40 in the full 20-opponent Contest pool and added 200 aggregate gems (36,000 vs 35,800). A two-game side-swapped direct test split 1–1 (200:1,000 and 1,000:200), so this was only a matchup hypothesis. Test v95's exact mirrored lineup was confirmed in [the Mite group](https://2026a.battlecode.co.uk/game/match-groups/dbffabee-68c9-4ddd-a9eb-5e59b423e846), which lost 0–5. Contest was 0:0 gems, 2:128 camp-clear entries, 3.6k:191.4k monster damage, 141:0 deaths, and 0:117 kills. It logged five caught `Champion cannot act` errors and zero platform faults. The first enemy sighting was r20–21; our first death was Ryth at r28. The exact draft mirror did not change the opening collapse; reject v95 for general use.

Other Mite results were Swirl 0:1,020 gems, Interlock 480:1,034, Rows 528:1,012, and Eight 198:1,008. A same-map follow-up against rank-50 Bamboo Teahouse in [group 51e941e4-5904-4c2d-bd75-87d761c2b0c3](https://2026a.battlecode.co.uk/game/match-groups/51e941e4-5904-4c2d-bd75-87d761c2b0c3) also finished 0–5 with zero platform faults. Contest banked 0:800 gems (6:116 camp-clear entries, 20.2k:236.6k monster damage, 123:3 deaths); Swirl 0:1,020; Interlock 546:1,054; Rows 660:1,056; Eight 36:1,038. Interlock is the one relative bright spot, but none converted into a win. The live campaign is **4 wins / 600 top-50 maps**, max streak 1, current 0/10. Keep v95 test-only; production remains unchanged.


### Rows: Varg does not obtain a solo target

The Bamboo Rows replay isolates a farm-race deficit: no champion damage or deaths, but 660:1,056 gems, 11:17 clears, and 45.544k:68.850k monster damage. Camp-group capture events show our side cleared home groups 0/2/4 ten times total; Bamboo cleared 1/3/5 sixteen times. Their first group-5 capture was r105; our corresponding group 4 was not captured until r175. At several of our captures, Varg shared the 66-gem reward with teammates and received 22, while Bamboo's Varg took 66 alone.

Rows diagnostics showed Varg's `farm_target` stayed empty, so he fell back to the fighter's shared objective. The solo selector excludes wolf packs with combined strength above one wolf. Candidate c409 relaxed that for Varg to three-wolf packs, but its side-B Varg traveled to a far camp at (42,5); it scored 9/14, winning 7/7 side-A games and 2/7 side-B games. c411 restricted the route to the allied half and scored 12/14 (7/7 side A, 5/7 side B), but split 1-1 against c404. Other candidate isolates (c405/c406 leader objective sync and c407 skipping Varg's capture join) also showed no stable gain. Keep all local-only. The useful next step is stable, side-aware Varg routing that starts with a nearby eligible wolf camp and avoids detours; the current tests do not justify an upload.


## v96-likely map results and Rows correction (18 Oct 2026)

The new [rank-50 umamusume group](https://2026a.battlecode.co.uk/game/match-groups/819e5b24-2227-4065-9eda-d49419a8568f) lost 0-5 without platform bot faults. Rows stayed a low-contact farm race (528:1,056 gems, 11:17 camp clears, 42.7k:68.9k monster damage). Lanes was similar (590:1,016; 24:46; 40.3k:69.4k). Eight and Interlock added major survival costs: 24:6 and 15:1 deaths. Contest was another collapse: 0:200 gems, 3:129 clears, 28.8k:187.8k monster damage, 98:7 deaths, and 7:72 kills. Team A's Cassi and Issac both died at r45 to enemy Ren; Team A collected 200 gems but never banked them. The replay also reports ten fuel-exhaustion events for our Contest team, including six at r35-r39. This can suspend a champion's turn without a platform bot fault; profile these spikes before changing only the combat plan.

The c413 “early Rows route” was inactive because `game_phase()` returns midgame for Rows from the first round. Its 11/14 screen included a 1-1 comparison against c411 and otherwise matched c411's 10/12 proxy results; do not count it as a strategy gain. c411 was submitted separately as test v96, but the fresh top-50 group did not validate its Rows wolf route. Keep v96 test-only. Campaign: **4 wins / 605 maps**, best streak 1, current **0/10**; production remains unchanged.

## v97 map results and Contest carrier-loss finding (18 Oct 2026)

The v97-likely group against rank-50 Live Love Larp, [bab275a5-8821-4586-81e2-23b16e626e90](https://2026a.battlecode.co.uk/game/match-groups/bab275a5-8821-4586-81e2-23b16e626e90), lost 0-5. Lanes, Eight, and Interlock each banked 648–672 gems, but still trailed on camp clears and monster damage. Rows remained a clean throughput loss with zero kills and only 528 gems. Contest was the sharpest mixed farming/survival loss: 0:1,000 gems, 8:119 camp-clear entries, 33.4k:206.5k monster damage, and 77:23 deaths. There were no platform bot faults.

Contest's clearest actionable moment was at r1018: Issac had collected 200 Monolith gems and was isolated near (24,35); enemy Stellar killed him and took the bag after enemy Tavi/Stellar were seen nearby at r1014. No teammate was near to escort. c420 tested shared carrier awareness but reached 6/8 local proxy wins versus c417's 7/8 and showed no direct advantage, so retain only the replay diagnosis, not its code change. Other candidates c416/c418/c419 also showed no reliable edge. Continue map-specific escort and carrier survival research, but measure it against the c417 control before upload.

## v98-likely map set and failed carrier response (18 Oct 2026)

The v98-likely group against rank-49 Please, [8a9a1654-7673-4da3-bbae-daaa2f5cc715](https://2026a.battlecode.co.uk/game/match-groups/8a9a1654-7673-4da3-bbae-daaa2f5cc715), lost 0-5 with no platform faults. Contest scored 0:200 gems (9:132 clears, 48.1k:170.8k monster damage, 85:23 deaths); Lanes 750:1,000; Eight 683:1,029; Interlock 204:1,004; Rows 528:1,056. Prism collected 200 gems at r1027, and Please's Ryth took them at r1063 and submitted at r1109. c421's threat-only frontline escort failed to prevent it despite 8/8 local proxy wins; keep it rejected and do not promote from this sample.

c422 tested the user-requested Contest rule to wait for an attack on the tank before fighting. It scored 1/8 local proxy games versus a fresh c417 control at 5/8; reject and keep local-only. Campaign is **4 wins / 615 top-50 maps**, maximum streak 1, current **0/10**. Continue Contest work on opening survival and camp tempo; do not infer a transferable gain from the local carrier screen.


## v99 Contest paired-draft result (18 Oct 2026)

The v99 [group against rank-45 Please](https://2026a.battlecode.co.uk/game/match-groups/e0cdf2be-2e78-4e8c-b4ed-9ca36db12ada) lost 0-5. Its Contest match had the same seed and opposing roster as v98. Changing our counterdraft from Ren to Tavi moved our first camp clear from r48 to r83, reduced our monster damage from 48.1k to 16.8k, and cut our clear entries from 9 to 2; deaths rose from 85 to 94. The Ren version gathered 200 gems, which Please stole and banked; the Tavi version banked no gems for either team. Keep the Ren counterdraft against this revealed lineup, while rejecting c418/v99 overall.

The other four map results were identical across the paired groups: Lanes 750:1,000 gems, Eight 683:1,029, Interlock 204:1,004, and Rows 528:1,056. The c423 local Contest farm window tied c417 at 5/8 wins but had lower aggregate gems (4,600 vs 6,200), so it was rejected without upload. Campaign is **4 wins / 620 top-50 maps**, best streak 1, current **0/10**. Production remains unchanged.


## Contest c425 opening-split screen (18 Oct 2026)

c425 uses the existing two farm squads from round 1 on Contest and keeps the early combat leash through r149. It beat c417 8/8 and earned 7,200 gems on the focused four-proxy screen, compared with c417's 5/8 and 6,200. Against the broader 20-opponent Contest pool, both scored 38/40; c425 earned 36,600 gems versus c417's 37,200. Against six stronger archived bots, c425 and c417 both scored 11/12, while c425 banked 10,200 gems versus 9,200. A side-swapped direct c425-vs-c417 comparison favored c425 2/2 (800:600 and 800:200); a repeat was byte-identical and is not an independent sample. Keep v100 as a candidate for its next live check, but do not treat it as a broad win-rate improvement. No fresh group has run because live tests are paused. The old user link adds no v100 result. Campaign remains **4 wins / 620 maps**, best streak 1, current **0/10**.

c426 kept the Contest split only through r149, then resumed normal phase logic. Its 20-opponent screen was 37/40, with 36,800 aggregate gems, versus c425's 38/40 and 36,600 and c417's 38/40 and 37,200. It lost both games against my-bot-v2 and one against opp-fai-melee; c417 beat my-bot-v2 2/2 and c425 split 1-1. Reject the shortened split; it does not improve the broad screen. Run: `matches/league/20261018-172325-c426-direct-contest-opening-split-r150/`. No upload or live result; live groups remain paused.

c427 restored Contest's 0.25 early gold value for 150 rounds while keeping c425's split. It scored 37/40 and banked 35,800 gems, below c425's 38/40 and 36,600; reject that valuation window. c428 returned early when all three SDK action flags (move, attack, cast) were clear. It removed `Champion cannot act` errors and scored 40/40 against the broad Contest pool, but fell to 10/12 on six stronger archived bots (c425: 11/12), lost both games against `opp-swirl-meta-core`, and scored 14/34 in a side-swapped 17-map matchup against c425. Reject the broad guard; it suppresses useful behavior on strong matchups and other maps. Keep c425/v100 as the next live-check candidate. Runs are recorded in PLAN.md #182–183; live groups remain paused.

c429 call-site logs showed the common stun errors were rejected recalls in `survive()` / `shopping_trip()` and rejected submissions in `bank()`, with all action flags and relevant restrictions disabled. c430 moved the guard after damage and shared-threat bookkeeping; it removed error-44/45 messages, but scored only 37/40 and 10/12 against stronger Contest bots versus c425's 38/40 and 11/12. Reject the guard family; retain the diagnosis and keep c425/v100 for its next live check. Details and run folders are in PLAN.md #184–185.

## Rows local follow-up (18 Oct 2026)

With unranked testing paused, local variants tested three more Rows ideas. Avoiding the central monolith before round 160 and making Varg skip nearby capture joins both produced six byte-identical replays to c417 against c404/c399/ming_bot, so neither branch affected those routes. Replacing Ryth or Stellar with Tavi each reduced the six-game result from c417's 4/6 to 2/6. Keep c417's Rows draft and route; do not upload these variants. The v96-likely replay shows Varg clearing only group 4 three times (r178/292/389), while the opponent's Varg cleared group 5 four times (r108/193/268/339). Further work needs route and damage-time measurements, not another blind draft swap. Full run paths and interpretation are in the latest Rows follow-up in PLAN.md.

## Contest fuel trace and compute-only screens (18 Oct 2026)

c436's local fuel trace found the largest median costs in role execution (~18.96k), objective selection (~13.40k), and scout logging (~7.34k), with individual turns approaching zero remaining fuel. Round-40 inner checkpoints showed pathfinding at up to ~8.8k fuel and objective selection at up to ~18.6k. c438's five-round SCOUT sampling tied c425 on the Contest pools but scored 167/204 after a rerun on six strong proxies across all maps, one win below c425. c440 skipped an objective-selection no-op for Mid/Late followers and tied c425 in all 204 all-map results, including gems and match rounds. Neither change is a validated improvement; both remain local. Details and paths are in the latest fuel-budget profiling section in PLAN.md.

## Contest burst leash and follow-up diagnostics (18 Oct 2026)

With live groups paused, c442 added the missing Contest-open leash to global burst casting so it agrees with the existing early combat reach. The initial c441 build accidentally spent extra query fuel on all maps; c442 made those queries conditional. The first c442 six-strong-proxy map screen scored 168/204. After moving state reads into a once-per-turn Contest-only branch, its rerun recorded 168/203 with one runner error; all 191 shared non-Contest win/gem results matched c425. The initial version's 204th game completed with the same win/gem result, though one Stampede game ended seven rounds later. Contest remained 11/12 and rose from 10,200 gems on c425 to 11,000 on c442. On the 20-opponent Contest pool, c442 scored 39/40 and banked 37,400 gems, versus the saved 38/40 and 36,600-gem c417/c425 result. Treat this as a Contest-only local signal, not a full-map improvement or live-validated update.

The one local `tralalerotrarala` loss exposed the economy/combat tradeoff: c442 collected 400 gems but banked none; it recorded 83 deaths, 36 kills, and 63.9k champion damage. The enemy recorded 52 deaths, 66 kills, and 94.6k champion damage, while c442 actually dealt more monster damage (64.3k:27.9k) and earned slightly more gold (3,905:3,615). The opponent's source uses shared sightings to converge on enemy champions and heavily prioritizes carriers. This points to combat focus and safe conversion of Monolith captures as the loss mechanism.

c443's ranged-carrier attack during banking remained 1/2 against that opponent and had no score improvement. c444's raw-damage/carrier threat formula scored 8/12 against six strong Contest proxies, below c442's 11/12, despite 2/2 against `tralalerotrarala`. c445's stronger carrier bonus tied c442 at 11/12 but banked 200 fewer gems and lost the same game. Keep c443–c445 rejected and do not upload. Run paths and per-champion statistics are recorded in PLAN.md.

Campaign and production state are unchanged: **4 wins / 620 maps**, max streak 1, current 0/10; production `bot.cpp` and ZIP still match the documented hashes. No fresh live group was run. v100/c425 remains the already uploaded live-check candidate; c442 remains local-only until the user resumes live testing.

Further Contest tests did not beat c442. c446 forced nearby combat after r149 but matched c442 exactly on all 40 broad-pool win/gem records (39/40; 37,400 gems) and went 1–1 head-to-head. c447 shared the last enemy sighting and directed allies to pursue/focus it; this scored 9/12 on the six strong proxies versus c442's 11/12. Keep both local-only and reject them. The only new candidate retained is c442's Contest burst leash; it remains unvalidated live.

## Wider Contest opening burst leash (18 Oct 2026)

c450 widens the Contest-opening global burst leash from 3 to 5 tiles (or the caster's attack range if greater). It scored 12/12 against six strong Contest proxies, 40/40 against the default 20-opponent Contest pool, and won both side-swapped games against c442. Against c425 it went 1–1 head-to-head. Its full 17-map screen against six strong proxies was 169/204 with zero runner failures, one win above c425; total gems were identical at 195,861, and all 192 matching non-Contest outcomes had the same winner and gems. A six-tile leash (c451) fell to 11/12 on strong Contest proxies. Retain c450 as the best local Contest candidate, but keep it unuploaded until live testing resumes.

The old Swirl 150-damage camp-safety variant was re-screened against six strong proxies and scored 7/12, matching c425/c450; it retained both losses to Ming and Xuanming and side A's loss to Faisal. The camp threshold does not fix the main Swirl matchup losses, so reject it as a follow-up. Run: `matches/league/20261018-190249-cand-swirl-camp-threshold150-v36-direct-swirl-threshold150-current-strong/`.

Swirl draft c452 traded Ren for Ryth while retaining Varg; it stayed 7/12 but reduced gems from c450's 9,642 to 8,797 and still lost both Ming and Xuanming sides. c453 also put Ryth with Cassi/Issac; all 12 winner, gem, and round records matched c452. Reject both tank variants. Runs: `matches/league/20261018-190436-c452-direct-swirl-tank-keeps-varg-strong/` and `matches/league/20261018-190543-c453-direct-swirl-ryth-escorts-ci-strong/`.

c454/c455 extend the five-tile burst leash to Swirl only against the observed C&I/Varg/Stellar/Vendetta draft. c455 scored 8/12 (9,954 gems) on six strong Swirl proxies and 170/204 (196,173 gems) across those six proxies and all maps; c450 scored 7/12 and 169/204 (195,861 gems). All 192 matching non-Swirl results had identical winners and gems. The new Swirl win was Faisal side A; both Ming and Xuanming sides still lost. The default Swirl pool stayed 32/40, unchanged from c450, and the c455/c450 head-to-head split 1–1. c456's stricter retreat threshold kept 8/12 but fell to 8,396 gems. Keep c455 as the leading local candidate only; its main top-team matchup is not fixed, and there is no live validation. Runs are in the c454–c456 section of PLAN.md.


## Swirl follow-ups after c455 (18 Oct 2026)

Local c457–c462 route/combat experiments did not improve the main Swirl matchup: c457 scored 9/12 but still lost Ming side A and both Xuanming sides; c458 and c460 forced outer/flank camps but the paths still crossed the same central corridor (8/12 each); c461 disabling opening burst and c462 copying 55%/75% retreat thresholds each scored 7/12. Source review found the top bot starts its first flank-wolf bank around r65, while our bot crowds the center with a lower retreat threshold; transplanting the threshold alone reduced farming output.

c459/c463 were invalid draft screens because they checked the opponent's full lineup before it was available during our pick turns; replay logs show the standard C&I/Stellar/Ren/Varg roster. Corrected map-only tests show Willow (c464) at 3/12, and Vendetta mirror (c465) at 7/12 strong / 28/40 default. A side-aware hybrid (c466: Ren on side A, Vendetta on side B) scored 8/12 strong and 30/40 default. The hybrid won side B against Ming and Xuanming but remained below c455's 32/40 default Swirl score. A direct c466-vs-c455 screen scored 2/2 for c466, but only the side-B game differed in lineup; side A used the same Ren/Ryth roster on both bots, and the repeat replay was byte-identical. Treat c466 as a targeted local hypothesis; c455 remains the broader candidate. No live test, upload, or production edit.

## Swirl c467–c476 local counterdraft results (18 Oct 2026)

The side-aware Vendetta + top-item experiments found a conditional Swirl draft improvement. c470's side-B Vendetta roster and strength/health/strength queue beat Ming and Xuanming from side B, but lost to `opp-swirl-meta-core` and `fx-dbllock`; overall it stayed 8/12 strong and 30/40 default. c471's flank route, c472's opening squad split, and c473's early solo Varg all lost their four top-two side swaps. c474's side-A item order scored 7/12, below c470.

c475 only selects the side-B Vendetta roster when the enemy C&I/Varg opening is visible; it restored the two other strong-opponent wins. c476 applies a Ren/Vendetta side-A lineup under the same condition. c476 scored 10/12 against six strong Swirl proxies, 32/40 on the default pool, and 172/204 against those six bots over all 17 maps (197,073 gems), versus c455's 8/12 Swirl, 32/40 default, and 170/204 (196,173 gems) all-map screen. The only six changed all-map side results are on Swirl; net gain is two wins and 900 gems. Against Ming and Xuanming, side A still loses (606 and 374 gems), while c476 wins both side-B games. This is local evidence, not live validation; do not promote while unranked matches are paused.

Full source/run ledger is in `bots/tungtungsahur/PLAN.md`, section “Swirl counterdraft and equipment follow-ups c467–c476.”

c477–c479 failed to convert the remaining side-A Swirl losses. Raising retreat to 55%/75% reduced output to 372 gems versus Ming and 12 versus Xuanming; avoiding fights through r79 produced 314/208 gems and gave up early kills; raw-damage target ranking produced 268/374 gems. All remained 2/4 top-two losses. Keep c476 as the best local candidate and continue investigating a side-A opening that can bank early without feeding the opposing fight. No live test or production change.

## Ming route-planner trace (18 Oct 2026)

`mingstudy-trace` beat c476 2/2 on Swirl. Its first deposits landed at r45/r51, while its draft-time trace assigns Cassi and Issac to one shared camp circuit and Varg, Stellar, and Vendetta to separate camp routes. This explains why c472's unplanned round-one split failed: the higher-ranked approach assigns camp ownership and bank points before play. The next local experiment should implement only the first Swirl route cycle and keep the linked pair together. Run: `matches/league/20261018-195650-mingstudy-trace-direct-inspect-ming-routes-vs-c476/`.

The c480 side-A split with an altar-camp embargo reduced deaths (38/37) but cut gems to 18/154, so safe separation without planned camp circuits loses too much farm time. Reject it; c476 remains best locally. Run: `matches/league/20261018-195853-c480-direct-swirl-side-a-split-safe-camps-top2/`.

## Swirl c481–c484 flank route tests (18 Oct 2026)

c481's geometric three-lane and c482's four-lane assignment both stayed 2/4 against Ming/Xuanming and were early farm failures: side-A scores were 308/236 and 240/356. c481's five champions were all dead by r49 before depositing gems; c482 lost Cassi/Issac by r24. These results show that assigning lanes without a safe shared first bank can expose the team sooner.

c483 sent the full team to the opposite-flank 88-gem pack at `(13,13)` for one opening cycle. It scored 3/4 against Ming/Xuanming, converting Xuanming side A while raising the Ming loss from 606 to 885 gems. On six strong Swirl proxies it tied c476 10/12 and gained 841 total gems over the three top-team side-A games: Ming 606→885, Xuanming 374→1,024, Faisal 1,012→924. The default Swirl pool remained 32/40. Strong all-map results were 171/204 and 197,818 gems versus c476's 172/204 and 197,073; the only non-Swirl delta was an Xuanming Lanes result on a separately generated map file, so treat the one-win difference as noisy. Retain c483 as a targeted Swirl hypothesis, with c476 as the balanced local baseline.

c484 switched back to c476's normal phase after the first 88 gems were banked; it scored 4/6 versus three strong opponents and lost side A to both Ming and Xuanming. Reject it. No production change or live test; see the c481–c484 section in `bots/tungtungsahur/PLAN.md`.

c485 extended that shared flank opening until two 88-gem deposits. It tied c476/c483 at 10/12 strong and 32/40 default Swirl; it beat Ming side A at 1,034 gems but lost to Xuanming (684) and Faisal (924). c483 has the reverse Ming/Xuanming result, so neither is a universal upgrade. c486's Ren Monster Strength first purchase reduced the strong Swirl score to 9/12; reject it. Keep c476 as the balanced local baseline and c483/c485 as matchup alternatives until live testing resumes.

## Swirl adaptive fight switch c487–c488 (18 Oct 2026)

c487 detected a nearby enemy Varg at 60% health or lower. The trigger appeared against Faisal at r53 and converted its side-A matchup, but c487 also let the ordinary fight alarm end the shared flank route after routine tank damage. Its 10/12 strong Swirl and 171/204 all-map scores therefore do not isolate the trigger; reject c487's phase-switch implementation.

c488 uses shared-memory byte 6's otherwise unused stamp value 127 as a persistent route-abort marker. This makes the route change team-wide and independent of the temporary fight alarm. Two separate six-proxy Swirl screens scored 11/12 each; the default pool remained 32/40. Against Faisal side A the marker fired at r53 with Varg at 58% health. On a new 204-game all-map screen c488 scored 172/204 and 198,133 gems, equal to c476's wins and +1,060 gems, and +1 win / 315 gems over c483. It beat both Xuanming and Faisal sides while still losing to Ming side A. Keep c488 as the current local Swirl candidate; do not copy it to production until live unranked validation resumes.

Runs: `matches/league/20261018-202539-c488-direct-persistent-weak-varg-abort/`, `...202551-c488-direct-persistent-weak-varg-default/`, and `...202611-c488-direct-persistent-weak-varg-strong-all-maps/`. No live match or upload; production source and ZIP remain unchanged.

## Lanes early-split checks c489–c490 (18 Oct 2026)

c489 split both sides from round 1 and scored 6/12 on six strong Lanes proxies versus c488's 7/12 all-map subset. c490 split only side B and scored 5/12 in a separate unseeded screen. Neither beat Ming or Xuanming; c490 also lost the meta-core side-B game that c488 won. In the Ming side-B replay, both split variants banked 970 gems with no deaths versus c488's 772 and two deaths, but still lost 970–1,012. This shows that fewer deaths and higher banked gems from the split were insufficient to win; reject the blanket phase change and keep c488's shared opening. Runs: `matches/league/20261018-202952-c489-direct-lanes-round1-split-strong/` and `matches/league/20261018-203045-c490-direct-lanes-side-b-round1-split/`.

## Pilgrimage mirror opening c491 (18 Oct 2026)

c491 held the shared first camp through r119 against the Ren/Stellar/Cassi-and-Issac/Ryth/Varg mirror, while keeping Varg's squad assignment unchanged. It lost both sides 556–1,032 and 524–1,064; c488's separate baseline losses were 940–1,014 and 524–1,002. Deaths fell from 22 to 17/19 but the score collapsed, so reject a full-team opening for this matchup. Run: `matches/league/20261018-203342-c491-direct-pilgrimage-meta-shared-r120/`.

## Lanes movement diagnostics c492–c493 (18 Oct 2026)

c492 instruments c488's movement purposes; c493 adds the side-B round-one split. In their two-game Ming/Lanes screen, side A matched exactly at 1,000–924, r637. Side B still lost, with the split raising banked gems 802→838 but finishing 12 rounds later (r549 vs r537). Through the last logged checkpoint at r525, side-B movement changed camp steps 274→254, capture steps 695→655, altar steps 290→230, fight steps 29→6, with logged gem pickup events 32→31; the final 12 rounds were unlogged. This modest one-game farm gain did not convert the result. Use it to guide a targeted Lanes route; do not promote the split. Runs: `matches/league/20261018-203744-c492-direct-lanes-move-diagnostic-shared/` and `matches/league/20261018-203746-c493-direct-lanes-move-diagnostic-side-b-split/`.

## Lanes first-bank follow-ups c494–c496 (18 Oct 2026)

c495 kept Lanes side B on the shared opening until the first deposit, then split the squads. It matched a fresh c488 control at 7/12 strong-proxy games. Against Ming it changed side B from a 772–1,012 loss to a 1,000–968 win; against Faisal it changed side B from a 1,008–564 win to a 956–1,012 loss. The initial deposit matched at r65 / 36 gems in both replays, so the unconditional phase switch is a matchup trade, not a global gain. c496 split only if the team trailed by at least 20 gems after its first bank; it also scored 7/12 and lost both Ming and Xuanming games. Reject both general changes.

c494's 8/12 was diagnostic-only: it inherited movement counters and output from c492, and its result differed from clean builds. Do not use that screen as strategy evidence. Runs are listed in `bots/tungtungsahur/PLAN.md`. Live tests remain paused; source and submission ZIP remain unchanged.

## Corners mirror-counterdraft retreat c497–c498 (18 Oct 2026)

c497 raised the retreat distance from four to six tiles for every Corners matchup. It tied c488 at 8/12: one meta-core side-A win was offset by two new losses against `fx-dbllock`. c498 narrowed the rule to the exact mirror draft (Cassi & Issac, Ren, Stellar, Ryth, Varg). It scored 9/12 on Corners and 173/204 across six strong opponents on all maps. The only changed result was the mirror side-A game: c488 lost 724–1,018 with 22 deaths; c498 won 1,010–572 with 11 deaths. The full 20-opponent pool tied clean c488 at 624/680 after recovering c488's one failed runner match; all shared outcomes matched. Keep c498 as an unvalidated local counterdraft option, not a general or production update. Full run paths are in `bots/tungtungsahur/PLAN.md`.

## Pilgrimage squad and opening audit c499–c500 (18 Oct 2026)

c499 changed Ren's squad flag but exactly matched the saved reference outcomes in all 18 target games. Ren is a fighter, so his route does not consume the only fighter-visible behavior tied to that flag. c500 skipped the shared-camp choice only for the exact mirror draft; its turn handlers still used the early `team_farm` action. It fell from 5/18 to 3/18, converting Ming side B and Xuanming side A to losses. Reject this partial mirror-opening override, not the broader role split. Full details are recorded in `bots/tungtungsahur/PLAN.md`.

## Pilgrimage side-B retreat follow-up c501–c503 (18 Oct 2026)

A six-tile retreat radius for all Pilgrimage spawns raised the focused nine-opponent score to 6/18 from 5/18, but dropped the default 20-opponent pool to 27/40 from 28/40. Restricting it to the side-B spawn at `(46,1)` retained 6/18 and improved the default pool to 29/40 in two matching runs. It converted Faisal-bot and my-bot side B to wins, while giving up opp-tts-locker side B. Across six strong opponents and all 17 maps, c503 tied c488 at 172/204 with no changed win outcomes. Keep the side-B rule isolated for further local validation; do not promote it to production. Full run data is in `bots/tungtungsahur/PLAN.md`.

## Pilgrimage mirror counterdraft and side-B retreat c504–c506 (18 Oct 2026)

Starting the role-objective phase at round 1 converted Xuanming side B to a win and improved the six-strong all-map screen 172/204→173/204, while tying the default Pilgrimage pool at 28/40. The unconditioned side-B six-tile retreat interfered with that Xuanming result. Gating retreat to side B against non-mirror drafts kept both observed gains: c506 scored 7/18 in two targeted runs, 29/40 twice in the default Pilgrimage pool, and 173/204 across six strong proxies/all maps. It still trades a win against opp-tts-locker side B for the Faisal-bot and my-bot side-B wins. Retain c506 as a local candidate; it has no live validation. Full run evidence is in `bots/tungtungsahur/PLAN.md`.

## Packs leash plus Pilgrimage side strategy c507–c508 (18 Oct 2026)

A Packs-only early attack-range leash through round 599 scored 33/40 twice versus c488's 32/40, converting all v4/v5 games while trading away side-B wins to Faisal-bot and v3 plus one tungtungsahur-v1 side-A win. Combined with c506's Pilgrimage changes, c508 completed 626/680 after recovering two replay-name collisions, versus c488's 624/680. The only map totals that changed were Packs (32→33) and Pilgrimage (28→29). The six-strong all-map screen was 173/204 versus 172/204; the Pilgrimage side-B Xuanming conversion raised the total, while Packs exchanged two `fx-dbllock` wins for losses to Xuanming and `opp-swirl-meta-core`. Keep c508 as a local integrated candidate for later live validation. Detailed runs are in `bots/tungtungsahur/PLAN.md`.

## Swirl and Lanes follow-ups c509–c511

c509's universal Swirl Ryth/C&I/Stellar/Tavi roster scored 5/12 against six strong proxies and lost both Ming/Xuanming sides. It dropped Varg's independent farming slot; reject it. c510 retained c508's roster and enabled the side-A flank opening only against Ryth/C&I/Stellar/Tavi drafts. It tied c508 at 11/12 strong and 32/40 default Swirl. It gained the `opp-tts-v4` and `opp-tts-aggro` side-A wins, offset by losses to `opp-fai-mirror` and `opp-tts-locker`; gems increased by 197. Keep as a matchup hypothesis, not a general improvement.

On Lanes, c511 swapped Ryth for Vendetta to match Ming's draft. It fell from c508's 7/12 to 5/12 on six strong proxies, losing both Ming and Xuanming games. Across c508's four Lanes losses, deaths ranged from zero to six, pointing to farm throughput rather than a need for another fighter. The source route planner in `mingstudy-trace` assigns separate camp circuits and altar stops per body; a generic role split and draft copy have already failed. Keep c508 unchanged while working on a more specific route plan. Run folders are listed in `bots/tungtungsahur/PLAN.md`.

## Lanes round-50 split and Corners mirror defense c512–c516

Starting Lanes' role-based split at round 45 improved the six-strong screen from 7/12 to 10/12, repeated identically; however, the round-60 version traded a Ming win for a meta-core win, while round 30 fell back to 7/12. Round 50 swept all 12 strong Lanes games in two matching runs, including both sides against Ming and Xuanming. The 20-opponent Lanes pool remained 39/40 with the same winners as c508. Across the strong all-map screen c515 reached 179/204, five wins above the recovered c508 baseline; the five Lanes flips explain the strategy gain, while one unrelated Corners side-B result also varied between runs.

c516 adds the previously tested Corners mirror retreat. Against the six strong Corners proxies it scored 10/12 versus c515's 9/12, converting the `opp-swirl-meta-core` side-A loss from 724–1,018 and 22 deaths to a 1,010–572 win and 11 deaths. The combined c516 strong all-map score was 180/204 after recovering one replay-publication collision; its full 20-opponent map pool scored 626/680, the same as c508. This is the best integrated local candidate, but it has not been tested in live unranked play and has not met the ten-win target. Full run paths and comparisons are in `bots/tungtungsahur/PLAN.md`.

## Eight mirror counterdraft c517–c519

The exact five-pick condition in c517 was not visible early enough to affect drafting. A visible-Ren trigger in c518 did work: using Tavi instead of Ren on both sides converted the meta-core side-B loss to a win, but caused a severe side-A farm collapse (176 gems versus 1,002). c519 restricts Tavi to side B and keeps Ren on side A. It repeated the focused 10/12 and raised the strong six-proxy all-map score from 180/204 to 181/204. The full 20-opponent Eight pool remained 35/40, and the recovered full 20-opponent, 17-map pool finished 626/680, matching c516. This is a specific counterdraft result rather than a broad improvement. All runs are local; no live group, upload, production edit, or streak win was recorded.


## Offline targeted Contest and Willow-Lanes profiles c644–c646 (19 Oct 2026)

For the recorded rank-49 Please draft, c644's exact-order Contest response beat the synthetic roster-matched proxy 2/2 but did not change outcomes in strong or broad local Contest pools. c570's Lanes Ryth strength queue beat a synthetic Willow-layout proxy 2/2 while matching current-source win counts in the six-strong and 20-opponent Lanes screens. c646 combines those separate gates. It held 79/80 across the broad local Contest+Lanes pools, with no winner flips against c553, and exactly matched c553's 182/204 strong all-map records. These local counters remain unvalidated against the ranked Please executable. See `bots/tungtungsahur/PLAN.md` for details and replay paths.


### Recorded Please Lanes roster correction and tests

The archived rank-49 group lists Please's Lanes picks as `[9,3,4,8,10]`, which decode through `champion_draft` to Varg/Cassi & Issac/Stellar/Ren/Tavi. c646's Lanes Willow gate is a different synthetic matchup and does not fire for this recorded roster. Team A's Monster-then-Power Ryth profile in c647 matched the roster but stayed at 2/2 against its synthetic proxy; its full local Lanes pool remained 39/40 with no winner change. Power-then-Monster c648 scored 1/2; the Tavi-for-Ryth c569 draft swap scored 0/2. There is no validated Lanes improvement against Please yet. c644 still directly matches the recorded Contest draft order, but that is synthetic proxy evidence only.

## Contest profile follow-up c649–c654 (19 Oct 2026)

c652's 2-tile Team-A leash through round 99 improved the result against the synthetic archived-draft proxy, repeating 2/2 with a 1,000:400 Team-A finish. Broad and strong Contest pools remained exactly unchanged from c646 (40/40 and 12/12). Other leash duration variants were less successful. This is a targeted matchup hypothesis, not general map evidence or an official win. Full details are in `bots/tungtungsahur/PLAN.md`.
The c652 cutoff follow-up found that `round < 90` produced the same proxy results as `<100`, while including round 100 (`<101`) changed Team A from a 1,000:400 win to a 200:400 loss. Longer 105/110 cutoffs also lost on Team A. Keep the c652 threshold unchanged; treat the apparent round-100 breakpoint as synthetic-matchup evidence only.
Contest-specific equipment check: c659 replaced Stellar's first Power Focus emblem with Monster Focus only against the archived Please draft. It scored 1/2; Team A tied gems 600:600 and lost the gold tiebreak, while c652 with Power Focus scored 1,000:400. Retain Power Focus for this contested map profile; the Monster Focus camp bonus that works on other farm maps did not improve this proxy matchup.
## Please Lanes route detail and opening split check

The archived Please Lanes replay confirms a pure farm-rate loss (no deaths): Please first cleared with Ren at r35 and Varg at r41; our Issac first cleared at r47 and our Varg at r146. Please logged 43 clears and banked 1,000 gems versus our 30 clears and 750 gems. Splitting on turn 1 or round 45 against this exact roster both scored 1/2 against a synthetic proxy and repeated the same 904:1,012 Team-A loss; the round-50 control remained 2/2. Retain the round-50 opening for now. This proxy result does not settle the actual ranked matchup.
Please Lanes Varg-route follow-up: removing Varg from early capture duty did not change any target or broad-pool result. Sending Varg to a solo passive camp (c663) or safe active camp (c664) reduced the Team-A proxy score to 984:1,012 or 962:1,012. The current grouped opening remains better on this local proxy; these are not results against Please's executable.

Delayed solo-route starts at r35 (c665) and r40 (c666) also failed to improve Lanes: each scored 1/2 versus c646 control 2/2. Team A lost 882:1,012 and 868:1,012 respectively; Team B repeated the control 1,020:990. Reject both and retain the grouped opening for this proxy. This local proxy does not settle the ranked matchup.

Rows draft follow-up: c593 used Varg/Cassi & Issac/Ryth/Ren against the Please-style proxy's Varg/Cassi & Issac/Stellar/Ren and won 2/2. Production c553 won the same 2/2 with identical round, score, kill/death, and draft results, so the draft rule did not improve over current production. c593 also split direct Rows games with c553 by side (1,056:990 on side A; 990:1,056 on side B). Do not count the proxy win as a gain against Please.

Rows replay route update: the first clear was nearly tied (r29 us vs r25 Please), while the full match ended 11:17 camp clears. Our Cassi recorded zero clears and Issac one; Please's Stellar and both C&I champions contributed 2–3 clears each. A draft-only c667 that preferred Stellar after enemy Varg/C&I scored 46/48 against 24 local Rows opponents versus production's 47/48, with no new wins and one added `ming_bot` side-B loss. Reject the draft swap; focus on sustained camp cadence and role participation.

c667 full Rows screen: 46/48 across 24 local opponents versus a fresh c553's 47/48. It gained no wins and added a `ming_bot` side-B loss; the direct c553 matchup split by side. Reject the Stellar draft change. The official replay has a near-tied first clear (r29/r25) but an 11:17 total camp-clear gap, so continue examining repeated farm activity.

Rows item check: Please's Cassi had five Power Focus and four Durability Focus shards by r32, while our recorded Cassi first bought at r201 and then chose Durability Health; her monster damage was 4.1k versus Please's 14.6k. Switching the second queue to Durability Focus (c668) regressed the 24-opponent screen 46/48 vs c553's 47/48. Lowering Cassi's safe shop-trip threshold to 75 gold (c669) lost both direct production games. Reject both; the purchase difference may follow the gold/clear lead rather than cause it.

Rows objective test c670: Ren followed Issac's fresh shared target instead of publishing a competing camp. It matched production at 47/48 against 24 local opponents with no win flips; against the exact-draft proxy it stayed 2/2 but banked fewer gems. Reject; the route hypothesis remains unproven.


## Rows follow-ups c671–c672 (19 Oct 2026)

c671 let Cassi take a separate passive camp. It went 4/6 on a focused local screen and lost side B to both c553 and the synthetic Please-layout proxy; c553 beat that proxy 2/2, so reject the change. c672 gave only Rows Ryth Monster Strength before Power Health. It matched the fresh c553 control at 47/48 over 24 opponents with no winner flips; the candidate finished about 1.8 rounds sooner on average but earned 3.7 fewer own gems on average. This is not a win improvement; reject it. Keep c553 unchanged.


Rows c673 made Ryth ignore gold-only camps and wait for a gem camp. The candidate lost both direct games to c553 at 990 gems each; it beat the synthetic Please-layout proxy 2/2, but production also beats that proxy 2/2. Reject this route. Gold-only camps may provide useful income between gem-camp respawns.


### Rows Ren solo gem-route candidate c674

c674 lets Ren farm a safe separate gem camp on Rows and fall back to Issac's objective when none is safe. It tied c553 at 47/48 over 24 opponents and 11/12 over six strong opponents, with no winner changes. It slightly raised own gem totals and materially lowered opponent gems in the strong screen (791.1→752.6 average), finishing about 20 rounds sooner; most of this came from Ming/Xuanming. The synthetic Please-layout proxy remained 2/2 for both bots and the meta-core side-A loss remained. Retain as an isolated local candidate only; no live top-50 result validates it.


### Integrated Rows route candidate c675

c675 adds c674's Rows Ren solo gem route to broad candidate c604. It exactly matched c604's six-strong 187/204 and 20-opponent default 631/680 win counts, with no winner flips. Strong-set changes were confined to Rows; several match margins and finish times improved, while no win was added. One default run had a replay-writer failure after an engine win; an exact retry confirmed the 1,008–490 win. Keep c675 isolated for potential live validation, not as a verified upgrade.


## Current top-50 replay update: Stampede, Corners, Collision, and Expanse (19 Oct 2026)

The latest ladder read and two newest groups are summarized in `top50-evaluation-20261019.md`.
Intercontinental Fish lost Stampede to Univardisty of Shingtonwash 0–1,080 despite nearly equal
monster damage (43.6k–42.8k). Fish's first camp clear was r106, it made five camp clears, and it died
eight times; Univardisty cleared first at r19, made 17 clears, and died twice. The rosters differed:
Fish used Stellar/Tavi/Prism/C&I/Ren, while Univardisty used C&I/Stellar/Varg/Tavi/Ren. Mite later beat
Sneaky Bush Campers on Stampede 1,008–0, with 15 camp clears versus 6 and deaths 2–7. Those replays
make early gem-camp access, safe repeated clearing, and deposits the current Stampede focus. They do
not isolate draft from bot policy.

The cross-map results reinforce that an early clear is not sufficient. On Corners, Mite cleared first
at r11 but lost to SBC with 24 clears to 40 and 16 deaths to 4. On Collision, Mite had 45 clears and
collected 1,068 gems versus 41 clears and 1,056 collected for SBC, but banked 804 versus 1,012 after
9 deaths versus 2. On Expanse, Fish's four champions all used Monster emblems before Power; the local
c676 copy gave no wins over c553 and had lower gem margins. Do not copy that item queue solely from
one replay.

Stampede roster checks: c677 copied Univardisty's C&I/Stellar/Varg/Tavi/Ren lineup and fell to 7/12
against a fresh c675 control at 11/12 on six strong local proxies. c678 kept Ryth and Tavi but replaced
Prism with Varg; it scored 10/12 and added a `ming_bot` side-A loss, with no win gained. Reject both.
The next Stampede test should target why the first Gem group is missed or delayed, and preserve a
fresh side-by-side control. Do not use the copied top-5 lineup as a production draft.


## Latest local Stampede route test: c679–c680 (19 Oct 2026)

c679 added an early Ryth alert when the known five-pick core came within 10 tiles; alone it delayed but did not win the local meta-core side-A game. c680 paired the alert with an Issac route to a safe separate gem or gold camp before round 150. It won 12/12 on the six strong local Stampede proxy games in two repeated runs. The meta-core side-A result changed from c675's 0–720 loss at r913 to 900–720 at r1761. On the 17-map all-strong screen, c680 was 188/204 vs c675's 187/204, with only that winner changed.

This supports testing safe early side-camp income together with a fight warning on Stampede; it does not establish a win against Univardisty's real bot. The unranked pause remains, and production is unchanged.


## Stampede: protect the gem carrier and repeat bank cycles (19 Oct 2026)

The later ranked Stampede replays point to gem possession and banking as the main bottleneck. In the Univardisty–Pantheon result, Univardisty made 16 camp clears but collected no camp gems; its only 360 submitted gems came from Ren killing Pantheon's Stellar while she carried a bag. Pantheon made 10 clears, collected 1,440, and submitted 1,080 through repeated deposits after Stellar's first death. In Fish–Boost, Fish Stellar collected and submitted the entire 1,080, with four kills and no deaths; Fish made 10 clears and the team died five times, while Boost had two clears and eight deaths. More clear counts or monster damage alone do not show whether a team can carry and bank the reward.

Local tests support keeping the opening fight alert and Issac's separate safe camp route before r150 (c680). The best broader candidate is c686: one Durability Health shard between Power Focus purchases for Stellar only on Stampede. It scored 633/680 across 17 maps and 20 local opponents versus c675's 631/680, and it remained 12/12 on the six-strong Stampede screen. Copying Fish's full Power/Home/Durability queue fell to 8/12 strong; gating the c686 durability step to one draft core scored 37/40 default Stampede; applying it only on side B scored 11/12 strong. c686 has now been uploaded as test v101; its fresh unranked validation is pending.

Next local work should measure who carries each gem bag, whether the carrier survives the walk to a camp, and how often the team repeats a deposit route. Do not treat camp clears, monster damage, or a copied item build as the win condition by themselves. Ranked match summaries and candidate run/hash details are in `analysis/top50-evaluation-20261019.md` and `bots/tungtungsahur/PLAN.md`.
