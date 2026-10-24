# Economy profile of tungtungsahur (overnight version, vs bots/zz-idle)

Saved from the analyst's output (it could not write this file itself). Regenerate the tables with
`python analysis/econ_profile.py matches/league/20261015-091619-prof-tts --json prof.json && python analysis/econ_tables.py prof.json`.

## Summary

The report file analysis/econ-profile.md was NOT written: the harness blocks subagents from writing .md report files and said to put the content here instead. So the full results are in this output. The scripts to regenerate every table are on disk: analysis/econ_profile.py (now accepts any prof-* bot), analysis/econ_tables.py (new), analysis/econ_waste.py (new).

Uncontested (prof-tts, an instrumented copy of the current tungtungsahur, vs bots/zz-idle), the bot needs 331-872 rounds to reach 1000 gems, i.e. 1.15-3.02 gems/round. The worst maps are rows, collision, monolith and packs. The top player does 2.0-3.0 gems/round while being contested. A farming simulator says 250-460 rounds is reachable per map, a gap of 8-45% (largest on monolith, collision and rows).

Only about 35% of champion turns produce gems. Pooled over 19 valid idle games: 21% following a leader without hitting, 20% walking to camps, 18% walking to the altar or tributing. Separately, 16% is camp work that ends in a retreat or death; that overlaps the walking time.

Three outright bugs are confirmed in replays:
- Respawn deadlock: a blocked respawn reports timer 0, which the bot treats as "alive now" (bot.cpp:457, 573-579). On corners A, 5 of 6 champions froze from round 95 to round 2000.
- Engaging enemies who sit in their own spawn: filtered only while hunting (bot.cpp:770). This is 25% of all turns on packs; Ryth stood on one tile for 330 turns.
- Issac fights elk groups alone, because camp value assumes 250 DPS and ignores incoming damage (bot.cpp:499). On corners B he and Cassi died together 5 times, each dead 65% of the game, against an idle opponent.

Structural losses: banking one cluster per trip (bags 18-31 gems vs the top player's 46-61; 0.6-1.5 champion-turns per gem), back-liners following on far-camp maps (26-43% of turns), and capture walks that earn nothing on single-tile maps (lanes 18%, collect 12%).

Fix experiment: bots/prof-fix3 (deadlock fix, spawn-sitter filter, capture coordination, and a solo check when picking a camp) cut the summed rounds-to-1000 over the 20 idle games from 11106 to 10409 (-6%), which matches ming_bot's 10508. Packs improved 669 -> ~530. Against ming_bot it stayed at 14/20, within noise.

Hard survivability gating with a fixed damage formula (prof-fix4) froze whole teams: 6 of 20 idle games never finished. Treat that as a negative result; the fight-safety fix needs a softer, value-based model.

## Findings

### Uncontested economy is far slower than the top player and than a simulated optimum

**Evidence:** prof-tts vs zz-idle, rounds to 1000 (A / B) and gems/round. corners 2000*/463 (*deadlock; the unmodified bot did 427) 2.16; collect 380/331 2.63-3.02; lanes 402/376 2.49-2.66; interlock 426/434 2.3; expanse 471/484 2.1; packs 669/669 1.49; elkring 577/595 1.7; monolith 703/595 1.42-1.68; rows 872/679 1.15-1.47; collision 746/748 1.34. ming_bot vs idle: corners 390/341, lanes 307/313, collision 568/590, rows 707/697, packs 754/724, monolith 745/767. Top player on the platform (timelines.txt): about 1000 at r335-475 while contested, 2.0-3.0 gems/round, first tribute r35-75. Simulator best plans for our half of the map (analysis/plan_results.txt, 100 DPS per body): corners 318, collect 251, lanes 297, interlock 397, expanse 338, packs 431, elkring 463, monolith 349, rows 451, collision 419. Gap from the original bot's average to the sim best: 29/28/32/8/29/36/21/45/42/44%. The base-stat model (analysis/econ_optimum.py, half map) gives 438/369/448/542/423/640/659/570/947/645; it is pessimistic.

**Implication:** Even with perfect fighting we would lose the gem race on rows, collision, monolith, packs and elkring. Fixing the economy is a prerequisite for beating the top player.

### Turn budget: only about 35% of champion turns produce gems

**Evidence:** Pooled over 19 idle games (deadlock game excluded), % of champion turns: walk to camp 20, hit camp 17, capture 6, join capture 7, wait for respawn 1, walk to altar 14, tribute 4, shop 2, retreat 2, fight 4 (all spent on spawn-sitters), follow 21, dead 2. Per map, follow = 43% monolith, 31% rows, 30% elkring, 26% collision. Productive share (hit + capture + join + tribute) is 32-47% on collect and lanes but 23-35% on monolith, rows and collision. Waste attribution (analysis/econ_waste.py, % of turns, all maps): futile 16, solo leader hits 3, follow 21, spawn-fight 4, capture walks that earned nothing 4, bank 19, shop 2, dead/retreat 4, block 1. Against ming_bot: futile 42, dead/retreat 19, fight 16, dead 14.

**Implication:** The largest pools are following, banking walks and failed camp attempts, not fights or fuel. Fuel suspension was 0-7 turns per game, and the idle games lost no turns to exceptions.

### BUG: respawn deadlock when a champion stands on a respawning camp's tile

**Evidence:** Replay matches/league/20261015-091619-prof-tts/002-prof-tts-vs-zz-idle-corners.repl26a. At r86 Tavi, walking towards a full capture, stops on group 3's tile (36,37). Group 3's respawn is due at r93 but the occupied tile holds it (GameRules.md:192). The SDK reports camp_group_respawning{timer=0} (cambc.h:4305). update_ledger stores ready = round + 0 (bot.cpp:457). farm_group's respawning check `ready_round > round` (bot.cpp:573) fails, so it sets goals = g->tiles (bot.cpp:579). Ryth, Stellar and Tavi stand on or next to the tiles; Cassi and Prism wait for a free goal tile. 5 of 6 champions are frozen from r95 to r2000, and the score is 816 at r2000 vs an idle opponent. Partial blocking elsewhere: corners B 352 block turns, elkring 28-60, and 17-58 per game against ming_bot.

**Implication:** Rare but game-losing. It could also explain platform games where scoring stopped (069a8cb7: 2 tributes in 400 rounds), though that can't be checked without replays. The fix is one line plus masking follower goals.

### BUG: champions engage enemies standing in their own spawn and freeze

**Evidence:** read_context (bot.cpp:761-775) removes spawn-sitters only when ctx.hunt (bot.cpp:770). Otherwise engage = !ctx.enemies.empty() (bot.cpp:1094, 1136, 1187, 1256, 1303). attack_enemies fails and keep_distance(...,1,1) (bot.cpp:1107) can't step onto the enemy spawn. Packs A: Ryth stood on (22,26) for 330 turns and Stellar on (26,26) for 124. This was 25% of all turns on packs and 7% on rows. With the filter always on (prof-fix variants), packs went from 669/669 to 527/539, 522/485, 522/541 and 548/536 (every variant), and spawn-fight time to 0%.

**Implication:** Against the top player this fires whenever their champions recall, shop or respawn within 8 tiles of our farm. Cheap, robust fix.

### BUG-like: leaders solo fighting camps; Issac's deaths also kill Cassi

**Evidence:** choose_camp values gems/(d + health/250 + 5) (bot.cpp:499), i.e. 250 DPS and no incoming damage. One leader does 45-69 DPS. Back-liners run join_capture and farm_nearby_cluster first (bot.cpp:1208-1211, 1278-1281, 1343-1346), so they are often away. 39% of Issac's and 49% of Ryth's hits on wolf/elk groups had no ally within 4 tiles (collect Issac 86%, packs Ryth 83%, expanse Ryth 100%). Retreats within 6 turns of hitting: collect Issac on EE x16, collision EGGG x32, elkring EO x24, rows WWW x14. Lanes: Ryth walks 36 tiles to an elk, hits alone 15 turns and recalls, twice, before his first tribute at r180. Corners B: Issac attacks G+2 elks alone at r29, 122, 215, 308 and 401 and dies each time; Cassi dies with him (GameRules.md:427). Each is dead 65% of the game. Futile camp work (econ_profile extra_metrics, an upper bound) is 5-37% of turns per idle game (corners B 37%, collision 30-35%).

**Implication:** A large share of leader time is thrown away, and Issac's deaths cost two bodies. A fixed damage formula used as a hard gate does not fix this (see the fix experiment finding).

### Banking every single cluster: small bags, expensive round trips

**Evidence:** Bag at tribute start (idle): almost always one camp. 24 (gem cluster), 22 (wolf), 18 (half an elk on elkring, 102 of 107 tributes), 33 (a third of WWW on rows); collision 52 (EGGG split two ways). Bank::bank tributes as soon as gem_count() > 0 (bot.cpp:901-903). Walk to the altar per tribute = BFS distance from the capture tile: lanes 6.4, packs 7.3, expanse 8.1, interlock 7.5, collect 8.8, elkring 11.5, monolith 12.2, rows 20.4, collision 24.6 turns. Round trip plus channel per gem: corners 0.25, lanes 0.62, packs 0.54-0.67, expanse 0.66, interlock 0.72, collect 0.70-0.83, collision 1.0-1.1, monolith 1.1-1.16, elkring 1.33, rows 1.5. The whole team spends 2.1 (collect) to 3.9 (rows) champion-turns per gem in total. Top player's tribute windows average 46-61 gems (16-21 tributes to about 1000). Sim: banking at a 50-gem threshold saves 23-63 rounds on collect, lanes, packs, elkring, monolith and collision; a 150 threshold saves up to 120 on rows. 737 tribute starts, 2 failures.

**Implication:** On rows, elkring, monolith and collision about a third of all effort is banking trips. Banking about 2 camps per trip (with an enemy-seen override) matches the top player's pattern.

### Back-liners follow instead of farming on far-camp maps

**Evidence:** Per-champion follow share (idle, mean of both sides). Monolith: Stellar 76%, Tavi 75%, Cassi 55%, Prism 53%; Stellar delivers only 10% of the gems. Rows: Stellar 54, Tavi 51, Cassi 49. Elkring: Stellar 53, Tavi 51, Cassi 38, Prism 37. Collision: Cassi 51, Stellar 53. The solo-cluster rule (radius 16, bot.cpp:30, 588-607) works only on cluster-rich maps (collect follow 1%). Shared gem captures: elkring 89-93%, rows 81-88%, interlock 71%, monolith 50-56%. Sim: a better squad split with immediate banking saves 42-164 rounds vs the 2-squad structure (e.g. monolith 582->455, elkring 568->505, collision 522->480).

**Implication:** The biggest single pool of wasted turns on the slow maps. It needs a pair-based or free-roaming back-line design, not parameter tuning.

### Capture coordination waste on single-tile groups

**Evidence:** Lanes gem groups are single tiles (analysis/map-dumps/lanes.txt). A joiner takes the tile via join_capture (bot.cpp:611-633, range 6 at bot.cpp:34). The killer keeps trying to reach the occupied tile (farm_group bot.cpp:579). Example: lanes A r113-119, Cassi stands 7 turns at (32,10) while Prism holds the tile. Lanes A: 53 of 69 capture-walk streaks and 44 of 67 join streaks gave that champion no reward; lanes had 0 shared captures. Capture walks that earned nothing = 18% of all turns on lanes, 12% on collect, 6% on corners. With move-on and free-tile checks (F2): lanes 8%, collect 7%.

**Implication:** Worth 5-10% of turns on cluster maps. Simple to fix without removing gold-sharing joins, which PLAN exp 26 showed are valuable.

### Camp supply is not the bottleneck on cluster maps; reaction to respawns is slow elsewhere

**Evidence:** Idle camp-time (gem groups alive and untargeted per round, our half): collect 12-16, lanes 11-16, corners 10, expanse 7-11, collision 7, interlock 5, monolith 4-7, packs 2-3, elkring 1-4, rows 1-3. Gem groups never captured all game: collect 23-24 of 36, lanes 21-26 of 36, expanse 17 of 22, monolith 7-9 of 14, collision 8-9 of 14. Rounds from respawn to recapture: 20-35 on collect, lanes, interlock and expanse; 55-147 on packs, elkring, monolith, rows and collision.

**Implication:** On cluster maps more independent farmers help directly. On sparse maps the squads are too few and too slow to cycle respawns.

### Fix experiments: F1-F3 are safe gains; a hard fight-safety gate is harmful

**Evidence:** Summed rounds-to-1000 over 20 idle games: original tts 11106, prof-tts 12620 (includes the deadlock), prof-fix (F1-F4) 11236 (elkring B 1184), prof-fix2 (F1-F3) 10533, prof-fix3 (F1-F3 + solo-only camp-choice check) 10409, prof-fix4 (+ engage-time check with allies counted) 19355 (rows, collision, elkring A and expanse A never finished), prof-fix5 (solo-only engage check) 10930, ming_bot 10508. Per map, prof-fix3 vs original: corners 341/373 vs 427/463, packs 522/541 vs 669/669, lanes 384/388 vs 438/433, collision 729/686 vs 758/748, rows 773/697 vs 872/679; the rest within noise. Wins vs ming_bot out of 20: prof-tts 14, fix 15, fix2 11, fix3 14, fix4 12, fix5 14 (noise). Runs: matches/league/20261015-134013-prof-fix, 134215-prof-fix2, 134236-prof-fix3, 134412-prof-fix4, 134539-prof-fix5. Fixes are marked [prof-fix] in bots/prof-fix*/src/bot.cpp.

**Implication:** Ship F1 (deadlock), F2 (capture move-on and free-tile join) and F3 (spawn-sitter filter) now. The fight-safety logic needs a value-based model plus waiting at range, not a hard skip. Fights, not economy, still decide the ming_bot games (14% of turns dead).

## Recommendations

- **Restructure the back line on far-camp maps: farm in pairs (e.g. Ryth+Tavi and Issac+Cassi, with Stellar and Prism free), or let a follower take any camp it can clear alone (wolves) within ~10 tiles of the leader instead of shadowing at ring 1-2.** Impact: Largest: follow time is 26-43% of turns on monolith, rows, elkring and collision. Sim estimate 40-130 rounds faster on monolith, elkring, collision and interlock (e.g. monolith 582->455). Effort: Medium-high (role and squad logic). Must be validated by rounds-to-1000 and vs ming_bot, because PLAN exp 3 (fully solo back-liners) lost on league wins.. Where: bots/tungtungsahur/src/bot.cpp farm_nearby_cluster 588-607 (radius 16 at line 30), follower branches 1213-1216, 1283-1286, 1348-1357, Bot::init squad assignment 784-806
- **Batch banking: tribute when the bag is >= ~48 gems, or an enemy is in sight or was seen in the last ~10 rounds, or the nearest altar is <= 4 steps away or on the way to the next camp, or the next camp's respawn wait exceeds the detour. Pick the altar nearest the next target.** Impact: Banking is 19-20% of turns and 0.6-1.5 champion-turns per gem; bags are 18-31 vs the top player's 46-61. Sim: about 23-63 rounds per map at a 50-gem threshold (monolith 455->392, collision 480->435, packs 522->468); more on rows with larger thresholds. Effort: Low-medium (one function plus an enemy-memory flag). Carry risk must be bounded (killer takes the bag), so keep the enemy-seen override.. Where: bots/tungtungsahur/src/bot.cpp Bot::bank 901-982 (trigger at 903); call order in play_turn 1061-1064
- **Realistic camp valuation and engagement safety: clear time = health / (60 x bodies within 4 of the leader) in choose_camp's value (soft, not a hard skip). At the first hit, if the leader would die before the camp and no ally is within 4, wait at range 4 (camps are passive until hit) for up to ~8 turns, then retarget. Issac retreats at 50% when alone (his death kills Cassi).** Impact: Futile camp work is 16% of turns (corners 37%, collision 30%). Removes Issac+Cassi double deaths (65% dead on corners B) and Ryth's 140-turn solo elk failures on lanes. Expected 5-15% faster on corners, collect, lanes and collision. Effort: Medium. The hard-gate versions (prof-fix4/5) froze teams or slowed rows, collision and monolith, so tune against both idle and ming_bot.. Where: bots/tungtungsahur/src/bot.cpp choose_camp 470-515 (value at 499), farm_group 562-584, choose_objective 999-1024, survive 850-880
- **Always drop enemies standing in their own spawn region from ctx.enemies (still keep them in bank()'s danger map).** Impact: Packs 669 -> about 485-548 rounds in every tested variant (-20%); rows A 872 -> 705-845. Removes freezes whenever the top player recalls or shops near our farm. Effort: Trivial (implemented in bots/prof-fix*: read_context).. Where: bots/tungtungsahur/src/bot.cpp read_context 761-775 (condition at 770); engage checks 1094, 1136, 1187, 1256, 1303
- **Fix the respawn deadlock: update_ledger uses ready = round + max(1, timer) for respawning groups, and every wait/follow goal excludes the tiles of respawning groups (off_respawning mask).** Impact: Removes 2000-round stalls (1 of 20 idle games: 816 gems at r2000 with 5 champions frozen) and up to 352 blocking turns per game. Small average gain, large tail-risk reduction. Effort: Trivial (implemented in bots/prof-fix*).. Where: bots/tungtungsahur/src/bot.cpp update_ledger 446-463 (line 457), farm_group 573-580, follower rings 1215, 1285, 1350, 1356
- **Capture coordination: when every spawn tile of a cleared target is occupied, mark it taken for ~8 rounds and move on. join_capture only joins if a tile is free and the walk is <= 4 rounds.** Impact: Capture walks that earned nothing: lanes 18% -> 8%, collect 12% -> 7% of turns. Lanes 402/376 -> 348-388, collect 380/331 -> 300-347 in the fix variants. Effort: Low (implemented in bots/prof-fix*: taken_until, free-tile check).. Where: bots/tungtungsahur/src/bot.cpp farm_group 576-580, join_capture 611-633, choose_camp 470-515, farm_nearby_cluster 588-607
- **Faster opening: every champion starts on the nearest gem clusters; leaders take elks and wolves only once followers are within 4 tiles.** Impact: Team first tribute is r82 on rows and r116 on collision; Ryth's own first tribute is r142-210 on lanes, interlock and collision. The top player's first tribute is r35-75 while contested. Effort: Low-medium.. Where: bots/tungtungsahur/src/bot.cpp choose_objective 999-1024, tank_turn 1085-1121, fighter_turn 1125-1176
- **Shop opportunistically: only when passing spawn anyway, or raise shop_trip_gold to about 250 on far maps.** Impact: Small: shopping is 1-3% of turns (elkring 141 per game, rows 103, monolith 90). PLAN showed no league difference for 100/250. Effort: Trivial.. Where: bots/tungtungsahur/src/bot.cpp shopping_trip 984-995, shop_trip_gold line 21
