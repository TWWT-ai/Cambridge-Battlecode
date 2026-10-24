# ming_bot study: what makes it strong, what tungtungsahur should take from it

Source studied: `bots/ming_bot/src` (5,411 lines plus 1,135 in `tactic/`). It was not modified.
Every experiment used a new copy named `bots/mingstudy-*`.

## 0. TL;DR

1. **ming_bot beats tungtungsahur (tts) with its spells, not its economy.** Ablations against tts (20 games each, all maps, both sides; tts wins out of 20 and average final gems, tts vs ming):

   | ming variant | tts wins | gems tts - ming |
   |---|---|---|
   | ming_bot (unchanged) | 12/20 | 885 - 789 |
   | **all tactics off** (`mingstudy-notactic`) | **19/20** | 970 - **525** |
   | **burst off** (spells on champions, `mingstudy-noburst`) | **17/20** | 971 - **600** |
   | poke off (basic hit on champions in range) | 15/20 | 877 - 718 |
   | grouped opening off (`mingstudy-noopen`) | 14/20 | 871 - 754 |
   | altar locks off (`mingstudy-nolock`) | 14/20 | 866 - 799 |
   | peel off / gank off / deny off | 12 / 12 / 12 of 20 | 872-786 / 881-791 / 871-774 |

   Almost all of ming's edge over tts comes from `tactic/burst.cpp`. It runs every turn before banking and farming. It casts whichever ready spell hits the most enemy champions, then deals the most engine-computed damage. Peel, gank, deny and locks have no measurable head-to-head value.
2. **Porting burst into tts helps head-to-head without hurting the league.** I added about 120 lines, a copy of ming's burst scoring, to a tts copy (`bots/mingstudy-ttsburst`). Results:
   - vs ming_bot: **15/20** (baseline tts 12/20).
   - vs current tts: **13/20**, 925 - 777 gems.
   - On the 20-opponent league it scored 362/400, exactly the same as tts.

   This is the most direct thing to port.
3. **ming's economy is faster than tts on maps with many small camps, and slower on maps with only big packs.** Rounds to 1000 against an idle opponent (A/B):
   - Faster: collision 568/590 vs tts 758/748; lanes 307/313 vs 438/433; corners 390/341 vs 427/463; collect 315/324 vs 379/316.
   - Slower: packs 754/724 vs 669/669; monolith 745/767 vs 675/595; elkring 651/589 vs 577/595.
   - Mean over all maps: ming 525 rounds, tts 555.

   The drivers are:
   - One cyclic solo route per body, compiled during the draft.
   - Single-body captures: the others move on instead of standing on the tiles.
   - An opening that gets the first tribute at r28-50 on every map except elkring. tts gets it at r40-55, r85 on rows and r98 on collision.

   The grouped opening chain itself is worth only about 8 rounds when ablated.
4. **ming's weaknesses:**
   - Solo farmers in the contested middle get killed by squads. On packs as team B, ming spent **48 %** of champion turns dead and scored 84 gems.
   - On maps where no camp is "soloable" (rows, elkring) its draft plan is empty.
   - On packs, 3 of its 4 bodies get a single centre camp and idle or wait 43-48 % of turns.
   - It never farms the monolith.
   - Its burst and poke keep firing at enemies healing on their spawn. On corners against an idle opponent, Stellar spent **82 %** of its turns in the tactic state.
5. **For beating the top player**, the platform evidence ming's team collected agrees with the burst result. See `explanation.md:1780-1786`:
   - The top two teams make their first capture at about **r26**.
   - 30 % of their camp-hit rounds have several allies attacking.
   - They deal about 3x more damage to champions and die about 3x less.

   Ranked actions for tts:
   1. Port burst, with escape casts and Cassi's stun.
   2. Make the opening faster: first capture by about r30.
   3. Add map-gated parallel farming on small-camp maps. Three simple solo ports lost league wins, so this needs real per-body partitions.
   4. Keep tts's squads and fight-odds check, which beat ming-style solo farmers.

## 1. Evidence used (all reproducible)

| What | Where |
|---|---|
| ming vs tts, 20 games (baseline, tts as candidate) | `matches/league/20261015-085651-tungtungsahur/`, re-run identically in the ablation league |
| ming vs zz-idle (pure economy) | `matches/league/20261015-091645-ming_bot/` |
| tts vs zz-idle (pure economy) | `matches/league/20261015-091636-tungtungsahur/` |
| Instrumented ming (`bots/mingstudy-trace`: ming_bot plus SCORE / MCAP / MTRIB / MDEATH / MSUM / PSLOT stdout lines, behaviour unchanged) vs idle and tts | `matches/league/20261015-133755-mingstudy-trace/`; parse with `python analysis/ming_trace.py <dir> [--per-slot]` |
| Ablations: tts vs ming / nolock / notactic / noopen | league tag `ming-ablations` (history.csv 13:4x) |
| Ablations: tts vs nopeel / nogank / noburst / nodeny / nopoke | league tag `ming-tactic-ablations` |
| Burst port in tts: 22 opponents x 10 maps x 2 sides | league tag `ming-burst-port`, `bots/mingstudy-ttsburst` |
| ming's "solo-fitness" gate ported to tts back-liners | `bots/mingstudy-solo` (league 343/400 vs 362 baseline), `bots/mingstudy-solo2` (see section 9) |
| tts economy profile (from the earlier run) | `python analysis/econ_profile.py matches/league/20261015-091619-prof-tts` |
| ming team's own platform data | `explanation.md` (their handbook) lines 470-500 and 1770-1790 |

Caveat found while instrumenting: ming's draft is **fuel-critical**. My first trace build printed the compiled plan inside the draft turn (`bots/mingstudy-plandump/src/draft.cpp:116-132`). On expanse, lanes and collect that pushed the draft over its fuel, the pick was lost, and the engine drew random champions (Tavi, Ren and Prism on expanse). The final trace bot prints the plan at round 6 instead. With that change its idle-game end rounds match ming_bot within a few rounds.

## 2. Architecture

```
main.cpp            draft vs game dispatch, catch-all, end_turn
draft.cpp           fixed pick order; builds Atlas + Plan blob into draft_memory BEFORE pick()
atlas.{h,cpp}       draft-time map compile: camp table + BFS distance matrix (camps, altar rings, spawn)
planner.{h,cpp}     partition camps into one cyclic route per body; splice altar stops
plan.h              1 KB draft-memory blob codec (roles, bag caps, altar per camp, routes)
bot.cpp             per-turn: collect Obs -> ledger -> exec::tick/apply -> shop -> warm caches -> ward
obs.h / turn.h      per-turn observation snapshot + memoised engine reads (fuel)
ledger.{h,cpp}      camp respawn table (ready_round, last_seen)
exec.{h,cpp}        the runtime FSM (1,908 lines): guard list, route scan, opening chain, retreat, bank
nav.{h,cpp}         distance-field descent with hidden-occupant retries
econ.{h,cpp}        shopping queues, consumables, dynamic bag cap
tactic/*.cpp        peel > gank > lock > burst > deny > poke, offered before the route step
camp_scoring.h      camp spell/attack value (kill bonus, AoE, never splash a foreign group)
warding.cpp         ward near the nearest altar while carrying gems
runtime_policy.h    small pure rules (retreat %, wait/stale windows, altar ranking)
observation_health.h, progress.h   robustness: partial-vision flags, "no progress" watchdog
wire.h              8-byte shared memory (only the gank sighting is actually read)
```

### 2.1 Draft and roster
- **Pick order** (`draft.cpp:22-34`): Cassi & Issac, Varg, Stellar, Vendetta, Tavi; then Ren, Ryth, Marcella, Willow, Prism, Vesper as fallbacks. Every pick turn projects the full roster from this order. On turn one, still inside the 10x draft fuel budget, it:
  1. builds the atlas (`draft.cpp:102`),
  2. compiles the plan (`:105`),
  3. writes it to `draft_memory` (`:109`), round-trip checking it (`:115-118`),
  4. only then picks (`:132`), because picking freezes draft memory.

  Fuel gates are 350k before the atlas and 240k before the compile (`:96`, `:103`).
- **Roles** (`planner.cpp:30-42`):
  - Vendetta = FARMER.
  - Cassi, Tavi, Stellar, Vesper = CARRY.
  - Issac = ESCORT.
  - Everyone else (Varg) = FLEX.

  Roles only select plan bag caps. Shopping queues are keyed on champion type (`econ.cpp:51-75`).
- **Counter-drafting:** none. The order is fixed. Their handbook (`explanation.md:479-491`) cites a ≥1600-Elo sample where Ren, Stellar and Tavi have the best pick-presence win rates and top teams rarely open Vendetta.

### 2.2 Atlas (draft-time map precompute, `atlas.cpp`)
- Each camp group gets:
  - spawn tiles, gems, gold and respawn period;
  - the sum of member health and strength ("dps");
  - passive and monolith flags (`atlas.cpp:64-85`).
- Each altar gets its walkable tribute ring.
- POI distance matrix [camps | altar rings | own spawn] (`atlas.cpp:99-228`):
  - It starts from a Chebyshev lower bound.
  - It then runs one host BFS (`distance_field`) per POI, in farthest-point order, while fuel stays above an adaptive reserve (430k at first, then `2*spent+390k`).
  - Pairs that never got a BFS are estimated with landmark bounds from up to 16 rooted POIs.

  The draft turn's 10x fuel is what pays for all this. tts has nothing equivalent: it computes distances on demand during play.

### 2.3 Planner and opening routes (`planner.cpp`)
- **Clear-speed estimate per body** (`kit_for`, `:45-58`): dps = strength x camp multiplier + (ranged ? 2 x focus : basic)/8.
- **Service time** (`:64-76`) = clear + 5 capture turns + extra sorties. A sortie is a heal trip, needed whenever pack dps x clear exceeds 60 % of the body's health.
- **Candidate camps** (`:198-212`): not the monolith, reachable from spawn, and soloable by **some** body. Soloable means pack dps x clear turns < 2 x body health. Clusters always qualify.
- **Order** (`:229-240`): earliest-deadline order (slowest clears first), then a stable sort that puts gem camps first. Their comment: clustering by geography alone "parked two bodies on all-gold routes on rows".
- **Assignment** (`:246-290`):
  - LPT-style: each camp goes to the feasible body minimising Chebyshev leg from the body's centroid + current load + service time.
  - A body that cannot solo the camp is skipped (`:263-266`).
  - Unassignable camps stay unrouted (`:282`).
- **Cassi and Issac** routes are merged into one shared route (`:296-311`), so the tank stands between the pack and the caster.
- **Route order** (`:313-370`):
  - nearest-neighbour chain from the camp closest to spawn;
  - a bounded 2-opt polish (`:80-105`);
  - rotation so the route starts at the camp nearest spawn;
  - team B rotates one more stop as a mirror-break (`:363-364`).
- **Altar stops** (`splice_altars`, `:127-165`) are inserted wherever the running bag passes the role cap (`{40,48,40,32}`, `:177`). Each camp group also records its nearest altar.
- A "capture-overlap" flag is computed (`:139-143`) but **never read at runtime**: dead code.
- Compiled routes in practice (PSLOT lines from the trace run):
  - collision, corners, lanes, expanse, interlock, monolith and collect get real per-body routes.
  - **elkring and rows get empty routes** (no camp passes the soloability gate). The runtime falls back to a modulo partition.
  - **packs** gives Cassi+Issac one camp (C3), Stellar one camp (C2) and Varg six wolf pairs.

### 2.4 Runtime FSM (`exec.cpp:862-1570`): the guard order every turn
1. Round 1 fast path: walk straight to opening stop 0 (`:878-907`).
2. Mid-channel or stunned: wait (`:912-914`).
3. **Capture stay** on its own reward tiles, uncontested or inside a contested grace window. It takes free hits only on harmless camps (`:1007-1039`).
4. **Retreat / pitstop** (`:1053-1119`):
   - Triggers at HP < 55 %, or < 75 % with an enemy within 3 (`runtime_policy.h:29-32`).
   - Walks away first; recalls only if nothing threatens within 5. At most 3 cancelled recalls, then it walks home.
   - Heal-to-need: leaves spawn once health covers the fled camp's remaining hp x dps x 1.25 + 55 % (`:1053-1062`). Camps do not regenerate, so a half-cleared pack can be finished on the next sortie.
   - Strike watchdog: 3 sorties broken by an enemy on the same camp blacklist it for 200 rounds (`:1083-1101`, `:56-57`).
5. Winning bag (enough to reach 1000): bank immediately (`:1124-1129`).
6. **Tactics** (`tactic::offer`, `:1133-1136`). The order is peel > gank > lock > burst > deny > poke (`tactic/tactic.cpp:6-20`).
7. **Bank** when gems ≥ the plan cap or the econ rule fires (`:1140-1165`). See section 3.4.
8. **Opening chain** (rounds ≤ 90, `:1320-1392`). See section 3.2.
9. **Route scan** (`:1167-1455`). Candidates are this body's route camps plus its modulo-partition camps plus "open nearby" gem camps within 6 tiles that no ally is next to. Rules:
   - A pending reward outranks a live camp.
   - Cost = distance + expected extra sorties x 60.
   - Gold-only camps are picked only when no gem camp is actionable.
   - Hysteresis: a rival target must be 8 tiles cheaper.
   - "Desperate" mode (no soloable gem camp owned) grinds anything.
   - A remote fallback is taken unless an owned camp respawns sooner.
10. **Haul** (`:1489-1534`): wait on the ring of the owned camp that respawns soonest, at most 12 turns, never on its tiles.
11. **Idle** (`:1536-1551`): step off camp tiles so respawns are not delayed.

### 2.5 Other modules
- **Ledger** (`ledger.cpp:123-189`):
  - A visible respawn timer is authoritative.
  - A completed capture sets `ready_at = round + period` (`:89-97`).
  - A reward seen but not captured is `never` until seen again, and is re-inspected after 24 unseen rounds (`runtime_policy.h:44-49`).
  - tts has an equivalent table (`bot.cpp:432-463`).
- **Nav** (`nav.cpp:42-123`):
  - BFS from the goal set to self.
  - A failed move reveals a hidden occupant; the bot re-queries and retries up to 3 times.
  - A "no progress for 10 rounds" or "6 nav failures" watchdog blacklists that camp or altar for 40 rounds (`exec.cpp:1800-1865`, `progress.h`).
- **Econ** (`econ.cpp`):
  - Power-shard queues by champion: Str/Hp/Str for melee, Foc/Hp/Foc for casters, Foc/Str/Foc for Tavi. The last shard repeats forever.
  - A lock (10 g) and a teleport crystal are stocked first if the route passes an enemy-side altar (`:132-179`, `:222`).
  - **No deliberate shopping trips**: it only shops on spawn turns or while dead.
- **Warding** (`warding.cpp:33-120`): while carrying gems near an altar (≤ 8), place a ward on an approach tile that sees at least 4 new tiles, with bushes counted double.
- **Robustness** (`observation_health.h`, `exec.cpp:1552-1569`, `main.cpp:13-22`):
  - Partial vision is "unknown", never "empty".
  - Every throw costs at most one turn.
  - A cast-fizzle watchdog retires a spell slot after 3 failed casts (`exec.cpp:916-937`).
- **Fuel discipline:**
  - Memoised vision lists (`exec.cpp:414-475`, `turn.h`).
  - Static caches are built one per light turn (`exec::warm_statics`, `:1889-1907`).
  - The shop is skipped on round 1.
  - Priority is randomised every turn (`bot.cpp:111`), so the results are not fully deterministic.

## 3. Economy in detail

### 3.1 Many bodies farm in parallel, each on its own route
Every body except the Cassi/Issac pair has its own cyclic route. That is 4-5 independent farmers on 4-6-body maps, against tts's two squads plus back-liners who solo only gem clusters within 16 tiles (`tts bot.cpp:588-607`).

Trace numbers against zz-idle (`analysis/ming_trace.py`). Captures per 100 rounds count distinct camp-capture events. "Single" is the share of captures paid to one body.

| map | ming captures/100r | single-body captures | tts captures/100r (prof-tts) | tts single |
|---|---|---|---|---|
| lanes | 13.1-13.9 | 100 % | 9.7-11.2 | 100 % |
| collect | 11.2-11.5 | 91 % | 8.9-10 | 85 % |
| collision | 7.8-8.3 | 100 % | 1.7-2.0 | 38-60 % |
| corners | 6.9-7.1 | 32-58 % | 4.5 | ~10 % |
| monolith | 6.4 | 96-98 % | 3.9-4.5 | 45-50 % |
| interlock | 5.6-6.2 | 63-64 % | 4.0 | 30 % |
| expanse | 4.7-5.4 | 43-61 % | 4.6 | 35-40 % |
| elkring | 4.5-5.0 | 41-55 % | 4.7-4.8 | 7-11 % |
| packs | 2.9 | 41-52 % | 3.3 | 36-68 % |
| rows | 2.3-2.4 | 56-71 % | 1.8-2.4 | 13-19 % |

- **Collision** shows the gap clearly. ming's four bodies each solo single wolves (22 gems) on their own routes: 46-47 captures.
- tts's two squads take 13-15 captures, mostly the elk+3-gem group plus shared wolves. Each squad captures together, so 2-3 bodies stand still for 5 rounds.
- Result: ming reaches 750 at r475 vs tts r600.

Milestones against idle (average of A/B):

| map | ming 100/250/500/750 | tts 100/250/500/750 |
|---|---|---|
| collect | 58/112/185/258 | 70/120/200/278 |
| collision | 108/205/340/475 | 120/210/448/600 |
| corners | 50/120/208/280 | 65/132/210/285 |
| elkring | 135/250/402/518 | 90/182/322/462 |
| expanse | 105/185/270/372 | 68/170/270/400 |
| interlock | 65/130/220/320 | 70/142/235/355 |
| lanes | 72/118/200/255 | 88/155/252/342 |
| monolith | 100/235/408/592 | 92/210/370/510 |
| packs | 65/142/355/568 | 98/162/270/458 |
| rows | 120/250/420/585 | 95/220/418/638 |

Where ming is slower (elkring, monolith, packs after 250), its plan is empty or tiny and bodies idle or wait. Packs: idle 26-31 % plus haul 16-17 % of turns. Elkring: every route is empty.

Per-turn state shares against idle (all maps):
- travel 44 %
- clear 19 %
- bank 16 %
- channel 6 %
- capture 5 %
- idle 3.4 %
- pitstop 3.3 %
- haul 2.5 %

ming spends far fewer turns following or idle than tts's back line. tts's own profile shows follow + follow_idle at 20-40 % on collision, monolith and rows.

### 3.2 The grouped opening (`exec.cpp:303-377`, `:1320-1392`)
- Up to three opening stops, chosen identically by every body from static data:
  - Score = gems / (BFS travel from the previous stop + group health / whole-team basic dps).
  - Elk and monolith groups are excluded. Clusters and wolves qualify.
- All bodies go to stop 0 together. Round 1 takes a fast path that skips everything else (`:878-907`).
- When the stop is cleared, **only the body nearest a free capture tile stays** (ties go to the lower slot). The others walk on to the next stop. This is how ming avoids shared captures: the team total is the same, but the other bodies do not waste 5 rounds.
- Result: first tribute at r28-50 against idle (elkring r68-89).
- Ablating the chain (`mingstudy-noopen`) cost ming about 35 gems and 2 wins against tts. That is useful, but not decisive.
- Against idle, the same ablation (the round-1 fast path to stop 0 is kept) changes rounds-to-1000 by only **+8 on average** (533.9 vs 525.4). The effect varies by map:
  - Helps: rows (+68), packs (+40), collect (+28).
  - Hurts: expanse (−31), interlock (−22).
  - Flat elsewhere.

  ming's early tributes come mostly from its routes and the round-1 move, not from the chain itself.

### 3.3 Avoiding shared captures and wasted presence
- The route scan skips a reward whose free tiles are all occupied by allies (`exec.cpp:1216`).
- "Open nearby" camps are skipped if any ally is within 2 tiles (`:1302-1303`).
- Idle bodies step off camp tiles (`:1538-1543`), because occupancy delays respawn.
- **tts does the opposite on purpose.** Back-liners join any cleared camp within 6 tiles to share the gold (`bot.cpp:611-633`). Experiment 26 in PLAN.md showed that removing this hurts tts (301 vs 345 of 380). In tts the non-joiners have nothing better to do; in ming each body has its own next stop.

### 3.4 Banking
- Two caps decide when to bank (`exec.cpp:1144-1156`):
  - **Plan cap:** 40 / 48 / 40 / 32 by role.
  - **Dynamic cap** (`econ.cpp:100-108`): 10 + round/60, clamped to 10-40, lowered by up to 10 when behind on score.
- **Hard ceiling** (the "piñata" rule) of 45 gems (`:258`).
- A forced bank when the remaining rounds barely cover walk + channel (`:259-262`).
- Since single captures are 22-48 gems, **in practice ming banks after every capture**: average bag 22-33, 43-47 on rows. tts does the same (bank on any gems). **Banking policy is not a differentiator.**
- Altar choice (`exec.cpp:668-753`, `runtime_policy.h:52-66`):
  - BFS distance to each altar ring; hostile-locked altars rank last.
  - It diverts from a locked altar only if the open one is under 3 tiles further.
  - Occupied rings cool down for 12 rounds.
  - tts (`bot.cpp:901-979`) has the same idea (+4 for a lock), plus a safer route around enemies.

### 3.5 Respawn timing
- The ledger records `ready_round`, and the route skips groups that will not be ready when the body arrives.
- Haul waits on a ring only when the respawn is due within travel + 12 rounds (`runtime_policy.h:36-38`).
- A remote job is abandoned if an owned camp respawns sooner than the remote clear would take (`exec.cpp:1409-1431`).
- tts's `choose_camp` already uses `wait = ready - round - d` (`bot.cpp:491-497`), and `farm_group` waits one step off the tiles (`:572-577`). This is equivalent.

### 3.6 Camp damage micro (`camp_scoring.h`, `exec.cpp:491-663`)
- Basic attacks and spells on camps are scored as:
  - useful damage clipped to remaining HP,
  - + 0.3 x the monster's strength,
  - + a kill bonus of 80 + strength.
- AoE (Varg splash, Stellar area, Ryth area) is **rejected if the blast touches another group's spawn tiles** (`farm_area_safe`, `exec.cpp:512-524`), so it never wakes a second pack.
- tts's `hit_camps` (`bot.cpp:531-558`) sorts by lowest health and casts its area spell at the target with no spill check.

## 4. Combat

- **burst** (`tactic/burst.cpp:38-236`). This is the module that matters. Whenever HP ≥ 60 % and any ready slot is damage, AoE or CC:
  - Every enemy-target slot is scored on every visible enemy in reach.
  - Every ground slot is scored on the 9 centres around each enemy.
  - Ranking: avoid re-stunning a stunned target; most enemies hit; most `damage_amount` (engine value, includes items); then channelling > low HP > big bag.
  - Otherwise, shields and heals go on itself or an ally under 70 % HP that an enemy can reach next turn.
  - Otherwise, an attack reset is cast when a basic hit lands this turn.
  - Burst runs **before banking and routing** (`exec.cpp:1133-1136`), so carriers and travellers cast too.
- **poke** (`tactic/poke.cpp`): any enemy in basic range, at HP ≥ 60 %, is hit, preferring tribute-channelers and then the lowest HP.
- **peel** (`tactic/peel.cpp`):
  - Interrupts enemy channels by remaining time x bag: a basic hit cancels a recall, a stun or primed enhanced attack cancels a tribute, a carried lock placed on the altar cancels it outright.
  - Otherwise it raises a wire alarm that nobody reads.
  - It printed 1-19 cancels per game against tts, but ablating it changed nothing (12/20).
- **gank** (`tactic/gank.cpp`):
  - Only for bags ≥ 20, own bag < 30, HP ≥ 45 %.
  - It commits only if the burst is **provably lethal** within the window: a channeler's remaining channel time, or a runner's distance to an altar plus channel ticks.
  - The damage sum counts helpers' basic hits plus its own best spell.
  - Converges allies through a wire sighting (`:206`, `:244-253`).
  - Stole 72-166 gems per game on collision, elkring, interlock and rows, but the ablation showed no win effect.
- **lock** (`tactic/lock.cpp:28-80`):
  - Insurance lock on the altar it is about to tribute at.
  - Denial lock on an enemy-side altar within 2.
  - About 1-9 placements per game. Ablation: no gain (+2 wins for tts when removed).
- **deny** (`tactic/deny.cpp`):
  - Step onto an enemy's capture region to reset it, or park on an enemy-claimed respawning group in the last 2 rounds of its timer to delay the respawn.
  - Budget of 8 turns per group. Ablation: no effect.
- **Retreat:** 55 % / 75 % (enemy within 3) is far more cautious than tts's 30-35 %. Escape casts are allowed (`exec.cpp:758-799`): walking-compatible spells always; excludes-walking spells only if the escape step failed.
- **What ming lacks:**
  - No fight-odds check; burst and poke fire whenever in reach.
  - No squads and no focus fire across bodies; each body picks its own target.
  - No hunting.

  In its own platform data (`explanation.md:1782-1784`) losses averaged 8.1 deaths and 3.3k champion damage, vs opponents' 2.5 and 9.7k.

## 5. Idea-by-idea: does tts have it, value, how to port

| # | ming idea (file:line) | tts equivalent | Measured / expected value | Port sketch |
|---|---|---|---|---|
| 1 | **burst**: score every ready damage/AoE/CC slot by hits > damage_amount > channel/low-HP/bag; run before bank and route (`tactic/burst.cpp:75-172`, `exec.cpp:1133`) | Partial: role code casts only in `engage`, after `bank()` returns. Mage uses `is_single` = slot 0, so **Cassi's stun is never cast in fights** (`bot.cpp:206`, `:1294-1339`). Nothing is cast while banking or falling back (`:1095-1099`). | **High.** ming without burst: 17/20 for tts. Port tested: tts+burst 15/20 vs ming (from 12), 13/20 vs tts, league unchanged 362/400 | `bots/mingstudy-ttsburst/src/bot.cpp`, function `burst()` (about 120 lines), called right before `bank()` in `play_turn`. Excludes enemies on their own spawn. Next: also cast during `fall_back`/`survive` (ming's `protect_escape`, `exec.cpp:758-799`) |
| 2 | Grouped opening chain: best 3 gem/(travel+clear) non-elk stops; one body captures, the rest move on (`exec.cpp:303-377`, `:1320-1392`) | None. tts's "grouped opening" (rejected in PLAN.md) kept everyone together | Low-medium: for ming, 2 wins / 35 gems vs tts and 8 rounds on average vs idle. The top teams still capture first at ~r26 (`explanation.md:1780`); tts takes r40-98 | Rounds ≤ 90: the squad leaders target the same `opening_stop` list. When a stop is cleared, only the nearest body stands on it and the others take the next stop. Replaces `join_capture` for the opening only |
| 3 | Per-body cyclic routes compiled in the draft (`planner.cpp:171-389`) plus the runtime partition (`exec.cpp:213-220`) | None. Two squads, with back-liners soloing clusters within 16 | Potentially high on collision / lanes / collect / corners (ming 750 at r475 vs tts r600 on collision; r255 vs r342 on lanes). Negative on packs / elkring / rows. **Three simple ports into tts all lost league wins:** `mingstudy-solo` 343/400, `mingstudy-solo2` 349/400, another analyst's `mp-solowolf` 345/400 (baseline 362) | Not a drop-in. It needs a real per-body route or partition, used only on maps whose gem camps are soloable singles (collision, lanes, collect), and keeping the squads elsewhere. Effort: large |
| 4 | Don't share captures; vacate tiles (`exec.cpp:1216`, `:1302`, `:1383`) | Opposite: `join_capture` (`bot.cpp:611`) is worth +44 wins in tts | Only with item 3. Without other work, sharing is better | Keep `join_capture` while a back-liner has nothing in range; skip it when its own camp is ready |
| 5 | Heal-to-need recovery + no camp regen (`exec.cpp:1053-1068`) | tts heals to full at spawn and re-chooses camps by base health (`bot.cpp:499`) | Low-medium | In `choose_camp`, use the remembered remaining health of a wounded group (no regen) |
| 6 | Strike watchdog: 3 contested sorties → blacklist 200 rounds (`exec.cpp:1083-1101`) | None | Low-medium against a top player who holds the middle | Count retreats caused by an enemy per target group; skip that group in `choose_camp` |
| 7 | AoE spill check `farm_area_safe` (`exec.cpp:512-524`) | None (`bot.cpp:547-550`) | Low | Skip an area cast whose radius covers another group's spawn tile |
| 8 | Camp spell scoring with kill bonus and clipped damage (`camp_scoring.h:104-117`) | Lowest-health first | Low | Optional |
| 9 | Dynamic bag cap 10+r/60, 45 ceiling (`econ.cpp:100-108`, `:254-264`) | Bank any bag (PLAN #37 tested best) | None: same behaviour in practice | Don't port |
| 10 | Peel with lock, gank, deny, insurance lock (`tactic/*`) | Peel by stun, lock denial (`bot.cpp:664-722`) | ~0 in ablations; tts's own tests 21 and 24 also found nothing | Don't port |
| 11 | Draft-time atlas BFS matrix (`atlas.cpp`) | On-demand distances | Indirect: enables planning; fuel-risky | Port only if a planner is ported |
| 12 | Wards near altars (`warding.cpp`) | None | Unknown, small | Skip |
| 13 | Round-1 fast path (`exec.cpp:878-907`) | tts spends its first turn on init and shopping | Small: 1-2 rounds of opening | Move on round 1 before any cache building |

## 6. ming's weaknesses and how it lost to tts

From ming's own traces against tts (`matches/league/20261015-133755-mingstudy-trace`), the share of ming champion turns spent dead:

| map / ming side | result | ming dead % | note |
|---|---|---|---|
| packs B | 84-976 | **48 %** | Cassi+Issac route = only C3, Stellar = only C2. Both are the centre gem groups (`map-dumps/packs.txt`), where tts's squads fight. 23 deaths |
| monolith A/B | 762-980, 484-978 | 22 %, 29 % | 18-23 deaths; ming never farms the monolith (`exec.cpp:1204`, `planner.cpp:202`) |
| corners A/B | 776-956, 374-980 | 14 %, 23 % | travel 35-41 %; tts fights on |
| collect A/B | 912-982, 744-958 | 15 %, 27 % | |
| interlock B / A | 956-994 / 968-946 win | 28 % / 22 % | Both bots slow each other badly: ming at r200 was 72-152 vs 426-470 against idle |
| expanse B, lanes A, rows B, elkring A | close races, 816-986 to 936-972 | 4-19 % | economy races decided by map side |

In its wins (collision both sides, lanes B, elkring B, packs A, rows A, interlock A) ming stole 90-166 gems by kills, and tts was dead 23-30 % of the time (prof-tts profile).

What ming does badly:
1. **Isolated farmers vs squads.** No fight-odds test, burst and poke in reach at HP ≥ 60 %, and single-camp routes in the contested centre. Squads that hunt solo bodies win the trade. Its own platform data shows the same: 8.1 deaths per loss vs 2.5.
2. **Empty or degenerate plans.** No route on rows and elkring. On packs, 3 bodies share 2 centre camps, so 26-31 % idle and 16-17 % haul. Economy on those maps is 50-90 rounds slower than tts.
3. **No monolith play**: it hands the 200-gem monolith to the opponent.
4. **Fixed draft with no reaction** to the enemy draft.
5. **Tactic sink on enemies at spawn.** Burst and poke target champions healing on their spawn. On corners against idle, Stellar spent 82 % of its turns in tactic; the team spent 14-24 %. A bot that lingers near its own spawn can bait ming's bodies there.
6. **Fuel-fragile draft.** Any extra draft work makes the pick random (seen in my trace build).

How a bot can exploit it: hunt in groups of 2-3 near the centre camps and its route camps. ming's bodies are predictable because routes are compiled from static data, so they come back to the same camps every respawn period. Use the fight-odds check so you only take fights you outnumber. Farm the monolith and the big packs it leaves alone.

## 7. Recommendations for tts vs the top player (ranked by expected impact)

1. **Port ming's burst.**
   - Already built and tested in `bots/mingstudy-ttsburst`: +3 wins vs ming, 13/20 vs current tts, league unchanged.
   - Then add casts while retreating or falling back (`protect_escape`).
   - Let Cassi use her stun in fights; today `is_single` picks slot 0 only, so she never does.

   The top teams out-damage everyone on champions 3:1; this is the lever.
2. **Faster opening.**
   - Move on round 1.
   - Precompute 3 opening stops (gems / (BFS travel + health / team dps), no elk).
   - Leave one body per cleared stop and move the others on.
   - Target: first capture ≤ r30 (top teams r26; tts r40-98). ming's own chain is worth only about 8 rounds, so expect a modest gain; test map by map.
3. **Parallel farming on small-camp maps** (collision, lanes, collect).
   - This is the biggest economy gap: about 100-125 rounds on collision and lanes.
   - Simple "back-liners solo wolves" ports failed three times (343, 349 and 345 of 400). It needs a map-gated per-body partition, not a tweak.
4. **Keep the squads and the fight-odds check.** That is what beats ming-style solo farmers (packs A, monolith, corners). Optionally add a strike watchdog so a squad stops returning to a camp the enemy holds.
5. Small items:
   - AoE spill check on camp spells.
   - Remaining-health memory for wounded camps (camps do not regenerate).

## 8. Artifacts created

- `analysis/ming_trace.py`: parser for `mingstudy-trace` replays.
- `bots/mingstudy-trace`: instrumented ming_bot (behaviour unchanged; plan printed at round 6).
- `bots/mingstudy-notactic`, `-noopen`, `-nolock`, `-nopeel`, `-nogank`, `-noburst`, `-nodeny`, `-nopoke`: ablations.
- `bots/mingstudy-ttsburst`: tts plus ming's burst (recommended starting point).
- `bots/mingstudy-solo`, `-solo2`: tts back-liners using ming's solo-fitness gate.
- `bots/mingstudy-plandump`: do not use (it breaks the draft on big maps).
- `bots/mingstudy-probe`: altar-terrain probe from the earlier run.

## 9. ming solo gate in tts (follow-up)

- `mingstudy-solo`: back-liners solo any soloable camp (gate 0.8 x hp). Result 343/400 vs 362 baseline.
- `mingstudy-solo2` (fighting camps only within 8 of the squad anchor):
  - 20-opponent league **349/400** (baseline 362). Faisal family 158/160.
  - vs tts 9/20 (887-876 gems).
  - vs ming_bot 13/20 (856-749).
  - It loses mostly against tts copies on lanes, collect, corners and rows.
- The parallel experiment by another analyst (`mp-solowolf`, history.csv 13:52) scored 345/400.

Conclusion: ming's solo farming does not carry over to tts as a back-liner tweak. In ming it works because every body has its own route and does not depend on a squad leader.

Also in the same table: the `mingstudy-noopen` idle run (rounds-to-1000, mean 533.9 vs ming 525.4) is in history.csv, tag `ming-noopen-idle`.
