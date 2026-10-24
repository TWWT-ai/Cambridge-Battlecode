# Mechanics that matter for (a) gem income speed and (b) beating a faster-economy opponent

> **Historical model warning (21 October 2026):** This probe/calculator predates the uploaded current
> `GameRules.md` and `BotAPICpp (1).md`. Its numeric tables are for the earlier local runner and conflict
> with the current handbook on camp rewards/ranges, champion stats, Vesper/Prism passives, kill gold,
> and altar-lock hits. Keep it as historical evidence only; do not use it to choose current builds or
> routes. See [`game-update-20261021-strategy.md`](game-update-20261021-strategy.md) for the current
> document review and refresh requirements.

Sources: `GameRules.md`, `BotAPICpp.md`, `sdk/cpp/cambc.h`, plus three experiment runs of
mechanics-probe bots against an idle opponent on corners:
`bots/mx-probe-a` (Ryth, Cassi&Issac, Stellar, Tavi, Prism), `bots/mx-probe-b` (Vendetta, Varg,
Ren, Marcella, Vesper), `bots/mx-probe-c` (Varg on elk, Vendetta on GG, Ren on elk, Marcella on
wolves with Jungle, Willow), opponent `bots/mx-idle`. The extracted logs are in
`analysis/mx-logs/probe-{a,b,c}-corners.txt` (line numbers below refer to them). The calculator
behind the tables is `analysis/mechanics_calc.py` (turn-by-turn model, checked against the logs).

## 0. Summary

- **Gem clusters are the fastest gems, by far.** Gems per point of camp health: gem cluster 0.048,
  wolf 0.016, elk 0.015, monolith 0.010. Gem clusters never hit back, so they need no recall.
  One naive **Varg** probe alone, farming the 4 GG groups beside corners' central altar, captured
  **744 gems by round 355** (16 captures, about 2.1 gems/round from one champion). The probe
  team (a naive bot) had 998 tributed at round 340 and won at about round 361 against an idle
  opponent. Varg's basic attack
  splashes onto the second cluster, so a GG group (1000 hp) dies in **9 turns** (6 with 5 Monster
  Strength shards). Varg is not in our draft.
- The top player's tribute timeline matches a solo GG farmer of exactly this kind: many **+48**
  steps (one GG capture), plus +22/+44 steps (wolves). In match 1 it scored +48 every 10-20 rounds
  from round 215 to round 385 (`matches/platform-logs/timelines.txt`).
- **Parallel bodies beat damage per second on gem clusters.** The 5-round capture timer and the
  ceil(g/10) tribute cost the same time at any damage level. Extra allies do not speed up a capture
  and only split the reward. Today tungtungsahur's Cassi and Prism are idle about 30% of their
  turns, and Stellar and Tavi spend about 28% following (`analysis/trace_summary.py
  matches/mp-trace`).
- **Camps never heal** (an elk left at 975 hp stayed at 975 for 68 rounds; probe-b lines 233/443).
  **A champion standing on a cleared group's spawn tile stops it from respawning for as long as it
  stands there** (Issac blocked a GG group from round 85 to round 261; it respawned the round he
  stepped off; probe-a lines 402-1020).
- **Engine settings** (probe-a line 49): spawn healing restores **100% of max health per round**;
  passive gold 0; assist gold 0; kill gold 50; capture time 5; camps sleep after 2 rounds out of
  range; respawn 60; recall 5; tribute ceil(gems × 0.1) turns, minimum 1, from altar range 1;
  altar lock needs 3 hits; teleport crystal channel 3; ward vision 6, placement 2, no expiry,
  recharge 1 round.
- **Draft visibility:** at our k-th draft pick, `current_draft(team::enemy)` already returns the
  enemy's first k-1 picks. From the first gameplay turn it returns all enemy picks (probe-a lines
  1-6). Enemy champion handles outside vision throw "Unit is not in vision" (line 128).
- **Against a faster economy, the biggest lever is killing solo farmers.** A stun chain plus a
  double turn makes a gank close to certain: act second in round r, then first in round r+1.
  Our current draft has 4 stunners (Ryth, Cassi, Tavi, Prism). Stellar + Tavi + Prism deal about
  1000 damage in 2 turns. A kill swings the carried gems twice (they lose them, we gain them) and
  costs the victim about 60 + walk-back rounds of farming, worth about 60-150 gems.

## 1. Verified by experiment (where the docs were ambiguous)

| mechanic | result | evidence |
|---|---|---|
| Ranged: spell and basic attack in the same turn | yes, if the champion did not move (Tavi 220 + 35) | probe-a l.34 |
| Ranged: attack reset gives a second basic attack | yes (Tavi `ATK RESET ATK`, 70) | probe-a l.36 |
| Melee: move, attack and reset in the same turn | yes (Ryth `MOVE ATK RESET ATK`) | probe-a Ryth R30 |
| "Excludes walking" spells after a move | refused: engine error 126 "cannot be cast after normal movement" | all probes |
| Cooldown cycle | each slot recasts every 8 turns (reset at R30, R38, R46) | probe-a Ryth |
| Camp attacks | strength once per round on the nearest champion; a 1-round stun skips one camp attack | probe-a Ryth R32-R41 |
| Camps heal? | **no**, damage persists through sleep (elk 975 hp at R35 and at R103) | probe-b l.233, l.443 |
| Spawn-tile blocking | an occupied spawn tile holds the group at "respawning 0" indefinitely; it respawns the round after the tile is freed | probe-a l.402-1020 |
| Reward split | 2 allies on one GG got +24 each; alone, +48 | probe-a R35 vs R57 |
| Monster emblem | ×1.1 to **both** spells and basic attacks vs camps (352 → 387.2; 35 → 38.5); `damage_amount()` does not include it | probe-a l.625 |
| Jungle emblem | wolf hit 20 → 14 | probe-a l.1281 |
| Ryth passive | +1 strength per 100 bonus health (12 health shards: str 50 → 62) | probe-a R279-281 |
| Health bought on spawn | heals by the amount gained; the spawn tick then fills the rest | probe-a R279-280 |
| Varg shield vs camps | absorbs camp hits (250 per cast, 5 turns) | probe-c l.158, l.209 |
| Ren retaliation vs camps | yes, 0.2×Focus = 20 per hit taken | probe-b l.43/136 (wolf -65 = Vesper 45 + 20) |
| Vendetta kill reset on camps | yes, reset recast 7 turns after the last cast, right after a gem-cluster kill | probe-c l.210 |
| Spell kiting | range-4 spells vs range-3 camps take 0 damage (Cassi solo wolf, 0 hp lost, but 67 rounds) | probe-a l.1237 |
| Tribute timing | 24 gems: start R37, score R40, and the champion acts normally on R40 (completion at turn start costs no extra turn) | probe-a Stellar |
| Recall | start R274 → arrives at R279 turn start, can shop and act; full health at end of that turn | probe-a Ryth |
| Enemy roster in play | `current_draft(team::enemy)` works in gameplay; `champions(team::enemy)[i].champion_name()` throws when not visible | probe-a l.6, l.128 |

## 2. Champion vs camps (solo, from first hit, in range, cooldowns ready, no shards)

Kits, damage per 8-turn cycle on a single target (8 basic attacks + reset + spells):
Ryth 50·9+100 = 550 (68.8/turn, area stun); Vesper 45·9 = 405 (50.6); Vendetta 70·9 = 630 (78.8);
Cassi 30·8+140 = 380 (47.5); Issac 40·9 = 360 (45); Stellar 35·8+200+140 = 620 (77.5);
Prism 35·8+120+80 = 480 (60); Marcella 45·9+100 = 505 (63.1); Tavi 35·9+220 = 535 (66.9);
Willow 45·9 = 405 (50.6); Ren 40·8+125 = 445 (55.6), +20 per camp hit taken from retaliation;
Varg 50·9 = 450 (56.3), doubled on 2-camp groups by splash.

Turns to kill and health lost (`python analysis/mechanics_calc.py`):

| champion | HP/Str/Foc | G (500) | GG (1000) | W (1350, str 20) | E (2400, str 60) | M (20000, str 200) |
|---|---|---|---|---|---|---|
| Ryth | 1200/50/100 | 7 | 12 | 18 t, -280 hp (23%) | 34 t, -1680 **DIES** | 290 t **DIES** |
| Vesper | 900/45/100 | 10 | 21 | 26 t, -500 (56%) | 48 t **DIES** | **DIES** |
| Vendetta | 800/70/100 | 7 | 14 | 17 t, -320 (40%) | 31 t, -1800 **DIES** | **DIES** |
| Cassi | 700/30/70 | 9 | 20 | 27 t, -440 (63%) | **DIES** | **DIES** |
| Issac | 900/40/100 | 11 | 23 | 30 t, -580 (64%) | **DIES** | **DIES** |
| Stellar | 750/35/100 | **5** | 10 | 17 t, -320 (43%) | 30 t **DIES** | **DIES** |
| Prism | 700/35/80 | 9 | 15 | 22 t, -360 (51%) | **DIES** | **DIES** |
| Marcella | 1200/45/50 | 8 | 16 | 21 t, -340 (28%) | 38 t, -1920 **DIES** (seen, l.233) | **DIES** |
| Tavi | 750/35/100 | 7 | 14 | 18 t, -280 (37%) | 34 t **DIES** | **DIES** |
| Willow | 700/45/105 | 10 | 21 | 26 t, -500 (71%) | **DIES** | **DIES** |
| Ren | 900/40/100 | 9 | 18 | 18 t, -280 (31%) | 33 t **DIES** | **DIES** |
| Varg | 1000/50/100 | 9 | **9** | 24 t, **-160 (16%)** | 42 t, -1150 **DIES** | **DIES** |

Observed in the probes (with walking and some allied help): Varg GG 9 turns (probe-b l.175-202),
Stellar GG 11, Vendetta GG 16 (melee repositioning between the clusters), Ryth wolf 19 turns /
-320, Tavi wolf 16 with Cassi chipping in, Marcella died on an elk at 975 hp left.

Shard builds (5 shards = 150 gold; "Power" counts as 6 shards and has no passive):

| champion | best farm build (5 shards) | GG turns | W turns, hp lost | E turns, hp lost (of max) | wolves per full HP |
|---|---|---|---|---|---|
| Varg | base | 9 | 24, -160 | 42, -1150 of 1000 DIES | 6.2 |
| Varg | Monster Strength | **6** | 15, **-80** | 26, -690 of 1000 | 12.5 |
| Varg | Monster Str + Jungle Health (10 shards) | 6 | 15, -56 | 26, -378 of 1500 | 26.8 |
| Vendetta | Monster Strength | 8 | **11**, -200 | 20, -1140 of 800 DIES | 4.0 |
| Ryth | Monster Strength | 9 | 12, -180 | 23, -1140 of 1200 (barely) | 6.7 |
| Ryth | Jungle Health ×10 | 12 | 17, -196 | 30, -1050 of 2200 | 11.2 |
| Stellar | Monster Focus | 8 | 10, -180 | 19, -1080 of 750 DIES | 4.2 |
| Tavi | Monster Strength | 9 | 12, -180 | 23, -1140 of 750 DIES | 4.2 |
| Tavi | Power Focus (what tts buys) | 9 | 17, -280 | 26, -1260 DIES | 2.7 |
| Issac | Monster Strength | 14 | 17, -320 | 31 DIES | 2.8 |
| Prism | Monster Str/Foc | 10 | 16-17, -260 | 27 DIES | 2.7 |

Takeaways:
- **Elk** (36 gems, 60 str) cannot be soloed by any base champion. It needs about 10 shards
  (Jungle + Monster) on Varg or Ryth. At 36 gems per 23-30 turns of fighting plus recall time, it
  is about 4× worse than a GG group even then.
- **Monolith** cannot be soloed. A team of 5 standing in its range 3 takes 200/turn for 50+ turns.
  Kiting with range-4 spells only (our 5 casters: about 1000 per 8 turns) takes about 160 turns
  for 200 gems. Not worth it in a race.
- **Wolves:** Varg takes almost no damage (its shield absorbs 5 of every 8 wolf hits), so it can
  chain wolves without recalling. Vendetta, Ryth and Tavi with Monster Strength clear a wolf in
  11-12 turns.
- **Strength beats Focus for farming** on every non-Stellar champion, Tavi included. Tavi with
  Monster Strength clears a wolf in 12 turns; with Power Focus (tts today, `bot.cpp:648`) it takes
  17. Stellar is the one champion that should buy Focus (Monster Focus).
- Camps attack the **nearest** champion. A melee tank takes every hit while ranged allies at
  range 3 take none (this is what tts squads already do).

## 3. Items and consumables (income or protection)

| item | effect (verified) | income effect | verdict |
|---|---|---|---|
| Monster emblem (5 shards, 150 g) | +stat ×5 and ×1.1 vs camps | -30 to -40% clear time on wolves; -33% on GG for Varg | **best farming buy** |
| Jungle emblem | ×0.7 camp damage taken | +40% wolves per full HP; makes elk possible with 10 shards | for wolf/elk farmers |
| Power emblem | 6 shards' worth, no passive | Health/Focus versions are weaker than Monster for farming | PvP only |
| Durability | ×0.9 all damage taken | none | PvP |
| Treasure | +20% gold (Vesper +40%) | gold only; 0 gems | skip |
| Home | recall 5 → 3 turns | saves 2 turns per recall; at one recall per 50-100 rounds that is under 4% | skip |
| Altar lock (10 g, carry 1) | placed within 2 of an altar; **cancels enemy channels at that altar**; enemy needs 3 basic attacks (tributing auto-converts into attacking it) | costs them about 2-3 turns plus the lost channel progress (up to ceil(g/10)) | cheap denial, key at endgame |
| Teleport crystal (10 g) | 3-turn channel, then a 3-tile jump through walls; stun or death interrupts | saves time only when the detour is longer than 6 tiles; escape tool | niche |
| Ward (free) | vision 6 around a spot within 2 tiles, permanent, can move every round; **not shared with allies** | none directly; vision on enemy farm spots and altars for ganks (8-byte shared memory to relay) | use for scouting |
| Tavi remote shop | buys shards anywhere (not consumables); field Health shards raise max HP without healing | Monster shards right after each capture, with no spawn trip | already used |
| Spawn heal | **100% per round** | recall is about 6 turns for a full heal | recall early, never die |

Gold sources: wolf 90, elk 160, gold cluster 35, kill 50, no passive income. On gem-only maps the
team must take some wolves or gold clusters to afford the Monster emblem.

## 4. Capture and tribute rules worth exploiting

1. **Solo captures, maximum parallelism.** The reward is split among allies present
   (`GameRules.md:192,203`) and more allies do not speed it up. Joining an ally's capture on a
   **gem-only group** (gold 0) adds no gems: it splits the bag and costs the joiner 5+ rounds.
   tungtungsahur's `join_capture()` (`bot.cpp:611-632`, radius 6 at `bot.cpp:34`) joins any
   cleared group. It should skip groups with `gold_value() == 0`. Gold sharing on wolves and elk was
   measured as +50 wins, so keep it there.
2. **Overlap capture with the next clear.** The capturer only has to stand on a spawn tile. A
   ranged champion (range 3, spells 4) standing on group A can already be hitting group B
   (corners: the GG pairs are 2 tiles apart), which saves up to 5 rounds per cycle.
3. **Tribute cost is ceil(g/10) turns, and completion at turn start is free** (verified). Bag size
   barely matters: 2×48 and 1×96 both cost 10 turns. Choose when to bank by **walking distance
   and kill risk**, not by tribute time. Small bags are only worse through extra walks.
4. **Captures resolve before channels, and completion tributes the whole bag**
   (`GameRules.md:228-230`). A champion standing on a capture tile within range 1 of an altar could
   start a 1-tick tribute and bank the capture with it. **No official map has a camp tile within
   Chebyshev 1 of an altar** (closest: the corners GG groups at distance 2). Not usable today.
5. **Damage does not interrupt a tribute; stun, death and a new altar lock do**
   (`GameRules.md:222,271`). A tribute of 2+ ticks always leaves us at least one turn to stun it.
   A **1-tick tribute (10 gems or fewer)** started in a round where the tributer **acts second**
   finishes at its turn start next round, when it acts first, so no enemy turn falls in between. That
   makes it impossible to interrupt. Use this for our own small banks under threat. Damage
   interrupts **recall** but not tribute.
6. **Killer takes all carried gems** (`GameRules.md:360`). Camp kills destroy them. In a gank
   where the victim is also fighting a camp, our champion must land the last hit. Cassi and Issac
   die together and drop both bags.
7. **Respawn 60 rounds**, then walk back from spawn. Recall costs about 6 turns. Never let a
   farmer die to a camp.
8. **Camps sleep after 2 rounds with no champion in range 3, and never heal.** Partially damaged
   camps are free value: finish a camp an enemy abandoned (e.g. when they recalled), and resume
   our own chip damage after a recall.
9. **Occupied spawn tiles block respawn indefinitely** (verified). Uses: (a) deny an enemy-side
   gem group by parking on it; (b) a capture in "reward available" state stays open until someone
   captures it (seen for 8 rounds in probe-a R278-R286), so a camp the enemy cleared and left can
   be taken.
10. **Contested capture:** an enemy on the region resets the timer (`GameRules.md:192`). Stepping
    onto an enemy's cleared group stops their 5-round capture without dealing any damage.

## 5. Draft

**Visibility.** `current_draft(team::enemy)` (`BotAPICpp.md:5617`) returns the enemy's completed
picks. At our pick k we see their picks 0..k-1, but never their pick k (simultaneous). In gameplay
it returns the full enemy roster from turn 1 (probe-a l.6). `champions(team::enemy)` gives handles
whose data throws outside vision (l.128), so **the roster has to come from `current_draft`**. The
draft phase gets 10× fuel and a 1024-byte draft memory, so the counter plan can be computed there
and stored.

**Counter strategy from the enemy draft** (decided in draft, refined on turn 1):
- Enemy has Varg or Stellar (GG farmers): expect central gem clusters to be contested. Send a
  gank squad to their GG farm and contest the capture.
- Enemy solo farmers with 750 HP or less (Cassi, Prism, Willow, Stellar, Tavi): gank mode. Our
  Stellar + Tavi + Prism deal about 1005 in 2 turns.
- Enemy with 3+ stunners (Tavi, Prism, Ryth, Ren, Cassi, Marcella): our tributes will be stunned.
  Bank in smaller bags (1-2 tick tributes) and bank at altars they cannot see. Marcella is the only
  stun-immune champion.
- Enemy Marcella or Varg (1200 HP or a 250 shield): only gank with 4 bodies.
- Duplicates are allowed, so a pick can never deny the enemy a champion. Draft only for our own plan.

**Best econ-race drafts** (bodies in brackets):
- 3 picks: **Varg, Cassi&Issac, Stellar** [4]: Varg on GG and wolves, Stellar on GG and single
  G, Cassi and Issac as two parallel single-G farmers.
- 4 picks: + **Ryth** [5] (wolves, tank, area stun for fights) or Vendetta (fastest wolf farmer
  with Monster Strength) on wolf-heavy maps (packs, rows).
- 5 picks: + **Tavi** [6] (remote Monster shards, 220-damage stun, wolves in 12 turns with Monster
  Strength).

**Current draft** (`bots/tungtungsahur/src/draft.cpp:12-13`: Ryth, C&I, Stellar, Tavi, Prism):
very good bodies and stuns (6 bodies, 4 stunners). Weakness for an econ race: no Varg, and the 5th
pick, Prism, is the worst gem farmer in the lineup (GG 15 turns, wolf 22 turns and 51% of its
health). PLAN.md exp. 45 ("Varg instead of Ryth as the tank") lost, but that put Varg in the
squad-leader role. The recommendation here is **Varg instead of Prism** (pick 4 or 5) as a
dedicated solo GG/wolf farmer with a Monster Strength build. That needs a solo role in the code,
which the earlier test did not have.

## 6. Disruption options against a fast solo-farming economy

Assume an enemy solo GG farmer cycling 48 gems every ~20 rounds (about 2.2 gems/round, as in the
probes and the platform timelines), carrying 0-96 gems. "Swing" is the change in the score
difference (ours minus theirs).

| option | what it takes | gem swing | notes |
|---|---|---|---|
| **Gank a solo farmer** | 3 of ours within spell range 4, about 2-3 turns of burst | **2 × carried** (0-96) **+ 60-80 rounds of their farming** (about 60-150) + 50 gold + often their uncaptured group (48) | best option; see thresholds below |
| **Steal or contest their capture** | 1 body on any spawn tile of their cleared group | **up to 96** (48 to us instead of them) if we hold it 5 rounds; at least 48 denied while contested | camps never heal; the group waits in "reward" state |
| Stun their tribute | any stunner within 4 of the tributer | 0 gems; costs them up to ceil(g/10) turns | decisive only on the **winning tribute** or to hold them for a kill |
| Altar lock their altar | 10 g, within 2 tiles | 0 gems; about 2-3 turns to break + lost channel progress | tts already does this; best combined with a stun or gank |
| Camp their altar | 2-3 bodies near the altar they use | carried bags (48+) per kill | strong on 2-altar maps (collision, elkring, rows); weak on lanes (18 altars), expanse (10) |
| Block their gem-group respawn | 1 body parked on their cleared G tile | denies about 0.74 gems/round per GG group | our blocker gives up about 0.5-2 gems/round of its own farming, so roughly break-even; endgame only |
| Finish camps they damaged | any farmer | the camp's gems at a discount | free; needs vision (wards) |

**Kill thresholds** (damage to a champion, standing in range with cooldowns ready; from `mechanics_calc.py`):

| ours | 1 turn | 2 turns | 3 turns | stuns |
|---|---|---|---|---|
| Tavi | 255 | 325 | 360 | 1 (with the 220 hit) |
| Stellar | 235 | **410** | 445 | 0 |
| Prism | 155 | 270 | 305 | 1 |
| Ryth | 150 | 250 | 300 | 1 (area, radius 1) |
| Cassi | 170 | 200 | 230 | 1 (no damage) |
| Issac | 80 | 120 | 160 | 0 |
| Vendetta | 140 | 210 | 280 | 0 (kill resets cooldowns) |
| Varg | 100 | 150 | 200 | 0 |

- Stellar + Tavi + Prism: **1005 in 2 turns**, 1110 in 3, with 2 stuns.
- Ryth + Stellar + Tavi: 985 in 2 turns.
- All 6 of our bodies: 1575 in 2 turns.
- Base HP: 700 (Cassi, Prism, Willow), 750 (Stellar, Tavi), 800 (Vendetta), 900 (Issac, Vesper,
  Ren), 1000 + 250 shield (Varg), 1200 (Ryth, Marcella). Each enemy Health shard adds 50-100.

**Make the gank certain:**
- **Double turn.** The starting team alternates each round, and team A starts round 1
  (`GameRules.md:34`). Our turns in round r (acting second) and round r+1 (acting first) are
  back to back. Open a gank on a round where the enemy has already acted:
  `has_completed_turn()` on a visible enemy, or round parity plus our team.
- **Stun chain.** Each 1-round stun costs the victim its next turn and also cancels its recall,
  tribute and teleport channel. Turn order for a victim V when we open acting second in round r:
  V(r) | ours(r), ours(r+1) | V(r+1), V(r+2) | ours(r+2), ours(r+3) | V(r+3), V(r+4) ... A stun
  in ours(r) removes V(r+1), and one in ours(r+2) removes V(r+3). So with a stun every second round
  (our 4 stunners, 8-turn cooldowns), **V acts once per 4 of our turns**. It can neither walk out
  of range nor recall. Stuns that overlap the same victim turn are wasted, so stagger them.
- **Pinned victims.** A farmer is easiest to catch while capturing (5 rounds standing still),
  tributing (channel) or fighting a camp. It sees 8 tiles and walks as fast as we do, so a
  plain chase never closes. Approach through bushes or from outside its vision.

## 7. Ranking by expected impact for tungtungsahur

| # | mechanic / change | why | expected impact | effort | where |
|---|---|---|---|---|---|
| 1 | **Solo GG farmer: draft Varg (for Prism), Monster Strength, dedicated solo gem-cluster/wolf role** | GG in 6-9 turns; wolves at about 0 health cost; one probe Varg made 744 gems by r355 | very high: about +1.5-2 gems/round on G-rich maps (corners, collect, expanse, lanes) | medium (new role) | `draft.cpp:12`, roles `bot.cpp:787`, shop `bot.cpp:643-652` |
| 2 | **More parallel farming:** idle and follower bodies farm their own G or wolf groups | capture and tribute time is per body; Cassi/Prism idle about 30%, Stellar/Tavi follow about 28% | high | medium | squad logic `bot.cpp:760-1000` |
| 3 | **Gank solo farmers** with stun chain and double-turn timing | swing of 60-250 gems per kill; top player solo-farms GG | high vs this opponent | medium-high | new hunt mode; targets from wards and vision; 8-byte shared memory |
| 4 | **Contest or steal enemy captures; finish abandoned or damaged camps** | camps never heal; reward state waits | medium-high (up to 96 per steal) | low-medium | `join_capture()` variant for enemy-cleared groups |
| 5 | **Farming builds:** Monster Strength for Tavi, Ryth (when farming), Issac, Varg, Vendetta; Monster Focus for Stellar; Jungle only for wolf/elk farmers | Tavi wolf 17 → 12 turns; Stellar GG 10 → 8 | medium | low | `build_for()` `bot.cpp:643-652` |
| 6 | **Do not join captures of gem-only groups** | sharing adds 0 gems and costs the joiner 5+ rounds | low-medium | trivial | `join_capture()` `bot.cpp:611` |
| 7 | Endgame tribute denial (stun + lock on the enemy's final tributes) | stops a winning tribute | decisive in close games only | low | lock code `bot.cpp:664` + stun trigger |
| 8 | Altar camping on 2-altar maps (collision, elkring, rows) | they must bank at one of 2 altars | medium on those maps | medium | — |
| 9 | Draft counters from `current_draft(enemy)` (plan in draft memory) | pick gank mode or race mode | low-medium | low | `draft.cpp` |
| 10 | Respawn blocking, Home, Treasure, teleport crystal, monolith kiting | negative or negligible net value | ~0 | — | — |

Reproduce: `./cambc.exe run bots/mx-probe-a bots/mx-idle --map corners --rounds 450` (likewise -b,
-c), then read `team-a.stdout` from the replay zip. Tables: `python analysis/mechanics_calc.py`.
