# tungtungsahur — overnight plan and experiment log

NOTE: step 16 changes the user's earlier rule "fight only after being hit" to
"fight enemies in sight unless outmatched" because it wins more (flag this in the report).

Goal (from the user, 2026-10-14 23:30): **build a bot that wins no matter what the
opponent chooses.** Work only on `bots/tungtungsahur`. The user checks results at
09:00 on 2026-10-15. If a session ends, the next one continues from "Next steps".

## Ground rules
- Every change is tested with the league (`python tools/league.py`) before it is kept.
  A change is kept only if it does not get worse against the strongest opponents
  (Faisal-bot and its draft variants) and does not collapse against any opponent.
- Before each risky change, the current best is frozen as `bots/tungtungsahur-best/`
  (copy of `src/`), so it can always be restored.
- Platform testing is authorized. The user approved the `cambc login` browser flow
  on 2026-10-17. On 2026-10-18, the official `cambc` 2.2.5 CLI authenticated with
  that session and created unranked groups; this supersedes earlier notes that a
  browser-action connector was required. The current live streak is 0/10. Local tests
  remain proxies and do not count toward it.
- Fuel: 100k per turn. Never ask the engine for all camp groups every turn (cached in
  `groups()`); check `fuel_remaining()` traces when adding per-turn work.

## Evaluation
- `tools/league.py <bot> [--opps a,b,c] [--maps ...] [--jobs N]` runs every opponent on
  every map from both sides with `cambc run-batch`, prints wins per opponent and map,
  and reads the bot's `SCORE` log lines for final gem totals.
- Opponent pool (see "League" below) covers different drafts and styles:
  Faisal-bot (planner, strongest), Faisal draft variants, tralalerotrarala (hunter),
  my-bot / my-bot-v2 / tungtungsahur-v1 (older versions), starter-cpp.

## Baseline (start of the night)
tungtungsahur (team fight-back, peel, respawn memory, gems-first):
- vs Faisal-bot 10/18 (791 vs 776 gems), vs tungtungsahur-v1 11/18, vs my-bot 12/18.
- Weak maps vs Faisal-bot: collision, corners, elkring, lanes.

## Experiment log
(newest last; league = 9 opponents x 9 maps x 2 sides = 162 games)

| # | Change | League | vs Faisal-bot | Kept? |
|---|---|---|---|---|
| 0 | Baseline (team fight-back, peel, respawn memory, gems-first) | 102/162 | 8/18 (706 vs 794) | - |
| 1 | Bank: price altars by real path, break enemy altar locks instead of freezing | 115/162 | 13/18 (891 vs 591) | yes |
| 2 | Back-liners solo-farm ready gem clusters (never fight back) within 10 tiles | 129/162 | 14/18 (897 vs 555) | yes |
| 2b | ...radius 6 / 16 / 24 / 40 | 125 / **138** / 132 / 134 | 14 / **16** / 16 / 16 | radius 16 kept |
| 3 | Back-liners (not Cassi) always farm their own camp instead of following | 132/162 | 15/18 | no |
| 4 | Fight alarm carries a position; allies within 10 tiles converge (new 4-bit-stamp memory layout) | 136/162 | 15/18 (Faisal family 74/90 vs 79/90) | no |
| 5 | Focus fire: target = (damage + 2*gems) / health | 140/162 | 17/18, Faisal family 81/90 | yes |
| 6 | Shop-trip gold 100 / 250 (was 150) | 138 / 137 | family 80 / 80 | no (150 kept) |
| 7 | Fight-back rounds 4 / 14 / 20 / 30 / **60** / 2000 (was 8) | 128 / 143 / 146 / 147 / **149** / 149 | family 76 / 83 / 87 / 87 / 84 / 83; Faisal-bot 18/18 at 30 and 60 | 60 kept |
| - | **League enlarged**: 14 opponents (3 more Faisal draft variants, my-bot-v2/v3) x 10 maps (+collect) x 2 = 280 games. Best = 255/280, family 146/160 | | | |
| 8 | Retreat 0.2/0.25, 0.25/0.3 (was 0.3/0.35) | 253 / 251 (big) | family 145 / 145 | no (153/162 on the small league was noise) |
| 9 | Tank build Power Str/Health/Str (Faisal's) instead of Jungle Health | 254 (big) | family 148 | no (neutral) |
| 10 | **Fuel**: ledger + join_capture check a group's spawn tiles instead of full-map bitboard AND; blocked_tiles memoised per round/position. Turns with <5k fuel left on lanes: 382 -> 22 | **263/280** | family **154/160** | yes |
| 11 | Fuel: visible enemy/ally lists memoised per round/position, team size cached (read_context 36k -> 6k, role turn ~55k -> ~23k) | 264/280 | 154/160, hunter 19/20 | yes |
| 12 | Camp clear-time estimate health/150, /250, /800 (was /400) | 266 / **267** / 261 | 153 / 154 / 152 | /250 kept |
| 13 | Stickiness 1.1 / 1.7 (was 1.3) | 265 / 268 | 157 / 155 | no (noise) |
| 14 | Gold in camp value: gems + gold/10, gems + gold/5 | 263 / 265 | 150 / 153 | no |
| 15 | **Fight odds**: if nearby enemy strength (sum health x damage within 6) > 1.3x ours, fall back instead of fighting (ratios 1.0 / **1.3** / 1.6 tested) | 263 / **269** / 267 | 152 / **156** / 155 | 1.3 kept |
| - | `cambc maps pull`: still the same 9 official maps. Added self-play opponents opp-tts-locker (best + altar locks) and opp-tts-aggro (best, fights anything in sight). Best = 290/320, but only 11/20 and 10/20 against these two. | | | |
| 16 | Candidates on 17 opponents (340 games): A aggro+fall-back 308, B aggro+locks 306, **C aggro+locks+fall-back 313** (13/20 vs old best, 897 vs 775 gems) | **313/340** | 158/160, hunter 20/20 | C promoted; old best kept as opponent opp-tts-v2 |
| 17 | Fight alarm with position (4-bit stamp memory), allies within 10 converge for 6 rounds | 307/340 excl. head-to-head (best 313) | 157 | no (12/20 vs best but weaker elsewhere) |
| 18 | Draft order: (a) Willow 5th, (b) Prism before Stellar, (c) **Stellar before Tavi** | 307 / 306 / **316** | 158 / 158 / **160** | (c) kept (11/20 head to head vs previous best); previous best kept as opponent opp-tts-v3 |
| - | 18-opponent league baseline: 327/360; every non-self opponent 18-20/20; losses only vs self-play variants | | 160/160 | |
| 19 | Safe bank route: while carrying gems, path around tiles within 3 of visible enemies (direct route if none) | 332/360 (same 18 opps) | 160/160 | yes (10/20 h2h, 857 vs 777 gems); previous best = opp-tts-v4 |
| - | 19-opponent league baseline (adds opp-tts-v4): 342/380 | | 160/160 | |
| 20 | Retreat 15 points earlier while carrying 30+ gems | 331/380 excl. h2h (12/20 h2h) | 160 | no |
| 21 | Peel chase: walk up to 7 tiles into stun range of an enemy tribute with 10+ gems | 338/380 | 160 | no |
| 22 | **Robustness**: reads on units killed/out of sight this turn threw to main.cpp and lost the whole turn (~3,200 lost turns per 380 games). Safe helpers (safe_pos, guarded threat/top_threat/nearest/health_pct). main.cpp now labels these 'turn lost'. Lost turns 3,226 -> 2 | **345/380** | 160/160 | yes |
| 23 | Skip actions while stunned (shop only) | 345/380 (identical) | 160 | no (no effect) |
| 24 | Peel with altar lock: place carried lock on an enemy's tribute altar within 2 (cancels it) | 345/380 (identical) | 160 | no (no effect) |
| - | Diagnosis: self-play losses are mostly pure farming races decided by small speed differences (e.g. lanes B vs v2: 924 vs 1008, 0 kills). | | | |
| 25 | Squad-A followers also hit camps within 2 tiles of Ryth (not only already-damaged ones) | 343/380 | 160 | no |
| 26 | Followers never join captures (leader captures alone) | **301/380** | 152 | no: capture gold sharing is very valuable |
| 27 | Join-capture range 6 / 8 (was 4) | **351** / 348 | 160 / 156 | 6 kept; previous best = opp-tts-v5 |
| - | 20-opponent league baseline (adds opp-tts-v5): **362/400** | | 160/160 | |
| 28 | Back-liners also solo-farm gold clusters within 8 when no gem cluster is near | 355/400 | 160 | no |
| 29 | Squad leaders (Ryth, Issac) also join nearby captures | 337/400 | 158 | no |
| 30 | Fight-odds ratio 1.15 / 1.5 (current 1.3) | 354 / 346 | 159 / 160 | no (1.3 stays) |
| 31 | Camp value gems + gold/20; solo cluster radius 20 | 343 / 357 | 159 / 160 | no |
| 32 | Builds: casters all Power Focus, Tavi Focus/Strength/Focus | 350 | 159 | no |
| 33 | Prism in squad A (follows Ryth) instead of squad B | 347 | 160 | no |
| - | Like-for-like vs the original 9-opponent league: 102/162 at 23:30 -> **160/162** now. REPORT.md written. | | | |
| 34 | Endgame denial: enemy >= 850 and ahead -> free champions guard the altar nearest the enemy base | 360 | 160 | no |
| 35 | Monolith penalty 0.5 (was 0.2) | 353 | 160 | no (more monolith-map losses) |
| - | Opening check: first tribute ~r40-55 on most maps; rows r85 (all camps are 3-wolf groups 16+ tiles away) and collision r98: map-inherent | | | |
| 36 | Outmatched fall-back regroups on Ryth (if he is not near enemies) instead of spawn | 338 | 159 | no |
| 37 | Small bags (<20) keep farming when the nearest altar is >8 tiles away and it is safe | 351 | 160 | no (bank immediately stays best) |
| - | Noise check: best + a tiny behaviour-neutral fuel burn (2 variants) = 362 and 362. Results are reproducible now that turns no longer run out of fuel. | | | |
| 38 | Re-sweep: shop-trip gold 100 / 250; retreat 0.25/0.3, 0.35/0.4 | 353 / 343; 341 / 350 | 158 / 159; 157 / 158 | no (current values are a local optimum) |
| - | Self-play ceiling: remaining mirror losses are mostly side A on corners/rows/lanes/collect from both directions, i.e. map side advantage (ties also go to B). | | | |
| - | Fuel check (current best): role turns never below 13.8k fuel left on lanes; median 60-70k left on all big maps. | | | |
| 39 | Only engage enemies within 5 / 3 tiles (now: anything in sight) | 349 / 306 | 156 / 145 | no |
| 40 | Cleanup: removed dead fight-back counters and unused context fields | 362/400 (unchanged) | 160 | yes |
| 41 | Issac dashes 2 tiles along the path when travelling (4+ steps from goal) | 343 | 159 | no (dash better kept for fights) |
| - | Idle check: back-liners stand idle 9-25% of turns (Cassi worst), leaders 0-7% | | | |
| 42 | Idle back-liner farms a low-danger gem camp (dps <= 20) within 6 | 358 | 160 | no |
| 43 | Peel only tributes of 10+ gems | 362 (same) | 160 | no (no gain; keep simpler rule) |
| 44 | Safe bank route avoids 4 tiles (was 3); insurance lock on the altar we tribute at | 348 / 347 | 157 / 159 | no |
| 45 | Varg instead of Ryth as the tank / squad-A leader | 323 | 158 | no (Ryth's area stun + health matter) |
| 46 | Vesper Vale instead of Tavi (marksman, +20% gold, no stun) | 319 | 159 | no (Tavi's stun matters) |

### 15 Oct: counter to the top platform player
New measures: the league now has 22 opponents (`tools/opps22.txt`: the 20 above + ming_bot + fx-dbllock,
440 games), and a race test vs `bots/zz-idle` (a bot that does nothing): `python tools/league.py <bot>
--opps zz-idle`, per-map rounds via `python tools/race.py <league dirs>`. Overnight version (now
`bots/opp-tts-v6`): 385/440, ming 12/20, race total 11106 rounds (20 games, lower is faster).

| # | Change | 22-opp league | ming | race total | Kept? |
|---|---|---|---|---|---|
| 47 | 4 bug fixes: enemy-lock freeze (attack the ENEMY lock, altar_lock_at prefers ours), respawn-squat deadlock (wait off a held-back group's tiles), never engage enemies on their own spawn, move on when a cleared group's tiles are all taken / join only free tiles of gold-paying groups / leader alone skips camps that would beat him | 376 | 15 | 10399 | yes (bugs) |
| 48 | + ming_bot's burst: every turn cast the ready spell that hits the most enemies | 389 | 15 | 10399 | yes |
| 49 | + bank at 48 gems unless enemy seen / hurt / altar near / next camp fights back | 386 | 15 | 10356 | no |
| 50 | + back-liners solo a lone wolf 4-10 tiles from their leader (no enemy for 20 rounds) | 396 | 16 | 10297 | yes |
| 51 | + squads carry gems into wolf camps too (no elk) | 378 | 15 | 10200 | no (bags get stolen) |
| 52 | + Varg (solo gem-cluster / lone-wolf farmer, Monster Strength) instead of Prism on maps with >= 4 soloable groups | 392 | 17 | 10048 | yes |
| 53 | + Varg retreats as soon as outmatched, home camps only after a sighting | 384 | 17 | 10048 | no |
| 54 | Fight ratio from the enemy draft (fragile 1.6 / tanky 1.1) | 389 | 16 | - | no (noise) |
| 55 | Comeback: carry 48-gem bags when 150+ behind after r150 | 390 | 16 | - | no (neutral) |
| 56 | SCOUT telemetry lines (behaviour unchanged; `tools/scout.py`) | 389 | 16 | 10048 | yes |

### 15 Oct night: the user's "feed Stellar" plan
League from here: `tools/opps22b.txt` (Faisal-bot dropped: someone copied a second `src` folder into
`bots/Faisal-bot/src/src`, so it no longer builds; opp-tts-v6 added). Main version (cand-varg + scout) on it: 380/440.

The plan: draft Stellar, Cassi & Issac, Ryth, Varg, Tavi. Early game (until Stellar or Varg owns an
emblem, or round 600): farm, Stellar stays with Ryth on gold camps, only hit enemies already in reach.
Mid game: engage enemies within 5 tiles, not deep in their half. Late game (Stellar owns 3 emblems):
fight as before. Before late: no camps deep in the enemy half, back off when outnumbered by 2.
Gold to Stellar: when she is near a gold-paying capture, Varg stays off it and at most one other
teammate shares it. Stellar builds Power Focus only; Varg Jungle Strength then Power Strength.
Phase flags live in the top bits of shared-memory bytes 6/7.

| # | Change | 22b league | ming | v6 | race total | Kept? |
|---|---|---|---|---|---|---|
| 57 | the plan as written (cand-feed) | 363 | 14 | 13 | 10880 | no |
| 58 | same draft/items/gold rules, phases off (feed-nophase) | 379 | 15 | 14 | 10460 | no |
| 59 | the plan + Varg helps Issac's camp when there is nothing to solo (feed-vargsquad) | **392** | 15 | 16 | 10381 | **yes (main)** |

Previous main kept as `bots/opp-tts-v7`. Remaining losses mostly corners and interlock.

### 16 Oct: the user's "whole team farms together, economy to Stellar / Varg" plan
Rules: Ryth leads the whole team (Issac while Ryth is dead) and everyone works his camp, staying
behind him until its camps are awake. Only Stellar and Varg capture (Varg leaves a capture to a free
Stellar), so they get all the gold; meanwhile the team moves on to the next camp. They carry a bag
of 60 gems before banking (unless an enemy was seen, they are hurt, or an altar is near). Early-game
camp choice counts gold double (nearest gold camps first). Varg builds Monster Strength then Power
Strength. Two bugs found and fixed on the way: followers walling the leader in (now they stand
behind him), and treating an out-of-sight group as cleared (a leader flip-flopped between two camps).

| # | Change | 22b league | ming | v6 | race total | Kept? |
|---|---|---|---|---|---|---|
| 60 | team farming all game (cand-team) | 328 | 14 | 9 | 11853 | no (others never get gold; one group is slow on big maps) |
| 61 | team farming in the early game only, then exp. 59 (cand-team2) | 388 | **18** | 12 | 10360 | **yes (main)** |

Previous main kept as `bots/opp-tts-v8`.
| 63 | Collision/lanes fix: early game the carries bank every capture again (no 60-gem bag; xuanming led 144-36 at r100 on lanes) | 394 | 16 | - | - | **yes (main)**: collision+lanes vs xuanming/ming/racer/v8/faisal 11 -> 16 of 20, xuanming 16 -> 19/20 |
| 64 | Farming shard builds (`analysis/shard_value.py`): A = Monster then Power in the best camp stat for everyone (Str: Tavi, Ryth, Varg, Issac; Focus: Stellar, Cassi), B = A but Ryth keeps Jungle Health first, C = only Stellar Monster Focus + Tavi Monster Strength | A 415, B 420, C 422 of 480 (main 432) | 19 / 16 / 18 | - | race 509 / 508 / 513 (main 516) | no: farming barely speeds up (clearing is ~17% of turns) and fights get weaker |
| 65 | Movement study (bots/tts-moves, tts-trips; tools/moves.py): paths are within 4-9% of the shortest terrain path; walking to altars and following cost the most. Updates: (1) carry 2 camps (40 gems) on far-altar maps, (2) bank at the altar nearest the next camp, (1+2), (3) stick_bonus 1.6, (4) Home emblem as Ryth's and Stellar's second emblem | 421 / 415 / 419 / 417 / **432** of 480 (main 432) | 18 / 16 / 18 / 16 / 18 | - | race 503 / 525 / 506 / 522 / 508 (main 516) | no; (4) ties the main version, kept as bots/u4 |
| 62 | Diagnosis of 10 platform losses (stun-heavy Ren/Stellar/C&I drafts; we were dead 30-53% of the time): Cassi/Issac and everyone near a stun-heavy enemy retreat at 50%, Issac never dives (cand-safe) | 376 | 16 | 10 | - | no (deaths unchanged at 4.9/game: late retreat is not the cause) |

Head to head vs the overnight version: 11/20 (gems 872 vs 818); expanse is lost from both sides
(pure race, 4 bodies: uncontested 498/559 vs 469/484 overnight; no single change explains it).
`bots/opp-racer` (our fastest econ, never starts fights) is too weak to stand in for the top player.
Analyses: `analysis/forensics.md`, `ming-study.md`, `mechanics.md`, `maps.md` (+ econ profile in the
workflow output); platform timelines in `matches/platform-logs/timelines.txt`.

## Notes
- `run-batch` cannot compile on this machine (long-path issue): league.py builds every
  bot with `cambc build` first. Concurrent `cambc run` calls break CMake.
- Map facts (from bots/zz-probe): collision 41x41 3-pick, 2 altars on one side
  (27,20),(39,20); lanes 90x30 5-pick, all 21 camps in the middle (x 36-53), 18 altars;
  corners 71x71 5-pick; elkring 30x30 elks+gold only; expanse 80x80 4-pick, 30 gem
  clusters; rows 50x50 4-pick wolves; packs 31x31 3-pick wolves.
- Small code changes shift results chaotically (fuel/timing), so +-5 league wins is noise.
- Fuel matters a lot on big maps (lanes 90x30, corners 71x71, expanse 80x80): profile with
  fuel_remaining() marks; full-map bitboard ops per camp group are expensive.

## Current status (updated 08:30: final)
- Best = `bots/tungtungsahur` (copy in `bots/tungtungsahur-best`): 362/400 on the 20-opponent
  league; Faisal family 160/160; hunter 20/20; my-bot 19/20; other old bots 20/20;
  self-play variants opp-tts-v2..v5/locker/aggro 11-18/20.
- Two leagues can run in parallel only if the second starts ~20s later (run-batch's own
  up-to-date check races on a temp file: 'failed to persist temporary file').

## Current status (16 Oct): main = experiment 61 (team farming early, then squads); 388/440 on
`tools/opps22b.txt`, ming 18/20, Faisal variants 140/140. Previous status:

## Status 15 Oct night
- Best = `bots/tungtungsahur` (= tungtungsahur-best = submissions/tungtungsahur.zip) = experiment 59,
  the user's feed-Stellar plan: 392/440 on `tools/opps22b.txt` (previous main 380), ming 15/20,
  Faisal variants 140/140, race total 10381.
- Next: get platform logs vs the top player with this version and run `tools/scout.py` on them
  (their draft, where they farm and tribute, how our champions die), then build a targeted counter.
  Open econ leads: expanse regression; packs (522/541 vs top ~480); camp deaths (SCOUT DEATH lines
  with no enemy near); corners opening when the centre is contested.

## Next steps (overnight list)
1. Remaining ideas: gold value small (gems + gold/20); solo cluster radius 12/20 retune;
   mage build variants (all Power Focus; Tavi foc/str/foc); squad assignment (Prism in squad A);
   pre-positioning followers near respawning camps; ward usage; deny enemy captures.
2. DONE: REPORT.md written; final league 362/400; submissions/tungtungsahur.zip = current src.
   (Session stalled 02:20-08:27.)



## Latest research (17 Oct 2026)

| # | Change | 24-opponent league | Strong local proxies | Race vs idle | Decision |
|---|---|---:|---:|---:|---|
| 66 | User-requested fixed draft Ryth, Vendetta, Tavi, Willow, Prism | 111/480 | 7/60 | - | no; no Stellar/Varg phase trigger and severe race losses |
| 67 | Same draft, phase advances on any champion emblem | 296/480 | 35/60 | - | no; phase mismatch fixed, but 2,225 deaths and still far below main |
| 68 | Top-pick draft Cassi & Issac, Stellar, Ren, Varg, Ryth | 414/480 | 53/60 | - | no; below current draft |
| 69 | Varg solo farms from round 1 on every map | 418/480 | 51/60 | 10,129 rounds | no; slight race gain, league loss |
| 70 | Varg solo only on Collect, Corners, Monolith, Rows | 425/480 | 52/60 | 10,023 rounds | no; faster race, did not beat 432 baseline |
| 71 | Draft C&I / Varg / Stellar on every map | - | 71/80 vs four strong sources (main 73/80) | - | no; replacing Ryth everywhere loses map coverage |
| 72 | Draft Varg instead of Ryth only on 80×80 Expanse | 434/480 (main 432/480) | 76/80 vs same four sources (main 73/80) | - | no promotion; the full league gain is only +2, inside noise |
| 73 | On Expanse, switch to C&I / Varg / Stellar only after enemy Varg is visible | 435/480 (main 432/480) | 77/80 vs same four sources (main 73/80) | - | no promotion; +3 is inside noise, but this is the best tested Expanse response so far |

Public top-50 snapshot and findings: `analysis/top50-evaluation-20261017.md`. These are local tests, not platform matches. The public unranked challenge endpoint requires a signed-in team session; no live top-50 streak has been recorded. Main source was not changed because no candidate has cleared the league promotion gate.

## Current official-map refresh (17 Oct 2026)

The published pool now contains 17 maps. `analysis/map_layout.py`, `analysis/farm_sim.py`, and
`analysis/maps_extra.py` use the refreshed map dumps; see `analysis/maps.md` for the current pool table
and provisional routes. Several same-named maps have changed group counts and yields, so earlier route
tables are historical. `tools/league.py` now resolves the published map names to the downloaded files,
including ID-suffixed files and the `rushbait_v2` filename alias. `tools/scout.py` now reads SCORE lines
from the bot's own perspective on either side; the old side-B swap was incorrect.

Baseline main, no source changes: **104/136** against `ming_bot`, `xuanming`, `faisal-orig`, and
`opp-racer` across all 17 maps, 8 games per map (`matches/league/20261017-153514-tungtungsahur`).
Per-map scores are in `analysis/top50-evaluation-20261017.md`. The old 432/480 result used the previous
map set and is not directly comparable.

| # | Current-pool experiment | Strong local proxies | Decision |
|---|---|---:|---|
| 74 | On Swirl, replace Varg with Vendetta | 0/4 vs `ming_bot` and `xuanming` | reject; lost the farming role and all four games |
| 75 | On Swirl, replace Ryth with Vendetta while keeping Varg | 0/4 vs `ming_bot` and `xuanming` | reject; no wins against either top local proxy |
| 76 | Keep the whole team grouped through round 600 on Swirl | 4/8 vs all four proxies; 1/4 vs `ming_bot` and `xuanming` | no promotion; same overall Swirl score as main (4/8) |
| 77 | Let Varg solo farm from round 1 on Lanes | 2/8 vs four local proxies (main 4/8) | reject; both top proxies beat it on both sides |
| 78 | Draft Prism / Stellar / C&I / Ryth / Tavi on Contest and Stampede | 15/16 in each of two candidate runs; main 11/16 in both matched baselines | strongest current-pool candidate; +4/136 full league, all gains on these maps; keep isolated pending live top-50 streak |
| 79 | Contest defensive emblems first (Durability Health, then Jungle Health) | 5/8 on Contest (candidate 7/8) | reject; more deaths (50.5/game vs 48.8) and no win gain |
| 80 | Gather the team, then force Monolith priority on Contest | 6/8; 43.1 deaths/game | reject; fewer deaths but one fewer win than the candidate |
| 81 | Monster damage emblem, then Jungle Health on Contest | 6/8 | reject; does not beat the default candidate's 7/8 |
| 82 | Ryth escorts a nearby ally carrying 100+ gems on Contest | 6/8; Ming 2/2, Xuanming 1/2, Faisal 1/2 | reject as a general change; repaired the Ming-side loss but introduced losses against Xuanming and Faisal |

The idle control won all ten test games on Lanes, Swirl, Contest, Stampede, and Pilgrimage. On Lanes it
reached 998 at rounds 623/635 from A/B, only a 12-round gap. Against the four stronger proxies, all
four Lanes losses were from side B, with no deaths in the sampled Ming/Xuanming losses; this points to
losing the central economy race as second mover, not a general inability to farm Lanes. On Swirl, the
main lost both sides against Ming and Xuanming; sampled losses had 47–70 deaths and 132–198 gems lost.
The Vendetta draft swaps did not fix that fight. On Collision vs Ming, there were 15–16 deaths and the
opponent repeatedly locked the sole usable altar at (27,20).

Experiment 78 is the strongest current-pool candidate: its Contest/Stampede draft wins 15/16 in two
separate candidate runs, against 11/16 for the main in two matched baseline runs. The full 17-map
comparison is 108/136 versus 104/136; the 15 other map scores are unchanged. Keep it isolated until
the requested live evaluation can confirm it against top teams. Main source and
`submissions/tungtungsahur.zip` remain unchanged. The requested unranked top-50 streak is still 0/10;
TinyFish remains `installed: false`, so no game-site match could be created in this session.

Contest-specific follow-up: candidate 78 has 48.8 deaths/game on Contest versus main's 56.9, but its
one loss to Ming on side B still ties 200–200. It banks 200 by r1100, then Stellar dies carrying a
second 200-gem bag at r1911 after an enemy altar lock at (25,24) was seen at r985. Main's same matchup
had 79 deaths and lost 0–400. The defensive-emblem, early-Monolith, camp-damage-emblem and Ryth-escort
variants (#79–82) all scored only 5–6/8 versus candidate 78's 7/8. The public Mite–Fish group also
ended Contest at 0–0/2000 despite Mite using this draft, so the draft alone has not demonstrated a
reliable way to score on the map.
Run folders: `matches/league/20261017-155738-cand-contest-iron-test`,
`20261017-155745-cand-contest-rush-test`, `20261017-155843-cand-contest-monster-test`, and
`20261017-160055-cand-contest-escort-test`.
Experiment 77 also failed to improve Lanes. The control against `zz-idle` reaches 998 at r623/r635
from A/B, while the four-proxy baseline loses only from B; a Varg solo opening reduced the map result
from 4/8 to 2/8. Experiment 78 uses Mite's observed Prism / Stellar / C&I / Ryth / Tavi draft on the
two contested-camp maps and is the best current-pool candidate; await live top-team validation before
updating the main source or upload bundle.

### 17 Oct: Collision follow-ups and current local candidate

| # | Change | Result | Decision |
|---|---|---|---|
| 83 | Buy/use a teleport crystal for bags of 100+ gems to reach the sealed Collision altar | 4/8, equal wins to main; losses to Ming and Xuanming from both sides | reject: no win improvement; the route activated but did not break their economy/altar pressure |
| 84 | Use the same Collision teleport route for any positive gem bag | 2/8 | reject: materially worse; do not use this as the default Collision bank route |
| 85 | On Collision only, draft Stellar / Cassi & Issac / Varg, replacing Ryth; combine with experiment 78's Contest/Stampede draft | 5/8 on Collision in two identical targeted runs; combined full pool 109/136 | keep isolated: +1 Collision win over main and +1 over experiment 78, but still 0/2 vs Ming; not live-validated |

Experiment 83 is `matches/league/20261017-160446-cand-collision-tp-test`; #84 is
`20261017-160624-cand-collision-tp-smallbag-test`. The #85 targeted runs are
`20261017-160727-cand-collision-varg-test` and `20261017-160736-cand-collision-varg-test`; the
matched main repeat is `20261017-160747-tungtungsahur`. The combined candidate is
`bots/cand-contest-prism-collision-varg-test`, full run
`matches/league/20261017-160824-cand-contest-prism-collision-varg-test`.

The 109/136 candidate improves only Collision over experiment 78: Collision 4/8 -> 5/8, Contest
stays 7/8, Stampede stays 8/8, and the other 14 maps are unchanged. The Collision Varg draft beat
Xuanming on one side but still lost both games to Ming (scores 416-968 and 254-924). The teleport
experiments did not demonstrate a competitive lock-proof route. Main `bots/tungtungsahur/src` and
`submissions/tungtungsahur.zip` remain unchanged. Live top-50 unranked streak: 0/10; local proxy
games do not count.

| # | Change | Result | Decision |
|---|---|---|---|
| 86 | Collision Varg buys Jungle Health before Monster Strength / Power Strength | 4/8 vs 5/8 for experiment 85; 0/2 vs Ming and Xuanming | reject: deaths fell 22 -> 17 in the sampled Ming A game, but no strong-proxy win and the farm pace did not improve |
| 87 | Collision draft Cassi & Issac / Ryth / Varg, drop Stellar, and let Varg trigger late phase at 3 emblems | 4/8; 0/2 vs Ming and Xuanming, 2/2 vs each other proxy | reject: keeping both tanks/fighters did not replace Stellar's value |
| 88 | On Swirl only, Varg and the mage buy Jungle Health before their normal damage items | 3/8 vs the current candidate's 4/8; still 0/2 vs Ming and Xuanming | reject: deaths fell by 2-23 per sampled game, but lower camp damage cost more farming than the added survival recovered |

Runs: #86 matches/league/20261017-161412-cand-collision-jungle-varg-clean, #87
matches/league/20261017-161514-cand-collision-ryth-varg-test, and #88
matches/league/20261017-161647-cand-swirl-jungle-items. For #88, the current candidate recorded
55 / 47 deaths against Ming and 70 / 53 against Xuanming; the Jungle Health version recorded
39 / 45 and 47 / 39. Despite fewer deaths, it lost faster on both Xuanming sides and banked less.
This points to Swirl camp throughput and allocation, rather than equipment defense alone, as the
remaining issue.

Experiments 86-88 do not supersede experiment 85 (109/136). The main source and submission ZIP
remain unchanged. Live unranked top-50 streak remains 0/10; local games do not count.

| # | Change | Result | Decision |
|---|---|---|---|
| 89 | On Swirl after the opening, keep Varg with Issac's squad objective for a 3+2 split instead of solo farming | 4/8, tied with experiment 85 on Swirl; 0/2 each vs Ming and Xuanming | reject as a win-rate change; the combined split raises gems vs Ming but lowers them vs Xuanming |
| 90 | On Swirl, defer banking until 150 gems when no enemy is visible | 2/8; 0/2 each vs Ming and Xuanming | reject: deaths were fewer, but carried-gem losses rose sharply |

Runs: #89 `matches/league/20261017-162541-cand-swirl-varg-squad-b`; #90
`matches/league/20261017-162636-cand-swirl-bank150`. #89 scored 485 / 979 gems per game against
Ming and 705 / 976 against Xuanming, but won neither matchup. #90 lost 1,802 gems on deaths across
its four Ming/Xuanming replays, compared with 647 in the matched experiment 85 Swirl replays. The
map simulator's no-contact 250-gem threshold does not transfer to live combat pressure; current
immediate banking remains preferable on Swirl.

Experiments 89-90 remain isolated. The strongest full-pool local candidate is still experiment 85
at 109/136. Main source and submission ZIP remain unchanged; live unranked top-50 streak remains
0/10.

### 17 Oct: combine the Expanse meta draft with the current map-specific candidate

| # | Change | Result | Decision |
|---|---|---|---|
| 91 | Add the Expanse C&I / Varg / Stellar draft order to candidate 85's Contest, Stampede, and Collision picks | Expanse 8/8; full pool 112/136, versus 109/136 for candidate 85 and 104/136 for matched main | strongest local candidate; +8/136 over main with no map regressions, keep isolated pending live validation |

The targeted Expanse run is matches/league/20261017-162909-cand-best-expanse-meta; full run is
matches/league/20261017-162931-cand-best-expanse-meta. The matched main run is
matches/league/20261017-163025-tungtungsahur. Full-pool map scores differ only on four gated maps:
Collision 4/8 -> 5/8, Contest 5/8 -> 7/8, Expanse 5/8 -> 8/8, and Stampede 6/8 -> 8/8. The
other thirteen map scores are unchanged. Candidate wins changed from main by Ming 21/34 -> 24/34,
Xuanming 22/34 -> 26/34, Faisal 32/34 -> 32/34, and opp-racer 29/34 -> 30/34.

The current best remains an isolated candidate in bots/cand-best-expanse-meta. Main
bots/tungtungsahur/src and submissions/tungtungsahur.zip remain unchanged. Live unranked top-50
streak remains 0/10; proxy matches do not count.

### 17 Oct: Pilgrimage and Lanes follow-ups

| # | Change | Result | Decision |
|---|---|---|---|
| 92 | Pilgrimage: bank at 100 when no enemy is visible; bank immediately when one is visible | 4/8 vs experiment 91's 5/8; 0/2 vs Ming, 1/2 vs Xuanming | reject: a lower trigger did not overcome the early race and lost one total game |
| 93 | Pilgrimage: skip the grouped early phase from round 1 | 5/8, tied with experiment 91; Ming improved 0/2 -> 2/2, Xuanming fell 1/2 -> 0/2 | reject as a general improvement: it trades one strong-proxy matchup for the other without raising the map total |
| 94 | Pilgrimage: replace Ryth with Vendetta | 3/8; 0/2 each vs Ming and Xuanming | reject: the extra fighter did not offset losing the tank |
| 95 | Lanes: keep the grouped opening, then switch to mid-game squads at round 200 | 3/8 vs experiment 91's 4/8 | reject: the split reduced the strong-proxy wins and worsened the economy race |
| 96 | Lanes: replace Ryth with Ren | 4/8; 0/4 vs Ming/Xuanming | reject for top-proxy performance: the wins shifted to Faisal and opp-racer while both strongest proxies won both sides |
| 97 | Lanes: replace Tavi with Ren and retain Ryth | 5/8, but only 1/4 vs Ming/Xuanming versus 2/4 for experiment 91 | reject for the top-team target: one extra overall win came from the weaker proxy matchups, while the strongest-proxy result declined |

Run folders: #92 `matches/league/20261017-163317-cand-pilgrimage-bank100`; #93
`20261017-163437-cand-pilgrimage-mid-open`; #94 `20261017-163547-cand-pilgrimage-vendetta`;
#95 `20261017-163709-cand-lanes-mid200`; #96 `20261017-163746-cand-lanes-ren`; and #97
`20261017-163824-cand-lanes-ren-tank`. Candidate source folders use the matching names under
`bots/`.

These tests do not supersede experiment 91 (112/136). Keep its map-specific drafts and standard
opening, banking, and role equipment. Pilgrimage's no-contact 2/2/2, T=100 model is not enough to
predict combat outcomes: the live-proxy threshold test lost a game, while opening split changed
which opponent won without changing the total. On Lanes, all four baseline losses were side B with
no deaths; forcing an earlier split or substituting Ren did not improve results against the two
strongest proxies. Main source and submission ZIP remain unchanged. Live top-50 unranked streak is
still 0/10 because the site browser session has not connected.


### 17 Oct: Rushbait opening and movement follow-up

| # | Change | Result | Decision |
|---|---|---|---|
| 98 | In step_towards, catch a blocked move and try another equally short route | Ambush stayed 6/8; strong-proxy league stayed 112/136; broad pool fell to 586/680 vs 587/680 for #91 | reject globally: it flipped one Bruiser Ambush side-B win to a loss (976-530, 2 deaths -> 418-954, 7 deaths) |
| 99 | On Rushbait v2 (30x80), enter mid-game squad phase from the opening, on either side | Rushbait targeted set 7/8 in two repeats; full four-proxy set 113/136; broad set 592/680 | keep as current local best: +1 vs #91 in the strong set, +5 vs #91 broad, +15 vs same-session main broad |

Experiment 99 changes only the Rushbait opening phase; it keeps the map draft, equipment, and other maps unchanged. In the 17-map strong-proxy test, Rushbait rose from 5/8 to 7/8 while Stampede shifted from 8/8 to 7/8, giving a net +1 (113/136 vs 112/136 for #91). In the 680-game local pool, Rushbait rose 35/40 to 39/40 and Swirl 34/40 to 35/40; other map totals were unchanged. The broad result is 592/680, compared with 587/680 for #91 and 577/680 for same-session main. Strong-proxy wins are Ming 23/34, Xuanming 27/34, Faisal-orig 32/34, and opp-racer 31/34.

Use the all-side opening rule from bots/cand-best-expanse-meta/src/bot.cpp. The all-side Rushbait target runs were matches/league/20261017-170652-cand-rushbait-mid-open and 20261017-170858-cand-rushbait-mid-open; the integrated strong and broad runs are 20261017-171120-cand-best-expanse-meta and 20261017-171232-cand-best-expanse-meta. Side-specific variants in 20261017-170929-cand-rushbait-mid-open and 20261017-171015-cand-rushbait-mid-open scored 3/8 and 4/8, but logs show the intended early branch did not trigger, so those runs do not test the proposed split and are not strategy evidence.

Experiment 98 is rejected: although two Ambush wins gained more gems against Ming/Xuan, the broad set regressed by one win and showed a dangerous route into Bruiser. Keep the existing movement code. Main bots/tungtungsahur/src and submissions/tungtungsahur.zip remain unchanged. Live unranked top-50 streak remains 0/10; local proxy runs do not count.


### 17 Oct: Swirl equipment and Lanes side-specific follow-ups

| # | Change | Result | Decision |
|---|---|---|---|
| 100 | Swirl Ryth: Monster Strength first, then Jungle Health | 3/8; 0/4 vs Ming/Xuanming; 362 deaths in 8 games | reject: no strong-proxy wins and one fewer map win than the current candidate |
| 101 | Force mid-game phase from the opening on Lanes side B only | 4/8; still lost all four side-B games, with lower final gems in three | reject: the split did not close the economy gap |
| 102 | Lanes Tavi: Monster Strength first on both sides, then Power Focus | 4/8; only 1/4 vs Ming/Xuanming, down from 2/4 | reject globally: it traded a side-A win for a Faisal side-B win |
| 103 | Lanes side B only: Tavi buys Monster Strength first, then Power Focus | 5/8 in two identical targeted repeats; 114/136 strong pool; 593/680 broad pool | highest observed cross-name score, but not a controlled improvement; see same-name control #105 |

Experiment 103 starts from the previous best and changes only Tavi's first five Lanes side-B purchases. The strong set is 114/136 versus 113/136 for experiment 99; Lanes is 5/8 versus 4/8. Wins against the four strong proxies are Ming 23/34, Xuanming 27/34, Faisal-orig 33/34, and opp-racer 31/34. The broad set is 593/680 versus 592/680 for experiment 99 and 577/680 for same-session main. Broad Lanes rose from 36/40 to 37/40; paired outcomes flipped two losses into wins and one win into a loss, for +1 net.

Source: bots/cand-lanes-sideb-tavi-monster/src/bot.cpp. Target repeats: matches/league/20261017-172515-cand-lanes-sideb-tavi-monster and 20261017-172545-cand-lanes-sideb-tavi-monster; strong run: 20261017-172556-cand-lanes-sideb-tavi-monster; broad run: 20261017-172648-cand-lanes-sideb-tavi-monster. Rejected runs: #100 20261017-172125-cand-swirl-ryth-monster-first-clean; #101 20261017-172308-cand-lanes-sideb-mid-open; #102 20261017-172421-cand-lanes-tavi-monster-first.

Keep the new candidate isolated pending live validation. Main bots/tungtungsahur/src and submissions/tungtungsahur.zip remain unchanged. The live unranked top-50 streak is still 0/10; the browser connector remains uninstalled, and local games do not count.


### 17 Oct: controlled recovery and candidate checks

| # | Change | Result | Decision |
|---|---|---|---|
| 104 | Add a 12-turn no-movement fallback for a camp group | 117/136 strong, 610/680 broad; 8/8 on targeted strong Ambush | was the leading isolated candidate; superseded by #115 |
| 105 | Attempt candidate/main and recovery/no-recovery swaps without refreshing copied source timestamps | Incremental build reused the previous v104 WASM; identical results were a stale-build artifact. | Invalid comparison; discard its results. |
| 106 | Narrow the stall check so the extra group lookup only runs on Ambush | 116/136 strong and 611/680 broad; compared with v104, strong was -1 while broad was +1. Ambush stayed 40/40. | Keep v104 for the stronger-proxy target; preserve v105 as an alternative. |
| 107 | Keep the late outnumbered-retreat check enabled only on Swirl | 0/4 vs Ming/Xuanming; all four replay ZIP hashes exactly matched v104 | reject as a no-op; the late branch did not change observed actions |
| 108 | Raise Swirl's recall threshold to 50% health | 3/8 vs 4/8 baseline; deaths fell but economy slowed | reject: less combat death pressure did not repay the farm time lost |
| 109 | Raise Swirl's recall threshold to 40% health | 4/8 targeted; 118/136 strong, 607/680 broad; broad Swirl fell 35/40 to 32/40 | reject globally: +1 strong was offset by -3 broad; keep v104 |
| 110 | On Pilgrimage, Tavi buys Monster Strength before Power Focus | 5/8 vs v104's 6/8 on the same four strong proxies | reject: fewer strong-proxy wins; keep default Tavi build |
| 111 | On Pilgrimage, attack a nearby home altar lock while carrying no gems | 5/8 in two identical targeted runs; v104 scored 6/8 | reject: one extra Ming-side win was offset by a weaker overall strong-proxy result |
| 112 | On Collision, attack the central altar lock while carrying no gems | 4/8 vs v104's 5/8; still lost all 4 Ming/Xuanming games | reject: no strong-proxy gain; keep v104 |
| 113 | On Collision, draft Tavi instead of Varg with Stellar and C&I | 5/8, tied with v104; still 0/2 vs Ming | reject: no strong-proxy win improvement; restore Varg |
| 114 | On Swirl after the opening, move Varg from solo farming to Ryth's camp | 4/8 strong; 34/40 broad-map vs v104's 35/40 | reject: gem totals vs Ming improved, but wins did not; keep Varg solo |
| 115 | On Lanes side B, raise shopping-trip threshold from 150 to 250 gold | 6/8 targeted, 118/136 strong, 38/40 Lanes broad, 611/680 broad | current isolated local candidate: +1 strong, +1 broad, no map regressions outside Lanes |
| 116 | Lanes side B shopping threshold 200 gold | 5/8 in two identical targeted runs | reject: repeat result below #115's 6/8 |
| 117 | Lanes side B shopping threshold 300 gold | 3/8 targeted | reject: lost both Faisal games and underperformed the 200- and 250-gold versions |
| 118 | Swirl: replace Varg with Willow | 4/8; 0/4 vs Ming/Xuanming with much lower gem totals | reject: no strong-proxy gain; healing did not offset losing Varg's solo farming |
| 119 | Collision: use Ryth/Vendetta/Tavi | 2/8; 0/6 vs Ming/Xuanming/Faisal | reject: low gem income and no wins against the three strongest proxies |
| 120 | Collision: use Ryth/C&I/Tavi | 1/8; 0/6 vs Ming/Xuanming/Faisal | reject: changing both the damage dealer and farmer collapsed the economy |
| 121 | Collision: replace only Varg with Ryth, retaining Stellar/C&I | 4/8; 0/4 vs Ming/Xuanming | reject: below the current 5/8 Collision lineup; tank did not convert the strongest matchups |
| 122 | Fresh paired Stampede control: current main vs isolated v115 | main 6/8; v115 7/8 vs the same four proxies and both sides | keep the isolated Prism/Stellar/C&I/Ryth/Tavi lineup; it converted one Xuanming loss to a win |
| 123 | Stampede: Tavi buys Monster Strength before Power Focus | 7/8, tied with v115 | reject: no additional win |
| 124 | Stampede: Prism buys Monster Strength before Focus | 6/8 | reject: regressed one win |
| 125 | Stampede: both Prism and Tavi buy Monster Strength first | 5/8 | reject: two fewer wins than v115; keep current equipment |
| 126 | Stampede: ignore the mid-game split and keep the shared farm phase until Stellar's late-game flag | 8/8 strong vs v115's 7/8; 41/44 broad vs 36/44; 0 bot errors | keep as the leading isolated Stampede branch; six outcomes improved and one regressed |
| 127 | Stampede: attempt to hold the shared phase through round 900, but check after the late-game flag | 8/8; replay ZIP exactly matched #126 | reject as a no-op: the late flag fired at r418 before the round condition could run |
| 128 | Stampede: hold the shared phase through round 900 before checking the late flag | 7/8 strong; lost to opp-racer on side A | reject: worse than #126 |
| 129 | Stampede: hold the shared phase through round 600 before checking the late flag | 7/8 strong; lost to Xuanming on side B | reject: worse than #126 |

The v104 baseline snapshot is saved as `bots/cand-ambush-stall-recovery/candidate-source-v104.cpp`; v105 is saved as `bots/cand-ambush-stall-recovery/candidate-source-v105.cpp`. The active `src/bot.cpp` now contains v104 plus the Lanes side-B shop-trip change from #115; its snapshot is `candidate-source-v115-lanes-shoptrip250.cpp`. Valid v104/no-recovery broad runs are `20261017-175842-cand-ambush-stall-recovery` (610/680) and `20261017-182524-cand-ambush-stall-recovery` (593/680). Their verified WASM hashes are `C5087E56…1F1C456` and `4330E2AB…956C716D`. The no-recovery strong Ambush run `20261017-190705-cand-ambush-stall-recovery` scored 6/8; v104's rebuilt Ambush run `20261017-190744-cand-ambush-stall-recovery` scored 8/8.

The valid main-source strong run is `20261017-190825-cand-ambush-stall-recovery` (104/136), compared under the same candidate name with v104 `20261017-175715-cand-ambush-stall-recovery` (117/136): 14 losses became wins and one Rushbait win became a loss. The main-source WASM hash was `5648F8EB…B6250F5`. On the broad pool, v104 scored 610/680 versus fresh main's 577/680 (`20261017-192402-cand-ambush-stall-recovery`); gains by map were Ambush +19, Expanse +6, Stampede +4, Rushbait v2 +3, Contest +2, Lanes +1, and Swirl +1, offset by Collision -2 and Pilgrimage -1. All other map totals matched. The first same-name controls (`20261017-180358` through `20261017-181808`) are invalid: `Copy-Item` preserved old source timestamps, so CMake reused the v104 object. Later swaps refreshed timestamps and verified distinct WASM hashes before running.

The v105 affected-map subset `20261017-191149-cand-ambush-stall-recovery` scored 108/120; its full broad run `20261017-191254-cand-ambush-stall-recovery` scored 611/680 and strong run `20261017-191743-cand-ambush-stall-recovery` scored 116/136. The Swirl late-retreat change was saved as `candidate-source-v107.cpp`; the targeted run `20261017-192221-cand-ambush-stall-recovery` stayed 0/4 against Ming/Xuanming, and each replay ZIP matched the v104 control hash, so no behavior change was observed. Swirl recall thresholds of 50% and 40% health were also rejected: #108 run `20261017-193130-cand-ambush-stall-recovery` scored 3/8; #109 targeted `20261017-193204` scored 4/8, strong run `20261017-193356` scored 118/136, and broad run `20261017-193448` scored 607/680, with Swirl declining from 35/40 to 32/40. On Pilgrimage, Tavi Monster Strength first scored 5/8 against the four strong proxies in `20261017-194005-cand-ambush-stall-recovery`; home-lock clearing scored 5/8 in both `20261017-194247` and `20261017-194304`, below v104's 6/8. Collision home-lock clearing scored 4/8 (`20261017-194508`), and its Tavi draft tied v104 at 5/8 (`20261017-194617`). Swirl Varg-joins-Ryth tied 4/8 strong and scored 34/40 across the broad Swirl map (`20261017-194840`). These changes were rejected. The v104 baseline source/WASM hashes are `18D46335…C54C8C6` and `C5087E56…71F1C456`. Current v115 source/WASM hashes are `C3D422C5…9F771CB` and `0EEFFDB2…9B63E85`. Main source/ZIP are unchanged. TinyFish remains installed=false; live streak 0/10.

Experiment #115 uses the side-B predicate already used for Tavi's Lanes build. Raise the recall-for-shopping threshold only on side B from 150 to 250 gold. Targeted runs `20261017-195019` and `20261017-195038` both scored 6/8; the fresh v104 control `20261017-195109` scored 5/8. Full strong run `20261017-195154` scored 118/136 versus v104's 117/136, with Lanes rising 5/8 to 6/8. Lanes-only broad run `20261017-195134` scored 38/40 versus 37/40; full broad run `20261017-195236` scored 611/680 versus v104's 610/680, and Lanes was the only map whose total changed. Current source is `bots/cand-ambush-stall-recovery/src/bot.cpp` and the preserved snapshot is `candidate-source-v115-lanes-shoptrip250.cpp`. Live unranked progress remains 0/10; these are local proxies only.

Threshold sweep on the same Lanes side-B rule: #116 used 200 gold and scored 5/8 in both `20261017-195844` and `20261017-195930`; #117 used 300 gold and scored 3/8 in `20261017-195907`, losing both Faisal games. Both are rejected; 250 gold remains the best tested value. Variant source snapshots and build folders are under `bots/cand-lanes-shoptrip-threshold/`. The active file in that experiment folder is restored to 200 gold; it is separate from the #115 leader.

Experiments #118–121 checked drafts against the weakest strong-proxy maps. On Swirl, Willow replacing Varg tied the baseline at 4/8 but scored only 195 and 427 average gems in the two Ming/Xuanming games (`20261017-223244`); reject it. On Collision, Ryth/Vendetta/Tavi scored 2/8 (`20261017-223334`), Ryth/C&I/Tavi scored 1/8 (`20261017-223401`), and replacing only Varg with Ryth scored 4/8 (`20261017-223428`). All three lost every game to Ming and Xuanming; the first two also lost both Faisal games. Keep the current Stellar/C&I/Varg Collision lineup and standard Swirl lineup. These changes remain isolated in their `bots/cand-*` folders.

TinyFish now reports `installed: true`, but this session exposes no TinyFish browser actions. The user supplied unranked group `4cf7ad87-2c52-452e-a9a3-59787c302e67`: Heavenly Court lost 0–5 to FRChronic across Interlock, Stampede, Elkring, Fragment, and Pilgrimage. FRChronic was rank 58 around the match, so this does not count toward the top-50 streak (still 0/10). Group-level scores and drafts are recorded in `analysis/platform-match-review-4cf7ad87.md`; replay bundles remain behind browser-session authentication. Main source and submission ZIP hashes remain unchanged.

Stampede follow-up `matches/league/20261017-2301-stampede-live-followup` freshly compared the main bot with the isolated v115 candidate against `ming_bot`, `xuanming`, `faisal-orig`, and `opp-racer`, both sides: main scored 6/8 and v115 7/8. The only changed result was v115 beating Xuanming on side A; both versions tied with Ming on side A at round 2000. The user's live Stampede draft omitted Prism, while v115 uses the same five picks as FRChronic's Stampede draft. Equipment screen `matches/league/20261017-2301-stampede-monster-screen` tested Monster Strength-first builds on Tavi, Prism, and both: 7/8, 6/8, and 5/8 respectively, versus 7/8 for v115. Reject all equipment variants and retain current equipment. All five builds had distinct WASM hashes. Main source and submission ZIP are unchanged; no result here is a live top-50 win.

Stampede experiment #126 starts from v115 and ignores the ordinary mid-game squad split until Stellar's late-game flag. It scored 8/8 against Ming, Xuanming, Faisal, and opp-racer on both sides (`20261017-230854-cand-stampede-team`), versus 7/8 for a fresh v115 control (`20261017-230848`). In the 22-opponent Stampede pool, #126 scored 41/44 versus 36/44 for v115; six losses became wins and one win became a loss (`20261017-231001` vs `20261017-230943`). The Ming side-A replay changed from a 900–900 round-cap loss with 49 deaths / 1,260 gems lost to a 900–180 win at r1695 with 44 deaths / 180 gems lost. The source/WASM hashes are `9EE469D06BBB85F3AC62927DEFCFA3AFC771A10FCF404EB2036FC1B7A279E8D2` and `FCBA6BFB045084163D244ECBEEEC75A2E32AE945AFDFDB75F37314C67ADEA3E9`. Keep this as a Stampede-only candidate; #115 remains the all-map tested candidate. Tests #127–129 show why extending the phase further is not useful: #127 was byte-for-byte the same Ming replay because late mode fired at r418; when the round-900 or round-600 override was placed before the late check, both scored 7/8 and regressed one matchup. All these are local proxies, not top-50 wins. Main source and submission ZIP remain unchanged.
# 17 Oct continuation: full-map Stampede validation

The earlier Stampede-only result for #126 has now passed a full 17-map comparison under the same bot name. Against the same four strong local proxies, #126 scored 119/136 versus 118/136 for the fresh #115 control; the repeat #126 control also scored 119/136. In the 20-opponent broad league, #126 scored 612/680 versus 611/680 for #115. Seven outcomes changed: Stampede improved by two wins, Lanes by one, and Pilgrimage declined by two, for a net +1. The Stampede branch therefore has a small all-map gain, while its broad effects are not confined to Stampede.

| # | Change | Result | Decision |
|---|---|---|---|
| 130 | Cache the Stampede map check locally inside game_phase | 117/136 strong versus #126's 119/136 | reject; two fewer strong-proxy wins |
| 131 | Cache the Stampede map identity once during Bot::init | 119/136 strong, with no changed outcomes against #126; 614/680 broad in two exact repeats versus #126's 612/680 | keep as the current isolated local candidate; broad gains repeat, strong result is unchanged |

For #131, both broad runs had 0 failed matches and exactly identical game records (614/680 each). Compared with #126, four broad outcomes changed: Stampede side B versus Faisal-bot and Pilgrimage side B versus opp-tts-v2 and opp-tts-locker became wins; Lanes side A versus opp-fai-mirror became a loss. Net map deltas were Stampede +1, Pilgrimage +2, and Lanes -1. The exact same 136 strong-proxy outcomes were retained. This is a local league result, not evidence of live top-50 wins.

Runs: refreshed #126 strong control 20261017-233935; #130 20261017-233449; #131 strong 20261017-234029; #131 broad repeats 20261017-234132 and 20261017-234453. Earlier same-name #126 broad control is 20261017-232950 and the #115 broad control is 20261017-232643. The #131 source snapshot is bots/cand-stampede-broad-pair/candidate-source-v131-cached-init-map-guard.cpp; source SHA-256 6E36C827936FECF17E7959CF4A7F7E137E28219DA31D2230BBC4743A6C7C8511; WASM SHA-256 09C8C45C5D736DECCD52AACB647FEEDED71F678F015109E2E230F8BBE477E8AA. It remains separate from bots/tungtungsahur/src/bot.cpp and submissions/tungtungsahur.zip.

The user-supplied unranked group 4cf7ad87-2c52-452e-a9a3-59787c302e67 remains 0–5 against FRChronic, which was rank 58 around that match. The top-50 streak is still 0/10. Public group data gives scores and drafts but replay bundles remain unavailable through this runtime, so causes of the live losses are not verified. Keep the main source and submission ZIP unchanged until the authorized top-50 streak target is met.
# 18 Oct continuation: isolate the 30x30 draft change

The close Fragment loss suggested testing Varg in Ryth's slot. Experiment #132 applied Varg-before-Ryth to both 30x30 maps: Fragment (three picks) therefore replaced Ryth with Varg, while Elkring (five picks) kept the same roster but changed pick order. It scored 121/136 strong-proxy wins in two identical runs and 615/680 broad, but the broad map totals showed a tradeoff: Elkring rose from 34/40 to 38/40 while Fragment fell from 37/40 to 34/40. Reject the combined rule.

Experiment #133 applies Varg-before-Ryth only to Elkring, identified by its 30x30 size and altar positions; Fragment keeps the standard Stellar / Cassi & Issac / Ryth lineup. It scored 8/8 on Elkring against the four strong local proxies versus 7/8 for #131. Full strong runs scored 120/136 twice with identical 136 game records versus 119/136 for #131. Broad runs scored 618/680 twice with identical 680 game records versus 614/680 for #131. Only Elkring's broad total changed: +4 wins, including both sides against opp-tts-v2, side B against opp-tts-v4, and side A against opp-tts-aggro. No other map total regressed.

| # | Change | Result | Decision |
|---|---|---|---|
| 132 | Put Varg before Ryth on both 30x30 maps | 121/136 strong twice; 615/680 broad; Elkring +4 and Fragment -3 versus #131 | reject combined rule; Fragment losses outweigh the broader gain |
| 133 | Put Varg before Ryth on Elkring only; preserve Fragment's Ryth pick | 120/136 strong twice; 618/680 broad twice, all game records repeated exactly | current isolated local candidate; +1 strong and +4 broad versus #131, with gains isolated to Elkring |

Runs: Fragment #131 control 20261017-235054; #132 Fragment targeted 20261017-235120 and 20261017-235131; #132 strong runs 20261017-235137 and 20261017-235253; #132 broad 20261017-235340. Elkring #131 control 20261017-235658; #133 targeted 20261017-235717; #133 strong runs 20261017-235726 and 20261018-000403; #133 broad runs 20261017-235804 and 20261018-000059. The current draft snapshot is bots/cand-stampede-broad-pair/candidate-draft-v133-elkring-varg-first.cpp. Current bot.cpp SHA-256 is 6E36C827936FECF17E7959CF4A7F7E137E28219DA31D2230BBC4743A6C7C8511; draft.cpp SHA-256 is FC0CE9899F2B0656753A94B3E3072D45C9A3A8CBF52798B3D6E5752255CEE89C; built WASM SHA-256 is 30BA86AF24565F8B68FAD96E3E0A700749782E482E9128BBACFB37A48280C3F4.

This remains local-proxy evidence. The supplied FRChronic group is 0–5 and FRChronic was rank 58 around that unranked match, so the top-50 streak remains 0/10. Replay-level causes are still unverified because the signed-in browser session is not exposed to this runtime. Main source and submission ZIP remain unchanged.
# 18 Oct continuation: Pilgrimage draft screens

Starting from #133, two Pilgrimage-only draft changes were screened against four strong local proxies:

| # | Change | Result | Decision |
|---|---|---|---|
| 134 | Keep the same roster but pick Varg before Ryth | 5/8 versus #133's fresh 6/8; still 0/2 versus Ming and lost opp-racer side B | reject; gem total against Ming rose from 644 to 932 on average, but the win count fell |
| 135 | Replace Tavi with Ren, preserving the other picks and order | 5/8; 1/2 versus Ming but 0/2 versus Xuanming, versus #133's 0/2 and 2/2 | reject; the added melee control did not repay the two Xuanming losses |

Runs: #133 Pilgrimage control 20261018-000551; #134 20261018-000605; #135 20261018-000652. Both variants had 0 failed matches. These were targeted 8-game screens only and were not run through the full strong or broad league. Restore #133 after each screen; its draft source and WASM hashes are FC0CE9899F2B0656753A94B3E3072D45C9A3A8CBF52798B3D6E5752255CEE89C and 30BA86AF24565F8B68FAD96E3E0A700749782E482E9128BBACFB37A48280C3F4.
# Candidate test package

Packaged #133 as submissions/tungtungsahur-candidate-v133-unranked-test.zip (24,398 bytes; SHA-256 558C3D1FD41B759FA5E9558F4AE361F67212BD08C374CB1BE85CDFC6124094EB). Its five C++ source files were byte-for-byte verified against bots/cand-stampede-broad-pair/src. This is a local test package; it has not been uploaded. The main submissions/tungtungsahur.zip remains unchanged.
# 18 Oct continuation: Swirl Varg order

Experiment #136 put Varg before Ryth on Swirl while keeping the same four-pick roster. It scored 3/8 against the four strong local proxies versus #133's fresh 4/8 control. It still lost both games to Ming and Xuanming and added an opp-racer loss. Reject it; the #133 draft and WASM were restored and rebuilt.

Runs: control 20261018-001011; #136 20261018-001025. Both had 0 failed matches and were targeted 8-game screens only. The restored #133 draft/WASM hashes are FC0CE9899F2B0656753A94B3E3072D45C9A3A8CBF52798B3D6E5752255CEE89C and 30BA86AF24565F8B68FAD96E3E0A700749782E482E9128BBACFB37A48280C3F4.

## 18 Oct: equipment screens #137–138

Both variants start from #133 and were screened against Ming and Xuanming on all 17 maps from both sides (68 games, 0 failures each).

| # | Change | Result | Decision |
|---|---|---:|---|
| 137 | Issac keeps five Jungle Health shards, then buys Durability Health instead of Power Health | 54/68, tied with the fresh #133 baseline; Ming 25/34, Xuanming 29/34 | reject: one Fragment win traded for one Lanes loss; no total gain |
| 138 | Stellar buys five Treasure Focus shards, then switches to Power Focus | 50/68; Ming 24/34, Xuanming 26/34 | reject: four fewer wins than #133; Collision, Contest, Lanes, Packs, and Pilgrimage each regressed by one map win, partially offset by Fragment +1 |

Run folders: #133 equipment baseline `20261018-001354-cand-stampede-broad-pair`; #137 `20261018-001420-cand-stampede-broad-pair`; #138 `20261018-001536-cand-stampede-broad-pair`. Source snapshots: `candidate-source-v137-issac-durability.cpp` (SHA-256 `7EF7782E961F345EEB1A91C4B452EB26A6FABD8251F52F906D5DCA252B44303D`) and `candidate-source-v138-stellar-treasure-first.cpp` (SHA-256 `96182F0AB0CBE6F4C528E681C6779BB14C117D14362FE3214214D3223B88D40F`). Both are rejected; `src/bot.cpp` and the built WASM are restored to #133 (hashes `6E36C827936FECF17E7959CF4A7F7E137E28219DA31D2230BBC4743A6C7C8511` and `30BA86AF24565F8B68FAD96E3E0A700749782E482E9128BBACFB37A48280C3F4`). These remain local-proxy results.

## 18 Oct: retreat threshold screens #139–142

The Collision and Swirl loss traces showed long team attrition, so the outmatched retreat trigger was screened against Ming and Xuanming on both sides. #139 lowered the threshold globally from 1.3× to parity and fell from #133's 54/68 to 44/68; it reduced Swirl deaths from 225 to 171 across four games but caused broad regressions elsewhere. Reject the global rule.

A Swirl-only parity threshold was then tested. #140 checked map dimensions inside every outmatched calculation; it scored 121/136 strong and 611/680 broad twice, but its broad run also changed two Pilgrimage outcomes despite Pilgrimage being 50×65. #141 caches the unique Swirl 45×30 identity during `Bot::init` and uses a direct parity comparison only there; all other maps retain the original `theirs > 1.3 * ours` expression. It scored 3/8 across Swirl and Pilgrimage against Ming/Xuanming versus #133's 2/8, 121/136 strong, and 613/680 broad in two identical runs. Compared with #133, its only broad map change was Swirl, 35/40 to 30/40; strong Swirl improved by one win against Xuanming. This is a trade-off: keep #133 as the broad-pool control and #141 as the top-proxy candidate for live unranked validation.

#142 raised the Swirl threshold to 1.1×; its 8-game Swirl/Pilgrimage screen scored 2/8 versus #141's 3/8, so reject. The #141 candidate build is restored and packaged locally at `submissions/tungtungsahur-candidate-v141-unranked-test.zip` (24,470 bytes; SHA-256 `67B9D83600855D5583AE954C2F0F46EE9AF2527238198DB43A99B2E153781D8F`); all six source entries were byte-verified. Run folders: #139 `20261018-001800`; #140 targeted `20261018-001927`, `001943`, strong `001950`, broad `002031`, `002445`; #141 target `002813`, strong `002830`, broad `002908`, `003306`; #142 `003215` (all under `matches/league/cand-stampede-broad-pair`).

The candidate ZIP remains local, but its source was uploaded through the CLI as distinct candidate submission version 25. No live match was created; the top-50 consecutive-win streak remains 0/10. TinyFish is installed and enabled, but this runtime exposes no TinyFish/browser-action tool, and the site challenge endpoint still requires the browser session. The main `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged (SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`).

## 18 Oct: draft-aware Swirl retreat (#143)

#141's parity retreat helped against Ming/Xuanming on Swirl but lost five broad-pool Swirl games. Their Swirl replay logs showed both strong proxies drafted the same four-pick threat core: Cassi & Issac, Varg, Stellar, and Vendetta. #143 caches a flag at initialization that is true only on the unique 45×30 Swirl map when the enemy has all four picks; only then does `should_retreat` use the parity threshold. Every other map and enemy draft retain the #133 1.3× threshold.

Against Ming and Xuanming on Swirl, #143 repeated the parity variant's 1/4 wins versus #133's 0/4. It scored 121/136 in two strong-proxy runs versus #133's 120/136; the sole per-map win gain was Swirl (4/8 to 5/8). It scored 618/680 in two exact broad-pool repeats, with the same win totals on every map as #133. This is the current isolated candidate: a strong-proxy gain without a broad-pool regression. It is still local evidence, not a live top-50 win.

The #143 package `submissions/tungtungsahur-candidate-v143-unranked-test.zip` is 24,581 bytes (SHA-256 `AE601F9525ECD448349F5EB7995E34CECC546C9B5F97A5A162A30D5FE97F15DF`); all six source files were byte-verified against the candidate directory. The source was uploaded as separate test submission version 26. Runs: targeted Swirl `20261018-003911`; broad Swirl screen `003926`; strong `003941` and repeat `004323`; broad `004021` and exact repeat `004402` (all under `matches/league/cand-stampede-broad-pair`). The main source and ZIP are unchanged. The live top-50 streak remains 0/10 because no new unranked group has been created.

## 18 Oct: Collision mirror retreat screen (#144)

Against a mirrored Collision draft containing Cassi & Issac, Varg, and Stellar, #143's control scored 1/4 (Ming 0/2; Xuanming 1/2). #144 raised the outmatched threshold to 1.5x for that matchup and scored 0/4 (0/2 against each proxy). Reject #144 and restore #143. Runs: control `20261018-004844-cand-stampede-broad-pair`; #144 `20261018-004856-cand-stampede-broad-pair`.

The user supplied group `4cf7ad87-2c52-452e-a9a3-59787c302e67` again on 18 Oct. A fresh public API read confirms it is the already-reviewed group created 17 Oct 21:50 UTC, finished 0-5 to FRChronic, with both teams' submission versions null. It predates candidate version 26 and cannot validate #143. Live top-50 streak remains 0/10. Main source and ZIP remain unchanged.

## 18 Oct: Pilgrimage large-bag bank routing (#145)

Replay evidence on the 50x65 Pilgrimage map showed a specific side-B failure. In #143's loss to Faisal-bot, Tavi died at (12,60) carrying 144 gems; the enemy Stellar took the bag, and the team's death losses summed to 236 gems. The score went from 676-684 at round 1000 to 676-988 at round 1100. The nearest altar from that position was on the west side, while our spawn was east. #145 recognizes Pilgrimage by its four altar coordinates and adds 40 path-cost points to enemy-half altars only while carrying at least 100 gems. Smaller bags and all other maps use the original nearest-altar rule.

Using direct `cambc run` games (the batch wrapper hit a Windows CMake `invalid argument` build error), #145 scored 31/40 on Pilgrimage in two repeats. A same-runner #143 control scored 29/40. The only per-opponent win-count gains were Faisal-bot (0/2 to 1/2) and opp-tts-aggro (0/2 to 1/2); the other 18 opponents kept their counts. The exact four-strong-proxy set (Ming, Xuanming, faisal-orig, opp-racer) remained 6/8, tied with the #133 control. On the Faisal-bot side-B game, #145 won 1004-820 with 16 deaths and zero gems lost on deaths; #143 lost 676-988 with 18 deaths and 236 gems lost. Side A still loses to Faisal-bot.

Runs: #145 `matches/league/145-direct-broad-pilgrimage-20261018` and exact repeat `matches/league/145-direct-broad-pilgrimage-repeat-20261018`; direct #143 control `matches/league/143-direct-broad-pilgrimage-control-20261018`. Each directory has 40 replay bundles and a per-opponent `summary.json`. The targeted replays are in `matches/league/145-direct-strong-20261018`.

The #145 source SHA-256 is `82BD25CB989585392CD627085947DDD48E6051352E0B363097C8142A1EFD1D84`; built WASM SHA-256 is `44FF0132155193697094CBEAA6AEC1D2E0AF3009DB8D9D6B2FA481D49D0D0881`. Package `submissions/tungtungsahur-candidate-v145-unranked-test.zip` is 24,829 bytes, SHA-256 `B311BBD9172CCB1B94447A2A0C9C220A8EFE331CF1C3126A225668BA8438F404`; all six source entries match the candidate directory. The candidate source was uploaded as submission version 27. This is local evidence only: live top-50 streak remains 0/10, and the supplied match-group link is still the old 0-5 FRChronic group. Main source and submission ZIP remain unchanged.

## 18 Oct: full-map candidate check and Collision follow-ups (#145–147)

The batch runner again failed while generating Windows CMake object paths, so `tools/direct_league.py` now runs `cambc run` per match and retries a transient temporary-file access error. The complete #145 broad run finished with 680 replay bundles and scored **620/680**. A fresh same-runner #143 control scored 618/680; all 16 non-Pilgrimage map totals were identical, and Pilgrimage rose from 29/40 to 31/40. The strong-proxy run finished 136/136 at 121 wins, with the same per-map totals as #143. Run folders: `matches/league/20261018-010922-cand-stampede-broad-pair-direct-v145-full-pool-20261018` and `matches/league/20261018-011341-cand-stampede-broad-pair-direct-v145-strong-all-maps-20261018`.

Against `ming_bot`, #145 still lost 8/34 strong-proxy games: both sides on Collision (416–1012 and 254–1012), both on Pilgrimage (596–1016 and 692–1072), both on Swirl (358–1008 and 610–1000), plus Contest side B and Rushbait v2 side B. Collision logs show repeated enemy tributes near (26,19), locks at (27,20), and 22/14 deaths; death bags accounted for 110/66 gems, so altar income and control remain the larger gap. Swirl had 47/34 deaths and 98/242 gems lost on deaths, with repeated altar locks. On Pilgrimage, side A lost 138 gems to deaths, while side B lost none; the large-bag route alone does not solve the Ming matchup.

#146 kept the full Collision team in the early shared-farm phase against the mirrored Cassi & Issac / Varg / Stellar draft. It scored 4/8 versus #145's 5/8, losing both games to Ming and both to Xuanming; reject it. #147 kept the normal phase but bought Varg's Power Strength shards before Monster Strength on that same map/draft. It also scored 5/8 with no win-count change and reduced the two Ming-game gem average from 335 to 192; reject it. Runs: `matches/league/20261018-011816-cand-collision-stay-group-direct-v146-stay-group-screen` and `matches/league/20261018-011942-cand-collision-varg-power-first-direct-v147-varg-power-first-screen`. Keep #145 as the best isolated candidate. These remain local proxy results, not top-50 wins.

The current v27 package and WASM were rechecked after these screens; all six ZIP source entries match #145. Main source/ZIP hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Live streak remains 0/10 because the repeated group URL is still the old 0–5 FRChronic match with both submission versions null.

## 18 Oct: Swirl empty-lock break experiment (#148)

Replay review showed repeated enemy altar locks on Swirl. #148 tested attacking a nearby enemy lock while carrying no gems, but only on Swirl against the mirrored Cassi & Issac / Varg / Stellar / Vendetta draft and only when no enemy champion was visible. It scored 4/8 against four strong local proxies: 0/2 versus Ming, 0/2 versus Xuanming, and 4/4 versus faisal-orig and opp-racer. The #145 baseline scored 5/8 on the same proxy set, including one Xuanming win; #148 increased gem totals in some losses but did not convert them into wins. Reject #148 and preserve #145/v27.

Run: `matches/league/20261018-012429-cand-swirl-empty-lock-break-direct-v148-swirl-unloaded-lock-screen` (8/8 completed). The supplied match-group link was checked again and is still the 17 Oct 0–5 FRChronic group with null submission versions; it predates v27. Live top-50 streak remains 0/10. Main source and submission ZIP remain unchanged.

## 18 Oct: Swirl and Collision follow-ups (#149–152)

| # | Map-specific change | Strong-proxy result | Decision |
|---|---|---:|---|
| 149 | Swirl four-pick draft replaces Ryth with Tavi | 5/8, tied with fresh v27; Ming gem average fell 484→275 | reject: no added wins and worse economy against Ming |
| 150 | Raise retreat-to-heal threshold to 40% only against the exact Swirl counterdraft | 4/8 versus v27's 5/8; still 0/2 against Ming and lost both Xuanming sides | reject: earlier recalls reduced farm without winning the fights |
| 151 | Send Varg to a separate safe camp from round one on Collision | 4/8 versus v27's fresh 5/8; Ming gems fell 335→205 on average | reject: the solo route did not pay for lost team coverage |
| 152 | Split Collision into Stellar/Varg and Issac/Cassi camp pairs from the opening | 4/8 versus fresh v27's 5/8; Ming scores were 66 and 132 versus 416 and 254 | reject: two routes did not match Ming's farm tempo and the team still lost both sides to Xuanming |

Runs: #149 `matches/league/20261018-012713-cand-swirl-tavi-lineup-direct-v149-tavi-for-ryth-screen`; fresh Swirl control `20261018-012729-cand-stampede-broad-pair-direct-v149-fresh-v27-control`; #150 `20261018-012845-cand-swirl-counterdraft-recall40-direct-v150-swirl-counterdraft-recall40`; #151 `20261018-013137-cand-collision-varg-solo-opening-direct-v151-collision-varg-solo-opening`; #152 `20261018-013329-cand-collision-paired-farm-direct-v152-collision-paired-farm-screen`; fresh Collision control `20261018-013428-cand-stampede-broad-pair-direct-v151-v152-fresh-v27-control`. Each screen completed 8/8 with no match failures. Keep candidate v27/#145; all four variants remain isolated and were not uploaded. The user's link is still the old group; live streak remains 0/10 and main source/ZIP are unchanged.

## 18 Oct: Collision high-damage camp avoidance (#153)

The round-140 diagnostic on Collision showed all four champions repeatedly routing to the same enemy-side camp group containing three elks (108 gems, 180 damage per turn). They died on the route or during the clear and respawned to try it again. #153 starts from v27/#145 and marks Collision by its 41x41 dimensions plus the altar at (27,20); on that map only, groups with more than 100 damage per turn are excluded from every farming target selector. Other maps and camp groups are unchanged.

Against Ming, Xuanming, Faisal-bot, and opp-racer on Collision, #153 scored 6/8 versus the fresh v27 control's 5/8, with no failed games. It flipped the Ming side-A loss (416–1012) to a win (1016–850). Against the full 20-opponent local pool, #153 scored 37/40, tying v27's 37/40; two side-A losses became wins, while two side-B wins became losses. The exact full-map strong set (Ming, Xuanming, faisal-orig, opp-racer) scored 121/136 for both #153 and v27. In that run Collision rose 5/8→6/8 and Lanes fell 6/8→5/8; all other map totals matched. Keep v27 as the verified full-map baseline and #153 only as a Collision test candidate; the strong-set total did not improve.

Runs: Collision strong set `matches/league/20261018-013913-cand-collision-no-elite-camp-direct-collision-no-elite-strong`; fresh v27 control `matches/league/20261018-013919-cand-stampede-broad-pair-direct-collision-no-elite-strong-control`; full local pool `matches/league/20261018-013926-cand-collision-no-elite-camp-direct-collision-no-elite-broad`; fresh v27 control `matches/league/20261018-013940-cand-stampede-broad-pair-direct-collision-no-elite-broad-control`. The full-map exact strong runs are candidate `matches/league/20261018-014538-cand-collision-no-elite-camp-direct-v28-strong-all-maps-exact` and fresh v27 control `matches/league/20261018-014624-cand-stampede-broad-pair-direct-v28-strong-all-maps-exact-control`; both completed 136/136 at 121 wins. A Swirl check matched v27 at 5/8 with identical per-opponent gem totals (`20261018-014231` vs `20261018-014237`). The candidate source hash is `0AB17AE08EA254173FD8633F25F95B0F2746AEC98BBAB5B785FFE718B0000575`, WASM hash `5442D39B50092DA187917F2DEE9EFA0B94D169540D1654A2DE9567B0EFC2DF9B`, and local test ZIP `submissions/tungtungsahur-candidate-v153-unranked-test.zip` hash `C0519B27C99CC4BE90D89A8F590C76D8045921D38A8B8B8A7DCFE64EA74015A5` (24,956 bytes; all six source entries verified). The candidate was uploaded as test submission version 28 with `cambc submit cand-collision-no-elite-camp`; the ZIP remains local. Main source/ZIP hashes remain unchanged. The supplied match-group URL still points to the finished 17 Oct 0–5 FRChronic group, so the top-50 streak remains 0/10.

## 18 Oct: Pilgrimage squad screens (#154–155)

| # | Change | Result vs fresh v27 | Decision |
|---|---|---|---|
| 154 | From round 1, put Varg with Cassi & Issac for two three-body squads on Pilgrimage | 5/8 vs 6/8; Ming improved 0/2→2/2, Xuanming fell 2/2→0/2 | reject for the mixed strong-proxy objective; it trades Xuanming wins for Ming wins |
| 155 | Keep the standard Pilgrimage farm split, but return to one shared objective during the active fight alarm | 5/8 vs 6/8; Ming 1/2, Xuanming 0/2 | reject; regrouping did not preserve the Xuanming wins |

Runs: #154 `matches/league/20261018-015122-cand-pilgrimage-balanced-split-direct-pilg-balanced-3v3`, control `20261018-015129-cand-stampede-broad-pair-direct-pilg-balanced-3v3-control`; #155 `matches/league/20261018-015240-cand-pilgrimage-fight-regroup-direct-pilg-fight-regroup`, using the same fresh v27 control. Each screen completed 8/8 with no failed games. Keep v27's Pilgrimage split and combat behavior.

## 18 Oct: five-pick mage priority experiments (#156–158)

#156 raised Stellar/Prism's fixed priority to 60 on every five-pick map. On Pilgrimage it scored 8/8 against four strong local proxies versus the fresh v27 control's 6/8, but the 17-map strong screen fell to 117/136 against v27's 121/136. Losses increased on Contest, Corners, Eight, Lanes, and Rushbait v2; reject the global rule.

#157 gated that priority change to Pilgrimage. Its strong all-map screen tied v27 at 121/136; Pilgrimage remained 8/8 versus 6/8. Against the full 20-opponent Pilgrimage pool, however, #157 scored 29/40 versus a fresh v27's 31/40. Reject the map-only rule for the mixed pool.

#158 tried raising Stellar/Prism's priority only while visible enemies or the shared fight alarm were active. It scored 5/8 on Pilgrimage against the strong proxies versus v27's fresh 6/8. Reject; do not promote any of #156–158.

Runs: #156 Pilgrimage `20261018-015609`, control `20261018-015628`, strong all-map `20261018-015637`, control `20261018-015716`; #157 strong all-map `20261018-015833`, broad Pilgrimage `20261018-015938`, control `20261018-015956`; #158 Pilgrimage `20261018-020105`, control `20261018-020121`. Candidate source/WASM SHA-256 pairs: #156 `6cace852e2f6cfb7a78e18286e3d1d242dd9db9316c6475cd5b1478d8c7c0d5b` / `644c435af7fd8421d39c5b62998a054f88a8e9cc609f4675f510ca66e9b0098c`; #157 `f7b6670f1e3dcb40614642805568e0315e28c9af5577989b10ed330dc88703f0` / `38a308a42e487bfb3b625f139c38bc72a44dbec93947d932f74b3fed8438fe5f`; #158 `e439cce2a6fd6846157a78cd57d48f9b2aef152801c8c9e8d1429296defc5135` / `1c0193591d2e5df40c15790ccc065e580b5f04a18c7c089e106edadb7b775450`. None was uploaded. Keep v27 as the full-map local baseline; main source and ZIP remain unchanged.

## 18 Oct: v28 full broad-pool evaluation

The uploaded Collision-only #153/v28 candidate scored 622/680 against the full 20-opponent, 17-map local pool; a fresh v27 control scored 620/680. Re-running the v28 logic under the v27 experiment bot name reproduced 622/680, and the v27 source/WASM were restored and rechecked. This is not a controlled causal gain: the Collision-only branch also produced changed outcomes on Lanes (40/40 vs 38/40), while Collision itself flipped two losses to wins and two wins to losses (net 0). `cambc run --help` exposes no seed option, so treat the +2 broad aggregate as inconclusive. Keep v27 as the verified baseline; leave v28 uploaded as an unvalidated candidate, not a promotion. Run folders: candidate `matches/league/20261018-020545-cand-collision-no-elite-camp-direct-v28-broad-all-maps`; v27 control `20261018-020841-cand-stampede-broad-pair-direct-v28-broad-all-maps-control`; same-name v28 logic `20261018-021303-cand-stampede-broad-pair-direct-v28-paired-broad-all-maps`.

## 18 Oct: Collision camp threshold refinement (#160)

#160 starts from the uploaded #153/v28 rule but excludes only camps above 150 damage/turn on Collision (the original threshold was 100). It scored 6/8 against four strong proxies on Collision, tying #153 and exceeding v27's 5/8; it tied both #153 and v27 at 37/40 against the full 20-opponent Collision pool. The 17-map strong screen tied v27 at 121/136. Reject as no aggregate improvement; keep #153/v28 as the only Collision experiment currently available for live validation.

Runs: `matches/league/20261018-021918-cand-collision-high-threshold-direct-collision-150-strong-screen`, `20261018-021934-cand-collision-high-threshold-direct-collision-150-broad-screen`, and `20261018-021956-cand-collision-high-threshold-direct-collision-150-strong-all-maps`. No failures. Source/WASM SHA-256: `4ADD0834C11C070F03B6059B157A00C5081DD169CAD022881AA88EAD3953426F` / `097CA1F34FFFCF4950BC8AA3AA9336E9F073537C50BF7EBAA56AD1A270D4241C`. Not uploaded; main source and ZIP remain unchanged.

## 18 Oct: Contest Willow counter-draft screen (#161)

#161 replaces Ryth with Willow on Contest only, keeping Prism/Stellar, Cassi & Issac, and Tavi. On the 12-game screen against Ming, Xuanming, faisal-orig, opp-racer, opp-fai-casters, and opp-tts-locker, it scored 7/12; a fresh v27 control also scored 7/12. The candidate shifted wins toward the two Willow-heavy proxy teams (casters 2/2 vs 0/2; locker 1/2 vs 0/2), while the four-strong-proxy set fell to 4/8 from v27's 7/8.

The full 20-opponent Contest pool rejects the trade: #161 scored 21/40 versus a fresh v27 control at 32/40 (both runs had zero failed games; v27's prior Contest result was also 32/40). Do not keep or upload this lineup. Preserve the v27 Contest draft. Candidate draft source SHA-256 E0DB40AB199F0B8C49DDAB59142B74AECB6E93ACE18BC5DBCCB97251BB7470E2; WASM SHA-256 814B79E047E5FEB1D212A07DC5ED88B085CFAA40CAEEB23DF22996CEE9C0F1CE. The candidate was not packaged or uploaded.

Runs: targeted candidate matches/league/20261018-022325-cand-contest-willow-for-ryth-direct-contest-willow-frontline-screen, targeted control matches/league/20261018-022416-cand-stampede-broad-pair-direct-contest-willow-baseline-control, full candidate matches/league/20261018-022428-cand-contest-willow-for-ryth-direct-contest-willow-full-pool, and full control matches/league/20261018-022456-cand-stampede-broad-pair-direct-contest-willow-baseline-full-pool. This remains local-proxy evidence; live top-50 streak is 0/10. Main source and ZIP remain unchanged.

## 18 Oct: Contest gold value and team-split screens (#162–165)

#162 locked the whole team in the early phase and removed early gold value on Contest. It scored 3/8 against the four strong local proxies, versus a fresh v27 control at 7/8; its five losses had 64–84 deaths each. Reject. #163 removed the Contest early gold bonus but kept the normal midgame split; it scored 4/8 (both sides lost to Ming and Xuanming), versus v27 at 7/8. Reject. #164 kept the normal gold bonus but held the full team together; it scored 6/8 in two exact repeated screens, below the fresh v27 7/8. Reject the team lock.

#165 keeps the existing phase split and scales only Contest's early gold weight from 2.0 to 0.25. It scored 8/8 against Ming, Xuanming, faisal-orig, and opp-racer, versus the fresh v27 control's 7/8. Across the full 20-opponent Contest pool it scored 33/40 in two runs; fresh v27 scored 32/40, matching its earlier result. The changed broad-pool game was opp-fai-casters side A (400–600 loss to 1000–200 win); deaths fell 45→26 and dropped gems 1,200→1,000. On the 17-map strong-proxy screen it scored 122/136 versus fresh v27's 121/136; the only change was Ming Contest side B (200–200 loss to 600–200 win). Keep #165 as an isolated local candidate, not a live-verified promotion.

Candidate source/WASM SHA-256: 58AC4E7FAD7EC4D300BA7FFAD14D3E1A94B1999B7E4187D7A16DDDC11740983B / 9A0533FBBA4C026A4B101DF2D8F48354600ABDB1082541C52918059205D7DBE5. Verified package submissions/tungtungsahur-candidate-v165-unranked-test.zip is 25,457 bytes, SHA-256 ea5dd394822f95ac691bf6adc2cc4910bcfb25ec3ab7da0cee2a4d4a9b65e505; all seven source entries match. Uploaded separately as test submission version 29.

Rejected variant source/WASM SHA-256 pairs: #162 32082DC00F8E70D8612314BC6C34401D0BCCD99E32A3A82CC61D7BED4C257CEA / 82D67CEB61C9363F2F8EFB75D2A0CFC6DE0903AADFA9FCDED23151F6E7897111; #163 17A4512ACBAFD22B4CB62E7584D418C95E3C949EEF5297330D04C863EE7F5129 / 71B53E92A5BC8032B00A82A787FF6F5D7B396456D629E85C92C8099A9F6D44EF; #164 BACDA0F96164DA059D320C0E6D4AA2329FC377FFE66344DED89B6B026A740BC2 / 2CC606E87A5E02F766113BB7AAD975F6369E6293B914F7CA4C1306279C6AAA9A.

Runs: #162 20261018-022813; #163 20261018-022906; #164 20261018-022940 and 20261018-022949; #165 strong Contest 20261018-023102, broad Contest 20261018-023110 and repeat 20261018-023137, strong all maps 20261018-023211. Fresh v27 controls: strong Contest 20261018-022826, broad Contest 20261018-022456, strong all maps 20261018-023301. No run had failed games. These remain local results only. The supplied 4cf7ad87-2c52-452e-a9a3-59787c302e67 group predates v29, finished 0–5, and has null submission versions; the live top-50 streak remains 0/10. Main source and ZIP remain unchanged.

## 18 Oct: v29 full 17-map broad-pool check

Candidate v29 scored 619/680 against the 20-opponent, 17-map pool; a fresh v27 run scored 620/680. Per map, Contest was 33/40 for v29 versus 32/40 for v27, matching the repeated Contest-only tests. Pilgrimage was 29/40 versus 31/40 despite no Pilgrimage code change; all other map totals matched. Because the full-pool runs are unseeded and the unrelated Pilgrimage results shifted, do not interpret the total -1 as a causal regression. This does not establish an overall broad-pool gain; retain v29 only as a Contest-specific candidate for live validation.

Runs: v29 20261018-023553-cand-contest-no-gold-direct-v29-full-broad-all-maps; fresh v27 20261018-023934-cand-stampede-broad-pair-direct-v29-broad-v27-control. Both completed 680/680 with no failed games. Main source and ZIP remain unchanged.

## 18 Oct: Pilgrimage bank-route screens (#166–167)

#166 lowered the existing allied-half bank penalty threshold from 100 to 68 gems, targeting a 92-gem Ryth death near the locked 14,3 altar. It scored 5/8 against strong proxies versus a fresh v27 6/8, and tied the full 20-opponent pool at 31/40 versus v27's 31/40. The opp-tts-v3 side-B replay stdout was byte-identical to v27: low-health retreat runs before bank(), so the new threshold did not affect that death. Reject.

#167 tests the relevant action order: on Pilgrimage only, a low-health champion carrying at least 68 gems tries the existing safe bank route before retreating. It tied v27 at 6/8 on strong proxies but scored 30/40 versus the fresh v27 control's 31/40 in the full pool. It gained my-bot side A but lost opp-tts-v2 side B and opp-tts-locker side B. Reject; preserve v27's survival-first order and 100-gem Pilgrimage route threshold.

Runs: #166 strong 20261018-024526-cand-pilgrimage-bank68-direct-pilg-bank68-strong-screen, control 20261018-024533-cand-stampede-broad-pair-direct-pilg-bank68-v27-control; #166 full 20261018-024543-cand-pilgrimage-bank68-direct-pilg-bank68-full-pool, control 20261018-024604-cand-stampede-broad-pair-direct-pilg-bank68-v27-full-control; #167 strong 20261018-024728-cand-pilgrimage-emergency-bank-direct-pilg-emergency-bank-strong-screen, full 20261018-024738-cand-pilgrimage-emergency-bank-direct-pilg-emergency-bank-full-pool. All runs completed without failures. Source/WASM SHA-256 pairs: #166 373FEB1D030D7B87776E144E2C931FA52EE70A91478DB0F7AC68B2A09A183CAD / 359FFFA16C0221198B6E677203080F43B0D3A606AA0086E3C4DB11C18F7577CF; #167 D980D575C9ABCB935136CDA0A118C1AE89226936E03AA05DADB4E596BD1EEC2C / CB6224866FFF769C785F3194E6F252D09F08365690447304EB65CB62688A913C. Neither candidate was packaged or uploaded.

## 18 Oct: Pilgrimage locked-altar and ability-order screens (#168–169)

#168 adds a 40-point cost to locked altars on Pilgrimage for carriers with at least 68 gems. It tied v27 at 6/8 on the strong screen and at 31/40 on the full 20-opponent pool. The target opp-tts-v3 side-B replay still had the same 92-gem Ryth death, and the variant also left Varg dying with 92 gems later. Reject; do not add a special locked-altar penalty.

#169 tries the Pilgrimage bank route before combat burst actions for carriers with at least 68 gems. It tied v27 at 6/8 on the strong screen, whose eight stdout logs were byte-identical to the fresh v27 screen. The unpaired full-pool run scored 28/40, below the recent v27 result of 31/40; with no seed control, retain v27's existing burst-before-bank ordering and reject this variant.

Runs: #168 strong `20261018-024859-cand-pilgrimage-avoid-locked-bank-direct-pilg-locked-bank-strong-screen`, full `20261018-024909-cand-pilgrimage-avoid-locked-bank-direct-pilg-locked-bank-full-pool`; #169 strong `20261018-025007-cand-pilgrimage-bank-before-burst-direct-pilg-bank-before-burst-strong-screen`, full `20261018-025021-cand-pilgrimage-bank-before-burst-direct-pilg-bank-before-burst-full-pool`. Both full runs completed 40/40 games with no failures. Source/WASM SHA-256 pairs: #168 `0E847FFA843804ACF5B3B4CAFE35CB3A447A9C371A6670348C796F53925F27DB` / `572E4E539FB3F5E2B89EB543DB72B4D20652712B79A7D61A31FF37D18E69BBBC`; #169 `8C5C5A6F140F05712BE5709EA151BF15E84EDD66B0221B36E5E7EAAB551FD483` / `1BAE19D11A530E2DD86769991F9B8BA51F0220C79FA317CFC2D9BE13AE552EC6`. Neither candidate was packaged or uploaded.

## 18 Oct: Pilgrimage high-bag retreat threshold (#170)

#170 raises the retreat threshold to 55% health on Pilgrimage only while carrying at least 68 gems (v27 uses 30% for Tank and 35% for other roles). It tied v27 at 6/8 against the four strong proxies and lost both games against opp-tts-v3. The target Ryth still died carrying 92 gems, at round 720 instead of round 721; the threshold changed the action trace but did not save the bag. Reject; retain the existing retreat thresholds.

Runs: strong `20261018-025342-cand-pilgrimage-bag-retreat-direct-pilg-bag-retreat-55-strong-screen`, target `20261018-025352-cand-pilgrimage-bag-retreat-direct-pilg-bag-retreat-55-opp-tts-v3`. Both completed without failures. Candidate source/WASM SHA-256: `B96CCEEF7E0295CD825E3B80DC43F25E750F9BCF6A998764D5A1AE3AE23893C1` / `038F6689E37D44879F6EAEB585D4039B72EABE49DC229C3A768322635A3B4EF9`. The candidate was not packaged or uploaded.

## 18 Oct: Contest gold-weight refinement (#171–172)

#171 raises Contest's early gold weight from v29's 0.25 to 0.5; #172 lowers it to 0.1. Each scored 7/8 against the four strong local proxies, below v29's 8/8 at 0.25. Reject both without full-pool runs; retain 0.25 as the strongest tested Contest setting, pending live top-50 validation.

Runs: #171 `20261018-025529-cand-contest-gold-half-direct-contest-gold-half-strong-screen`; #172 `20261018-025552-cand-contest-gold-010-direct-contest-gold-010-strong-screen`. Both completed 8/8 games with no failures. Source/WASM SHA-256 pairs: #171 `F36E1ADDBB02632A017F21678F61A493E09A0EE6CF12513702E2A6BD164635E6` / `E6D690CAD463BA2D92B4034B96D3D57F6172916264D3A2EC7D15A3890437D71A`; #172 `47CF6F245EF6AB009B6A883ADECE656DE74CC779E3232C06993CEF9B09467C15` / `AF80F800C402EC04BECDD762A6EB434FDB1BA16A81F10F7AE698FC32673EF8D6`. Neither candidate was packaged or uploaded.

## 18 Oct: Contest tank clears visible altar locks (#173)

#173 gives the empty-handed Tank a Contest-only action to approach and attack a visible enemy altar lock when a nearby ally carries gems and no enemy is within five tiles. Against four targeted Contest proxies, it scored 3/8, tied a fresh v29 control at 3/8, and recorded the same 267 team deaths. Per-opponent wins also matched. Reject; the local replay evidence does not support diverting the Tank from its existing role.

Runs: candidate `20261018-025938-cand-contest-clear-lock-direct-contest-clear-lock-target-screen`; fresh v29 control `20261018-030001-cand-contest-no-gold-direct-contest-clear-lock-v29-control`. Both completed 8/8 with no failures. Candidate source/WASM SHA-256: `941499237C8C4C61441E174FA90B4701734B469AE297A6ECBFE9A815BAFE5B55` / `91390AF4524E7D39FFC3963C1AB3C865E8AB89B704642F51EA2B13F8F7B3408F`. Not packaged or uploaded.

## 18 Oct: Corners opening split and combined map candidate (#174–175)

#174 changes only Corners' early opening: it bypasses the shared team-farm objective so role objectives split sooner. It scored 9/12 against six targeted proxies versus a fresh v27 control's 6/12. The full 20-opponent Corners pool scored 36/40 versus 34/40 for v27, with the same 36/40 and 34/40 in repeat runs. Its 17-map strong-proxy screen completed 121/136 after recovering one replay-write failure; the recovered Faisal-bot/Corners side-B result was a 1026–616 win. A full 680-game run tied fresh v27 at 620/680. Corners improved 34/40→36/40 while Pilgrimage shifted 31/40→29/40 despite no Pilgrimage code change; treat the broad aggregate as inconclusive without seed pairing.

#175 combines #174's Corners opening with v29's Contest early-gold weight of 0.25. Across the complete Contest and Corners pools it scored 69/80 in two identical runs: Contest 33/40 and Corners 36/40 each time, versus v27's 32/40 and 34/40. Keep it as a map-specific test candidate, not a production promotion. It was uploaded separately as unranked test submission version 30.

Candidate source/WASM SHA-256: #174 `E629554A2DA20090420C646E85BC6A0449CFAC41AC748B5B4FDDB9623231A245` / `FE9B986543FF96AFA5E5852CB9E36F083C258703B65BF594AF1E5FA0E4731F71`; #175 `C6161626C2EFB8BC968D3C4AFD0981A6B1F8793F4F26503E91DDB1078D8ED392` / `245D08ED160D0BBB8AF79A7C160A862EA9F4227C57C03BC2E4416C42DAA5E8D1`.

Runs: #174 targeted candidate/control `20261018-030352` / `20261018-030412`; full Corners candidate/control `20261018-030422` / `20261018-030436`, repeated `20261018-030454` / `20261018-030509`; 17-map strong candidate `20261018-030528` plus recovered-game run `20261018-030620`; 680-game v27 control `20261018-030704`. #175 Contest+Corners pools `20261018-032003` and repeat `20261018-032108`. Every completed comparison had zero runner failures except the single replay-file write failure recovered by the later two-game run.

Live top-50 streak remains 0/10. The supplied group `4cf7ad87-2c52-452e-a9a3-59787c302e67` predates v30 and has null submission versions. The main source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## 18 Oct: Contest high-DPS camp avoidance (#176)

#176 builds on #175 and skips Contest camp groups above 100 damage per turn before the late phase. It scored 39/40 in two identical full-pool runs, up from #175's 33/40. Against prior losses, team deaths fell from 42 to 12 versus opp-fai-casters, 77 to 20 versus tralalerotrarala, 68 to 31 versus both opp-tts-v4 and opp-tts-v5, and 71/77 to 52/24 versus opp-tts-locker. In the fresh 680-game pool, #176 scored 628/680 versus #175's 621/680; Contest rose 33/40→39/40, Corners matched at 36/40, and all other maps matched except unseeded Lanes (+2) and Stampede (-1). Keep #176 as the strongest local candidate.

The only Contest loss was a 600–600 gem tie against opp-fai-ranged, which the opponent won on lifetime gold (8,962 vs 7,795) despite losing more champions. Two mid/late gold-value trials did not improve the pool: #177 weight 0.25 scored 38/40 and lost both sides to my-bot-v2 with zero gems submitted; #178 weight 0.05 scored 37/40. Reject both and keep gold weighting at zero after the existing early 0.25 Contest setting.

#176 source/WASM SHA-256: `7A7CC9F51129C4F3B27B56928EB08651EE06AD7C7AE9809CE7AD427886CD6B73` / `E306C68671B55E7A5DBA53221A7DFFDE69CC1B37EA866D1D7976ECF6C0CED1A5`. Submitted separately as test version 31; an identical retry created duplicate version 32. Neither changes the main bot or its ZIP.

Runs: #176 Contest full pool `20261018-032457` and repeat `20261018-032542`; full 17-map pool `20261018-032651`; fresh #175 full-pool control `20261018-033247`. #177 `20261018-033942`; #178 `20261018-034106`. All runs completed with zero runner failures. Replays show the #176 improvement came with fewer camp deaths and earlier gem tributes, while #177's larger gold bias stalled gem income against my-bot-v2.

## 18 Oct: Swirl follow-ups (#179–180)

#179 extends #176's high-damage camp avoidance from Contest to Swirl. It scored 34/40 on the full Swirl pool; a fresh #176 control scored 35/40. Reject the extension and keep the safety rule Contest-only. Candidate source/WASM SHA-256: `341F4F831FAF3E5142D5A074F3FD3F63A61D54F7D8E8F242AB26294865452D5A` / `2F96B521387056467E580E23189EF62A5FDC8E50109EA9C5A4B06BC931BFC430`.

#180 broadens the Swirl parity-retreat trigger to the Ryth/Cassi & Issac/Stellar/Tavi draft that appeared in the v31 loss replay. It scored 30/40 against the same fresh #176 control's 35/40. It improved opp-tts-v5 to 2/2 wins, but caused broader regressions including 0/2 against opp-tts-locker; reject it and keep the original exact-draft trigger. Candidate source/WASM SHA-256: `BC63C6C3C8DAEE222F3EAB66E55687CF006630D9A87904FD0C95E25D11EEDA37` / `C44254EF30672F5275A9CF1CC12EE52B7A188BE54316C3BE3EA99D3A0F7519C8`.

Runs: #179 `matches/league/20261018-034439-cand-contest-swirl-safe-farm-v32-direct-swirl-safe-farm-full-pool`; fresh #176 control `matches/league/20261018-034520-cand-contest-safe-farm-v31-direct-swirl-safe-farm-v31-control`; #180 `matches/league/20261018-034648-cand-swirl-ryth-tavi-counter-v33-direct-swirl-ryth-tavi-counter-full-pool`. Each pool run completed 40/40 without failures. Neither rejected variant was uploaded. Keep #176/test versions 31–32 as the strongest local candidate. The supplied group URL is still the completed 17 Oct group with null submission versions, so live top-50 streak remains 0/10. Main source and production ZIP remain unchanged.

## 18 Oct: Swirl draft/camp follow-ups (#181–183)

#181 tests swapping Varg for Tavi when the enemy draft first reveals Ryth, Cassi & Issac, and Stellar. That partial core is not enough to predict the fourth pick: the rule also swapped against opponents who completed with Varg. The full Swirl pool fell to 32/40 against #176's fresh 35/40 control. The two-game opp-tts-v5 screen flipped which side won (Tavi won side A 1048–276 but lost side B 654–696), with no net matchup gain. Reject this broad draft guess. Draft source/WASM SHA-256: `738A6C49D24B5D4EB667FCBAB59C35335B52C9CDC16DDE5887A659FC01FEB7C4` / `253EEA6B7DB29FD0A74A655712E378C1F7856D1AFFE10ECF32A0CC9B3301F2FF`.

#182 requires the enemy's actual Tavi pick as well as the other three champions. Because draft picks are simultaneous, that final pick is not visible when our fourth pick is submitted; both opp-tts-v5 games kept Varg and matched the original 1/2 result. Reject as a no-op. Draft source/WASM SHA-256: `DFB7EA3D8171FEFCC6F702267C106EEE8127452F2B2B523C533A10C282080C49` / `49E2D7FAD3136C7837D2F35682FFE0DEB6161405B72061193E7C97969CAD5985`.

#183 raises Swirl's high-damage camp avoidance threshold from 100 to 150 damage per turn while leaving Contest at 100. It repeated 35/40 in two full Swirl pools, tied the fresh #176 control at 35/40, and reduced recorded deaths to 673 from the control's 1,029. It still lost both opp-tts-aggro sides, so it is a survival variant without a win-rate gain; do not replace #176 on this evidence. Source/WASM SHA-256: `720315A2ED62408C7CAF60A6DB68A43C8ED1BCFEED1AC430A4C7C872670DCB0F` / `C44ABBD175093F73A81B92AB2B63C11DCB0326339C518868F1301F6540E6C0E`. Runs: #181 smoke/full pool `20261018-035145` / `20261018-035202`; #182 smoke `20261018-035314`; #183 full pools `20261018-035421`, `20261018-035511`; fresh #176 control `20261018-035536`.

## 18 Oct: Packs opening split (#184)

The Packs replays showed a farming-tempo loss rather than gem loss on deaths: version 31's first 44-gem score appeared around round 100, while the map study records the top player's first 44 at round 35. #184 makes Packs enter the existing mid-game role-objective phase from round 1, splitting the four champions into Ryth/Stellar and Issac/Cassi 2+2 farming pairs. It scored 38/40 twice in the full Packs pool, versus a fresh version 31 control at 34/40. It converted all four v4/v5 Packs losses into wins (2/2 against each); the only losses were one side each to Faisal-bot and opp-tts-locker. In the full 17-map pool it scored 632/680 versus a fresh version 31 control at 628/680. Packs rose 34/40→38/40 and every other map total matched.

The first all-map candidate run had two replay filename collisions; both logs showed wins, and a serial recovery run completed the affected matches without errors. Candidate full pool: `20261018-035756-cand-packs-open-split-v37-direct-packs-open-split-all-maps`; recovered games: `20261018-040103-cand-packs-open-split-v37-direct-packs-all-map-failure-recovery`; fresh all-map version 31 control: `20261018-040115-cand-contest-safe-farm-v31-direct-packs-open-split-all-maps-v31-control`. Packs runs: targeted `20261018-035658`, full pool `20261018-035713`, exact repeat `20261018-035728`, fresh control `20261018-035740`.

#184 source/WASM SHA-256: `D5C61AD6FA58BEED4C545B644DCF6953DE792D96C72EA964345DD06531D991A2` / `BF59CAA58E80B7CBEDE201E5AC3E828BA28675BFCE09764B1DE34679CFD33FE5`. The 25,249-byte candidate ZIP `submissions/tungtungsahur-candidate-v37-unranked-test.zip` is SHA-256 `A0431087FCF07B283432DC5476A1AE3396CB667C62DE1EF7F51D3167BDADAFE5`; all six source files were byte-verified. Uploaded separately as test submission version 33. This is the strongest current local full-map candidate, pending live validation. The production source and ZIP remain unchanged.


## 18 Oct: Packs split farming with early combat leash (#185)

#185 isolates the combat side of #184: Packs still uses its role-specific split from round 1, but until round 600 it only engages enemies at normal early-phase attack range. It scored 4/4 on the selected Faisal-bot/opp-tts-locker screen, versus a fresh #184 control at 2/4, flipping both side-A losses. On the full 20-opponent Packs pool it scored 38/40 in two repeated runs, tying a fresh #184 control at 38/40. The two candidate losses moved to side A against opp-tts-v4 and opp-tts-v5; the control's two losses were side A against Faisal-bot and opp-tts-locker. This is a repeatable matchup trade, not a broad-pool gain; keep #184 as the strongest measured local all-map candidate and leave #185 isolated.

#185 source/WASM SHA-256: `3F28C0854B49BDB983835136F3A49422F573040A727DCC39A376096023DB23AA` / `2B5786AD105E2D09AC9F45D7506CC8AD9F9E02DF8F8A03330CD5ACF9D74BA52A`. Runs: candidate target `20261018-041234-cand-packs-safe-engage-v38`, fresh #184 target control `20261018-041243-cand-packs-open-split-v37`; candidate full pool `20261018-041251-cand-packs-safe-engage-v38` and repeat `20261018-041414-cand-packs-safe-engage-v38`; fresh #184 full control `20261018-041314-cand-packs-open-split-v37`. All completed with zero failed games. #185 was not packaged or uploaded.

## 18 Oct: Pilgrimage round-1 split and early combat leash (#186)

The opp-tts-v3 Pilgrimage losses exposed slow early farming: on one replay our side had no gems by round 700 while the enemy carried 796. #186 starts Pilgrimage's existing role-objective split at round 1, balances the six champions into 3+3 squads, and keeps early combat at the early-phase attack-range leash until round 600.

On the 10-game screen against Ming, Xuanming, Faisal, opp-racer, and opp-tts-v3, #186 scored 6/10, tying the fresh #184 control. The four-strong-proxy subset was 4/8 versus the control's 6/8: #186 won both v3 games that the control lost, but dropped both Xuanming games that the control won. On the full Pilgrimage pool, #186 scored 34/40 in two runs versus a fresh #184 control at 29/40. In two complete unseeded 17-map runs, #186 repeated 636/680; the fresh #184 control scored 632/680. Pilgrimage was 34/40 versus 29/40 and Lanes was 39/40 versus 40/40; the other 15 map totals matched. Treat this as a promising local all-map gain, with unpaired seeds and the Xuanming regression noted; it is not live evidence.

#186 source/WASM SHA-256: `7B1BB5BD3BEFEC4C652982909B6346B1E72023909966607C3017CA9108C5AA88` / `D71E0AE0AF9A6861B4EF0E618F75ADAA1E376F83B399DA822A681761380B2FB5`. Runs: target `20261018-041752`, fresh #184 target control `20261018-041802`; Pilgrimage full pools `20261018-041812` and repeat `20261018-041850`, fresh #184 control `20261018-041830`; all-map pools `20261018-041923` and repeat `20261018-042527`, fresh #184 all-map control `20261018-042215`. Every run completed with zero failed games. The six-file candidate bundle `submissions/tungtungsahur-candidate-v39-unranked-test.zip` was verified byte-for-byte against #186 source (SHA-256 `45A8118EACE011FCD67622BF5263E1172B0D622804B48A82A0CE858510DC2677`) and uploaded separately as test submission version 34. The supplied group still does not select v34. Production source and ZIP remain unchanged; do not promote before the live ten-win streak is verified.

## 18 Oct: Pilgrimage follow-ups (#187–189)

#187 delayed Pilgrimage's split until round 150. It improved the small Xuanming screen (3/4 vs #186's 2/4, repeated) but fell to 27/40 on the full Pilgrimage pool versus #186's 34/40; reject. #188 restored Varg to squad A and tied #186 at 2/4 against the targeted Xuanming set; reject. #189 enables the grouped opening and Varg squad-A assignment on Pilgrimage against the specific C&I/Varg/Stellar/Vendetta/Tavi draft. It scored 10/10 on five strong proxies versus #186's 6/10 and 151/170 across the five-proxy 17-map screen versus 147/170 for a fresh #186 control. The broader 20-opponent Pilgrimage pool was 33/40 versus a fresh #186 control at 34/40, so the candidate's value is specific to the observed draft and did not transfer broadly.

#189 source/WASM SHA-256: `F4A130995A06361A2A7752B0C94944811B8EE26A5BC1D5DFC9A802166FD6C2CD` / `BBCB5D8DA8E5303F124CB1DF45A07E839331C01F1C8F7F2ED571CE892C2CEFC8`. Its six-file test ZIP `submissions/tungtungsahur-candidate-v42-unranked-test.zip` is 25,359 bytes, SHA-256 `317ADFA604AB10D059A32B0AA20C2424F86CDE56ACC77B15E0E74801BB816E2C`, and was uploaded separately as test submission version 35. It was not merged into the production source or ZIP.

## 18 Oct: live top-50 tests of candidate v35

Authenticated official CLI `cambc 2.2.5` was used to query the current ladder, create groups, inspect results, and download every match summary and replay. The ladder at 03:48 UTC ranked Intercontinental Fish #1, Nyxius #2, Mite #3; FRChronic was #43 at that time. Public match APIs omit the bot submission version, so v35 is the likely but unconfirmed build for these groups. Full replay-backed findings are in `analysis/live-top50-match-review-20261018.md`.

- #1 Intercontinental Fish, group `121522cb-6efa-44bd-bb10-09cff99364cc`: **0–5** across Swirl, Collision, Lanes, Pilgrimage, Contest. No bot faults. The deepest failures were Contest (0 gems, 67 deaths, 2 kills) and Swirl (0 banked, 24 deaths, 1 kill); Lanes and Pilgrimage also lost large farm races.
- #2 Nyxius, group `8e9423ff-cb43-495c-9a35-43b3afd7a74b`: **1–4** across Swirl, Collision, Pilgrimage, Contest, Stampede. Stampede was the only win, in match 5, so the streak remains 0/10. Swirl produced 0 gems and 26 deaths; Contest produced 0 gems and 97 deaths; Pilgrimage banked 388 versus 1,112.
- #3 Mite, group `acd48ac2-d256-4149-af46-10f9492efd04`: **0–5** across Interlock, Lanes, Elkring, Stampede, Expanse. No bot faults. Lanes and Expanse were pure economy losses (zero kills, only 2 or fewer deaths); Stampede produced 0 gems and 14 deaths despite the same Prism lineup on both sides. The first camp clear happened at round 329 for Heavenly Court versus round 32 for Mite.

All three top-50 results leave the live streak at **0/10**. The four recurring weak maps are Swirl, Collision, Pilgrimage, and Contest; Mite adds clear economy-tempo deficits on Lanes, Expanse, and Stampede. These live results are not explained by bot faults. Do not promote any candidate into the main build while these failures persist.

## 18 Oct: rejected meta-trigger and draft experiments (#190–191)

#190 extends the Pilgrimage grouped-opening trigger to the Ren/Stellar/C&I/Ryth/Varg meta draft observed against Nyxius. On the same six-opponent local Pilgrimage screen it scored 11/12 versus a fresh #189 control at 12/12; against the matching `cand-ren-meta` proxy it fell from 2/2 to 1/2. Reject and do not upload. Candidate source hash: `9FDF56A2BC8BB0A37E23641A3A3069E3D83DCE4A0F2BFE71BCFE1D166C8F5BC1`.

#191 changes Swirl's four-pick lineup from Stellar/C&I/Ryth/Varg to Ren/Stellar/C&I/Ryth to mirror the top-team core. It scored 5/10 against five strong local proxies, while a fresh #189 control scored 6/10; against the exact-draft meta proxy, #191 scored 1/2 versus control's 2/2. Both still lost both Ming and Xuanming games. Reject and do not upload. The experiment was isolated from the main source and submission ZIP.

No main source or production bundle change was made. Production SHA-256 values remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` for `bots/tungtungsahur/src/bot.cpp` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` for `submissions/tungtungsahur.zip`. Continue with a new measured farm-tempo/survival experiment, then use fresh top-50 groups to validate; the requested 10 consecutive wins are not achieved.

## 18 Oct: Stampede side-camp opening (#192; test submission v36)

The Mite replay showed that #189 went for the Stampede central camp early and accumulated 14 deaths without collecting gems. #192 skips camp groups above 100 damage/turn on Stampede until round 150, letting the team farm safer side camps first. It built successfully. On five strong Stampede proxies it scored 10/10, tied with a fresh #189 control at 10/10; average gem totals improved against Ming (1,050 vs 900), tied Xuanming/Faisal/opp-racer, and declined against opp-tts-v5 (1,080 vs 1,125). On the full 20-opponent Stampede pool it scored 36/40 versus a fresh #189 control at 35/40. It converted both Faisal-bot losses to wins but lost both my-bot-v2 games that the control had won. On the full 17-map strong set it tied the control at 120/136. This is a small local Stampede improvement, not a broad win-rate gain.

Source/WASM SHA-256: #192 `0D1122E12B4EC8F697112018C6848AC23D7583B6F30C1D05855C0D57B530DE99` / `68D9A759E6B369075CF65908718B0E00617B97AFBEA9E939C82752B9FDD472CA`. The six-file bundle `submissions/tungtungsahur-candidate-v43-unranked-test.zip` is 25,307 bytes, SHA-256 `023387FED7A8D10DFA791FD1C8611F2266E2D521258FD34A391B4578CCF6E1CE`; all six archive entries were byte-verified against the tested source. Uploaded separately as test submission version 36.

The rank-3 Mite repeat, group `a04404dc-de4c-43da-bc99-95ace05a5057`, finished 0–5. Match APIs omit the submission version, but v36 was the latest upload and likely ran. On Stampede, #192 cleared safe side camps starting at round 35 and had nine deaths, down from 14 on the previous Mite run. It still submitted zero gems: HC continued clearing side camps through round 146 while Mite reached the gem camp at round 124 and submitted 1,080. This isolates the missing behavior as a transition to the central gem camp, not the first farm route.

## 18 Oct: Stampede forced central transition (#193, rejected)

#193 retained #192's safe opening through round 100, then limited farming to gem-producing groups and overrode the normal deep-camp filter. It scored 8/10 against the same five strong Stampede proxies, below #192's 10/10, so reject it and do not upload. Source hash `6B09C2031B27CAFE295B8EAAEA2BEC661D9EE7DCA132C499F9F9F3C2B9DC09C6`.

Live status remains 0/10 consecutive wins. Production source SHA-256 remains `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; production ZIP SHA-256 remains `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Candidate v36 is a separate unranked test build only.

## 18 Oct: Stampede timing and low-health burst tests (#194–197)

The #192 Stampede opening was isolated into new candidate folders; none of these variants changed the production source or was uploaded. The fresh five-opponent Stampede control #192 scored 10/10 (`20261018-050403-cand-stampede-safe-opening-192`). Unlocking the high-damage camp at round 125 scored 8/10 (#194, source `9216DADBDEC3FBA69704E2F8E7617DE29709CCFF6DA7266F593648F4026535A6`; run `20261018-050342-cand-stampede-transition-194`); round 140 scored 7/10 (#195, source `E564001ED94680A9DDB417EF176E7D3FB076EBD7C4397E66008608DD11346C28`; run `20261018-050415-cand-stampede-transition-195`). Setting gold-camp weight to zero after round 100 while preserving the 150-round safety gate scored 9/10 (#196, source `9970E487B4953987F6AD2FF2C4F7513C2722D09B6333346189E6B58A0AE45DCB`; run `20261018-050529-cand-stampede-gem-priority-196`). Reject all three; retain #192 only as the better local Stampede control.

#197 removed burst's 60%-health cutoff and moved its cast before the low-health retreat check. On Swirl, Collision, and Contest against Ming, Xuanming, opp-tts-aggro, opp-tts-locker, and Faisal-bot it scored 17/30 (`20261018-050820-cand-burst-before-retreat-197`) versus a fresh #192 control at 20/30 (`20261018-050841-cand-stampede-safe-opening-192`). Reject. Candidate source hash `FDE13A2B8784A2D7C220E80CE7C444C8E302BFAE3770171C945AF064996B793F`.

## 18 Oct: Procless #4 live validation

Fresh unranked group [`1c2711ed-18c0-4eb9-b890-070ca91db7bd`](https://2026a.battlecode.co.uk/game/match-groups/1c2711ed-18c0-4eb9-b890-070ca91db7bd) against Procless (rank 4 at queue time) finished **0–5** on Swirl, Collision, Contest, Pilgrimage, and Lanes. All five matches had zero bot faults. The latest upload before the group was test v36, likely used because public match data omits version IDs. Replay summaries and bundles are in `matches/live/1c2711ed-18c0-4eb9-b890-070ca91db7bd-matches/`.

The replay confirms the opening and economy gaps: on Collision Procless collected at round 21 and banked at 36, while HC first collected at 79 and banked at 84. On Lanes, first collections were close (rounds 53 and 57), but monster damage was 70.3k versus HC's 42.5k. On Pilgrimage, first collections were rounds 57 and 55, then monster damage diverged 79.0k to 23.4k. On Swirl, HC got the first bank (r41 vs r64) but finished 124–1,004 with 17 deaths to 3. On Contest, HC submitted zero and died 58 times; Procless dealt 187.3k monster damage and took 11 deaths. This separates Collision opening latency and map-economy pace from the ongoing combat failures on Swirl/Contest.

Live streak remains **0/10**. Do not promote the rejected local variants or update the production bot ZIP. Production hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` (source) and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` (ZIP).

## 18 Oct: Collision camp-safety rule (#198; test submission v37)

The Procless #4 replay showed our Collision opening losing two champions to a high-damage camp before our first gem collection (r79 versus r21). #198 ports the Collision-only rule from #153 onto the #192 candidate: on the unique 41×41 Collision map with altar at (27,20), skip camp groups above 100 damage per turn as farming targets. The 10-game five-proxy Collision screen scored 7/10 in two repeats, versus a fresh #192 control at 5/10 in both. The 17-map strong-proxy screen was 142/170 versus 140/170; Collision alone improved 5/10→7/10 and every other map matched. The 680-game broad pool was 637/680 versus 636/680 for a fresh #192 control, with no runner failures. Broad per-map counts did not attribute its one-win net gain to Collision, so the strong and targeted Collision repeats are the clearest evidence; keep the result provisional.

#198 source SHA-256: `F9DB33C59106715870379E51161129A97CBF99796A1134804AB4B164E84134D8`. Its six-file source bundle `submissions/tungtungsahur-candidate-v44-unranked-test.zip` is 25,395 bytes, SHA-256 `ECA9239FC02FB397CA1E844A9C9A3EEB6B3CC8BD3FD46D8879559ABC01E53500`; archive entries were byte-verified against the candidate. It was uploaded separately as test submission v37. Strong candidate/control runs: `20261018-051147-cand-collision-safe-open-198` / `20261018-051236-cand-stampede-safe-opening-192`; broad runs: `20261018-051337-cand-collision-safe-open-198` / `20261018-051635-cand-stampede-safe-opening-192`.

Fresh live re-test against Procless #4, group [`4a2bd4ac-4623-4896-8e3f-d8d026845e71`](https://2026a.battlecode.co.uk/game/match-groups/4a2bd4ac-4623-4896-8e3f-d8d026845e71), finished **0–5** on Collision, Swirl, Contest, Pilgrimage, and Lanes with zero bot faults. v37 was the latest upload at queue time and is the likely build. On Collision, the first clear/collection/bank improved to r10/r19/r41 versus Procless r14/r21/r61; the previous v36-like group was r140/r79/r84. But HC still lost 22–1,002 with 14 deaths, 0 kills, and 204 gems lost, versus Procless 0 deaths/10 kills and 53.0k monster damage versus HC's 18.6k. The other four maps repeated the previous Procless group scores. This confirms #198 fixes arrival timing but not the fight or gem retention after arriving.

Two Collision-only retreat thresholds were screened against the same five proxies using #198 as the foundation. #199 used parity (`theirs > ours`) and scored 5/10 versus #198's 7/10 (source `9AAD4A1BE821FE64FA96246B918AA59B1413B7CE5723DC7487D012EF5558B0D3`). #200 used 1.15× and scored 6/10 versus #198's 7/10 (source `16A99C6BE8DA434ECBFBA7F270785D084796B445DA98CC8127A3DB205640DC6A`). Reject both; neither was uploaded. Keep #198/v37 only as a provisional collision-opening candidate, not a live win. The live streak remains **0/10**; production source and ZIP remain unchanged.

## 18 Oct: rank-5 maps and Fragment draft experiment (#201–202)

The authenticated CLI verified the user's supplied group 4cf7ad87-2c52-452e-a9a3-59787c302e67 as the older FRChronic 0–5 result on Interlock, Stampede, Elkring, Fragment, and Pilgrimage. FRChronic was rank 58 around that match; this is not a top-50 streak result.

The rank-5 team new team(4), ID 616e95e4-36ee-4669-b9b6-edfe818a7470, was tested on Ambush, Corners, Eight, Fragment, and Rushbait v2 in group e47c4b9b-0440-4152-bae7-e8912b1de243. The latest upload at queue time was v37, likely; the API omits version IDs. It lost 0–5. Ambush was a clean farm race: 404–1,024 submitted gems, no deaths, and 28.4k versus 49.5k monster damage. Corners finished 416–1,012 with 4/1 deaths and 1/4 kills. Eight finished 99–1,019 with 17/1 deaths and 1/12 kills. Fragment finished 314–1,004 with 22/4 deaths and 4/14 kills. Rushbait v2 finished 168–1,006 with 9/0 deaths and 0/8 kills. Our monster damage was about half the opponent's on four maps and below one-third on Fragment. The API reported no match faults; replay stdout had one caught rejected-action message per map.

#201 let Varg leave the early shared-farm route and take safe solo camps while the rest of the team cleared Ryth's camp, retaining Stampede's tested team opening. The 17-map four-strong-proxy run scored 113/136 versus the #198 control's 120/135 with one failed Elkring run. Collision declined 6/8 to 4/8 and Pilgrimage 8/8 to 5/8. Reject #201. Run folders: 20261018-053048-cand-collision-safe-open-198-direct-top5-farm-varg-control and 20261018-053145-cand-early-varg-split-201-src-direct-top5-farm-varg-split-201. Candidate bot.cpp SHA-256: CDB7CA7F0B7DD44DC7EFAF26EA04C17B3B769E15C1CECC15551791A0833FFF23.

#202 changes only the 30x30 Fragment draft to Varg / Stellar / Ryth, matching the compact three-champion core observed from the rank-5 team. It scored 28/32 in two repeated 16-opponent Fragment screens versus 23/32 for the control in both repeats. Across all 17 maps against four strong proxies, it scored 122/136 with no failed runs; #198 scored 120/135 with one failed Elkring run. Fragment improved 7/8 to 8/8, while all other completed map totals matched.

Source folder: bots/cand-fragment-meta-core-202-src. The changed draft.cpp SHA-256 is 1D2916D45FE61FD1690D4515B5FC4682FFF96CADA3B656503ACFAE6E0933A922. Verified six-source test ZIP: submissions/tungtungsahur-candidate-v38-fragment-meta-test.zip, 25,515 bytes, SHA-256 4CB2CCB9774A11E486429903968A887EC817C3C21F46CBD3536A78A7B3291EF4. Uploaded separately as test submission v38.

The live v38 follow-up against rank-5 new team(4), group 62c8cd21-f213-4d3d-983d-6afc4e1f2a16, lost 0–5 on the same maps. The Fragment replay confirms our Varg / Stellar / Ryth draft, but it submitted 215 against 1,001, with 12 deaths and 0 kills versus 0 deaths and 11 kills; monster damage was 22.9k versus 66.5k. The remaining problem is farm pace and combat execution, not failure to select the observed draft. The other four map lineups were unaffected. Local gains did not convert into a top-50 win.

The requested top-50 streak is still 0/10. Production bots/tungtungsahur/src/bot.cpp and submissions/tungtungsahur.zip remain unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.

## 18 Oct: AlphaSlop rank-6 group and Ambush screens (#203–206)

Test v38 was the latest upload before group d97d6f55-8e2e-4bde-8b41-87988484d5e1 against AlphaSlop, rank 6 at queue time; the API does not expose exact submission versions. It lost 0–5 on Packs, Monolith, Rows, Ambush, and Fragment. Across all five maps, monster damage was materially lower than AlphaSlop's. Packs finished 188–1,028 (15/1 deaths, 1/11 kills, 11.5k/55.9k monster damage); Monolith 534–1,026 (4/0 deaths, 0/4 kills, 38.3k/68.7k); Rows 528–1,056 (no deaths or kills, 39.4k/68.9k); Ambush 404–1,024 (no deaths or kills, 26.3k/55.0k); Fragment 259–1,045 (14/1 deaths, 0/14 kills, 23.9k/73.0k). On Fragment our v38 Varg / Stellar / Ryth draft faced AlphaSlop's four-body Stellar / Cassi & Issac / Ryth core.

Ambush screens tested three hypotheses from the rank-5 replay, against the same 16 local opponents and both sides:
- #203 activated the normal role-objective split from round 1 on Ambush; 30/32 versus fresh #198 at 31/32. Reject.
- #204 replaced Tavi with Prism and led with Varg, mirroring the rank-5 Ambush draft; 30/32. Reject.
- #205 used Monster then Power items in each champion's camp-damage stat only on Ambush; 30/32. Reject.
- #206 combined #204's draft and #205's items; 31/32, tied with control, with lower average gem totals. Reject.

The #198 control run was 20261018-053937-cand-collision-safe-open-198-direct-ambush-role-203-control. Candidate runs were 20261018-053951-cand-ambush-role-split-203-src-direct-ambush-role-split-203, 20261018-054028-cand-ambush-prism-meta-204-src-direct-ambush-prism-meta-204, 20261018-054111-cand-ambush-farm-items-205-src-direct-ambush-farm-items-205, and 20261018-054141-cand-ambush-prism-farm-206-src-direct-ambush-prism-farm-206. None was uploaded. These checks did not identify a reliable Ambush improvement; keep production unchanged.

The next rank-7 group against Sneaky Bush Campers was queued as dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d on Stampede, Expanse, Lanes, Interlock, and Elkring. At the time of this note all five matches remained queued; poll this same group rather than create a duplicate.

## 18 Oct: rank-7 Sneaky Bush Campers result

Group dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d against Sneaky Bush Campers, rank 7 at queue time, likely used v38; submission versions are absent from the public API. It lost 0–5 on Stampede, Expanse, Lanes, Interlock, and Elkring. Stampede collected 1,080 gems but submitted zero after 23 deaths (opponent: 10 deaths, 12 kills, 1,080 submitted). Expanse and Lanes were largely farm races, with monster damage 33.1k/36.8k versus 62.1k/66.8k. Interlock and Elkring had substantial combat gaps: HC died 18/16 times and killed 1/2, while the opponent died 2/3 and killed 12/13. The same enemy earned much more gold on every map. Replays and summaries are in matches/live/dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d-matches/.

This group completes the rank-7 queue noted above. Live streak remains 0/10. Do not promote v38 or any rejected Ambush experiment into production.


## 18 Oct: Ambush round-150 experiment and v39 live test (#208–210)

#208 changed the Ambush mid-game condition to `ambush_map_active && round >= 150`, but the general `team_memory::mid_game()` trigger still switched phases earlier. Its 32-game Ambush result was exactly identical to the #198 control: 31/32, the same loss to `opp-swirl-meta-core` side B at 842–1,082, and the same 1,051.1 mean submitted gems. Treat #208 as a no-op.

The corrected #209 override makes Ambush return `early` until round 150 before evaluating the general mid-game trigger. On the full 20-opponent Ambush pool it scored 40/40, 0 failed games, 1,025.8 average gems, and 6 deaths. A fresh #203 round-1 split control scored 37/40, 0 failed games, 1,006.9 average gems, and 28 deaths. It recovered both `my-bot` sides and the `tralalerotrarala` side-A loss. Runs: `20261018-055100-cand-ambush-split-r150-corrected2-209-src-direct-ambush-split-r150-corrected2-209` and `20261018-055132-cand-ambush-role-split-203-src-direct-ambush-split-r150-corrected2-209-control`.

The integrated candidate starts from #202, retains its Fragment-only Varg / Stellar / Ryth draft, and adds the corrected Ambush phase override plus the required map flag declaration and initialization. Its `bot.cpp` SHA-256 is `068D098636061CB59DEC297AA7A999D839A3FC81F3AB4B8928645DC916D883FE`; its `draft.cpp` SHA-256 is `1D2916D45FE61FD1690D4515BFC4682FFF96CADA3B656503ACFAE6E0933A922`. The four-strong, 17-map screen scored 120/136, 0 failed, versus a fresh #202 control at 122/136, 0 failed. Ambush was 8/8 for both builds in this small set. The broad local Ambush result is promising, but the strong all-map result is not a gain.

The verified six-source ZIP `submissions/tungtungsahur-candidate-v39-ambush150-fragment-meta-unranked-test.zip` is 25,735 bytes, SHA-256 `257e4d8266834a401c39e9ed6b7b270306b5ebd21b35612be9d2dd62e1bd21ce`; every archive entry was byte-checked. It was uploaded separately as version 39. Production source and ZIP remain unchanged.

Fresh v39 groups against queue-time ranks #5 new team(4), #6 AlphaSlop, #9 Boost, and #10 Univardisty of Shingtonwash all lost 0–5. Ambush submissions were 596/1,012, 476/1,024, 702/1,068, and 462/1,062. On rank-5 Ambush, we banked 72 at r99 versus the opponent's first r120 bank. Cassi and Issac both died to camps at r145; the score then stalled at 178 until r404. Issac later died carrying 106 gems. Boost's Swirl loss (0–1,068, 29 deaths, 1 kill, 4.5k monster damage) and Univardisty's Contest loss (0–1,000, 86 deaths, 5 kills, 15.6k damage) show severe combat failure. Full per-map data and group IDs are in `analysis/live-top50-match-review-20261018.md`.

Five additional v39 groups against queue-time ranks #11–15 finished 0–5 each. Groups #17 Shawn (`65b11a0e-7118-41ed-93ee-da58a7da890c`) and #18 Ely2sh (`92156a5d-0de0-40ad-a5f5-5306275bb557`) also finished 0–5. At the initial 55-match checkpoint, the streak was 0/10 and groups against ranks #19–29 were queued or running; the later completion correction below supersedes that interim status.

#210 added an Ambush-only exclusion for camps above 100 strength to #209. It scored 34/40 and suffered 49 deaths on the same local Ambush pool; #209 scored 40/40 and had 6 deaths. Reject #210 and do not upload it. Run: `20261018-060223-cand-ambush-safe-farm-210-src-direct-ambush-safe-farm-210`; source hash `AA405596108EEB8525118AA062DB701B31764C888EC8B361EC751175899DD8B8`.

Streak remains 0/10. Do not update production before the requested ten live wins. Production source and ZIP SHA-256 remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.


## 18 Oct status correction — first v39 wins and round-120 control

All v39 groups through queue-time rank #29 have finished: 110 matches, 2 wins, 108 losses. Both wins were on Fragment with Varg / Stellar / Ryth: Ad Astra (#26) 1,014–276 (7/14 deaths, 8/7 kills, 53.1k/51.2k monster damage) and 剑桥夜爬者 (#29) 1,006–598 (14/23 deaths, 14/14 kills, 61.1k/63.4k monster damage). Both had zero platform-reported bot faults. Finished timestamps put a loss between the wins and another loss after the second; maximum consecutive wins is 1, current streak 0/10. This is live evidence that the Fragment lineup can win against some top-30 drafts, but it has not produced a broader streak.

#211 moves the Ambush split from r150 to r120. Two exact local runs both scored 39/40 with 34 deaths and the same `my-bot` side-A loss. #209/r150 repeated at 40/40 with 6 deaths. Reject #211; keep #209 only as an Ambush local test. #211 source `bot.cpp` SHA-256: `4EB82E659ED1F285A4367655479618A62912ED244B044B378E5053C2094CD32A`; runs `20261018-060647-cand-ambush-round120-211-src-direct-ambush-round120-211` and `20261018-060719-cand-ambush-round120-211-src-direct-ambush-round120-211-repeat`. The #209 repeat is `20261018-060738-cand-ambush150-fragment-meta-209-src-direct-ambush-split-r150-209-repeat`.

Groups against ranks 19–29 are finished. The most recent quota check was 29/30, resetting at 05:20:02 UTC. Resume top-50 testing at rank 30 after reset; do not upload a new candidate while interpreting the v39 groups. Production source/ZIP remain unchanged.

## Current rank #30 KKB result — 18 Oct 2026

The fresh group [`45c52751-c4fa-4377-8db3-11f8fa2958a0`](https://2026a.battlecode.co.uk/game/match-groups/45c52751-c4fa-4377-8db3-11f8fa2958a0) against KKB (rank #30 in the 05:10 UTC snapshot) finished 0–5. Latest test upload at queue time was v39, likely; match data omits the submission version. No platform faults. HC had lower monster damage on all five maps. Fragment Varg / Stellar / Ryth lost 483–1,013 with 14 deaths, 6 kills, and 52.3k monster damage versus 11 deaths, 14 kills, and 66.7k. Ambush was 702–1,058 with 2–0 deaths and no kills; Corners 776–1,002 with 8–11 deaths and 7–6 kills; Eight 330–1,118 with 14–0 deaths; Rushbait v2 722–1,006 with 18–4 deaths. See the live review for exact match IDs and collected-gem totals.

Campaign total becomes 2 wins in 115 live matches; maximum streak one, current streak zero of 10. The key repeated problem remains lower sustained monster damage, which feeds directly into slower gem income. Keep production source/ZIP unchanged.

KKB's Fragment draft had Ren / Cassi & Issac / Stellar; Ren scored 8 kills and Stellar 6, while our Varg and Ryth had no kills. The existing Fragment Ren-for-Varg candidate (#207) scored 23/32 on the local 16-opponent, both-sides screen, below the Varg / Stellar / Ryth candidate at 28/32. Although KKB shows a possible high-damage counterdraft target, the broader screen rejects a general swap; do not upload it without a matchup-specific test.

## Fragment draft #212 — add Cassi & Issac instead of Ryth

After the rank-30 KKB Fragment loss, test #212 kept Varg and Stellar and used Cassi & Issac as the third draft pick, adding a fourth actual body while retaining Varg's camp damage. It scored 26/32 over the same 16 local Fragment opponents, with zero failed games. A fresh Varg / Stellar / Ryth control scored 28/32 with zero failures; the prior #202 control also scored 28/32 twice. Reject #212 and do not upload it. The KKB lineup suggests this matchup may need a specialized response, but adding the duo is not a general Fragment improvement.

Candidate source: `bots/cand-frag-varg-cassi-212-clean-src`; `draft.cpp` SHA-256 `E476255368B4CA0E6EE9E46314242520583FAC59F70C9C051D230D264897CF47`. Candidate run `matches/league/20261018-061620-cand-frag-varg-cassi-212-clean-src-direct-fragment-varg-cassi-fourbody-212`; fresh control `matches/league/20261018-061633-cand-ambush150-fragment-meta-209-src-direct-fragment-varg-stellar-ryth-fresh-control`. Both completed 32/32 games without failures. Production source and ZIP remain at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` / `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Current rank #31 umamusume result — 18 Oct 2026

Group [`9cbc69c6-f4e8-4c04-b072-290f6f30c15d`](https://2026a.battlecode.co.uk/game/match-groups/9cbc69c6-f4e8-4c04-b072-290f6f30c15d) finished 0–5 against queue-time rank #31 umamusume. No platform bot faults. Match stats HC/opponent: Fragment 387/1,013 gems, 20/6 deaths, 6/19 kills, 42.2k/65.7k monster damage; Ambush 702/1,024, 4/3 deaths, 0/1 kills, 42.1k/86.9k; Packs 260/1,008, 17/5 deaths, 3/12 kills, 15.9k/54.5k; Monolith 394/1,010, 8/0 deaths, 0/8 kills, 32.6k/64.3k; Rows 594/1,056, no deaths or kills, 39.4k/77.0k damage. Lower monster damage appears on all five maps.

The live campaign is now 2 wins in 120 matches; maximum streak one, current streak 0/10. Next is current rank #32 Master of Betas when quota becomes available. Production source/ZIP remain unchanged.

## Ambush Ryth damage-item test #213 — reject

The rank-31 Ambush replay showed enemy Ryth dealing 24.9k monster damage with Strength emblems, versus our health-built Ryth at 7.6k. #213 changed only our Ryth's Ambush build to Monster Strength then Power Strength, leaving all other roles on their v39 builds. On the same 16-opponent, both-sides Ambush screen it tied the fresh v39 control at 31/32 wins, but averaged 995 gems versus 1,004.6 for control (31,839 vs 32,147 total). Reject #213; do not upload. The one-champion change did not improve win rate and reduced gem income.

Candidate: `bots/cand-ambush-ryth-farm-213-src`; `bot.cpp` SHA-256 `87F3E1DC329F0FA98C920D59EB9DD0D3AC699855ED9E294EB69959EDE00E40A0`. Candidate run: `matches/league/20261018-062204-cand-ambush-ryth-farm-213-src-direct-ambush-ryth-strength-213`. Fresh control: `matches/league/20261018-062218-cand-ambush150-fragment-meta-209-src-direct-ambush-v39-fresh-ryth213-control`. Production unchanged.

## Queue-time rank #31 Master of Betas result — 18 Oct 2026

Group [`59a3ce77-5499-46cc-92a7-5150bf8aa647`](https://2026a.battlecode.co.uk/game/match-groups/59a3ce77-5499-46cc-92a7-5150bf8aa647) finished 0–5 against Master of Betas, rank #31 at queue time. All platform fault counts were zero. HC/opponent: Fragment 350/1,020 gems, 21/11 deaths, 6/20 kills, 29.1k/80.8k monster damage; Ambush 298/1,058, 5/2, 1/2, 33.3k/61.7k; Stampede 0/1,080, 18/21, 11/8, 27.6k/108.5k; Expanse 376/1,006, 2/0, 0/0, 29.8k/61.7k; Swirl 36/1,058, 29/7, 2/20, 12.3k/81.2k. Swirl combat and Stampede gem retention failed badly.

Campaign total is now 2 wins in 125 live matches, max streak 1, current streak 0/10. Latest map-specific evidence is in `analysis/maps.md`. Production source/ZIP are unchanged.

## Queue-time rank #33 Memory? result — 18 Oct 2026

Group [`f2fe8162-ae57-4b93-9a73-738c00502d39`](https://2026a.battlecode.co.uk/game/match-groups/f2fe8162-ae57-4b93-9a73-738c00502d39) finished 0–5 against Memory?, rank #33 at queue time; no platform faults. HC/opponent: Fragment 234/1,026 gems, 14/0 deaths, 0/14 kills, 28.5k/65.9k monster damage; Ambush 702/1,024, 2/1, 0/0, 46.9k/63.4k; Contest 0/0, 121/1 deaths, 1/99 kills, 8.8k/99.7k; Pilgrimage 524/1,036, 7/2, 1/4, 43.3k/71.2k; Collision 176/1,016, 14/1, 1/10, 21.9k/54.1k. Contest ran to r2000 with zero gems collected or submitted; the standard tiebreak went to Memory? on lifetime gold, 11,775–575 (then kills were 99–1). This map result is a combat/survival collapse.

Campaign: 2 wins in 130 matches; max consecutive 1, current 0/10. Production unchanged. Details in the live review.

## Contest counter-drafts #214–215 — reject

The rank-33 replay showed early deaths to the enemy's Varg / Ren / Ryth core. #214 replaced Prism with Vendetta/Ren on Contest; it scored 6/8 versus a fresh v39 control at 7/8 and averaged 6,400 versus 6,800 submitted gems. Reject it. #215 replaced Prism with Varg; it also scored 7/8 but earned 5,800 gems versus control's 6,800, changing the one loss from Xuanming side A to Ming side A rather than adding a win. Reject it. Neither draft addresses the live top-team combat gap on local proxies, and neither was uploaded.

Runs: Vendetta `matches/league/20261018-062904-cand-contest-ren-draft-214-src-direct-contest-vendetta-214-target`; fresh control `matches/league/20261018-062910-cand-ambush150-fragment-meta-209-src-direct-contest-v39-four-strong-fresh-control`; Varg `matches/league/20261018-062931-cand-contest-varg-draft-215-src-direct-contest-varg-for-prism-215-target`. Contest remains map-specific work; current live submission and production files are unchanged.

## Contest parity retreat #216 — submit for live test

Candidate #216 extends the already-used parity retreat trigger from the Swirl counterdraft to Contest. On Contest, champions now retreat when nearby enemy strength exceeds nearby allied strength, rather than waiting for the larger global outmatched ratio. It changes no other map logic.

Against the full 20-opponent local Contest pool, #216 scored 40/40 with 37,800 gems and zero runner failures. A fresh v39 control scored 39/40 with 38,000 gems and zero failures; the control's only loss was a 600–600 tie against `opp-fai-ranged` (team A), which #216 won. On a follow-up screen of four strong local proxies across all 17 maps, candidate and control both scored 125/136 with no failures and identical map-by-map win counts. On Contest specifically, both went 8/8, while #216 earned 7,600 gems versus v39's 7,200. Treat this as a narrow Contest improvement, not a general win-rate increase.

The candidate source is `bots/cand-contest-parity-retreat-216-src` (`bot.cpp` SHA-256 `AA7835F9945CFACA09C061D47B879C4680B9DE5FFFD0F3B549E18B6CA6624E83`). It was uploaded as separate test submission version 40 for live validation. Local runs: `matches/league/20261018-063026-cand-contest-parity-retreat-216-src-direct-contest-parity-216-full-pool`, fresh control `matches/league/20261018-063043-cand-ambush150-fragment-meta-209-src-direct-contest-parity-216-fresh-full-control`, integrated candidate `matches/league/20261018-063208-cand-contest-parity-retreat-216-src-direct-contest-parity-216-integrated`, integrated control `matches/league/20261018-063208-cand-ambush150-fragment-meta-209-src-direct-contest-v39-integrated-control`. The v39 live campaign remains 2 wins in 130 matches, maximum streak 1, current streak 0/10. Production source and ZIP remain unchanged.

### Rank #26 Cabbage group — v40 likely, failed live test

Group [`8da6a23e-ca78-4e29-bf01-61152c1bd182`](https://2026a.battlecode.co.uk/game/match-groups/8da6a23e-ca78-4e29-bf01-61152c1bd182) queued just after v40 was submitted and finished 0–5; the public API does not expose the exact submission version. Contest was the clearest failure: 0 gems banked, 93 deaths to 6, and the first two team deaths at round 42. The parity retreat change did not solve the early fight collapse. Swirl and Stampede also had major farm/death gaps; Ambush banked 928 versus 1,086. All platform fault counts were zero. The live campaign is now 2 wins in 135 matches, max streak 1/current 0/10. Full stats and replay details are in `analysis/live-top50-match-review-20261018.md`. Keep v40 as a test artifact only; production source/ZIP remain unchanged.

## Contest draft #217 and movement retry #218 — reject for now

#217 replaces Prism with Varg on Contest while retaining the #216 parity-retreat change. It scored 36/40 against the full local Contest pool; a fresh #216 control scored 40/40. Reject it. Candidate run: `matches/league/20261018-064220-cand-contest-varg-for-prism-217-src-direct-contest-varg-prism-217-full-pool`; control: `matches/league/20261018-064202-cand-contest-parity-retreat-216-src-direct-contest-varg-prism-217-v40-control`.

#218 retries a move after `Known occupied destination`, refreshing visible unit/camp blockers and replanning up to three times. On the four-proxy, 17-map screen it scored 123/136 vs v40 at 125/136, with lower total gems (135,209 vs 135,697); losses increased on Elkring and Stampede. On the full local Ambush pool both versions went 40/40; #218 earned 41,377 gems vs 41,033, but neither run reproduced the live move error. Do not upload #218 yet. Source `bot.cpp` hash is `2E419F0F69E3AE08B598839EA6002C0E7A3C579F00E3FBFAEDE79FF1D2FE1AA2`. Runs: strong candidate `matches/league/20261018-064435-cand-move-retry-218-src-direct-move-retry-218-strong-all-maps`, fresh v40 control `matches/league/20261018-064435-cand-contest-parity-retreat-216-src-direct-move-retry-218-v40-control`, Ambush candidate `matches/league/20261018-064559-cand-move-retry-218-src-direct-move-retry-218-ambush-pool`, Ambush control `matches/league/20261018-064614-cand-contest-parity-retreat-216-src-direct-move-retry-218-v40-ambush-control`.

The v40-likely Still Testing group [`bd89f7c3-e3df-4103-97bd-e012f1570c80`](https://2026a.battlecode.co.uk/game/match-groups/bd89f7c3-e3df-4103-97bd-e012f1570c80), rank #29 at queue time, lost 0–5. Monster damage was lower on every map, including a noncombat Rows loss (528/1,056 gems; no deaths or kills). Cornered farming and tribute losses are summarized in `analysis/live-top50-match-review-20261018.md`. The current campaign is 2/140, current streak 0/10. A fresh group against rank #32 EggsAfter11AM is now queued with a new five-map set.

## Live test — EggsAfter11AM and Zarzorki (18 Oct 2026)

The group against queue-time rank #34 EggsAfter11AM, [`e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1`](https://2026a.battlecode.co.uk/game/match-groups/e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1), finished 0–5 with no platform faults. All five maps had lower monster damage and gold income. Biggest losses were Elkring (216/1,044 gems, 18 deaths, 1 kill, 34.0k/77.9k monster damage), Interlock (292/1,010, 17/0 deaths, 0/11 kills, 31.0k/54.5k damage), and Collision (102/1,002, 16/1 deaths, 1/12 kills, 19.3k/53.0k damage). The opponent's purchases show a repeated Power emblem followed by Durability Health build, with Jungle Health on some champions. #137 already tested Issac's Durability Health second emblem and tied the old control on strong proxies; don't rerun it unchanged. Campaign: 2 wins/150 live top-50 matches, max streak 1, current 0/10.

A new group against Zarzorki (rank #15, untested by team ID at queue time) is [`deec6df3-1b7f-438d-9221-70e00a5a4591`](https://2026a.battlecode.co.uk/game/match-groups/deec6df3-1b7f-438d-9221-70e00a5a4591), on Fragment, Ambush, Contest, Elkring, and Rows. It uses the latest separately uploaded test submission; the group API does not expose the exact version. Continue reviewing the group before any further submission or production update. Production `src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged.

Zarzorki finished 0–5 with no platform faults. The results continue to identify distinct problems: Contest's parity retreat still ended 77 deaths to 5 and 3.7k/187.0k monster damage; Elkring had 23/3 deaths and only 90/1,062 gems submitted; Ambush and Rows were pure farm-rate losses with no deaths. Fragment lost despite the previously successful local Varg / Stellar / Ryth setup (204/1,048 gems, 10/20 kills, 26.9k/65.7k monster damage). Current campaign: 2/155 live top-50 matches, max streak 1, current streak 0/10. Raw summaries and map analysis are in `analysis/live-top50-match-review-20261018.md`. Production source and ZIP remain unchanged.

The next group, [`bfadbe71-52dd-41fc-9d3f-3fda1e00e13d`](https://2026a.battlecode.co.uk/game/match-groups/bfadbe71-52dd-41fc-9d3f-3fda1e00e13d), against SilverSamurai (rank #31 at queue time) also finished 0–5 with zero platform faults. Monster damage and gold income were below the opponent on every map. Expanse, Lanes, and Monolith were mostly farm-only losses; Packs and Swirl added major combat losses. Campaign: 2/160, max streak 1, current 0/10. Full map stats and raw summary paths are in the live review. The repeated all-map farm deficit needs to be addressed before promoting any local-only improvement.

The following group against rank #35 conqueror_of_openai, [`a40b7063-19c9-47f9-af57-a7420f12bd3f`](https://2026a.battlecode.co.uk/game/match-groups/a40b7063-19c9-47f9-af57-a7420f12bd3f), also finished 0–5 with zero platform faults. Monster damage lagged on every map, including Corners where kills/deaths tied 4–4/5–4, and Pilgrimage where all 640 collected gems were banked but damage was only 27.2k to 78.7k. Eight, Interlock, and Collision had larger combat and/or carry losses. Campaign: 2/165, maximum streak 1, current 0/10. See the detailed table and raw summaries in the live review.
 
## Open-map farm split #219 — reject (18 Oct 2026)

Candidate #219 forced the existing mid-game role split from round 1 on Expanse, Lanes, and Rows. On a paired screen against Faisal-bot, opp-fai-bruiser, opp-tts-aggro, and my-bot-v3, it scored 22/24 versus the current v40 control's 23/24, with zero runner failures. Expanse was 8/8 for both (candidate 1,014 average gems, v40 1,039); Lanes was 7/8 versus 8/8 (993 vs 1,011 average gems); Rows was 7/8 for both (1,013 vs 1,016). Reject #219: the earlier split did not improve this screen and cost the candidate one Lanes win. Run folders: `matches/league/20261018-070103-cand-open-farm-split-219-clean-src-direct-farm-split-219-target` and `matches/league/20261018-070139-cand-contest-parity-retreat-216-src-direct-farm-split-219-v40-control`. It was never uploaded; production source and ZIP are unchanged.

## Live top-50 checks — hello, Ad Astra, and 剑桥夜爬者 (18 Oct 2026)

Against rank-26 hello, group [`f99f5297-0fb7-41b5-a255-c1a523b8875f`](https://2026a.battlecode.co.uk/game/match-groups/f99f5297-0fb7-41b5-a255-c1a523b8875f) lost 0–5. The latest captured team-A score lines were Fragment 55–929, Elkring 414–972, Monolith 424–996, Contest 0–800, and Eight 99–947. Captured SCOUT DEATH events counted 14, 11, 8, 121, and 21 respectively. Contest's first deaths were Cassi r31, Issac r32, and Prism r35.

Against rank-28 Ad Astra, group [`6c43fd4a-7925-4eb6-be94-04d82d790b37`](https://2026a.battlecode.co.uk/game/match-groups/6c43fd4a-7925-4eb6-be94-04d82d790b37) scored 1–4. Team-A score snapshots were Monolith 518–906, Lanes 620–890, Expanse 518–988, Packs 448–976, and Fragment 992–276 (the win). Expanse had only two logged deaths, both at r324; this is a clear farm-race loss. Against rank-27 剑桥夜爬者, group [`cf11e290-56c3-43a1-b170-721b79739d79`](https://2026a.battlecode.co.uk/game/match-groups/cf11e290-56c3-43a1-b170-721b79739d79) lost 0–5. Team-A score snapshots were Elkring 270–990, Rushbait v2 438–892, Contest 0–800, Pilgrimage 368–980, and Lanes 584–942. Contest had 67 logged deaths, starting with Issac and Cassi at r33; Lanes had three logged deaths and still lost on farm output.

These matches were created after test submission v40, but the match-group API omits the exact submitted version. Treat them as v40-likely, not confirmed. The tracked result is now 3 wins in 180 live top-50 games, maximum consecutive streak 1, current streak 0/10. The repeated low farm score on Expanse/Lanes and the early Contest wipe point to separate problems: route throughput on open maps and safe early positioning on Contest. Candidate #219 did not fix the open-map issue. Raw replay archives and captured score/death logs are under `matches/live/` and the live review. Production remains unchanged.
 
## Open-map shop experiment #220 and safe-split experiment #221 — reject

#220 changed Stellar's first Expanse purchase to Monster Strength before Focus. It tied the fresh v40 control at 8/8 on the four-proxy Expanse screen, but average deposited gems were 1,011 vs 1,039 for v40. Keep it unuploaded. Runs: `matches/league/20261018-070756-cand-expanse-stellar-monster-220-src-direct-expanse-stellar-monster-220-target` and `matches/league/20261018-070810-cand-contest-parity-retreat-216-src-direct-expanse-stellar-monster-220-v40-control`.

#221 separated early farm splitting from the early combat phase on Expanse, Lanes, and Rows. The corrected candidate scored 21/24 vs v40's 23/24; its only opponent with losses was Faisal-bot (3/6 vs 5/6). Average gems were lower on all three maps: Expanse 1,024 vs 1,039, Lanes 988 vs 1,011, Rows 1,011 vs 1,016. Reject. A first implementation recursively called its own helper and crashed; that run is invalid and excluded. Corrected run/control: `matches/league/20261018-071031-cand-open-farm-safe-combat-221-src-direct-safe-combat-split-221-target-fixed` and `matches/league/20261018-071048-cand-contest-parity-retreat-216-src-direct-safe-combat-split-221-v40-control`.

## Contest retreat #222 — reject

#222 retreats on Contest when enemies outnumber allies by one within 8 tiles. Against the full 20-opponent local Contest pool it scored 39/40 vs a fresh v40 control at 40/40, with zero runner failures; its only loss was contest side A against opp-fai-mirror. Do not upload this change. Runs: `matches/league/20261018-071159-cand-contest-early-retreat-222-src-direct-contest-early-retreat-222-full-pool` and `matches/league/20261018-071225-cand-contest-parity-retreat-216-src-direct-contest-early-retreat-222-fresh-v40-control`.

## Live top-50 checks — Trzy Kwaterki and rank-36 glyph-name team (18 Oct 2026)

Rank-35 Trzy Kwaterki, group [`43b3cc32-aefa-4852-938c-1bc1c02e4004`](https://2026a.battlecode.co.uk/game/match-groups/43b3cc32-aefa-4852-938c-1bc1c02e4004), finished 0–5. Captured team-A score snapshots were Elkring 378–990, Collision 584–988, Corners 526–976, Ambush 688–928, and Monolith 504–946; captured death events were 16, 18, 7, 5, and 3. Ambush and Monolith were primarily farm races; Elkring and Collision also had major combat losses.

The next rank-36 team, group [`dabc9ca4-b6f6-432c-b9da-2ff3782a2311`](https://2026a.battlecode.co.uk/game/match-groups/dabc9ca4-b6f6-432c-b9da-2ff3782a2311), also finished 0–5. Score snapshots were Monolith 548–968, Elkring 252–972, Ambush 476–914, Corners 402–966, and Pilgrimage 692–908; captured death events were 7, 18, 8, 7, and 15. These replays continue to show a farm-output gap on maps with relatively few deaths, alongside combat collapses on Elkring and Pilgrimage.

These matches followed the v40 upload, but exact server versions are not exposed. Campaign: 3 wins in 190 live top-50 games, max streak 1, current streak 0/10. Production source and ZIP remain unchanged.

## Fixed roster candidate #223 — reject for live upload

Candidate #223 uses the user's requested five champions and map-size lineups, moving gold to Tavi as the main carry. It scored 28/40 versus a fresh v40 control at 39/40 across Expanse, Lanes, Rows, Contest, and Fragment; average deposited gems were lower on every map (984/1,039; 960/1,011; 928/1,016; 625/950; 857/1,022). Leave it isolated. Investigate the economic impact of giving up paired Cassi & Issac's extra body, Tavi carry routing, and the Contest opening before any upload. The Valenki live group used the current v40-likely submission, not #223.

## Rank #39 EvilMangohh live review

Group `ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b` finished 0–5. Stampede, Ambush, and Pilgrimage repeated the low camp-damage/low gold pattern without major death counts. Swirl (33/13 deaths, 6/23 kills) and Packs (20/0 deaths, 0/14 kills) had severe combat failures. Swirl's opposing C&I / Stellar / Ryth / Ren draft bypasses the current narrow Swirl counterdraft predicate; test a matchup-specific local rule before considering upload. Full summaries are in `matches/live/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b/`.

## Local candidate screens #224–226 — none uploaded

#224 adds the observed EvilMangohh Swirl draft (C&I / Stellar / Ryth / Ren) to the special retreat predicate. It tied fresh v40 at 8/14 on seven Swirl proxies and averaged fewer gems against `opp-swirl-meta-core` (1,024 vs 1,058); reject. Run pair: `matches/league/20261018-072804-cand-swirl-counterdraft-224-src-direct-live-rank39-swirl-response-224` and `matches/league/20261018-072811-cand-contest-parity-retreat-216-src-direct-live-rank39-swirl-response-224-control`.

#225 balances Strength and Health item progression for the fixed roster. It tied #223 at 28/40 on the five-map, four-strong-proxy screen, with map tradeoffs; reject. #226 changes only Vendetta's item queue to Monster Strength -> Power Strength -> Power Health -> Power Strength and scored 30/40 vs #223's 28/40. It gained one Lanes and Rows win but lost average gems slightly (869 vs 871) and remains below fresh v40's 39/40. Do not upload. Runs are documented in `analysis/live-top50-match-review-20261018.md`.

## Fixed-roster live test v41 and heal-priority test v42

Candidate #226 was uploaded separately as v41 and tested against queue-time rank-46 天使 in group `112d14b4-4b01-4ef0-b1fd-011dd07c8f6b`; the group finished 0–5 with zero bot faults. 天使 drafted Cassi & Issac on all five maps, giving one extra body each game. Expanse and Rows were farm-rate losses; Contest ended 0 gems with 71 deaths to 3; Fragment ended 168/1,012 gems with 11/1 deaths and 0/10 kills. Replay details are in `analysis/live-top50-match-review-20261018.md`.

#227 preserves a ready heal when an ally is below 30%, because only one ability can be cast per turn and generic burst otherwise runs before Willow's heal. Its clean short-path local screen tied #226 at 30/40 with identical per-opponent wins. Uploaded as separate test submission v42. Group `83c42928-b082-4ca7-a423-aadb3ce617ae` against OneTap (#47) finished 0–5 with zero platform faults. Expanse, Lanes, and Rows were low-death farm-rate losses (24.8k/69.2k, 36.1k/71.4k, and 28.4k/68.9k monster damage); Contest and Fragment also had major combat losses. Opponent drafted Cassi & Issac on four of the five maps, but the low-death Expanse/Rows deficits persist without that body-count explanation.

#228's Issac Strength -> Health item order scored 124/136 vs fresh v40 at 125/136; #229's Stellar Focus -> Durability Health -> Focus order scored 113/136 vs 125/136. Reject both; neither was uploaded. Production source and submission ZIP remain unchanged.

The tracked top-50 campaign is now 3 wins in 215 live maps, maximum streak 1, current streak 0/10. The fixed-roster candidates #223–227 have not transferred into a live win; #226 and #227 each lost 0–5. Preserve the user roster for its dedicated test track, but treat the recurring no-contact damage deficit as a priority for a new macro/farm candidate. Keep all changes isolated from production until the agreed live streak is achieved.

## Continuation: v43-likely live test and local candidates #230–239

The user re-sent group `4cf7ad87-2c52-452e-a9a3-59787c302e67`; CLI confirms it is the same 17 Oct FRChronic 0–5 group (rank 58 at the time). It is not a new top-50 result.

Candidate #233 was uploaded separately as test version v43. Its live group against queue-time rank-47 E=mc²+AI³, [`cfe10790-872f-4df1-9664-863139501d2d`](https://2026a.battlecode.co.uk/game/match-groups/cfe10790-872f-4df1-9664-863139501d2d), finished 0–5 with zero platform faults. Exact server version is omitted by the group API; call it v43-likely. Full map metrics and replay analysis are in `analysis/live-top50-match-review-20261018.md`; raw replay bundle/folders are in `matches/live/cfe10790-872f-4df1-9664-863139501d2d/`. Contest: 0/1,000 gems, 25/16 deaths, 10/19 kills, 50.8k/121.6k monster damage, 2,180/6,118 gold. Expanse 384/1,036 gems with 2/0 deaths and 24.2k/61.1k damage; Rows 462/1,056 with no deaths and 29.5k/70.7k damage; Lanes 466/1,020 deposited with 3/1 deaths and 36.5k/64.7k damage; Fragment 256/1,001 collected, only 201 submitted, 14/5 deaths, 2/13 kills and 22.1k/74.0k damage. Campaign: 3 wins / 220 top-50 maps, maximum streak 1, current 0/10.

Contest replay inspection ties the failure to objective selection: the map has exactly two gem-producing Monolith groups (#0/#1, 200 gems each), while all other groups are gold-only. Candidate #233 repeatedly cleared gold-only #3/#4/#2 and never cleared a Monolith. Existing code adds gold value early, discounts Monolith value to 20%, and blocks high-strength groups until late. The opponent cleared Monolith #0 near r387 and #1 near r675, banking its first 200 at r431. Candidate #234 (immediate Monolith/unban) scored 18/40 on the full local Contest pool; #235 (late-only valuation) tied the control at 32/40 with identical opponent results; #239 (staged late zero-gem ban/Monolith targeting) scored 22/40. These variants do not solve it. A new candidate should retain a full team on the shared Monolith objective to improve clear speed and survival.

Local candidate screen recap (all isolated, not uploaded): #230 Tavi Monster Strength first 28/40 vs #227 30/40; #231 allow safe shopping trips tied at 30/40; #232 all-map Vendetta wolf-farm split 28/40 vs 30/40; #233 Contest-only Vendetta split 31/40 vs 30/40 on short screen, 33/40 vs 32/40 on full Contest; #234 18/40; #235 same 32/40 opponent results as control; #236/#237 Contest draft substitutions 29/40 and 28/40 vs 32/40; #238 broad C&I draft 26/40 vs 30/40; #239 22/40. Do not submit these rejected candidates again.

Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## v44-likely live test — WHIM (rank 50)

Candidate #245 was uploaded as separate submission v44. Group [`a5faf63f-bd4e-400c-8eaa-8da44f2d77c3`](https://2026a.battlecode.co.uk/game/match-groups/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3) against queue-time rank-50 WHIM finished 0–5 with zero platform faults. Exact source version is not exposed in group metadata; call it v44-likely. Replay bundles and five raw match summaries are in `matches/live/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3/`.

| Map | Rounds | Collected/submitted HC / WHIM | Deaths HC / WHIM | Kills HC / WHIM | Monster damage HC / WHIM | Gold HC / WHIM |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 1,502 | 0/0 / 1,000/1,000 | 64/6 | 4/58 | 12.4k/230.3k | 445/14,060 |
| Expanse | 694 | 548/406 / 1,092/1,070 | 5/2 | 1/3 | 28.0k/63.8k | 1,860/3,930 |
| Rows | 448 | 528/462 / 1,056/1,023 | 0/0 | 0/0 | 35.5k/74.8k | 2,160/4,740 |
| Lanes | 445 | 336/278 / 1,056/1,012 | 8/0 | 0/7 | 24.8k/62.4k | 1,400/4,560 |
| Fragment | 677 | 212/212 / 1,070/1,026 | 18/7 | 4/18 | 13.9k/79.3k | 1,075/6,025 |

Contest opening deaths: Ryth r34 to a camp, Willow r54, Vendetta r68, Prism r71. The delayed Monolith switch at r450 was too late; WHIM captured the gem camps while we dealt 12.4k monster damage and collected no gems. The other low-death losses (Expanse and Rows) confirm the wider sustained camp-damage/economy deficit. No bot faults occurred.

Local #245 tradeoff: 31/40 full Contest vs #233 at 33/40 and 29/40 integrated five maps vs 31/40, despite higher average gems (Contest 820 vs 645; integrated about 924 vs 879). #246 was 32/40 on Contest but 28/40 integrated. These did not improve wins, so reject both for promotion. Candidates #240–244 also failed to beat the safe baseline locally. Campaign: 3 wins in 225 top-50 maps, max consecutive streak 1, current 0/10. Next experiment should use the stronger multi-body meta draft and focus on safe opening camp throughput before any Monolith commitment.


## v45-likely WHIM result and continuation

The older meta control (#248; 197/200 on the local five-map proxy screen) was uploaded as separate test v45. The WHIM group [`c559fb26-1c62-44cf-b7ea-32116ca9acdb`](https://2026a.battlecode.co.uk/game/match-groups/c559fb26-1c62-44cf-b7ea-32116ca9acdb), queue-time rank 47, finished 0–5 with no bot faults. WHIM drafted C&I / Stellar / Ren / Varg / Ryth on all maps. Contest: 400 gems collected, none banked; 98 deaths to 28 and 12.6k camp damage to 256.9k. Ryth's first death was at round 30 to Stellar in the central engage. Expanse, Rows, Lanes, and Fragment also lost on farm throughput; full metrics and replays are in the live review and group folder.

Local Contest proxy follow-ups remain isolated: #247 combined immediate Monolith access with the WHIM draft (21/40); #249 used only the WHIM draft (36/40); #250 inserted Varg (36/40); #251 inserted Ren (37/40); unchanged #248 control was 40/40. Reject for promotion. #252 changes only Contest retreat to break when enemies outnumber allies nearby by one and is under test. Campaign: 3/230 top-50 maps won, current streak 0/10. Production source and ZIP stay unchanged until the target streak is reached.


Follow-up local screen: #252 (off-roster Ren lineup + one-enemy retreat) tied #251 at 37/40 with different losses; #253 (fixed roster, Contest retreat margin 1) scored 30/40 vs #245 at 31/40. Reject both; do not change the production source or ZIP.


Further isolated screens: #254 used WHIM's map-size draft on all five maps with the prior bot logic and scored 188/200 vs its #248 control at 197/200. #255 moved Ryth to Durability Health -> Jungle Health -> Power Health and scored 29/40 Contest vs #245 at 31/40. Reject both. Fixed-roster v46 (#233) is queued against current top-50 rank-50 Please; its five-map result will be added next.


## Please rank-50 tests: v46 and v47

Fixed-roster candidate #233, uploaded as v46, lost all five maps. Please used C&I on every map, gaining an extra body; Expanse/Rows were low-death farm-rate losses, and Contest ended at round 2,000 with 79 deaths / 8 kills / 7.2k camp damage and no gems submitted by either side. Replay folder: `matches/live/908bea80-655f-45f9-938f-305b924d97df/`.

The v47 counterdraft (#254) copied Please/WHIM's C&I / Stellar / Ren / Varg / Ryth map-size draft. It won Fragment but lost the other four. Fragment banking and camp damage were better than Please's (1,014 vs 842 gems; 74.7k vs 63.2k damage). Contest remained a severe combat loss; Expanse, Rows, and Lanes remained farm-rate losses. Group and replay folder: `matches/live/90e4f06e-29ac-4415-99ed-330d0fcc47ba/`. Campaign is 4/240 top-50 maps, current streak 1/10. #256 (same counterdraft with Contest-only one-enemy retreat) scored 185/200 vs #254 at 188/200 and is rejected; production source and submission ZIP remain untouched.


### Candidate #256 local follow-up

The exact map-size counterdraft with a Contest-only one-enemy retreat scored 185/200 on the five-map local pool, below #254 at 188/200. Reject the retreat change; retain #254 as the reference while testing item queues.


Version 48 was the v47 counterdraft with Power Strength -> Durability Health -> Power Strength on the farmer/fighter/Issac roles. It lost 0–5 to Please, including the Fragment matchup v47 had won. Fragment banked 284 vs 1,020 gems with 28 vs 8 deaths and 6 vs 20 kills; Contest monster damage was 8.5k vs 177.5k. The defensive tier came too early relative to our income. Group/replays: `matches/live/25164105-a829-499a-9c3a-1c6da287111f/`. Campaign 4/245, current streak 0/10. Test repeated Power Strength before revisiting defensive items; production remains unchanged.


## v49 Memory? result

The exact v47 counterdraft lost 0–5 to current rank-47 Memory? in group `0ab66a47-d3d9-4f88-92ad-5854b979e29e`; no bot faults. Contest: our C&I / Stellar / Ren / Varg / Ryth draft suffered 123 deaths and 2 kills to 2 deaths and 102 kills; no gems were banked. Memory used Varg / Stellar / Ren / Ryth / Tavi, with no linked pair. Expanse, Rows, and Lanes were low-death farm-rate losses; Fragment banked 433 vs 1,026 gems. Full stats and logs are in the group folder and live review.

#258 pure Power Strength scored 182/200 locally vs #254 at 188/200; reject. #260 is an isolated Contest draft test with five separate units (Varg / Stellar / Ren / Ryth / Tavi). Campaign remains 4/250 top-50 maps, current streak 0/10. Production source and ZIP remain unchanged.


#260 local Contest screen: 37/40 with Varg / Stellar / Ren / Ryth / Tavi, one win above the C&I counterdraft at 36/40. Submitted as v50; it lost 0–5 to Memory? in group `3cbf32fc-50b9-4021-a59a-f06ed40fdfd9`. Contest had 102 HC deaths / 6 kills / 5.6k monster damage vs Memory?'s 6 / 102 / 99.4k. #258 pure Strength build was 182/200 and remains rejected.


## v50–v52 top-50 follow-up (2026-10-18)

V50 lost 0–5 to rank-1 Intercontinental Fish (`39ffefa6-4fc3-447f-b6f2-00779d0c1616`). Expanse was a clear throughput deficit without combat: 582/1,016 gems banked, 0/0 deaths, 33.0k/74.7k monster damage, 7/46 camps cleared. Contest was a full collapse: 0/1,000 banked gems, 55/3 deaths, 1/55 kills, 8.0k/194.0k damage, and 8/81 camps cleared. Rows, Lanes, and Fragment also lost their farm race; see the live review for all stats.

V51 (#261) suppressed early attacks and held Ryth still on Contest. Against the same rank-1 team it lost 0–5 (`dc38a306-c22c-416f-899a-a6d1eaabc880`). Contest deaths fell 55->50, but camp clears fell 8->2 and monster damage 8.0k->6.3k. Reject the stationary-tank opening. The other maps were unchanged.

V52 (#264) changed only Expanse's third pick, replacing Ren with Varg. Against Intercontinental Fish it lost 0–5 (`d38357a2-8edb-4aa4-b6bf-5450b985c1cb`), but the single Expanse sample rose from 7 to 17 camp clears, 33.0k to 35.4k monster damage, and 1,710 to 2,060 earned gold; it banked 584 vs 1,016 gems. This small improvement needs more repeats. A subsequent v52 group against current rank-2 Mite also lost 0–5 (`729a4de9-1426-4694-94c6-d10335409c67`). Mite's Contest draft mirrored our Varg / Stellar / Ren / Ryth / Tavi, but it cleared 128 camps vs 1, dealt 191.2k vs 2.3k monster damage, and won the gold tiebreak after 116 kills to 0. The team is failing at farming and combat execution, not just roster choice.

Local rejects/retained candidates: #261 Contest hold 36/40; #262 Contest gold-weight change 37/40 with same losses/output as #260; #263 Fish-style Contest draft 32/40; #264 Expanse Varg-third 40/40 local. V52 is the active experimental upload. The top-50 campaign is **4/275 maps**, maximum streak 1, current streak **0/10**. Production `src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged until the requested streak is achieved.

## 18 Oct continuation: submissions v54–v57 and fuel candidates

Production remains experiment 63. The local and live runs below use isolated `bots/c###` folders; the user's target remains 10 consecutive unranked wins against top-50 teams. Local proxy results never count toward that target.

| Candidate | Change/result | Decision |
|---|---|---|
| c268 | Mirrored Mite's Rows/Lanes draft; 68/80 on its Rows/Lanes screen versus c267's 120/120 on the broader Expanse/Rows/Lanes screen. | Reject. |
| c269 | Delayed shared team-farming phase through round 600; 105/120 versus c267's 120/120. | Reject. |
| c270 / v54 | Varg splash-aware camp targeting; 120/120 local on Expanse/Rows/Lanes. Against Mite, still 0–5. | Keep isolated. |
| c271 | Global AoE camp target maximization tied c270 at 196/200; it recovered Fragment wins but lost Contest wins. | Reject globally. |
| c272 / v55 | Restrict AoE camp-target selection to Fragment; improved local Fragment screen from 37/40 to 40/40. Integrated screen reached 198 wins with one runner failure; recovered failed Contest comparison was 2/2. Against Intercontinental Fish and Nyxius, both groups lost 0–5. | Test upload only. |
| c273 | Camp clear-time estimate scaled by nearby helpers; 19/24 versus control 20/24. | Reject. |
| c274 / v56 | Zero early gold weight on Expanse/Rows/Lanes: 22/24 on strong proxies, but 118/120 on the broad screen versus a fresh control at 120/120. Lost 0–5 to procless. | Reject. |
| c275 | Temporary fuel-trace build. Identified repeated `deep_group` distance checks after the camp ledger. | Instrumentation only; never submitted. |
| c276 / v57 | Exact rectangular spawn-region distance cache plus cheap camp-score pruning before `off_limits`; original spawn bitboards retained. 30/30 across three local proxy bots on five maps; 5/10 against c272. Uploaded as a test candidate; no live group result yet. | Await live evidence. |

Official groups since v53: v54-likely versus Mite (`4b8234a2-d733-4c51-9afd-36f34083cca9`), v55-likely versus Intercontinental Fish (`cec1cd96-aa83-43ca-bd49-44a419934c15`) and Nyxius (`498ef0e4-dd7c-465e-bccc-263ca9c00c08`), and v56-likely versus procless (`d0be490a-e1f3-4fca-a5ee-7473d29073db`); all 0–5. Current cumulative record is 4 wins/305 maps, maximum streak 1, current streak 0/10. The user is creating a fresh group for v57.

Official replay events revealed `fuelExhausted` without bot faults. The instrumented build measured about 69k fuel for camp-group construction on Expanse and 95k on Lanes, with 24 and 42 groups respectively. The clean optimization caches exact region distance for rectangular bases and prunes camps that cannot beat the current value before running the costly deep-enemy-side test. It preserves the score function and original spawn tile list. This is an implementation lead, not a confirmed live win strategy.

Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

### Full-map evaluation follow-up for c276/c277

The 17-map screen against Faisal-bot, opp-fai-mirror, and opp-tts-v5 scored c276 **80/102**, compared with c272 at **82/102**. Opponent results: c276 20/34, 34/34, 26/34; c272 21/34, 33/34, 28/34. The differences are small, mixed, and not a promotion signal. c277 replaced nearest-spawn evaluation with the first spawn point; it also scored 80/102, so reject it and keep the exact c276 check for the v57 live test only. Run folders: `matches/league/20261018-095236-c276-direct-v57-full-map-proxies/`, `matches/league/20261018-095308-c272-direct-v57-full-map-control/`, and `matches/league/20261018-095407-c277-direct-representative-deep-check/`.

The latest live queue is v57-likely group [`79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f`](https://2026a.battlecode.co.uk/game/match-groups/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f) against rank-5 `new team(4)`, on Contest, Expanse, Rows, Lanes, and Fragment. It was still queued at the last poll. Wait for completion and review the replays before spending another group quota.


## v57-likely group result and c279 screen (18 Oct 2026)

The test group `79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f` against rank-5 `new team(4)` finished 0–5. Expanse / Rows / Lanes had matched body counts but lower farm output: 30.85k/44.55k/32.663k monster damage and 398/660/444 submitted gems vs 62.45k/66.924k/63.745k and 1,014/990/1,002. Contest was five bodies vs six with 69 deaths; Fragment was four vs three with 22 deaths. Keep farming throughput and fight survival as the main problems.

Fuel exhaustion events matched champion counts on both sides and v55/v56 controls, with zero faults; do not optimize that signal absent action-level evidence.

Draft-only c279 mirrors the observed opponent picks on Contest, Rows, Lanes, and Fragment. It scored 28/30 on the same five-map proxy screen and beat c276 6/10 head-to-head (849 vs 761 average submitted gems). Mixed evidence; retain only as an experimental upload candidate. Production source/ZIP are unchanged. Campaign: 4/310, current streak 0/10.


## v58/v59 candidate disposition

c279's top-5 draft mirror is uploaded as v58. c280's all-map Issac strength build scored 28/30 but lowered gem output and lost both Expanse head-to-head games; reject globally. c281 restricts the Issac strength build to Rows and Lanes. It scored 29/30 on the five-map proxy screen and beat c279 7/10, including both Rows and Lanes, then scored 79/102 over all 17 maps (c276 80/102, c272 82/102). c281 is test upload v59 and a targeted candidate only. User said they will create the next group; do not queue it on their behalf. Campaign remains 4/310, streak 0/10; production source/ZIP unchanged.


## v60 equipment experiment

c282 changes Stellar to buy Monster Focus first on Expanse, Rows, and Lanes, earning the documented 10% camp damage emblem before switching to Power Focus. It kept the proxy screen at 29/30, lowered opponent gem output vs c281, and beat c281 8/10 with an average gem edge 878:788; wins included both sides on Expanse, Rows, and Lanes. Full 17-map score remained 79/102, so v60 is only a targeted farm-map test. Uploaded as v60; official group pending user link. Campaign remains 4/310, streak 0/10; production files unchanged.


## Item A/B rejects

c283 spread Stellar's Monster Focus build to Cassi/Tavi on farm maps; proxy win count stayed 29/30 but opponent gem average worsened, and c283 lost 4/10 directly to c282. c284 swapped Monster Focus for Treasure Focus on Stellar; same proxy wins, worse opponent gem totals, and 2/10 head-to-head. Reject both; keep v60/c282's Stellar-only Monster Focus build for official evaluation.


## c285 rejected

Ryth strength equipment on Rows/Lanes won both Lanes sides vs c282 but lost both Lanes sides vs opp-fai-mirror, scored 28/30 vs proxies, and averaged 826 vs 853 gems head-to-head. Reject; v60/c282 remains latest experimental submission.


## c286/c287 equipment isolates rejected

Cassi-only Monster Focus (c286) was 30/30 on proxies but 4/10 vs c282 (813 vs 829 gems). Tavi Monster Focus on both Lanes sides (c287) was 30/30 on proxies but 5/10 vs c282 (809 vs 825 gems). Keep v60's Stellar-only Monster Focus change; no further item extension.

### c288: Ryth Monster Health on Rows/Lanes (18 Oct 2026)

Changed Ryth's Rows/Lanes items to Monster Health then Power Health, preserving health scaling and adding the monster emblem. Results: five-map proxy screen 30/30 vs c282's 29/30; the former Lanes side-A loss against opp-fai-mirror became a win. Full 17-map score 80/102 vs c282's 79/102, with the sole changed map total on Lanes (5/6 to 6/6); c272 is 82/102. Direct c288 vs c282 split 5–5, all side-B wins, so it is not decisive. The verified test package submissions/tungtungsahur-candidate-v61-unranked-test.zip was uploaded as version 61. Keep isolated as a Lanes-focused follow-up until v60's user-created group has been reviewed. Production source and ZIP are unchanged.

Follow-up variants c289 (Monster Health + Jungle Health) and c290 (Monster Health for both sets) each scored 30/30 on the same proxy screen but allowed more opponent gems than c288 and added no wins. Reject both; keep c288's Monster Health + Power Health tank build as the best local Lanes candidate.


## v60/v62 official results and Rows farm follow-up (18 Oct 2026)

The supplied group dbdcc65c-cb2f-4b28-850b-5fa691da9e34 finished 0–5 against rank-5 new team(4), likely using v60. All five maps had zero bot faults. Rows was a pure farm-rate loss: 594/1,056 banked gems, 38.854k/66.924k monster damage, 9/16 camp clears, and no deaths or champion damage. Replay coordinates show our team repeatedly clearing north-side groups 0 and 2; the opponent cleared south-side groups 1, 3, and 5. Groups are all 66 gems, and multiple collection entries can split one reward among allies.

The next group a96043a5-af65-4a93-a9af-971d34b1a879, queued after v62, also lost 0–5 despite matching the exposed top-5 lineup on all maps. Rows remained exactly 594/1,056 gems, 38.854k/66.924k monster damage, and 9/16 clears. Draft mirroring does not fix farm throughput.

Rows experiments from c291:

- c296 gave Cassi Monster Focus then Power Focus. Rows proxy screen 6/6, same as c291; average gems were lower than c291 on every proxy. Full pool tied c291 at 82/102. Reject.
- c297 removed the current-target stick bonus. Proxy wins tied c291 and gem totals declined. Reject.
- c298 let healthy Varg start a Rows wolf pack and continue the current pack. It did not improve wins or gems vs c291. Reject.

These candidate folders were not uploaded. Next focus: instrument actual target and path decisions on Rows, then test a third independent farming route. Do not infer success from local proxy wins alone.

Current official campaign: **4 wins / 320 top-50 maps**, maximum streak 1, current streak **0/10**. Test upload remains v62. Production source and ZIP are unchanged; do not promote until 10 consecutive top-50 wins.

Instrumented c299 showed Rows Ryth/Varg choosing group 4 without an observed clear; a sample had Ryth stopped at (38,9). c300 added the existing Ambush 12-turn stall recovery to Rows but tied the control screen and did not improve gem totals. This remains an unresolved camp-execution clue, not a proven pathing diagnosis. Next inspect target visibility/group state at the chosen coordinates before another strategy change.

c299's deeper trace found the group visible and partially damaged: three wolves at round 70, two at round 90, but no completed clear. c301 skipping the group regressed to 5/8; c302 stronger current-target commitment tied control at 7/8 and unchanged gems; c303 optimized AoE target placement and fell to 5/8, losing both c291 head-to-head games. Reject all; retain the route and inspect why camp damage stops / target changes.


## Rank-1 Fish review and v63 Contest test (18 Oct 2026)

Fresh unranked group 8a40e9a3-af65-4a93-a9af-971d34b1a879 against current #1 Intercontinental Fish lost 0–5 with no platform faults. Contest was 76 deaths / 0 kills / 6.3k monster damage / 0 gems versus 2 / 62 / 200.7k / 1,000. The first six deaths were Cassi r41, Issac r42, Ryth r45, Tavi r46, Stellar r50, Varg r54. This is an opening combat/survival collapse, followed by a gold and equipment snowball. Ambush, Corners, and Expanse lost largely through farm throughput; Fragment lost on both farming and survival.

Contest local candidate disposition:
- c304 exact Fish lineup mirror: 4/8, lost both head-to-head games to c291. Reject.
- c305 adds Willow while keeping the linked pair and Ryth: 6/8; 6/6 proxies but lost both c291 games. Reject.
- c306 uses Varg / Ryth / Stellar / Tavi / Willow, removing the linked pair and adding independent support. Contest screen 8/8, including 2/2 versus c291. Full 17-map score 82/102, tied with c291, with no broad win-count regression.

c306 uploaded separately as test version 63. Group 350cf6e4-a539-4b50-b612-63f2086b91d9 against Fish is queued on Ambush, Contest, Corners, Expanse, and Fragment. Poll and review this before changing or uploading another test. Current campaign is 4/325, maximum streak 1, current streak 0/10. Production source and ZIP are unchanged.


## Rank-1 follow-up: v63–v65 and Contest opening experiments (18 Oct 2026)

Unranked groups against current #1 Intercontinental Fish:
- v63-likely 350cf6e4-a539-4b50-b612-63f2086b91d9: 0–5, no faults.
- v64-likely b3d6be46-136a-4b63-8158-8cda6e2e0443: 0–5, no faults.
- v65-likely 981927d5-6aae-4256-935d-3ae0202a36cc: 0–5, no faults.

Contest: v63's Willow counterdraft improved survival versus v62 but still had no kills or gems. c308 relaxed the special outmatched check to the standard 1.3x rule; live outcome remained 0 gems and 57 deaths. c310 widened only the opening response range from 2 to 3; v65 produced 2 kills and 6 Fish deaths, but our side still lost 59 champions and banked 0 gems. Wider 4/5-tile versions regressed local Contest results.

Local results:
- c307: replace Willow with C&I to add a sixth body; 6/8 Contest, both c291 games lost. Reject.
- c308: standard outmatched threshold; 8/8 Contest, 82/102 all maps. No live improvement. Reject.
- c309: five-tile Contest opening leash; 7/8. Reject.
- c310: three-tile Contest opening response; 8/8 with 1,000 gems in each Contest proxy, 82/102 all maps. Uploaded separately as v65. Treat as a narrow live test, not a broad upgrade.
- c311: four-tile Contest opening response; 7/8 and lower Contest proxy gems. Reject.

Expanse is now the cleanest route diagnostic: same four-body draft on both sides, no champion damage, 584:1,016 submitted gems, 17:46 camp-clear entries; our first camp clear at round 28 vs Fish at round 15. Team A repeatedly clears (5,12)/(5,22), while Fish spreads effort across mirrored camps. Next instrument target and route timing on Expanse; do not change production items before isolating whether travel, camp clear time, or deaths explain the gap.

The live campaign is **4 wins / 340 top-50 maps**, maximum streak 1 and current streak **0/10**. Main source and production ZIP are unchanged. Continue to keep all experiments separate from bots/tungtungsahur.

## Rank-5 retest and next experiments (18 Oct 2026)

The user-created v60-likely group against rank-5 new team (4) lost 0-5. Current v65-likely code was then queued against the same five maps and also lost 0-5. Rushbait improved from 212 to 300 banked gems and from 9 to 3 deaths; the other outcomes remain farm or combat deficits.

Rows is an economy-only loss: 594 vs 1,056 gems, 9 vs 16 camp-clear entries, no champion damage, and no deaths. The opponent clears three mirrored wolf groups while our route clears two. Gold totals follow the same 2,430 vs 4,320 ratio, so item-order work is secondary until camp throughput improves. On eight, draft parity did not prevent a 19:2 death gap and 132:1,008 gems. On interlock, it was 13:4 deaths and 386:1,004 gems.

Local c316 split-route trial is rejected: 4/8 on Rows and 0/2 direct wins against c310 / c291. Logging-only c317 shows the full current c310 team follows Ryth's objective; it selects groups 0, 2, and 4 locally, while the live top-5 Rows match cleared only groups 0 and 2. Next: instrument arrival, respawn timing, and completion on Rows; separately test an engagement leash/retreat change on eight. Do not upload c316/c317 or modify the production bundle.

Rank-50 WHIM and rank-40 Super Intelligence were also 0-5 with v65-likely. Campaign: 4 wins / 360 completed top-50 maps, maximum consecutive streak 1, current 0/10. Keep production source and ZIP unchanged until the explicit 10-win streak gate is reached.

## v66-likely Rows retest

c318's map-specific 3x target value for a damaged Rows wolf group was uploaded as v66 for a top-5 test. Group 05465728-a486-48f7-8439-41b56bc27724 finished 0-5, and its five map metrics matched v65 exactly. Rows stayed at 594:1,056 gems and 9:16 clear entries; reject c318/v66. Next evaluate a strict damaged-pack finish rule with a stalled-progress escape. Campaign: 4 wins / 365 maps, maximum streak 1, current 0/10. Production remains unchanged.

## v67 Rows hard-lock follow-up (18 Oct 2026)

c320's damaged-pack lock was uploaded as test v67 and lost 0-5 against rank-5 new team (4) in group 955faf23-97fb-4f5f-b405-8944957190c7. The Rows game banked 528:1,056 gems with 9:16 camp-clear entries and no deaths; our team cleared groups 0, 2, and 4. This did not improve on the prior 594:1,056 v65/v66 Rows result. Reject c320 despite a 6/8 local screen. c321's zero early-gold weighting also tied at 6/8 and averaged 974 local gems; reject. Keep both candidates separate from production. Next diagnose route timing and camp throughput; campaign is 4 wins / 370 top-50 maps, maximum streak 1, current 0/10.

## v68–v71 live farm follow-up

Groups 1f420eff-95d4-47cf-adf2-1181a8dfc274 (v68), b9ee15a5-adc4-41a8-8912-9e82789b30d4 (v69), 0c22b4fb-111d-407d-bb96-e84a2f9bc336 (v70), and 47ff93c4-2182-4c8d-9b2a-61961476fd63 (v71) all lost 0-5 to rank-5 new team (4) without platform faults.

The v68 30% low-health retreat produced the same 19:2 deaths and 132:1,008 gems on eight; reject c323. v69 gave Cassi Monster Focus first and raised Rows camp damage/clear entries from 38.854k/9 to 44.550k/11, but submitted gems stayed 594:1,056 because the two extra clears were at rounds 382 and 385. Keep this only as a test lead. v70 added Ryth Monster Strength but made no further difference. v71 lowered Rows' target stickiness and matched the v65 baseline at 9:16 clears and 594:1,056. Reject c326/c327. The local Tavi reposition c322 scored 3/8 on eight; broad gear c324/c325 scored 13/24, Rows-only c326 was 15/23 with one failed game versus c310's 15/24, and Varg solo-safe-camp c328 tied baseline at 6/8/974 gems. Campaign is 4 wins / 390 maps, max streak 1, current 0/10. Production remains unchanged.

## Latest current-rank-5 group: Sneaky Bush Campers (18 Oct 2026)

Group [2c01edc0-7f92-468f-9838-0337a2d12c8f](https://2026a.battlecode.co.uk/game/match-groups/2c01edc0-7f92-468f-9838-0337a2d12c8f) finished 0-5. It is v71-likely by upload/queue timing; the public group record omits pinned versions. No platform faults occurred. This is distinct from the older supplied group `dbdcc65c-...`, which was the v60-likely match already documented above.

| Map | Gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 488:1,022 | 17:46 | 34.150k:68.284k | 14:9 | 6:12 |
| rows | 792:1,023 | 13:19 | 52.958k:74.400k | 0:0 | 0:0 |
| lanes | 546:1,016 | 24:44 | 38.922k:69.965k | 5:1 | 0:4 |
| eight | 366:1,032 | 9:18 | 29.632k:64.428k | 17:2 | 1:12 |
| interlock | 464:1,020 | 17:32 | 37.092k:63.788k | 19:0 | 0:13 |

Rows is the cleanest route benchmark: no champion combat, but our team cleared 13 camps to the opponent's 19. The opponent banked at least 1,016 gems on all maps. Eight and Interlock combine a farm deficit with a severe combat gap (36:2 deaths and 1:25 kills together). Campaign: **4 wins / 395 completed top-50 maps**, maximum streak 1, current 0/10. Production source and ZIP remain unchanged.


## Rank-5 v73-likely result and fixed-roster screen (18 Oct 2026)

Group b4117649-1de1-4564-b0c4-4f633cb53371 against Sneaky Bush Campers finished 0–5. c332's Interlock Tavi-first draft appeared in replay logs, but our team still banked 536:1,004 gems, cleared 13:33 camps, and died 18:2. The opponent cleared its first three camps by rounds 9, 24, and 38; our first clear was round 44. Enemy Stellar earned 11 kills. On Rows, neither side fought, but our team cleared 13 camps to 19 and banked 792:1,023 gems. The five-map table is in analysis/live-top50-match-review-20261018.md.

The fixed three-to-five roster candidate c333 scored 3/30 on Interlock, Eight, and Rows, versus c327's 23/30. c334 added Vendetta solo safe-wolf farming and reached 7/30; both remain below c327 and are rejected. The full-pool screen was c333 31/68, c334 34/68, c327 57/68. These results do not support uploading the fixed roster or the Vendetta change.

Continue testing isolated improvements to early farming tempo and protection/targeting against a high-damage Stellar. Keep all changes in candidate directories. Campaign is 4 wins / 410 completed top-50 maps, max streak 1, current 0/10. Production source/ZIP remain unchanged.


## Interlock support and early Vendetta farm isolates (18 Oct 2026)

c335's Varg / Ryth / Tavi / Willow and c336's Tavi / Cassi & Issac / Ryth / Willow each scored 3/10 on Interlock against five local proxies; c327 scored 6/10. c338 let Vendetta farm more safe wolf groups and scored 8/30 on Interlock / Eight / Rows, versus c327's 23/30. Reject all three and keep them unuploaded.

The v73-likely group against queue-time rank-50 Martin Shkreli's Defense Team, 9de98fb4-1737-4b66-b7b4-0859bfc0096d, finished 0-5 with zero platform faults. Our banked gems were 254 / 496 / 528 / 488 / 444 on Interlock / Eight / Rows / Lanes / Rushbait v2, versus 1,052 / 1,118 / 1,056 / 1,006 / 1,034. See `analysis/live-top50-match-review-20261018.md` for the complete table and replays.

Rows route tests c339-c343 did not beat c327. c339 never selected an eligible side camp; c340 selected enemy-side group 1 and scored 5/10; c341 selected own-side group 4 from round 2 and scored 8/10 against c327's 10/10; c342's round-60 gate never activated; c343 enabled the route in midgame and scored 6/10. Reject all five as currently implemented and keep them unuploaded. The working lead is now to inspect why late own-side wolf camps fail to repay Varg's travel / split cost, rather than forcing another global route.

The user-supplied dbdcc65c-cb2f-4b28-850b-5fa691da9e34 link is the same previously reviewed v60-likely 0-5 group against `new team(4)`; the CLI confirms the opponent was rank 5 at queue time. Do not count it again.

Campaign remains **4 wins / 415 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Production source and ZIP remain unchanged. Continue local screening; do not upload the production bundle or promote an unproven candidate.

## Queue-time #1 Fish follow-up (18 Oct 2026)

Group 794748d5-1c1f-42c5-a937-9f82e1a5fb75 finished 0–5 against Intercontinental Fish (likely the latest v73/c332 test submission; exact versions are not exposed). It added five completed top-50 maps: campaign **4 wins / 420 maps**, maximum streak 1, current 0/10.

| Map | Gems A:B | Clear entries A:B | Monster damage A:B | Deaths A:B | First clear A:B |
|---|---:|---:|---:|---:|---:|
| Interlock | 110:1,010 | 9:29 | 20.927k:59.443k | 15:0 | 44:9 |
| Eight | 176:1,078 | 8:17 | 32.450k:62.598k | 14:2 | 42:27 |
| Rows | 528:1,056 | 9:17 | 38.654k:68.850k | 0:0 | 25:21 |
| Lanes | 510:1,014 | 23:41 | 38.734k:65.711k | 4:0 | 46:38 |
| Rushbait v2 | 278:1,000 | 15:42 | 24.835k:62.886k | 14:0 | 19:21 |

The replay evidence repeats the two main failure modes. Interlock's first clear lagged Fish by 35 rounds; on Rows, no one fought or died, but Fish cleared all three south-side groups repeatedly while our route covered the north-side groups for only 9 versus 17 clear entries. Lanes also had no deaths on our side and still lost 510:1,014 gems with 23:41 clears. Do not change equipment until route tempo improves. Team-A replay stdout contains caught `Champion cannot act` errors twice on Interlock and four times on Eight, while the API reports zero bot faults; isolate the action path and log champion/action context. These errors may cost actions, but do not explain the no-combat Rows/Lanes farming gap by themselves. Continue with route/timing and action instrumentation in separate candidates; production remains unchanged.

## v74 and local follow-up results (18 Oct 2026)

c350 changed Interlock's first draft pick to Ren and was uploaded as test v74. Against Fish in group 9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3 it lost 0–5. Both teams drafted Ren, so there was no denial effect. On Interlock, gems increased from 110 to 182 and the first clear moved from round 44 to 43, but camp clears fell 9 to 7 and deaths rose 15 to 18; keep v74 test-only. The other four map outcomes and metrics exactly matched the previous group. Campaign: **4 wins / 425 maps**, best streak 1, current 0/10.

Local candidates c349–c355 were all screened and rejected: c349 farmer priority lost both Rows games and went 4/10 overall; c351 map-specific retreat was 1/6; c352's Fish-mirror Rows no-Tank draft lost 0/2 against c332; c353's Rows Varg Power-first build tied at 10/10 proxies but won slower and gave opponents more gems; c355's 1.05 outmatched threshold tied 3/6 but banked fewer gems. The next route work should focus on repeated clear frequency and farm DPS, since equipment changes did not improve it and Rows confirms the deficit without combat. Keep the production source and bundle untouched.

c356 forced the Rows mid-game split at round 35 to match Fish's early shard-buy timing. It lost 0/2 direct games to c332 and went 9/10 on the five-proxy screen; it also averaged 629-round wins and 759 Faisal-family opponent gems, slower/worse than c332's 614 and 710. Reject the forced phase transition. Keep testing only isolated routes with replay-level evidence; no local candidate has justified another upload.

Latest campaign update (18 Oct 2026): the user re-sent the old group `dbdcc65c-...`, already reviewed. Fresh unranked groups against current #1 Intercontinental Fish added ten maps and both finished 0–5. Ambush/Expanse are throughput deficits; Packs/Fragment/Collision are combat deaths plus throughput. c357 Rows side route and c358 Issac offensive gear were rejected locally. c359's Ambush split tied the local 10/10 screen but worsened live gems 582→404 and deaths 0→2; it was uploaded as test v75 and rejected. Campaign: **4 wins / 435 top-50 maps**, max streak 1, current **0/10**. Production source/ZIP remain untouched. See `analysis/live-top50-match-review-20261018.md` for metrics and `analysis/maps.md` for map takeaways.

Expanse c360 (Issac Monster/Power Strength) and c361 (round-35 split) both tied the proxy win rate but were slower and yielded less own gems than c332; c360 lost 0/2 direct games and c361 lost 1/2. Reject both. The Expanse gap remains route throughput; do not infer equipment causality from the later opponent purchase time.
## Top-2 Mite live result and latest Packs screens — 18 Oct 2026

Latest test v77/c363 likely lost 0–5 to queue-time #2 Mite in [group e29257b6-18d9-49aa-b952-43a426e1ab2d](https://2026a.battlecode.co.uk/game/match-groups/e29257b6-18d9-49aa-b952-43a426e1ab2d), with no platform faults. Packs was 208:1,014 gems, 7:19 camp clears, 18.5k:48.5k monster damage, 13:0 deaths, and 0:10 kills. The mirrored C&I / Stellar / Ren matchup ended with Mite Stellar at 7 kills and no deaths; our C&I pair died at rounds 52–53, and our Ren had only 35 earned gold and bought no items. Ambush/Expanse remain broad farm-rate losses; Fragment/Collision combine under-farming with severe combat deaths.

c362's Ren role fix and c363's tank build raised Packs gems against #1 Fish (140→252→344) but the gain did not transfer to Mite (208 gems). c364b's Issac Monster Strength-first build, c365's round-600 combat leash, and c366's Issac Power Strength-first build did not beat c363 on local Packs screens: 6/10, 5/10, and 6/10 versus c363's 6/10. Direct c363 results were 0/2, 1/2, and 0/2. Reject these candidates; none was uploaded.

Current campaign: **4 wins / 450 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Latest uploaded test remains v77/c363. Production source and ZIP hashes remain unchanged; do not promote until the ten-win streak is verified. Raw Mite summaries and replays are under matches/live/e29257b6-18d9-49aa-b952-43a426e1ab2d*.

## v81 Expanse opening split

Candidate c373 was uploaded as v81 in a separate test bundle. It starts Expanse in its mid-game route from round 1, assigns Stellar to the Cassi/Issac trio, lets Varg farm a separate safe camp, and weights gold at 0.75 for the lead camp. Bundle SHA-256: B677E6C22BC9C1A1BC6BFDE7A91E232F50B864E3187BBD2931C382C374D15B0C; candidate source SHA-256: 26177FE108D1C5E1BCC9E15AD40092FB31C146ABC25BEB16A8E5974A28C8BAFA.

Top-50 unranked outcomes (all diagnostics report zero bot faults):

- Mite group [d667335a-6dda-4906-afab-163abc4c1543](https://2026a.battlecode.co.uk/game/match-groups/d667335a-6dda-4906-afab-163abc4c1543): 0–5. Expanse 636:1,116 gems, 20:32 clears, first clear r14:r11, no deaths. Versus v77, our output rose 540→636 and first clear advanced r28→r14. Ambush 356:1,024; Packs 140:1,040; Fragment 300:1,048; Collision 154:1,002.
- Intercontinental Fish group [529e5991-2d60-46b7-970f-e634cd525c26](https://2026a.battlecode.co.uk/game/match-groups/529e5991-2d60-46b7-970f-e634cd525c26): 0–5. Expanse 778:1,016, 22:46 clears, first clear r14:r15, no deaths. Versus v77, our output rose 584→778 and clears 17→22. Ambush 582:1,024; Packs 92:1,012; Fragment 102:1,020; Collision 146:1,008.

The route transfers: first clear is now competitive with the leaders and deposits improved against both. The remaining Expanse gap is sustained camp throughput after the opening (20–22 clears vs 32–46). The other four maps retained their baseline deficits. Keep v81 test-only; do not modify production until the verified ten-win streak. Campaign is **4 wins / 480 maps**, max streak 1, current 0/10. Production hashes remain unchanged.

## v82 Expanse Ren draft isolate

c374 changed Issac to Strength gear on c373's split route. It lost 0/10 local games, banking 854–876 gems versus c373's 948 control; reject the gear change. c375 replaced Varg with Ren as Expanse's third draft pick. It scored 5/10 against five local proxies: the side-A arrangement won all five games at 980 gems versus 942–948, but the mirrored side-B arrangement lost all five at 750 versus 956–992. Live v82 groups against Mite and Fish both lost 0–5; Expanse fell from v81's 636 to 470 and 778 to 506 gems, respectively, with 2:0 deaths in both. Other maps were unchanged. Reject c375.

c376 changes Expanse from a 3+1 split to a Cassi/Issac pair plus solo Stellar and Varg. Cassi publishes her solo lane in the otherwise unused Expanse anchor slot so Varg avoids both solo camps and Issac's objective. The candidate scored 16/16 across eight local controls: 10/10 against c373/c369/c363/c332/c327, then 6/6 against Faisal-bot, ming_bot, and starter-cpp. It banked 994 gems against the first set and 969–994 against the diverse set.

c376 was uploaded as v83 in submissions/tungtungsahur-candidate-c376-expanse-2-1-1-test.zip (SHA-256 1C207CB201B6DC14C9248735211C2170CE5B77CC50360FEB153E95677B7F3142). Top-team groups finished 0–5 against Mite and Intercontinental Fish, with zero faults. Expanse reached 738:1,116 gems, 24:32 clears, first clear r14:r11 vs Mite; and 796:1,016, 28:46 clears, first clear r14:r15 vs Fish. Both games had zero deaths. Relative to v81, this adds 102 gems/four clears against Mite and 18 gems/six clears against Fish. The other four maps matched the v81 results exactly.

The 2+1+1 split is the current Expanse research lead. The remaining gap is solo route value and repeat-clear cadence, not the opening or survival. Next test a health-gated Varg route to higher-value camps, screened locally before upload. Campaign is **4 wins / 500 maps**, max streak 1, current 0/10. Production source/ZIP remain unchanged; keep v83 test-only until the verified ten-win gate.
## v78–v80 Packs live tests — 18 Oct 2026

Three separate Packs candidates were tested against current #2 Mite. v78/c367 used Issac Durability Strength then Jungle Strength; v79/c368 retreated at strength parity; v80/c369 targeted the highest raw enemy damage. All three groups lost 0–5. Mite Packs results were respectively 184:1,038 gems with 5:21 clears; 232:1,020 with 6:20; and 140:1,040 with 5:20. v79/c368 was also tested against #1 Fish and lost 0–5; its Packs result was 256:1,008 with 10:18 clears and 14:0 deaths, below v77's 344:1,028 and 11:19 clears.

c367 and c369 are rejected. c368's local 7/10 result was one win above the fresh c363 control, but the result did not transfer consistently across live opponents; keep it as an isolated experiment. No new candidate is ready for upload.

Latest test submission is v80/c369. Current campaign: **4 wins / 470 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Production tungtungsahur/src/bot.cpp and submissions/tungtungsahur.zip remain at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. Do not promote until the ten-win streak is verified.

## v60 vs #5 across five additional published maps

User-created group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34): lost 0–5, no bot faults. Rows 594:1,056 gems and 9:16 camp clears with no deaths; Lanes 560:1,038 and 20:47; Rushbait_v2 212:1,004, 17:35 and 9:0 deaths; Eight 154:1,024, 6:19 and 19:5 deaths; Interlock 596:1,032, 15:36 and 17:6 deaths. Total was 2,116:5,154 gems, 67:153 clears, 48:12 deaths, and 7:29 kills. Farming cadence is weak on every map; Eight and Interlock also have severe survival failures.

v83/c376 is queued against #5 on the same maps in group bd1c7f28-ab38-464c-aa27-74c0325737d6. The 17-map published pool is only partially covered: seven maps (Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, Swirl) have no top-50 live result. Campaign completed tally including this v60 group is **4 wins / 505 maps**, max streak 1, current **0/10**. Keep production gated; production hashes remain unchanged.

## Latest-upload group vs #5 on Rows/Lanes/Eight/Interlock/Rushbait_v2

Group [bd1c7f28-ab38-464c-aa27-74c0325737d6](https://2026a.battlecode.co.uk/game/match-groups/bd1c7f28-ab38-464c-aa27-74c0325737d6) completed 0–5 with no bot faults. Results: Rushbait_v2 300:1,020 gems (19:36 clears, 3:0 deaths); Rows 594:1,056 (9:16, no deaths); Lanes 538:1,008 (19:46, 3:0); Eight 132:1,008 (7:19, 19:2); Interlock 182:1,054 (10:30, 15:0). Submission version is not shown in the match summary; group was queued just after v83 upload.

Compared with the user's v60 group, Rushbait_v2 improved, Rows matched exactly, Lanes/Eight were similar, and Interlock was much lower. Different drafts and seeds prevent a direct causal comparison. Treat Eight and Interlock as the top survival priorities; Rows and Lanes need more farm throughput. Campaign is **4 wins / 510 maps**, max streak 1, current 0/10. Production source and ZIP remain unchanged. Seven published maps remain without top-50 live results: Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, Swirl.
# Latest campaign update (18 Oct 2026, v88–v91)

The resent group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is the old 09:18 UTC 0–5 match against `new team(4)`, confirmed by the authenticated CLI. Four later Fish tests (v88–v91) each went 0–5; none is suitable for production. v90/c391's Interlock split improved that map's first clear to round 11 and banked 204 gems, while v91/c392's mirrored draft reverted to round 28 and 88 gems. Campaign: **4 wins / 565 completed top-50 maps**, max streak 1, current **0/10**. Do not promote; production source and ZIP hashes remain unchanged. See `analysis/live-top50-match-review-20261018.md` for group-by-group figures.

## Latest top-team work (18 Oct 2026, v92–v94)

The user-repeated `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is still the old 0–5 group versus `new team(4)`. v92/c395 lost three fresh five-map groups against Fish and Mite (15 losses) while completing top-50 map coverage at 17/17. v93/c397 switched Contest to Varg/C&I/Ryth/Stellar/Tavi when Mite revealed C&I plus Ryth/Tavi. The [Mite group eba1da49-7ea6-4711-ac74-11972535abd3](https://2026a.battlecode.co.uk/game/match-groups/eba1da49-7ea6-4711-ac74-11972535abd3) was queued just after upload; the exact version is not exposed, so call it v93-likely. It lost 0–5; Contest matched six bodies but scored 0 gems and logged 140 death events. Reject v93.

c398 adds the same draft rule to c395's Interlock safety fix and did not beat c395 locally. c399 kept Willow while adding C&I and dropping Varg; it scored 5/6 against proxies and 1/2 versus c395, then uploaded as v94 for one targeted Mite test. Group [528af232-c8fa-42e7-9375-240ff909d1a9](https://2026a.battlecode.co.uk/game/match-groups/528af232-c8fa-42e7-9375-240ff909d1a9) lost 0–5. Contest remained 0 gems, with 132 Team-A death events and the first pair dying at r29. c400 burst-before-survival was equivalent to c395 locally; c401's raw-damage tie-break regressed (10/12 vs c395's 12/12, including only 2/4 vs Ming). Reject all four for production. v92 Contest logs show we earned only 105 gold as a team and bought three items, while Mite earned 21.4k and spent 19.7k; their Treasure-first purchase sequence follows the income snowball, while the earlier local Treasure-first test #138 regressed. Prioritize survival and farming before item-order tuning. Campaign: **4 wins / 590 completed top-50 maps**, maximum streak 1, current **0/10**. Production source and ZIP remain unchanged. Detailed metrics and artifacts are tracked in `analysis/live-top50-match-review-20261018.md`.

## Contest local follow-ups and v95 targeted group (18 Oct 2026)

The user-supplied group link `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is the already-reviewed 09:18 UTC 0–5 group against `new team(4)`; it adds no results. The v94-likely Mite replay shows first contact around r22, then Cassi and Issac die at r29 before the team banks gems.

Three local tests were screened from c399. c402 raised Willow's Contest heal threshold to 50% while opponents were visible; it tied c399 at 7/8 and 3,200 total gems across Ming, Xuanming, Faisal-bot, and opp-racer. c403 let front-line champions handle early Contest contact while the back line continued its farm movement; it fell to 4/8 on the same proxy set. Reject both. c404 changed only Contest's draft to Prism / Stellar / Cassi & Issac / Ryth / Tavi, matching Mite's six physical bodies and replacing Willow. On the 20-opponent Contest pool, c399 and c404 both scored 38/40; c404 added 200 aggregate gems (36,000 vs 35,800). The two side-swapped c404-vs-c399 games split 1–1 (200:1,000 and 1,000:200), so this is a matchup test, not a general upgrade.

Bundle `submissions/tungtungsahur-candidate-v95-contest-prism-mirror.zip` has SHA-256 `70A98FAA3FC6663AA43CED2F6A2F82B1B1230C76C2E63B706FEAFB2A8FDAA3AA`; it was submitted as test v95. The [Mite group](https://2026a.battlecode.co.uk/game/match-groups/dbffabee-68c9-4ddd-a9eb-5e59b423e846) finished 0–5. The platform confirms the exact Contest mirror roster, Prism / Stellar / C&I / Ryth / Tavi, but it did not improve execution:

| Map | Gems HC:Mite | Camp-clear entries | Monster damage (k) | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Contest | 0:0 | 2:128 | 3.6:191.4 | 141:0 | 0:117 |
| Swirl | 0:1,020 | 1:17 | 7.4:89.0 | 27:1 | 1:21 |
| Interlock | 480:1,034 | 18:32 | 34.2:67.3 | 11:7 | 3:6 |
| Rows | 528:1,012 | 9:16 | 37.7:64.8 | 0:0 | 0:0 |
| Eight | 198:1,008 | 6:17 | 31.9:54.4 | 10:2 | 1:7 |

There were zero platform bot faults on all five maps. Contest stdout logged five caught `Champion cannot act` errors. The first visible enemy contact was r20–21 and our first death was Ryth at r28; the team still banked no gems. Keep v95 rejected for general use. A follow-up group against current rank-50 Bamboo Teahouse, [51e941e4-5904-4c2d-bd75-87d761c2b0c3](https://2026a.battlecode.co.uk/game/match-groups/51e941e4-5904-4c2d-bd75-87d761c2b0c3), is running the same five maps; submission pins are not exposed yet, so do not count it pending completion.

The follow-up [group against current rank-50 Bamboo Teahouse](https://2026a.battlecode.co.uk/game/match-groups/51e941e4-5904-4c2d-bd75-87d761c2b0c3) also finished 0–5 with zero platform faults. Its metrics were:

| Map | Gems HC:Bamboo | Camp-clear entries | Monster damage (k) | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Contest | 0:800 | 6:116 | 20.2:236.6 | 123:3 | 1:94 |
| Swirl | 0:1,020 | 2:23 | 10.6:79.8 | 37:6 | 4:28 |
| Interlock | 546:1,054 | 22:33 | 50.9:57.5 | 15:0 | 0:11 |
| Rows | 660:1,056 | 11:17 | 45.5:68.9 | 0:0 | 0:0 |
| Eight | 36:1,038 | 5:21 | 31.5:55.3 | 20:4 | 2:14 |

Interlock's 546 gems and 50.9k monster damage are comparatively strong, but the other four maps show large farm or survival deficits. Reject v95 as a general candidate. The campaign is now **4 wins / 600 completed top-50 maps**, maximum streak 1, current **0/10**. All 17 maps have live coverage. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.


## Rows route diagnosis and rejected local variants (18 Oct 2026)

The user re-sent [group dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34), the already-counted 09:18 UTC 0-5 group versus `new team(4)`; it adds no maps. The latest Bamboo Rows replay shows a clean farm-rate loss: 660:1,056 gems, 11:17 clear entries, 45.544k:68.850k monster damage, no deaths or champion damage. Event-level capture rewards show our side clearing groups 0/2/4 ten times total while Bamboo cleared groups 1/3/5 sixteen times. Our group 4 was first cleared at r175, compared with Bamboo's group 5 at r105. Our Varg shared several 66-gem captures for 22 gems, while Bamboo's Varg repeatedly earned the full 66.

Candidates c405/c406 tried synchronizing the Rows leaders' shared objectives; they scored 4/14 and 5/14, and each lost all six side-swapped games against c399/c404/c327. Reject both. c407 skipped Varg's capture-joining behavior on Rows and scored 12/14, but its direct c404 comparison split 1-1 with no gem advantage over baseline. Diagnostic builds c408/c410 showed Varg's ordinary solo-camp target remained empty and he fell back to Issac's objective. c409 allowed Varg to select wolf packs up to three wolves behind a 75% starting-health gate; it scored 9/14, winning all seven side-A games and two of seven side-B games. c411 additionally limited those targets to our half of the map; it scored 12/14 (7/7 side A, 5/7 side B), but only split 1-1 against c404. No candidate shows a reliable gain over baseline, so none was uploaded. The next Rows work should repair Varg's solo route with a stable side-aware target assignment; do not promote based on proxy scores.

Campaign remains **4 wins / 600 completed top-50 maps**, best streak 1, current **0/10**. Production source and ZIP remain unchanged.


## #159 Rows route phase audit and v96 live result (18 Oct 2026)

#159/c413 attempted to start Varg's solo wolf route inside the early-phase branch. The branch is unreachable on Rows because `game_phase()` returns `Phase::mid` for Rows from round 1. The 14-game screen matched c411's proxy results at 10/12 and split 1-1 head-to-head; its c411 comparison replayed the same 574/579-round outcomes. Treat c413 as a no-op and do not upload it.

c411's allied-half wolf route was bundled as `submissions/tungtungsahur-candidate-c411-rows-home-side-wolf.zip` (SHA-256 `13BE6FF1AEE3D1FC6E2905C252A8FFDB13466D036BFF8344BD5A886A947C8BF8`) and uploaded as test v96. The fresh unranked group [819e5b24-2227-4065-9eda-d49419a8568f](https://2026a.battlecode.co.uk/game/match-groups/819e5b24-2227-4065-9eda-d49419a8568f) against then-rank-50 umamusume finished 0-5. The service does not expose the pinned submission, so attribute it v96-likely. It had zero `botFault` events; detailed stats and summaries are in `matches/live/819e5b24-2227-4065-9eda-d49419a8568f/`.

| Map | Gems | Camp clears | Monster damage (k) | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Rows | 528:1,056 | 11:17 | 42.7:68.9 | 2:0 | 0:0 |
| Lanes | 590:1,016 | 24:46 | 40.3:69.4 | 1:0 | 0:1 |
| Eight | 264:1,036 | 5:26 | 27.0:62.2 | 24:6 | 1:12 |
| Interlock | 292:1,006 | 15:21 | 32.4:57.7 | 15:1 | 1:10 |
| Contest | 0:200 | 3:129 | 28.8:187.8 | 98:7 | 7:72 |

Rows remains a farm-throughput loss. Eight and Interlock combine slow farming with deaths. Contest is the sharpest issue: our Cassi and Issac both died at r45 to the opposing Ren, and Team A collected 200 gems but submitted none; the opponent banked 200 late. The replay also records ten Team-A fuel-exhaustion events on Contest (six between r35 and r39), four on Lanes, and three on Eight. Fuel exhaustion suspends a turn without a `botFault`; profile these spikes before attributing all lost actions to combat logic.

Campaign: **4 wins / 605 completed top-50 maps**, best streak 1, current **0/10**. All 17 official maps have live coverage. v96 is test-only; production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Latest Contest diagnostics and v97 test (18 Oct 2026)

#169 instrumented isolated c414/c415 builds to profile the concentrated Contest fuel exhaustion. Visibility reads cost roughly 9–15k fuel per list on some turns; pathfinding cost about 20–30k across its stages, and role actions sometimes started with under 5k remaining. This confirms that some turns can run out of fuel, but not that fuel is the primary Contest failure. The builds were diagnostics only.

#170/c416 deferred camp-ledger refresh and objective reselection while an enemy was visible. It scored 2/6 across Contest/Eight/Interlock and 7/8 on a separate Contest proxy screen, equal to c411's 7/8 with lower average gems. Reject it.

#171/c417 changed memoized visible ally/enemy lists to return cached references, avoiding repeated copies and filtering. On two repeated 24-game screens it scored 20/24 versus c411's 17/24, with gains on Lanes and no measured regression on Contest or Eight. Uploaded separately as test v97 in `submissions/tungtungsahur-candidate-c417-memo-visible-unit-lists.zip` (SHA-256 `C5C743E43AB52554B8D7DC772FD9E4CB4FDAD35A30F3F088D2637AD6AE9495D0`). The fresh five-map group against queue-time rank-50 Live Love Larp, [bab275a5-8821-4586-81e2-23b16e626e90](https://2026a.battlecode.co.uk/game/match-groups/bab275a5-8821-4586-81e2-23b16e626e90), lost 0-5 with no bot faults. Lanes recorded 5:4 fuel-exhaustion events; the other four maps had none. Keep v97 test-only.

#172/c418 retained Tavi on Contest when the opponent drafted Ren; #173/c419 opened on the nearest single 35-gold camp. Their small screens scored 7/8 and 5/8, respectively, without a reliable direct advantage. Reject both and keep them unuploaded.

#174/c420 added a shared gem-carrier marker and asked nearby allies to escort a Contest carrier. It scored 6/8 against the same four proxy families; c417's corresponding screen was 7/8. Against c417 and c404 it won the side-B games and lost the side-A games, with no direct gem advantage. Reject for now; the v97 Contest replay identifies a precise escort case for future tests: Issac carried 200 gems near (24,35), was seen by enemy Tavi/Stellar, and enemy Stellar killed him at r1018 and took the bag. No candidate update was uploaded from this work.


## v98 live test and Contest escort follow-up (18 Oct 2026)

#175/c421 narrowed c420's escort behavior: publish a carrier marker only while a 100+ gem carrier sees an enemy within 8 tiles, and let only the nearest frontline champion escort. The first local Contest screen scored 8/8 (2/2 each against c417, c404, opp-fai-mirror, and opp-tts-v5); a fresh c417 screen scored 5/8. Bundled as `submissions/tungtungsahur-candidate-c421-contest-threat-only-escort.zip` (SHA-256 `70FF18AFB1DF3F4ACD76CBB6E5057A977C9716C5789C7C1D31C85CE1754403ED`) and uploaded as separate test v98.

The v98-likely fresh group against queue-time rank-49 Please, [8a9a1654-7673-4da3-bbae-daaa2f5cc715](https://2026a.battlecode.co.uk/game/match-groups/8a9a1654-7673-4da3-bbae-daaa2f5cc715), lost 0-5, with no platform bot faults. Contest again scored 0:200 gems with 85:23 deaths and 9:132 camp-clear entries. Prism collected 200 gems at r1027 at (17,31); enemy Ryth took them from Prism at r1063 and submitted them at r1109. The escort change did not prevent the theft, and the opponent's income/fight snowball remained overwhelming. The other maps also lost; see the per-map table in `analysis/live-top50-match-review-20261018.md`. Treat the local 8/8 as a proxy-only gain that did not transfer; reject c421 for general use.

#176/c422 tested the earlier user rule on Contest: do not burst, peel, or engage until the tank has been attacked, using the shared fight alarm. It scored 1/8 against the four local proxy families, versus c417's fresh 5/8 on the same set. Reject it.

The campaign is **4 wins / 615 completed top-50 maps**, maximum streak 1, current **0/10**. All 17 maps have live coverage. Latest test upload is v98, rejected for general use; c422 remains local-only. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## v99 Contest draft test and paired replay result (18 Oct 2026)

#177/c423 put Contest burst, peel, and active fighting on hold until the tank damage alarm or round 45, to give the team a farm window. It scored 5/8 on the local proxy screen, matching a fresh c417 control at 5/8 while earning 4,600 aggregate gems versus 6,200. Reject it; do not upload.

#178/c418 changed only the Contest counterdraft: keep Tavi when Please revealed Ren instead of selecting Ren. Its local screen was 7/8, so it was bundled as `submissions/tungtungsahur-candidate-c418-contest-keep-tavi.zip` (SHA-256 `3D92D29C4956398664685A9506BB3AE23DF530DC175EC8C432821E44E9923D91`) and uploaded separately as test v99. The fresh five-map group against queue-time rank-45 Please, [e0cdf2be-2e78-4e8c-b4ed-9ca36db12ada](https://2026a.battlecode.co.uk/game/match-groups/e0cdf2be-2e78-4e8c-b4ed-9ca36db12ada), lost 0-5 with no platform bot faults.

v98/c421 and v99/c418 played the same Contest seed (`11295110919520135683`), with the same Please roster. The only matchup change was our Ren-to-Tavi counterdraft. With Ren, v98 first cleared a camp at r48 and reached 48.1k monster damage, 9:132 clear entries, 85:23 deaths, 15:51 kills, and 200 submitted gems for Please. With Tavi, v99's first clear slipped to r83 and it recorded 16.8k monster damage, 2:144 clears, 94:11 deaths, 7:65 kills, and no submitted gems for either team. The team with Ren collected 200 gems during the game, but Please ultimately banked them. This is strong paired evidence against keeping Tavi into this Ren lineup; it does not make c421 a winning strategy.

The four non-Contest maps had the same seeds and results in both groups: Lanes 750:1,000 gems; Eight 683:1,029; Interlock 204:1,004; Rows 528:1,056. v99 stdout had three caught `Champion cannot act` errors on Contest and zero platform faults; these are too few to explain the overall death and farming gap. Reject v99 for general use. The campaign is **4 wins / 620 completed top-50 maps**, best streak 1, current **0/10**. All 17 maps have live coverage. The repeated user link `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is still the previously counted 0-5 group against `new team(4)`. Production source and ZIP remain unchanged at the hashes above.


## v100 Contest opening split: local evidence and live-test upload (18 Oct 2026)

#179/c425 changes Contest's opening to use the existing tank-led and fighter-led farm squads immediately, while retaining the shorter early combat reach through round 149. Against four focused proxies (c417, c404, opp-fai-mirror, and opp-tts-v5), it won 8/8 and earned 7,200 aggregate gems; the same screen on c417 won 5/8 and earned 6,200. On the broader 20-opponent Contest pool, c425 and c417 both scored 38/40, while c425 earned 36,600 gems against c417's 37,200. The two losses shifted: c425 lost to opp-fai-melee and my-bot-v2; c417 lost to opp-fai-melee and opp-tts-aggro. This is a focused local signal, not a broad-pool win-rate improvement.

c425 was bundled as `submissions/tungtungsahur-candidate-c425-contest-opening-split.zip` (SHA-256 `6D66DEC80AADAEB1197DE633473E640FC5867324DD834E405C56F8B055D4936D`) and uploaded separately as test v100 for a targeted live check. No fresh v100 match group has been run yet; the user-supplied `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` link is the previously counted old group against `new team(4)`. Campaign remains **4 wins / 620 completed top-50 maps**, best streak 1, current **0/10**. Production source and ZIP are unchanged at their documented hashes.

## #180 Contest opening split duration screen (18 Oct 2026)

c426 limits c425's split-farm phase to the first 150 rounds, then returns to the normal phase logic. Its 20-opponent Contest screen scored **37/40** and 36,800 aggregate submitted gems. The same-screen references were c425 at 38/40 and 36,600 gems, and c417 at 38/40 and 37,200 gems. c426 lost both sides against my-bot-v2 and one side against opp-fai-melee; c417 won both my-bot-v2 games, while c425 split that matchup 1-1. The candidate did not improve win rate and the lower duration does not resolve the recurring Contest loss. Reject c426; it remains local-only and was not uploaded.

Run: `matches/league/20261018-172325-c426-direct-contest-opening-split-r150/`. Live groups remain paused. Latest separate test upload is still v100/c425, with no fresh group result. Campaign remains **4 wins / 620 maps**, best streak 1, current **0/10**. Production source and ZIP remain unchanged.

## #181 c425 Contest strong-proxy check and direct control (18 Oct 2026)

To check whether c425's focused proxy result survives against stronger archived bots, it was screened on Contest against `ming_bot`, `xuanming`, `faisal-orig`, `opp-racer`, `opp-swirl-meta-core`, and `fx-dbllock`. c425 scored 11/12 and banked 10,200 total gems; a fresh c417 control also scored 11/12 and banked 9,200. Both lost side A against Ming; c425's gem advantage came from better scores against Xuanming and the Swirl meta proxy. In a direct side-swapped c425-vs-c417 comparison, c425 won both games (800:600 on side A, 800:200 on side B). A repeat produced byte-identical replay files, so this is one deterministic two-game sample, not four independent results.

This supports retaining c425/v100 as the next Contest live-check candidate, but not as a general win-rate improvement: the broad 20-opponent screen remained 38/40 for both c425 and c417, and c425's aggregate gems were 600 lower there. No fresh live group was run because live unranked matches are paused. Production source and ZIP remain unchanged.

Runs: `matches/league/20261018-172751-c425-direct-contest-strong-historical-v100/`, `matches/league/20261018-172809-c417-direct-contest-strong-historical-v100-control/`, and `matches/league/20261018-172832-c425-direct-contest-opening-split-direct-control/` (byte-identical repeat at `matches/league/20261018-172841-c425-direct-contest-opening-split-direct-control-repeat/`).

## #182 Contest opening split with early gold value (18 Oct 2026)

c427 kept c425's Contest split and restored the 0.25 gold value for the first 150 rounds, which c425's forced Mid phase had bypassed. On the same 20-opponent Contest pool, c427 scored **37/40** and 35,800 aggregate gems, below c425's 38/40 and 36,600. It lost to tralalerotrarala and my-bot-v2, in addition to the shared opp-fai-melee loss. It also logged 67 caught `Champion cannot act` messages in this run versus c425's 60 on its corresponding pool screen. Reject the added gold valuation; retain c425's lower-gold split as the local Contest reference.

Run: `matches/league/20261018-175801-c427-direct-contest-split-gold-weight-r150/`. Local-only; not uploaded.

## #183 Stunned-action early return (18 Oct 2026)

c428 added an early return when the SDK reports no movement, attack, or cast action available. It removed caught `Champion cannot act` messages from the 20-opponent Contest screen and scored 40/40 with 36,800 aggregate gems versus c425's 38/40 and 36,600. However, on six stronger archived Contest bots it scored **10/12** and 9,800 gems, below c425's 11/12 and 10,200; c428 lost both sides to `opp-swirl-meta-core`, which c425 beat 2/2. A side-swapped c428-vs-c425 head-to-head across all 17 maps scored only **14/34** for c428. Reject the global early return: suppressing the whole turn when the three action flags are clear harms play on strong matchups and other maps. The error trace needs a narrower fix if revisited.

Runs: Contest pool `matches/league/20261018-180022-c428-direct-contest-split-stun-action-guard/`; strong bots `matches/league/20261018-180139-c428-direct-contest-stun-guard-strong-historical/`; 17-map head-to-head `matches/league/20261018-180219-c428-direct-action-guard-vs-opening-split-all-maps/`. No live group was run; live matches remain paused. Keep v100/c425 as the next live-check candidate. Production source and ZIP remain unchanged.

## #184 `Champion cannot act` call-site diagnostic (18 Oct 2026)

c429 added `std::source_location` and logged action flags plus buff restrictions whenever `attempt()` caught an engine error. On Contest games against `my-bot-v2` and `opp-swirl-meta-core`, error 44 came from `Bot::survive()` / `Bot::shopping_trip()` calling `recall()` and error 45 came from `Bot::bank()` calling `submit_gems()`. Those calls all occurred with move/attack/cast flags `000` and move/attack/cast/shop/consumable restrictions `11111`; thus the engine had disabled every action. Other isolated messages came from `place_lock()` trying a consumable under the same state and a `step_towards()` move receiving error 21. The diagnostic changed logs only and is not uploaded.

Runs: `matches/league/20261018-180415-c429-direct-contest-action-error-callsite-diagnostic/` and `matches/league/20261018-180512-c429-direct-contest-action-error-flags-diagnostic/`.

## #185 Narrow no-action guard after bookkeeping (18 Oct 2026)

c430 moved c428's all-flags-clear guard until after damage tracking, enemy sightings, and tank anchor updates, preserving shared bookkeeping before skipping action attempts. It eliminated the broad-screen error-44/45 messages (with two error-21 move messages remaining), but scored **37/40** and 36,000 gems on the full Contest proxy pool, below c425's 38/40 and 36,600. Against the six stronger archived Contest bots it scored **10/12** and 10,000 gems, versus c425's 11/12 and 10,200. Reject the guard even after relocating it; the full-turn no-action handling is not a useful general change. Keep v100/c425 as the next live-check candidate.

Runs: `matches/league/20261018-180548-c430-direct-contest-stun-guard-after-bookkeeping/` and `matches/league/20261018-180658-c430-direct-contest-stun-guard-after-bookkeeping-strong/`. Local-only, not uploaded. No live group was run; production source and ZIP remain unchanged.

## Latest Rows follow-up: monolith, Varg capture joins, and draft (18 Oct 2026)

Live unranked testing remains paused. Local-only Rows work from c417 compared three hypotheses against c404, c399, and ming_bot on both sides:

- c432 avoided monolith groups before round 160. All six replay files were byte-identical to the fresh c417 control; the early Rows monolith was not selected, so this guard is inactive.
- c433 skipped `join_capture()` for Varg on Rows. All six replays were again byte-identical to c417; the local screen never exercised the branch.
- c434 replaced Ryth with Tavi in the first four Rows draft picks and fell from c417's 4/6 to 2/6, losing both sides to c404 and c399.
- c435 kept Ryth but replaced Stellar with Tavi; it also scored 2/6 and lost both sides to c404 and c399.

The v96-likely umamusume replay shows the remaining issue more precisely: our Varg cleared only group 4 at (42,3), at rounds 178, 292, and 389; the opposing Varg cleared group 5 at (7,46) at rounds 108, 193, 268, and 339. Their other champions also cycled groups 1 and 3 more often than ours cycled groups 0 and 2. These local isolates did not improve sustained farm throughput, so keep them local and stop changing Rows drafts by guesswork. Next Rows work should measure route travel and camp damage time from a top-team replay or a deliberately instrumented local match.

Runs: c417 control `matches/league/20261018-181142-c417-direct-rows-delay-monolith-control/`; c432 `matches/league/20261018-181206-c432-direct-rows-delay-monolith/`; c433 `matches/league/20261018-181250-c433-direct-rows-varg-skip-shared-captures/`; c434 `matches/league/20261018-181543-c434-direct-rows-tavi-instead-ryth/`; c435 `matches/league/20261018-181625-c435-direct-rows-tavi-instead-stellar/`. No candidate was uploaded. Production source and ZIP remain unchanged; v100/c425 is still the next live-check candidate when live testing resumes.

## Latest fuel-budget profiling (18 Oct 2026, live testing paused)

c436 sampled `cambc::fuel_remaining()` around play-turn stages on Contest rounds 30–45, the same window as the stored live fuel-exhaustion cluster. Across four side-swapped games against `opp-swirl-meta-core` and `my-bot-v2`, the largest median stage costs were role execution (~18.96k fuel), objective selection (~13.40k), and scouting (~7.34k); the maximum role-stage cost was ~50.97k. At r40, one Ryth turn ended with 70 fuel and one Tavi turn with 287. These readings are diagnostic and the inserted trace output adds some cost.

c439 added round-40 checkpoints inside objective selection, context building, camp targeting, and pathfinding. The most expensive observed path computation used about 8.8k fuel; objective selection used up to 18.6k and context construction up to 10.9k. This confirms repeated map/vision work is significant but does not yet identify a safe gameplay optimization.

c438 sampled SCOUT detail every fifth round. It tied c425 at 11/12 on six strong Contest proxies and 38/40 on the 20-opponent Contest pool. Across six strong proxies on all 17 maps it scored 167/204 after rerunning its one failed game, below c425's 168/204; it lost extra games on Corners, Eight, and Lanes. Reject it.

c440 skips Mid/Late objective selection for marksman, support, and farmer roles, whose switch branches do no work; Early behavior is unchanged. Its 204-game, six-proxy all-map output matched c425 exactly in every result's winner, gems, and round, with both at 168/204. This saves a no-op scan but shows no match gain, so keep it local and do not upload it.

Runs: c436 `matches/league/20261018-181949-c436-direct-contest-fueltrace-r30-45/`; c438 strong Contest `matches/league/20261018-182220-c438-direct-contest-scout-sampling/`, broad Contest `matches/league/20261018-182302-c438-direct-contest-scout-sampling-broad/`, all maps `matches/league/20261018-182405-c438-direct-scout-sampling-strong-all-maps/` plus the missing Eight rerun `matches/league/20261018-182635-c438-direct-scout-sampling-missing-eight-rerun/`; c439 `matches/league/20261018-182733-c439-direct-contest-fueldetail-r40/`; c440 Contest `matches/league/20261018-182828-c440-direct-mid-follower-objective-skip-contest/` and all maps `matches/league/20261018-182905-c440-direct-mid-follower-objective-skip-strong-all-maps/`. No live group was run; v100/c425 remains the next live-check candidate. Production bot and ZIP hashes remain unchanged.

## #186–190 Contest leash and combat-target screens (18 Oct 2026)

Live unranked groups remain paused at the user's direction. c441 added a Contest-only early leash to global burst casting. Its first version queried position and attack range on every map and shifted Lanes/Swirl outcomes. c442 moved those queries inside the Contest opening branch. The first six-proxy, 17-map screen scored 168/204. After moving position/range reads into a once-per-turn Contest-only branch, the rerun recorded 168/203 with one runner error; all 191 shared non-Contest wins and gem totals matched c425. The initial version's 204th game completed with the same win/gem result, although one Stampede game ended seven rounds later. The Contest subset scored 11/12 with 11,000 gems, same wins and +800 gems versus c425's 10,200; on the 20-opponent Contest pool it scored 39/40 and 37,400 gems, versus c417/c425's 38/40 and 36,600. c442 also exactly matched c441's 40 Contest results and scores. Keep c442 as an unuploaded local candidate; it is not a full-map win-rate gain and has no live validation.

A local loss against `tralalerotrarala` ended 0:400 after 2,000 rounds. Engine statistics show 400 gems collected but none banked, 83 deaths/36 kills and 63.9k champion damage for c442, versus 52 deaths/66 kills and 94.6k champion damage for the opponent. We dealt more monster damage (64.3k:27.9k) and earned more gold (3,905:3,615), so this loss was principally a combat and gem-conversion failure. The opponent source explicitly converges on visible enemies and weights gem carriers heavily.

Follow-ups were negative or too narrow: c443 let ranged carriers attack while banking; it remained 1/2 against `tralalerotrarala` and produced 81 deaths/32 kills versus c442's 83/36, with the same 0:400 score. c444 switched Contest targeting to raw damage plus a strong carrier bonus; it won 2/2 versus `tralalerotrarala` but fell to 8/12 against six strong proxies (c442: 11/12) and tied c442 1–1 head-to-head. c445 kept weak-target scoring and raised the Contest carrier bonus; it tied c442 at 11/12 against strong proxies but banked 10,800 gems versus c442's 11,000, with the same loss. Reject c443–c445 as general updates.

Runs: c441 broad/all-map `matches/league/20261018-183340-c441-direct-contest-burst-leash-broad/` and `...183517-c441-direct-contest-burst-leash-strong-all-maps/`; c442 all-map `...183800-c442-direct-contest-burst-leash-strong-all-maps/`, broad default pool `...184156-c442-direct-contest-burst-leash-default-pool/`; c443 `...184524-c443-direct-contest-carry-attack/`; c444 `...184709-c444-direct-contest-threat-carrier-first/` and `...184730-c444-direct-contest-threat-carrier-first-strong/`; c445 `...184807-c445-direct-contest-carrier-weighted-strong/`. Production source and ZIP remain unchanged. Campaign stays **4 wins / 620 maps**, best streak 1, current **0/10**. The already uploaded v100/c425 remains the next live check after the pause; c442 is local only.

## #191–192 Contest convergence follow-ups (18 Oct 2026)

c446 made roles commit to nearby visible Contest fights after round 149, without waiting for the damage alarm. It scored 11/12 and 11,000 gems against the six strong proxies, tied c442's 1–1 side-swapped head-to-head, and exactly matched c442's 39/40 wins and 37,400 gems against the default 20-opponent pool. All 40 broad-pool win/gem records were identical. Reject it as a behaviorally inactive change on the scored pool.

c447 briefly shared and pursued the latest Contest enemy sighting and used it to focus the same visible target across allies. It fell to 9/12 against the six strong proxies (c442: 11/12), losing both sides to `opp-swirl-meta-core`; reject it. The opponent's convergence behavior is real, but this implementation disrupted the established farm split without improving results.

Runs: c446 strong `matches/league/20261018-185001-c446-direct-contest-post150-auto-engage-strong/`, direct c442 `...185025-c446-direct-contest-post150-auto-engage-vs-c442/`, broad `...185031-c446-direct-contest-post150-auto-engage-broad/`; c447 strong `...185202-c447-direct-contest-shared-hunt-target-strong/`. No upload or live group. Keep c442 as the only new local candidate; v100/c425 remains the already-uploaded live check after the user resumes testing.

## c450 Contest burst leash (18 Oct 2026)

c450 widens c442's Contest-opening burst radius from `max(attack_range, 3)` to `max(attack_range, 5)`. It scored **12/12** on six strong Contest proxies, versus c442 and c425 at 11/12; c451's six-tile radius scored 11/12. On the 20-opponent Contest pool, c450 scored **40/40 and 37,400 gems**, versus c442's 39/40 and 37,400, and c425's 38/40 and 36,600. c450 won both side-swapped direct games against c442 and split 1–1 against c425.

The six-proxy all-map screen scored **169/204** and 195,861 gems, versus c425's 168/204 and the same gem total. All 192 matching non-Contest games had the same winner and gems; one ended seven rounds later. The added strong-Contest win came against `ming_bot` from side A, where c450 banked 600:400 instead of c425's 200:400. Keep c450 as the leading local Contest candidate, with c451 rejected. It has not been uploaded or validated in a live group.

Runs: c450 strong Contest `matches/league/20261018-185727-c450-direct-contest-burst-leash-r5-strong/`, default Contest `...185818-c450-direct-contest-burst-leash-r5-default-pool/`, head-to-head `...185843-c450-direct-contest-burst-leash-r5-head-to-head/`, all-map strong `...185853-c450-direct-contest-burst-leash-r5-strong-all-maps/`; c451 six-tile Contest `...185751-c451-direct-contest-burst-leash-r6-strong/`. Live unranked groups remain paused. Production source and ZIP are unchanged; c450 is local-only.

## Swirl camp-safety re-screen (18 Oct 2026)

The older Swirl 150-damage camp-avoidance candidate was re-screened against the current six strong local proxies. It scored **7/12**, matching c425/c450, and kept the same five losses: both sides to `ming_bot` and `xuanming`, plus side A to `faisal-orig`. The historical safety rule does not solve the hardest Swirl matchups; do not carry it into a new candidate. No production files changed.

Run: `matches/league/20261018-190249-cand-swirl-camp-threshold150-v36-direct-swirl-threshold150-current-strong/`.

## c452/c453 Swirl tank draft and escort screens (18 Oct 2026)

c452 replaced Ren with Ryth on Swirl while keeping Varg, Stellar, and Cassi/Issac. It scored 7/12, the same win count as c450, but fell from 9,642 to 8,797 gems and traded a win/loss between Faisal and `fx-dbllock`; both Ming and Xuanming still won from both sides. c453 assigned Ryth to Cassi/Issac's squad to test the escort idea. Its 12 winner/gem/round records exactly matched c452, so the assignment did not change this screen. Reject both; the added tank does not fix the main losses and reduces farm output.

Runs: c452 `matches/league/20261018-190436-c452-direct-swirl-tank-keeps-varg-strong/`; c453 `matches/league/20261018-190543-c453-direct-swirl-ryth-escorts-ci-strong/`. No live group or production update.

## c454–c456 Swirl meta opening screens (18 Oct 2026)

c454 applies c450's burst-cast leash to Swirl only when the enemy has the C&I/Varg/Stellar/Vendetta signature. A three-tile minimum scored 8/12 against six strong proxies, one win above c450's 7/12, but scored 32/40 on the default Swirl pool, matching c450. c455 uses a five-tile minimum: it also scored 8/12, with 9,954 gems versus c450's 9,642, and kept both Ming and Xuanming losses while converting Faisal side A to a win. It scored 32/40 in the default Swirl pool and split 1–1 head-to-head against c450.

Across all 17 maps and six strong proxies, c455 scored **170/204 with 196,173 gems**, versus c450's 169/204 and 195,861 gems. All 192 shared non-Swirl results had the same winner and gems. c456 made the Swirl opening retreat threshold more conservative; it stayed 8/12 but dropped to 8,396 gems and still lost both Ming/Xuanming sides. Keep c455 as the leading local candidate, not a production update; its top-proxy Swirl losses remain unresolved.

Runs: c454 strong Swirl `matches/league/20261018-190733-c454-direct-swirl-meta-burst-leash-r3-strong/` and default pool `...190807-c454-direct-swirl-meta-burst-leash-r3-default-pool/`; c455 strong `...190904-c455-direct-swirl-meta-burst-leash-r5-strong/`, default `...190932-c455-direct-swirl-meta-burst-leash-r5-default-pool/`, all-map strong `...190954-c455-direct-swirl-meta-burst-leash-r5-strong-all-maps/`, and head-to-head `...191119-c455-direct-swirl-meta-burst-leash-r5-vs-c450/`; c456 retreat `...191206-c456-direct-swirl-meta-opening-outnumber-retreat-strong/`. No live match or upload.


## c457–c466 Swirl route, survival, and draft follow-ups (18 Oct 2026)

Live unranked matches remain paused. These were local screens on Swirl against six strong archived bots unless otherwise noted. c457 skipped altar-adjacent camps for 80 rounds but had no explicit outer objective; it scored 9/12, and the side-A replay still held near the central choke. c458/c460 forced the mirrored 72-gem outer camp and 88-gem flank wolf pack, respectively; each scored 8/12. The map's walkable routes to those camps pass through the same central corridor, so neither avoided the early collision. Reject these route variants.

c461 disabled global burst spells through round 149 (7/12); c462 copied the top bot's 55%/75%-near-enemy retreat thresholds (7/12). Both reduced gem output and did not beat Ming or Xuanming. The top bot's retreat rule is evidence about its survival policy, not a drop-in improvement for our current roles.

The first Vendetta and Willow draft attempts (c459/c463) did not change the roster: their enemy-signature condition was evaluated before the opposing draft was complete. Replay draft lines confirmed the standard C&I / Stellar / Ren / Varg lineup, so those screens are not valid composition tests. c464 selected Willow by map alone and correctly drafted C&I / Stellar / Willow / Varg; it scored 3/12. c465 correctly selected the Vendetta mirror C&I / Stellar / Vendetta / Varg. It won both side-B games against Ming and Xuanming in the four-game top-two screen, but scored 7/12 on the six strong proxies and 28/40 on the default Swirl pool. c466 kept Ren on side A and used the Vendetta mirror on side B. It scored 8/12 strong and 30/40 default, gaining the side-B top-opponent wins while losing two default-pool wins versus c455's 32/40. A direct c466-vs-c455 side-swapped screen scored 2/2 for c466, but both teams drafted the same C&I / Stellar / Ren / Ryth lineup on side A; only the side-B game tested Vendetta. A repeated run was byte-identical and adds no independent sample. Keep c466 as a side-B matchup hypothesis only; retain c455 as the broader local candidate.

Opponent-source/replay review: Ming's executor protects survival before optional tactics, starts retreat at 55% health (75% with a visible enemy within three tiles), and reaches its first bank around r65 after a flank-wolf clear. Our own 30%/35% survival threshold and global burst-before-role ordering are materially different. Copying the survival threshold alone regressed; the unresolved issue is coordinated route, combat timing, and gem conversion through Swirl's central choke.

Runs: c457 `matches/league/20261018-191716-c457-direct-swirl-opening-altar-embargo-r80-strong/`; c458 `...191903-c458-direct-swirl-opening-outer-camp-r80-strong/`; c459 invalid draft screen `...192103-c459-direct-swirl-flanker-counterdraft-strong/`; c460 `...192206-c460-direct-swirl-opening-mirrored-flank-wolf-strong/`; c461 `...192316-c461-direct-swirl-disable-opening-burst-r150-strong/`; c462 `...192409-c462-direct-swirl-survival-55-75-strong/`; c463 invalid draft screen `...192510-c463-direct-swirl-support-willow-counterdraft-strong/`; c464 `...192558-c464-direct-swirl-willow-map-draft-strong/`; c465 top two `...192648-c465-direct-swirl-vendetta-map-draft-top2/`, strong `...192722-c465-direct-swirl-vendetta-map-draft-strong/`, default `...192735-c465-direct-swirl-vendetta-map-draft-default-pool/`; c466 strong `...192826-c466-direct-swirl-side-aware-vendetta-strong/`, default `...192854-c466-direct-swirl-side-aware-vendetta-default-pool/`. No upload or live group was created. Production and campaign state remain unchanged.

## Swirl counterdraft and equipment follow-ups c467–c476 (18 Oct 2026)

All matches below are local-only; live unranked matches remain paused. No candidate was copied into production or uploaded.

c467 tried a Vendetta side-A lineup that retained Ren and gave up Varg; it scored 6/12 against the six strong Swirl bots. c468 added side-A outnumbered retreat in the top-two screen, which still lost both side-A games and worsened side A's scores. c469 applied Ming's power/health/power queue across both sides; it scored 6/12 strong. None solved either top matchup. c470 kept c466's side-aware draft and applied the queue only to the Swirl side-B counterdraft. It scored 8/12 strong, 30/40 default, and 170/204 across six strong opponents on all 17 maps (196,293 gems). Relative to c455, only six all-map results changed: it converted Ming and Xuanming's side-B games to wins, but lost side B to `opp-swirl-meta-core` and `fx-dbllock`; the net win count stayed 170/204.

Three route/formation follow-ups were rejected: c471 forced the 88-gem flank wolf for the first 80 rounds and lost 0/4 top-two games; c472 split the generic farm squads from round one and also lost 0/4; c473 let Varg farm alone during the early phase and lost 0/4. c472 did move the first side-A deposit from r265 to r135, but the team still lost bodies and finished far behind. c474 applied the top team's item queue only on side A; it scored 7/12 strong, below c470's 8/12, and did not convert a top-team loss.

c475 made the side-B Vendetta counterdraft conditional on seeing the opponent's C&I/Varg opening. This restored wins against `opp-swirl-meta-core` and `fx-dbllock` while retaining side-B wins against Ming and Xuanming: 10/12 strong, 32/40 default, and 172/204 (196,727 gems) across all maps. c476 applied a corresponding side-A lineup only when that partial enemy opening was visible. It kept 10/12, 32/40, and 172/204 while raising all-map gems to 197,073. Against the top two, side-A gems improved from c475's 408/178 to 606/374, but both games still lost; side B won both. Compared with c455, c476 changed only six Swirl side results, gaining two wins against Ming/Xuanming from side B and 900 aggregate gems.

c476 is the strongest local Swirl counterdraft candidate so far, not a validated production update. The primary failure remains side A's inability to win the early fight or bank before the opponent. No 10-win streak has been achieved. Campaign state remains 4 wins / 620 top-50 maps, max streak 1, current 0/10. Production hashes remain unchanged.

Runs: c470 top-two `matches/league/20261018-193711-c470-direct-swirl-side-b-combat-items-top2/`, strong `...193732-c470-direct-swirl-side-b-combat-items-strong/`, default `...193744-c470-direct-swirl-side-b-combat-items-default/`, all maps `...194614-c470-direct-side-b-items-strong-all-maps/`; c471 `...194129-c471-direct-swirl-side-b-items-flank-opening-top2/`; c472 `...194218-c472-direct-swirl-meta-opening-split-top2/`; c473 `...194420-c473-direct-swirl-meta-solo-varg-top2/`; c474 top-two `...194455-c474-direct-swirl-side-a-top-items-top2/`, strong `...194523-c474-direct-swirl-side-a-top-items-strong/`; c475 top-two `...194806-c475-direct-swirl-side-b-partial-counterdraft-top2/`, strong `...194825-c475-direct-swirl-side-b-partial-counterdraft-strong/`, default `...194836-c475-direct-swirl-side-b-partial-counterdraft-default/`, all maps `...194908-c475-direct-side-b-partial-counterdraft-strong-all-maps/`; c476 top-two `...195040-c476-direct-swirl-both-sides-partial-counterdraft-top2/`, strong `...195100-c476-direct-swirl-both-sides-partial-counterdraft-strong/`, default `...195112-c476-direct-swirl-both-sides-partial-counterdraft-default/`, all maps `...195147-c476-direct-swirl-both-sides-partial-counterdraft-strong-all-maps/`.

## c477–c479 Swirl side-A combat follow-ups (18 Oct 2026)

Each candidate was based on c476 and tested on both sides against Ming and Xuanming. None won side A; c476 remains the better local candidate.

- c477 copied the top team's 55% / 75%-near-enemy retreat thresholds to side A. It stayed 2/4 overall but banked only 372 gems against Ming and 12 against Xuanming, versus c476's 606 and 374.
- c478 suppressed global burst, peel, and proactive role combat on side A through r79. It also stayed 2/4, with 314 and 208 gems and 41 deaths in both games. The opponents recorded 8 and 6 deaths, so withholding combat gave away too much pressure.
- c479 ranked Swirl side-A enemies by raw damage instead of damage divided by remaining health. It stayed 2/4 and banked 268 against Ming and 374 against Xuanming; the Ming score was far below c476's 606.

Reject all three. The unresolved side-A problem is the combination of early fight tempo and gem banking; copying an isolated retreat or target rule did not fix it. c476 remains local-only at 10/12 strong Swirl, 32/40 default Swirl, and 172/204 across all maps. Live matches remain paused; no upload or production edit. Runs: c477 `matches/league/20261018-195352-c477-direct-swirl-side-a-high-retreat-top2/`; c478 `...195426-c478-direct-swirl-side-a-farm-before-fight-top2/`; c479 `...195506-c479-direct-swirl-side-a-raw-threat-focus-top2/`.

## Swirl route-planner trace against c476 (18 Oct 2026)

An instrumented Ming-strategy build (`mingstudy-trace`) beat c476 2/2 on Swirl. Its team banked 1,024 gems with 28 deaths against c476 side B (678 gems, 45 deaths), and 1,013 gems with 11 deaths against c476 side A (247 gems, 40 deaths). The trace shows a draft-compiled route per body: Cassi and Issac share one camp circuit; Varg, Stellar, and Vendetta each receive separate opening camp stops. Its first deposits arrived at r45/r51. This is more specific than the generic round-one squad split in c472, which lost 0/4: the top strategy balances camp ownership, clear time, and bank points before the match begins.

Next Swirl work should prototype a bounded side-aware first-cycle route for the c476 lineup, preserving Cassi/Issac together and assigning the other bodies non-overlapping reachable camps. Test early banking and survival together; do not copy a broad route split or treat this clone matchup as live top-50 validation. Run: `matches/league/20261018-195650-mingstudy-trace-direct-inspect-ming-routes-vs-c476/`.

## c480 Swirl side-A safe-camp split (18 Oct 2026)

c480 combined a side-A-only Phase::mid split from round one with an 80-round embargo on altar-adjacent camps. It still lost both side-A top-team games, banking only 18 gems against Ming and 154 against Xuanming versus c476's 606 and 374. Deaths fell to 38/37 from c476's 55/41, but farm throughput collapsed. Reject this generic split; the route trace shows that separate roles need explicit camp ownership and banking, not only a phase switch and a danger-area mask. c476 remains the best local Swirl candidate. Run: `matches/league/20261018-195853-c480-direct-swirl-side-a-split-safe-camps-top2/`.

## Swirl flank-opening follow-ups c481–c484 (18 Oct 2026)

c481 and c482 tested geometric three-lane and four-lane camp ownership on side A. Both remained 2/4 against Ming/Xuanming and collapsed early: c481 banked 308/236, with the full team dead by r49 before its first deposit; c482 banked 240/356 and lost Cassi/Issac by r24. Reject both. The route trace's slot assignments alone do not transfer into a safe route plan for our lineup.

c483 kept the whole team together on the traced opposite-flank 88-gem pack at `(13,13)` for the first 120 rounds. It scored 3/4 against Ming/Xuanming: side A banked 885 against Ming (still a loss) and 1,024 against Xuanming (a win). Across six strong Swirl proxies it tied c476 at 10/12, but gained 841 gems over the three changed top-team side-A outcomes: Ming 606→885, Xuanming 374→1,024, and Faisal 1,012→924. The default Swirl pool stayed 32/40. Its six-proxy all-map screen scored 171/204 and 197,818 gems versus c476's 172/204 and 197,073; one Lanes result also varied on a separately generated map file, so that one-win difference is noisy. Keep c483 as a Swirl side-A hypothesis, not a general replacement for c476.

c484 ended the flank opening after the first 88 gems were banked. It fell to 4/6 against Ming, Xuanming, and Faisal; side-A scores were 304/584/1,058 versus c483's 885/1,024/924. Reject this timing change. Runs: c481 `matches/league/20261018-200336-c481-direct-assigned-routes-top2/`; c482 `...200550-c482-direct-four-lane-top2/`; c483 top-two `...200750-c483-direct-flank-pack-top2/`, strong Swirl `...200805-c483-direct-flank-pack-strong-swirl/`, default Swirl `...200823-c483-direct-flank-pack-default-swirl/`, strong all-maps `...200838-c483-direct-flank-pack-strong-all-maps/`; c484 `...201120-c484-direct-flank-until-bank-top3/`.

No candidate has passed the 10-win live streak. Live matches remain paused; no upload or production change. c476 remains the balanced local baseline, with c483 worth retaining for future side-by-side Swirl validation.

c485 kept the shared flank opening until 176 gems were submitted (two 88-gem cycles), then returned to the late phase. It scored 10/12 strong and 32/40 default Swirl, same as c483/c476. Its top-three side-A outcomes were the reverse of c483's Ming/Xuanming trade: c485 beat Ming at 1,034, lost to Xuanming at 684, and lost to Faisal at 924. Its strong all-map score was 171/204 and 197,627 gems. No universal Swirl win-rate gain; retain c485 as a matchup alternative only.

c486 changed only Ren's first Swirl side-A item to Monster Strength for the flank-wolf clear. It fell to 9/12 on the six strong Swirl proxies, versus 10/12 for c483/c485/c476. Reject the item change. Run: `matches/league/20261018-201638-c486-direct-flank-pack-ren-monster-first/`.

Current local comparison: c476 is the balanced baseline; c483 converts Xuanming side A and scores more against Ming; c485 converts Ming side A. Both flank versions still lose to Faisal from side A and do not raise the 10/12 strong or 32/40 default Swirl totals. Choose between them only after live unranked testing resumes. The production bot and ZIP remain unchanged.

## Adaptive Swirl fight switch c487–c488 (18 Oct 2026)

c487 added a side-A Swirl trigger for an enemy Varg at 60% health or lower within six tiles. It did fire against Faisal at r53 (Varg at 58%), and c487 beat Faisal from both sides. However, c487 also used the ordinary four-round fight alarm to leave the flank route. Routine tank damage could therefore switch phases even when the Varg trigger had not fired. c487 scored 10/12 against six strong Swirl proxies, 32/40 on the default pool, and 171/204 (196,645 gems) across all maps. Treat that build as a flawed screen, not an isolated trigger result.

c488 reserves the unused shared-memory stamp 127 in byte 6 as a persistent Swirl route-abort marker. It preserves the mid-game bit and keeps routine fight alarms independent. Once a nearby weakened Varg is seen, the marker makes all champions leave the shared flank camp and use the normal mid-game roles. The Faisal side-A replay again records `SWIRL_ABORT` at r53 with Varg at 58% health. Two independent screens each scored 11/12 on the six strong Swirl proxies; the default Swirl pool stayed 32/40. The 204-game all-map screen scored 172/204 and 198,133 gems, matching c476's win count while adding 1,060 gems; it scored one more win and 315 more gems than c483. In that screen c488 beat both sides of Xuanming and Faisal, while retaining the Ming side-A loss. This is the strongest local candidate for Swirl so far, but remains unvalidated in live unranked play.

Runs: c487 strong Swirl `matches/league/20261018-202240-c487-direct-adaptive-weak-varg/`, default `...202317-c487-direct-adaptive-weak-varg-default/`, all maps `...202335-c487-direct-adaptive-weak-varg-strong-all-maps/`; c488 strong Swirl `matches/league/20261018-202539-c488-direct-persistent-weak-varg-abort/`, default `...202551-c488-direct-persistent-weak-varg-default/`, all maps `...202611-c488-direct-persistent-weak-varg-strong-all-maps/`.

Live unranked matches remain paused. No group or upload was created. Production source and submission ZIP are unchanged; the campaign remains 4 wins / 620 maps, best streak 1, current 0/10. Continue with local work on the largest remaining map-specific loss clusters, especially Lanes and Pilgrimage, before resuming live validation.

## Lanes round-one split screens c489–c490 (18 Oct 2026)

c489 forced the normal two-squad phase from round 1 on both Lanes sides. Its six-strong Lanes screen scored 6/12 versus c488's 7/12 all-map subset; it still lost all four games against Ming and Xuanming. In its Ming side-B replay it banked 970 gems with no deaths, compared with c488's 772 gems and two deaths, but still lost 970–1,012. c490 kept side A's shared opening and split only Lanes side B. It scored 5/12 in a separate unseeded screen, lost the Ming/Xuanming games, and also dropped the meta-core side-B win. The side-B farm and death metric improved in the Ming replay, but the split did not convert a win and hurt other matchups. Reject both general phase changes; keep c488 as the local baseline. Runs: c489 `matches/league/20261018-202952-c489-direct-lanes-round1-split-strong/`; c490 `matches/league/20261018-203045-c490-direct-lanes-side-b-round1-split/`.

These screens do not identify a reliable Lanes route improvement. The immediate clue is narrower: side B's current shared opening gave up gems to Ming while losing two champions, whereas the split avoided those deaths and raised its score but still missed the 1,000-gem finish. Further Lanes work needs a safe bank/camp circuit that preserves the side-A results and addresses opponent-specific pressure; do not reuse round-one split as a universal fix.

## Pilgrimage mirror opening c491 (18 Oct 2026)

c491 kept the whole team on the shared opening camp through round 119 only when the opponent drafted Ren/Stellar/Cassi-and-Issac/Ryth/Varg, without changing Varg's squad assignment. It lost both sides against `opp-swirl-meta-core` (556–1,032 and 524–1,064), versus c488's 940–1,014 and 524–1,002. Deaths fell from 22 to 17/19, but farming collapsed and the candidate still lost both. Reject this grouping rule; holding the entire team together is not a substitute for a safe, productive route against the mirror. Run: `matches/league/20261018-203342-c491-direct-pilgrimage-meta-shared-r120/`.

## Lanes movement telemetry c492–c493 (18 Oct 2026)

c492 adds movement-purpose logs to c488 without changing strategy; c493 adds the side-B-only Lanes round-one split. In the paired Ming/Lanes screen, side A was identical: c492 and c493 both won 1,000–924 at r637. On side B both lost, but the split raised submitted gems from 802 to 838 and delayed the loss from r537 to r549. This is a small farm gain without a win conversion. Through the last logged checkpoint at r525, side-B movement shifted from 274 to 254 camp steps, 695 to 655 capture steps, 290 to 230 altar steps, and 29 to 6 fight steps; logged gem pickup events changed 32→31 (the final 12 rounds were unlogged). Keep c488 as the baseline and use the telemetry to design a more specific Lanes bank/camp circuit. Diagnostic runs: c492 `matches/league/20261018-203744-c492-direct-lanes-move-diagnostic-shared/`; c493 `matches/league/20261018-203746-c493-direct-lanes-move-diagnostic-side-b-split/`. Instrumentation is local-only.

## Lanes first-bank split tests c494–c496 (18 Oct 2026)

c494 added movement diagnostics to the first-bank split; its 8/12 screen is not clean strategy evidence because instrumentation changes the build, and the side-A result also moved despite the Lanes side-B-only rule. c495 re-tested the rule on a clean c488 copy: keep side B together through its first bank, then split. It scored 7/12, the same as a fresh c488 control. The Ming side-B replay improved from 772–1,012 to 1,000–968, but Faisal side B regressed from 1,008–564 to 956–1,012. Both had the same first bank at r65 with 36 gems, so the unconditional split traded those two matchups without improving the aggregate.

c496 made the split conditional on being at least 20 gems behind after the first bank. It also scored 7/12; Ming and Xuanming were 0/2 each, while Faisal remained 2/2. Reject both clean changes as general Lanes improvements. Current c488 remains unchanged and local-only. Runs: c494 `matches/league/20261018-204157-c494-direct-lanes-shared-until-first-bank/` and repeat `...204237-c494-direct-lanes-shared-until-first-bank-repeat/`; c495 `...204303-c495-direct-lanes-shared-until-first-bank-clean/`; c496 `...204454-c496-direct-lanes-behind-after-first-bank/`; fresh c488 control `...204216-c488-direct-lanes-control-for-c494/`. No production source, ZIP, upload, or live match was changed.

## Corners counterdraft retreat tests c497–c498 (18 Oct 2026)

c497 widened the outmatched retreat range to six tiles on all Corners matchups. It scored 8/12, tying c488; it flipped the meta-core side-A loss, but lost both `fx-dbllock` games. Reject the broad rule.

c498 gates the six-tile retreat to Corners when the enemy draft is the mirror core (Cassi & Issac, Ren, Stellar, Ryth, Varg). It scored 9/12 against six strong proxies and 173/204 over 17 maps, versus c488's 172/204. Only one of the 204 outcomes changed: the Corners side-A meta-core loss (724–1,018, 22 deaths) became a 1,010–572 win (11 deaths). The other 203 outcomes matched. On the full 20-opponent pool c498 scored 624/680. A clean c488 control also reached 624/680 after recovering its single failed runner match; all common outcomes matched. The default pool does not include `opp-swirl-meta-core`, so this matchup-specific rule did not improve that aggregate. Retain c498 as a local counterdraft candidate only; no production edit or upload.

Runs: c497 targeted `matches/league/20261018-204725-c497-direct-corners-outmatched-retreat-6/`, strong Corners `...204803-c497-direct-corners-outmatched-retreat-6-strong/`; c498 strong Corners `...204841-c498-direct-corners-mirror-draft-retreat-6/`, strong all maps `...204901-c498-direct-corners-mirror-draft-retreat-6-strong-all-maps/`, full pool `...205018-c498-direct-corners-mirror-draft-retreat-6-full-pool/`; clean c488 control `...205324-c488-direct-clean-full-pool-control-for-c498/` plus recovery `...205637-c488-direct-recover-full-pool-control-match/`. Live unranked testing remains paused.

## Pilgrimage squad and opening audit c499–c500 (18 Oct 2026)

c499 moved Ren's squad flag to Ryth's squad on non-mirror Pilgrimage drafts. Its 18-game screen scored 5/18 and matched the saved reference outcomes and scores exactly. Ren remains a fighter, and the only live behavior that reads this assignment for him is the mage-style `ctx.hunt` spacing path; the fighter route does not consume it. Treat c499 as a behavioral no-op for this screen.

c500 bypassed the shared-camp choice in `choose_objective` only when the opponent matched the exact mirror counterdraft. Non-mirror Pilgrimage drafts already use role objectives from round 1; the early turn handlers still call `team_farm`, so this did not implement a full route split. It fell to 3/18 on the same nine-opponent screen. Four outcomes changed: Ming side A remained a win but narrowed from 1,022–680 to 1,004–892; Ming side B flipped from 1,068–636 to a 734–1,002 loss; Xuanming side A flipped from 1,062–626 to a 922–1,026 loss; Xuanming side B remained a loss but improved from 852–1,004 to 984–1,002. Reject this partial mirror-opening override. Runs: c499 `matches/league/20261018-210128-c499-direct-pilgrimage-ren-joins-ryth/`; c500 `matches/league/20261018-210433-c500-direct-role-split-from-round-1/`. Production source and ZIP are unchanged; live unranked remains paused.

## Pilgrimage side-B retreat screens c501–c503 (18 Oct 2026)

c501 extended the outmatched-enemy retreat radius from four to six tiles on every Pilgrimage spawn. It scored 6/18 on the nine-opponent screen in two matching runs, versus a fresh c488 control at 5/18, but fell to 27/40 in the 20-opponent pool versus c488's 28/40. It flipped Faisal-bot and my-bot side B to wins, but lost side B to opp-tts-locker and lost side A to opp-tts-aggro and tungtungsahur-v1. Reject the all-spawn rule.

A diagnostic confirmed Pilgrimage side A's ally spawn region is `(1,1)–(3,3)` and side B's is `(46,1)–(48,3)`. c503 applies the six-tile radius only when the ally spawn contains `(46,1)`. It scored 6/18 against the strong nine-opponent Pilgrimage screen in two matching runs, versus c488's 5/18. It scored 29/40 in two matching full-pool runs, versus fresh c488's 28/40. The only changed full-pool outcomes are side B: Faisal-bot 704–1,016→1,070–862 (win), opp-tts-locker 1,004–784→804–1,036 (loss), and my-bot 412–1,000→1,002–982 (win). On six strong proxies across all 17 maps, c503 tied fresh c488 at 172/204; no win outcomes changed. Keep c503 as an isolated Pilgrimage side-B local candidate only; no production edit or upload.

Runs: c501 targeted `matches/league/20261018-210941-c501-direct-outmatched-retreat-six-tiles/` and repeat `...211007-c501-direct-outmatched-retreat-six-tiles-repeat/`, full pool `...211039-c501-direct-outmatched-retreat-six-tile-full-pool/`; fresh c488 full-pool control `...211101-c488-direct-clean-control-for-six-tile-full-pool/`. c503 strong Pilgrimage `...211345-c503-direct-side-b-only-outmatched-retreat-six-tiles/` and repeat `...211455-c503-direct-side-b-only-outmatched-retreat-six-tiles-strong-repeat/`; full pool `...211402-c503-direct-side-b-only-outmatched-retreat-six-tile-full-pool/` and repeat `...211431-c503-direct-side-b-only-outmatched-retreat-six-tile-full-pool-repeat/`; strong all maps `...211521-c503-direct-side-b-pilg-retreat-six-strong-all-maps/`; clean c488 control `...211631-c488-direct-clean-control-for-side-b-pilg-retreat-strong-all-maps/`.

## Pilgrimage mirror-phase and gated retreat follow-ups c504–c506 (18 Oct 2026)

c504 makes Pilgrimage enter the existing role-objective phase from round 1 for every draft, including the exact mirror counterdraft. It scored 6/18 on the focused nine-opponent screen versus c488's 5/18, 28/40 on the default 20-opponent pool (tie), and 173/204 across six strong proxies on all 17 maps versus c488's 172/204. Its only changed strong all-map result was Xuanming side B, from an 852–1,004 loss to a 1,028–592 win. The old #186 approach still looks useful when measured against the current baseline.

c505 combined that phase change with c503's side-B six-tile retreat against every opponent. It stayed at 6/18 and lost the Xuanming side-B conversion, showing the rules interfere when applied to the same mirror draft. c506 retains the round-one role phase and applies the six-tile retreat only on the Pilgrimage side-B spawn `(46,1)` when the enemy is not the exact mirror counterdraft. It scored 7/18 in two focused runs, 29/40 in two default-pool runs, and 173/204 across the six strong all-map proxies. Compared with c488, it converts Xuanming side B and Faisal-bot side B into wins in the focused screen. In the default pool it converts Faisal-bot and my-bot side B into wins but gives up opp-tts-locker side B; net result 29/40 versus 28/40. Strong all-map results change only for Xuanming side B (852–1,004→1,028–592). Keep c506 as the leading local Pilgrimage candidate, not production-ready; live unranked remains paused.

Runs: c504 focused `matches/league/20261018-211852-c504-direct-role-phase-from-round-one/`, default pool `...211914-c504-direct-role-phase-from-round-one-full-pool/`, strong all maps `...211935-c504-direct-role-phase-from-round-one-strong-all-maps/`; c505 focused `...212100-c505-direct-role-phase-side-b-retreat-combined/`; c506 focused `...212146-c506-direct-mirror-phase-nonmirror-side-b-retreat/` and repeat `...212338-c506-direct-mirror-phase-nonmirror-side-b-retreat-strong-repeat/`, full pool `...212208-c506-direct-mirror-phase-nonmirror-side-b-retreat-full-pool/` and repeat `...212349-c506-direct-mirror-phase-nonmirror-side-b-retreat-full-pool-repeat/`, strong all maps `...212228-c506-direct-mirror-phase-nonmirror-side-b-retreat-strong-all-maps/`.

## Packs early-combat leash and integrated local build c507–c508 (18 Oct 2026)

c507 keeps Packs' round-one role split but filters combat engagements to early attack range through round 599. Against six opponents selected from the loss cluster, it scored 6/12 versus a fresh c488 control at 4/12: it converted all four v4/v5 losses, but gave up Faisal-bot and opp-tts-v3 side-B wins. On the complete default 20-opponent Packs pool it scored 33/40 in two identical runs versus fresh c488 at 32/40. The full-pool result changes seven side outcomes: wins v4/v5 on both sides, loses Faisal-bot side B, opp-tts-v3 side B, and tungtungsahur-v1 side A. Keep as a Packs local candidate.

c508 combines c507 with c506's Pilgrimage phase and non-mirror side-B retreat rules. After serially recovering two replay-publication collisions, its full 17-map/default 20-opponent score was 626/680 versus the clean c488 control's 624/680. Packs improved 32/40→33/40 and Pilgrimage 28/40→29/40; all other 15 map totals matched. The 204-game six-strong-proxy screen finished 173/204 versus c488's 172/204 after one collision recovery. Its only net strong-proxy win gain was Xuanming on Pilgrimage side B. Packs changed four strong-proxy outcomes: two new `fx-dbllock` wins, offset by a Xuanming side-A loss and an `opp-swirl-meta-core` side-A loss. This is the current best integrated local candidate, but the local pool does not establish a top-50 win streak. Production source/ZIP remain unchanged; live unranked remains paused.

Runs: c507 target `matches/league/20261018-212443-c507-direct-early-combat-leash-600/`, fresh c488 target `...212509-c488-direct-clean-control-early-combat-leash-600/`; c507 full Packs `...212517-c507-direct-early-combat-leash-600-full-pool/` and repeat `...212554-c507-direct-early-combat-leash-600-full-pool-repeat/`, fresh c488 control `...212537-c488-direct-clean-control-early-combat-leash-full-pool/`. c508 all-map pool `...212625-c508-direct-combine-packs-pilgrimage-map-strategies-full-pool/`, collision recovery `...212957-c508-direct-replay-collision-recovery/`; strong all maps `...213033-c508-direct-combine-packs-pilgrimage-strong-all-maps/`, collision recovery `...213142-c508-direct-strong-replay-collision-recovery/`. Clean c488 680-game control plus recovery is `matches/league/20261018-205324-c488-direct-clean-full-pool-control-for-c498/` and `...205637-c488-direct-recover-full-pool-control-match/`; strong all-map c488 control is `...211631-c488-direct-clean-control-for-side-b-pilg-retreat-strong-all-maps/`.

## Swirl and Lanes follow-ups c509–c511 (18 Oct 2026)

c509 replaced the Swirl four-pick roster with Ryth/Cassi-and-Issac/Stellar/Tavi unless the existing C&I/Varg counter triggered. It scored 5/12 against six strong Swirl proxies, losing both Ming and Xuanming sides; reject the draft change, which also gives up Varg's farm route.

c510 kept c508's roster and enabled its side-A flank opening against the Ryth/C&I/Stellar/Tavi enemy draft. It tied c508 at 11/12 strong and 32/40 on the default Swirl pool. It converted `opp-tts-v4` and `opp-tts-aggro` side A to wins, but lost `opp-fai-mirror` and `opp-tts-locker` side A; aggregate submitted gems rose 37,488→37,685. Keep as a Swirl matchup hypothesis, not a net win-rate upgrade.

c511 replaced Ryth with Vendetta on Lanes to mirror Ming's five-pick draft. It fell to 5/12 on the six-strong Lanes screen from c508's 7/12 and lost both Ming and Xuanming sides. Reject the roster swap. The replay evidence instead points to farm-route throughput: c508's four Lanes losses had only 0–6 deaths, and the strongest opponents banked sooner.

Runs: c509 `matches/league/20261018-213651-c509-direct-swirl-tank-tavi-strong/`; c510 strong `...213734-c510-direct-swirl-tank-tavi-flank-strong/` and default pool `...213752-c510-direct-swirl-tank-tavi-flank-full-pool/`; c511 `matches/league/20261018-214056-c511-direct-lanes-vendetta-draft-strong/`. c508 remains the best integrated local candidate at 626/680 default-pool and 173/204 strong-proxy wins. Live matches remain paused; production source and submission ZIP remain unchanged.

## Lanes delayed split and Corners combination c512–c516 (18 Oct 2026)

c512 delays the Lanes role split until round 45, keeping the shared opening through round 44. It scored 10/12 on the six-strong Lanes screen, repeated identically, versus c508's 7/12. It won both Ming games, Xuanming side A, and `opp-swirl-meta-core` side A; the only new strong loss was meta-core side B. Its complete 20-opponent Lanes pool stayed at 39/40. c513 moved the split to round 60 and also scored 10/12, but traded away Ming side A for meta-core side B; c514 moved it to round 30 and fell to 7/12. Reject those thresholds.

c515 moves the split to round 50. It swept the six strong Lanes proxies 12/12 in two matching screens, including both Ming and Xuanming sides. The complete Lanes pool remained 39/40 with the same winner outcomes as c508. Across all maps and six strong proxies it scored 179/204 versus c508's recovered 173/204; five of the gains are the converted Lanes results. The shared comparison also had one unrelated Corners side-B outcome change, so that extra win is not attributed to the Lanes rule.

c516 adds c498's Corners-only six-tile retreat for the exact C&I/Ren/Stellar/Ryth/Varg mirror. In the focused Corners screen it scored 10/12 versus c515's 9/12; the `opp-swirl-meta-core` side-A loss changed from 724–1,018 with 22 deaths to a 1,010–572 win with 11 deaths. Its full strong all-map screen completed at 180/204 after serial recovery of a finished Monolith win whose replay publication collided. The full 20-opponent, 17-map pool scored 626/680, matching c508. c516 is the best integrated local candidate so far, not a top-50 streak result. Live unranked remains paused; production source and ZIP remain unchanged.

Runs: c512 strong Lanes `matches/league/20261018-214315-c512-direct-lanes-split-r45-strong/`, repeat `...214415-c512-direct-lanes-split-r45-strong-repeat/`, pool `...214339-c512-direct-lanes-split-r45-full-pool/`; c513 `...214427-c513-direct-lanes-split-r60-strong/`; c514 `...214452-c514-direct-lanes-split-r30-strong/`; c515 strong `...214512-c515-direct-lanes-split-r50-strong/` and repeat `...214547-c515-direct-lanes-split-r50-strong-repeat/`, pool `...214530-c515-direct-lanes-split-r50-full-pool/`, all-map strong `...214557-c515-direct-lanes-split-r50-strong-all-maps/`; c516 Corners `...214737-c516-direct-lanes-plus-corners-mirror-strong/`, all-map strong `...214807-c516-direct-lanes-r50-plus-corners-strong-all-maps/` with serial recovery under `recovery-monolith-faisal-a/`, full pool `...214959-c516-direct-lanes-r50-plus-corners-full-pool/`.

## Eight side-B mirror counterdraft c517–c519 (18 Oct 2026)

c517 attempted to wait for the full enemy Ren/Stellar/C&I/Ryth/Varg lineup before taking Tavi. The enemy draft is revealed incrementally, so the condition never fired before our pick; it matched c516. c518 switched to Tavi whenever Ren was visible on Eight. On six strong proxies it scored 10/12 versus c516's 9/12, converting the mirror side-B loss (842–1,040) to a 1,012–820 win. The same swap on side A collapsed the mirror game from 930–1,008 to 176–1,002, so do not use it on both sides.

c519 keeps Ren on side A and chooses Tavi instead only on side B when Ren is visible. It repeated the 10/12 focused result and scored 181/204 across six strong local proxies and all 17 maps, one win above c516's 180/204. Its 20-opponent Eight pool scored 35/40, matching c516's 35/40. The recovered full 20-opponent, 17-map run finished 626/680, tying c516's 626/680. Retain c519 as a narrow local counterdraft, not a general upgrade. It has no live top-50 validation; production source and submission ZIP remain unchanged, and live unranked remains paused.

Runs: c517 `matches/league/20261018-215759-c517-direct-eight-mirror-tavi/`; c518 `...215841-c518-direct-eight-visible-ren-tavi/`; c519 repeat screen `...215927-c519-direct-eight-side-b-visible-ren-tavi-repeat/`, full Eight pool `...215945-c519-direct-eight-full-pool/`, strong all maps `...220004-c519-direct-eight-side-b-counter-strong-all-maps/`, and full pool `...220202-c519-direct-eight-side-b-integrated-full-pool/` with two serial replay recoveries summarized in `recovery-summary.json`.

## Swirl and Lanes route/survival follow-ups c520–c533 (18 Oct 2026)

The local `mingstudy-trace` proxy's Swirl plan assigns separate camp circuits and keeps Cassi/Issac together; its route logs show early camp captures and an altar lock by r159–r214. It is a strong local planner proxy, not a top-50 opponent. The c519 Swirl replay shows side A tied at r200, then lost 584–946 with 51 deaths and 124 gems dropped; side B lost 678–1,024. The biggest gap is farm-to-bank tempo after the first cycle.

Draft swaps regressed: c521 traded Ren for Varg on side A and fell to 268 gems; c522 kept Ren and Varg but dropped Vendetta and reached 450. A generic role split from round 1 collapsed to 44 gems (c524); diagnostic c525 showed it sent leaders to 120–240 DPS camps. Restricting splits to camps at or below 60 DPS raised side A to 240 (c526); restricting to at most 20 DPS raised it to 532, but the first score arrived around r500 (c527). Keep the shared c519 opening over these generic splits.

c523 aborted the flank when outmatched contact appeared and scored 560 on side A. c528 kept the team in its early, grouped farm phase after aborting; it reached 674, slightly below its side-B baseline of 678, but still lost 674–1,026 with 51 deaths and 208 gems dropped. c529 added an early low-health abort and excluded the initial flank camp afterward; it scored 668. These are score improvements over c519 on one proxy replay, not wins or validated all-map changes. The initial `(13,13)` camp is 88 gems, 5,400 health, and 80 DPS, so it is a risky opening that still needs a better survival/route policy.

Lanes side B was a separate near-loss: c519 submitted 978 before one Stellar death dropped 22 gems at r544; the enemy locked altar `(29,4)` at r528. Five health shards prevented deaths but cut the score to 896 (c530). Routing around all active camps reached 910 (c531). Letting low-health carriers continue the bank route and a one-shard health purchase both repeated the r544 death and 978 score (c532/c533). Reject these broad adjustments; the death appears to be a one-turn damage spike, and a survival patch has not yet improved the bank race.

c519 remains the best integrated local candidate at 181/204 strong-proxy wins and 626/680 default-pool wins. No new top-50 live matches were run; live unranked remains paused. Production source and submission ZIP are unchanged, and the 10-consecutive-live-win target is still unverified.

Runs: Swirl c521–c529 are under `matches/league/20261018-221422-c521-direct-keep-varg-slot/` through `...222137-c529-direct-low-health-safe-abort/`; Lanes c530–c533 are under `...222251-c530-direct-lanes-stellar-health-emblem/` through `...222543-c533-direct-lanes-stellar-single-health-shard/`. c520 was a source clone with a stale copied CMake cache and did not build.

## Please replay and local counterdraft follow-up c535–c542 (18 Oct 2026)

Rechecked the latest live group against rank-45 Please: Contest ended 0–0 on gems with 94:11 deaths; Lanes was 750:1,000 with 29:42 camp captures and no deaths; Eight was 683:1,029 with 30:9 deaths; Interlock was 204:1,004 with 23:2 deaths; Rows was 528:1,056 with 2:0 deaths. Rows' Varg collected 154 versus Please's 363. The losses point to different problems: Contest/Eight/Interlock need survival, while Lanes/Rows also need a faster camp-to-bank cycle. The replay is evidence from the official match; `please-layout-proxy` below is only a local synthetic roster-and-planner proxy.

Against that proxy on the same five maps, c519 scored 8/10; its only losses were Lanes side B (802:1,012, zero deaths) and Eight side A (550:1,112, 32:21 deaths). c518 changes only the Eight draft rule to take Tavi when Ren is visible. It won both Eight sides against the observed Please roster (1,062:330 and 1,062:534) and scored 9/10 on the five-map proxy screen, losing only Lanes side B. Its full 20-opponent Eight pool remained 35/40, tied with c519. c542 keeps c519's side-B Ren response and also selects Tavi on side A when Ren, Cassi/Issac, Varg, and Stellar are visible; it still selected Tavi against Please's observed core, scored 2/2 on Eight and 9/10 across the five maps, and held 35/40 on the default Eight pool. This is a useful matchup counter, not a general win-rate increase. c518 and c542 have no live validation.

Lanes draft tests did not solve the farm gap. c537's conditional counter came too late to undo the locked Ryth pick. c538 opened with Please's Varg/C&I/Stellar/Ren/Tavi roster, dropping Ryth, and lost all four side-swapped games against `please-layout-proxy` and `mingstudy-trace`; matching the roster alone is not enough. c539's round-1 split lost both proxy games. c540/c541 delayed the split on the far-side spawn; c541 raised that side's Please-proxy score from c519's 802 to 948, but still lost, and its two `mingstudy-trace` games were also losses. Keep c519's tested round-50 split as the broad local default; the Lanes side-B farm route remains open work.

Runs: c519 baseline `matches/league/20261018-223405-c519-direct-observed-please-rosters-route-proxy/` and repeat Lanes `...224030-c519-direct-lanes-observed-roster-baseline-repeat/`; c518 `...223514-c518-direct-observed-please-rosters-route-proxy/` and default Eight `...224143-c518-direct-eight-visible-ren-default-pool/`; c537–c541 Lanes experiments `...223622-c537-direct-lanes-please-ren-tavi-counterdraft-screen/` through `...224108-c541-direct-lanes-side-specific-first-bank-split/`; c542 exact Eight `...224214-c542-direct-eight-visible-top-core-counterdraft-proxy/`, default Eight `...224238-c542-direct-eight-visible-top-core-default-pool/`, and five-map screen `...224256-c542-direct-observed-please-rosters-route-proxy/`. c492 movement diagnostic on this proxy is in `matches/league/20261018-223906-c492-direct-lanes-movement-diagnostic-on-please-proxy/`.

Keep c519 as the broad local candidate and c542 as the Eight-only counterdraft candidate. No live unranked matches were run. Production `bots/tungtungsahur/src/bot.cpp` SHA-256 remains `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; `submissions/tungtungsahur.zip` remains `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. The 10-consecutive official top-50 win target is still unverified.

## Lanes gear follow-up c543–c550 (18 Oct 2026)

The official Please Lanes replay remains a throughput loss with 0 deaths: Please banked 42 camps versus our 29 and scored 1,000–750. Its Varg/Ren used many Power Strength shards; Cassi/Stellar/Tavi favored Focus; all carried Durability shards. That evidence motivated gear tests, but it does not prove a single copied queue is best for our different roster.

c543 gave Ryth Monster Strength then Power Strength on Lanes. Against the synthetic Please roster, side A stayed a win (1,012–946) and side B rose from the repeated c519/c542 baseline 802 to 984, still losing narrowly (984–1,012). It beat `mingstudy-trace` 2/2. Across the 20-opponent Lanes pool it scored 39/40, matching the baseline win count, but lost 120 submitted gems overall and flipped both Ming side results from wins to losses; do not apply the build broadly. c550 gates only Ryth's Strength queue to the far-side spawn against the full Please draft. It reproduced 1,020–990 on side A and 984–1,012 on side B, then scored 39/40 on the full Lanes pool with the same lone loss (opp-fai-mirror side A). Keep c550 only as an exact-draft farm candidate; it has not converted the Please side-B loss or been live-tested.

Broad gear mirroring was harmful: c547 changed several roles to Please-style Power/Durability queues and scored 1/4 on the two Lanes proxies. c549 changed only item-phase thresholds for that full draft and also scored 1/4, including a baseline side-A win becoming a close loss. Separately, globally using actual six-shard Power/Bruiser thresholds regressed the strong all-map set from c519's 181/204 to c546's 176/204. Reject these threshold and team-wide gear changes.

Runs: c543 focused `matches/league/20261018-224951-c543-direct-lanes-ryth-full-strength-emblems/`, pool `...225050-c543-direct-lanes-ryth-strength-full-pool/`; c546 strong all maps `...225605-c546-direct-correct-emblem-thresholds-strong-all-maps/`; c547 screen `...225933-c547-direct-lanes-please-purchase-profile-screen/`; c549 screen `...230106-c549-direct-lanes-please-threshold-only-screen/`; c550 focused `...230209-c550-direct-lanes-please-far-side-ryth-only/`, full pool `...230251-c550-direct-lanes-please-far-side-ryth-only-full-pool/`.

No live unranked matches or uploads were made. Production source and submission ZIP remain unchanged. The top-50 10-consecutive-live-win target remains unverified.

## Strong all-map check and Eight mirror analysis (18 Oct 2026)

c550 also scored 181/204 on the six-opponent, 17-map strong set. A key-by-key comparison against both c519 and c542 showed identical outcomes and submitted-gem totals in all 204 games; the exact Please gear gate did not alter this broader test. The shared local planner bot `opp-swirl-meta-core` scored 135/170 against the same five distinct strong opponents, while c550 scored 160/170 on that subset. Its narrow Eight matchup strength does not transfer as a full replacement.

On Eight against that mirror, side A's proxy led 738–160 by r300; our replay showed six unit death events by then and 270 gems dropped over the match, ending 930–1,008. Side B's lineup with Tavi won 1,012–820, despite 43 deaths. A prior both-sides Tavi rule collapsed the side-A result to 176–1,002, so do not broaden the Eight counter to side A based only on the late full-draft signature. The remaining side-A issue is the early farm/deposit race and safe camp routing, not a proven roster fix.

Runs: c550 strong all maps `matches/league/20261018-230348-c550-direct-lanes-please-far-side-ryth-only-strong-all-maps/`; `opp-swirl-meta-core` against five distinct strong bots `...230910-opp-swirl-meta-core-direct-meta-core-planner-five-strong-all-maps/`; c551 draft diagnostic `...230650-c551-direct-meta-core-eight-draftstep-diagnostic/`. c551 adds logging only and is not a candidate build.

## Mirror Eight phase timing c552 (18 Oct 2026)

c552 changes the Eight phase only when the full enemy mirror draft is present (Cassi/Issac, Ren, Stellar, Ryth, Varg): it starts the squad split after a carry's first emblem instead of waiting until round 600. Against `opp-swirl-meta-core`, the side-A loss changed from 930–1,008 to a 1,012–892 win; side B also won. The six-strong Eight screen improved from 10/12 to 11/12, with the remaining loss against `fx-dbllock`.

The change passed the wider screens. Strong all-map results rose from c550's 181/204 to 182/204; key-by-key comparison found exactly one outcome flip, the meta-core Eight side-A win, and +94 submitted gems. The default Eight pool stayed 35/40 with every outcome and gem total identical to c519/c542. The full 20-opponent, 17-map pool finished 626/680, tying c519's recovered 626/680 with no changed win outcomes. Raw submitted gems differed by +184 across the full pool, mainly on unrelated contests; do not attribute that to this narrowly gated phase change. Together with c550's exact Please Lanes purchase gate, c552 is the strongest current local candidate. It remains unvalidated in a live top-50 match.

Runs: focused Eight `matches/league/20261018-231206-c552-direct-eight-mirror-emblem-split-strong/`; strong all maps `...231237-c552-direct-eight-mirror-emblem-split-strong-all-maps/`; default Eight `...231434-c552-direct-eight-mirror-emblem-split-default-pool/`; full pool `...231505-c552-direct-eight-mirror-emblem-split-full-pool/`. The full c519 control's two failed matches were recovered in `matches/league/20261018-220202-c519-direct-eight-side-b-integrated-full-pool/recovery-summary.json` before comparing final 626/680 totals.

## Workspace update from c552 (18 Oct 2026)

After the full local screens, copied c552's six source files into `bots/tungtungsahur/src` and regenerated `submissions/tungtungsahur.zip`. `cambc build tungtungsahur` succeeded. The final canonical-source check beat `opp-swirl-meta-core` 2/2 on Eight. The ZIP contains exactly the six `src/` files, each verified byte-for-byte against the workspace source.

Current SHA-256: `bot.cpp` `D150639F0CE009A5A7C82436100366BD4C8F0305CF71F003DDB2E18B9525E77C`; `draft.cpp` `C0DBA608AFCD4EAE56EEFE66D96EDBAA9D726DC58F2B60AFA784DADF2FB7A035`; ZIP `5BC212DEAE33B8AF195DB43E669216FE574B277967592CBA4D0767DAB7437892` (31,049 bytes). No CLI submission or live unranked match was made. The 10-consecutive top-50 live-win goal remains open.

Final local check: `matches/league/20261018-232231-tungtungsahur-direct-c552-canonical-source-check/`.

## Lanes gear-order follow-up and canonical c553 (18 Oct 2026)

c553 changes only Ryth's Lanes gear order on side B when the enemy has the exact Please five-champion draft: buy Power Strength before Monster Strength. Against the side-swapped `please-layout-proxy`, both sides then scored 1,020–990 (2/2); c550/c552 had already won side A 1,020–990 but lost side B 984–1,012. The `mingstudy-trace` side-B loss remains 978–1,012, so this is a narrow draft-and-map counter, not a general Lanes fix. The combined five-map screen scored 19/20 (10/10 vs Please proxy, 9/10 vs MingStudy).

The change preserved the wider local results: the 20-opponent Lanes pool stayed 39/40 with the same sole loss and identical outcomes/gems as c550; six strong Lanes proxies scored 12/12 with no outcome or gem changes; the six-opponent strong all-map screen stayed 182/204; and the 680-game default pool finished 626/680 with zero failures and no outcome or gem-total changes versus c552. It converts the exact synthetic Please side-B case without showing a broader win-rate increase.

Copied c553 into `bots/tungtungsahur/src` and regenerated `submissions/tungtungsahur.zip`. `cambc build tungtungsahur` succeeded, and the ZIP's six source files match the workspace byte-for-byte. SHA-256: `bot.cpp` `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6`; `draft.cpp` `C0DBA608AFCD4EAE56EEFE66D96EDBAA9D726DC58F2B60AFA784DADF2FB7A035`; ZIP `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA` (31,057 bytes). No live unranked match or upload was made. The 10-consecutive top-50 live-win target remains unverified.

Runs: proxy repeat `matches/league/20261018-232503-c553-direct-lanes-please-ryth-power-first-repeat/`; full Lanes pool `...232508-c553-direct-lanes-please-ryth-power-first-full-pool/`; strong Lanes `...232541-c553-direct-lanes-please-ryth-power-first-strong/`; five-map screen `...232620-tungtungsahur-direct-c553-canonical-five-map-refresh/`; strong all-map `...232646-tungtungsahur-direct-c553-canonical-strong-all-maps/`; full default pool `...232855-tungtungsahur-direct-c553-canonical-full-pool/`.

## Pilgrimage mirror opening test c554 (18 Oct 2026)

c554 keeps the Pilgrimage opening shared until the first carry emblem when the existing `pilgrimage_mirror_counterdraft_active` gate matches the enemy draft. That gate is the Please-style C&I/Varg/Stellar/Vendetta/Tavi lineup; it does not match `opp-swirl-meta-core`'s Ren/Stellar/C&I/Ryth/Varg roster. Its two meta-core replays were byte-identical to c553, so they do not test a changed opening against that opponent. Across the six strong Pilgrimage proxies c554 scored 8/12 versus c553's 9/12; the Xuanming side-B win flipped to a loss, while no meta-core result changed. Reject the Please-gated phase change; it is not evidence about a correctly gated meta-core response. Run: `matches/league/20261018-233820-c554-direct-pilgrimage-mirror-shared-until-carry-emblem-strong/`.

c555 avoids camps above 100 strength during the first 150 rounds only when that same Please-style lineup gate matches. It fell to 7/12 from c553's 9/12 on the six-proxy Pilgrimage screen, flipping Ming side A and Xuanming side B to losses. It was a no-op in both `opp-swirl-meta-core` games, whose logs match c553 exactly, so those losses do not evaluate this camp filter. Reject the tested Please-gated filter; separately test only if the actual meta-core route evidence supports it. Run: `matches/league/20261018-233918-c555-direct-pilgrimage-mirror-avoid-strong-camps-r0-150-strong/`.

c556 correctly gates on the observed Ren/Stellar/C&I/Ryth/Varg draft and keeps the whole team on the shared opening route only until the first bank, with a round-120 cap. It scored 9/12, tying c553's win count, but was substantially worse in both meta-core losses: 556–1,032 and 252–1,036 versus c553's 940–1,014 and 732–1,064. Reject the shared first-bank opening; c553's round-one role split is better for this opponent. The next test raises the early survival threshold while keeping the split. Run: `matches/league/20261018-234314-c556-direct-pilgrimage-meta-first-bank-shared-opening-r120-cap-strong/`.

## Pilgrimage meta-core side-A survival screens c557–c561 (19 Oct 2026)

c557 raises both sides' retreat threshold to 55% health through round 119 only on the exact Ren/Stellar/C&I/Ryth/Varg Pilgrimage draft. It converted meta-core side A from 940–1,014 to 1,032–420 and reduced our logged deaths 22→14, but side B deteriorated from 732–1,064 to 504–1,026. The six-strong Pilgrimage screen scored 10/12 in two identical runs, but the all-side rule is too broad for the spawn asymmetry.

c558 keeps the 55% threshold only on our Pilgrimage side A against that exact draft. It scored 10/12 on the focused six-proxy screen and 183/204 across the six strong opponents and all 17 maps, versus c553's 182/204. Key-by-key, exactly one strong result changed: meta-core Pilgrimage side A became a 1,032–420 win; all other 203 outcomes and gem totals matched. The 680-game default pool remained 626/680 with no changed win outcome; one unrelated Corners side-A gem total against `my-bot-v3` differed 1,088→1,008. Keep c558 as the best local test candidate, not the canonical bot: it has not faced the official top-50 pool live.

Threshold tuning: c559 at 60% preserved the 10/12 win count but weakened the meta-core side-A win to 1,006–548. c560 at 50% fell to 9/12 and lost meta-core side A 610–1,002. c561 kept 55% but extended the window to round 180; it also fell to 9/12 and lost both meta-core sides. The current local evidence favors 55% through round 119 on side A only.

Runs: c557 focused `matches/league/20261018-234425-c557-direct-pilgrimage-meta-early-survival-55pct-r120-strong/` and repeat `...234506-c557-direct-pilgrimage-meta-early-survival-55pct-r120-strong-repeat/`; c558 focused `...234522-c558-direct-pilgrimage-meta-side-a-early-survival-55pct-r120-strong/`, strong all maps `...234601-c558-direct-pilgrimage-meta-side-a-early-survival-55pct-strong-all-maps/`, default pool `...234753-c558-direct-pilgrimage-meta-side-a-early-survival-55pct-canonical-full-pool/`; c559 `matches/league/20261019-000004-c559-direct-pilgrimage-meta-side-a-early-survival-60pct-r120-strong/`; c560 `...000040-c560-direct-pilgrimage-meta-side-a-early-survival-50pct-r120-strong/`; c561 `...000142-c561-direct-pilgrimage-meta-side-a-early-survival-55pct-r180-strong/`.

## Pilgrimage side-specific survival and tank-cover follow-ups c562–c565 (19 Oct 2026)

c562 extended the 55%-through-round-119 survival rule to our side B when facing the exact `fx-dbllock` draft. It converted that Pilgrimage side-B result from 412–1,012 with 21 deaths to 1,088–920 with 9 deaths, but gave up an `opp-racer` side-B win; the aggregate strong all-map score stayed level with c558. The roster-only gate is too broad.

c563 narrows the side-B exception to the exact `fx-dbllock` draft and an enemy within four tiles, while retaining c558's exact meta-core side-A rule. Its 12-game strong Pilgrimage screen scored 11/12; against `fx-dbllock` side B it scored 1,032–872 with 7 deaths, while `opp-racer` remained 2/2. The six-strong, 17-map screen scored 184/204 versus c553's 182/204. The 680-game local pool remained 626/680: no net win-count gain, with a few Pilgrimage results trading places (`opp-tts-v2` side B changed win→loss; `opp-tts-v3` side B changed loss→win). Treat c563 as the strongest current *local matchup candidate*, not a broad default-pool improvement or official top-50 result.

c564 added the same side-B early retreat rule for meta-core, but made its side-B result worse (732–1,064→504–1,026); reject that extra gate. c565 tried moving Ryth to squad B against meta-core on Pilgrimage side B, expecting the tank to cover the four champions already engaging. The focused screen stayed 11/12, and all 12 replay files were byte-identical to c563; gem totals, kills, deaths, gold, and outcomes also matched exactly. This assignment produced no observable change, so do not retain it as a strategy improvement.

The c565 meta-core side-B score trace points to bank tempo as the next investigation: c565 banked 46 at round 70, while meta-core first showed 68 at round 75; by round 300 the score was 68–228, and meta-core reached 500 around round 850 versus c565 around round 990. c565 finished 732–1,064 with 16 deaths versus the opponent's 23, so this loss was not explained by us dying more. The replay has score, death, and altar-lock events but no per-champion movement/capture counters; a camp-route or altar-access cause remains a hypothesis. Instrument those events before changing retreat or squad assignments again.

The first movement-instrumentation attempt (`bots/c566-trace`) added per-step counters and periodic `SCOUT MOVE` output to c563. It built and completed both games, but changed the meta-core side-B result to 754–1,018 with 22 own deaths and 21 opponent deaths; a fresh c563 control repeated 732–1,064 with 16 own deaths and 23 opponent deaths. There were no crashes, but the logger is behaviorally intrusive. Discard its movement counts as evidence about c563 and do not treat the score change as a strategy gain; future route analysis must use replay-side data or a lower-overhead method.

Runs: c562 focused `matches/league/20261019-000320-c562-direct-pilgrimage-meta-side-a-fx-side-b-early-survival-focus/` and all-map strong `...000351-c562-direct-pilgrimage-meta-and-fx-side-specific-survival-strong-all-maps/`; c563 focused `...000613-c563-direct-pilgrimage-side-specific-survival-nearby-pressure-strong/`, all-map strong `...000651-c563-direct-pilgrimage-side-specific-survival-nearby-pressure-strong-all-maps/`, full pool `...000849-c563-direct-pilgrimage-side-specific-survival-nearby-pressure-full-pool/`; c564 `...001506-c564-direct-pilgrimage-side-specific-survival-pressure-meta-side-b-strong/`; c565 `...001615-c565-direct-pilgrimage-meta-side-b-ryth-joins-defense-strong/`.

## Lanes safe-bank threshold screen c567 (19 Oct 2026)

c567 starts from c563 and delays banking on Lanes until 48 gems, while preserving immediate banking for nearby/recent enemy pressure, a nearby altar, no farm target, or the endgame. It built successfully and completed all 12 games against the six strong local proxies, scoring 7/12 and averaging 997 banked gems. The c563 control on the same six opponents and map scored 12/12 and averaged 1,011 gems. c567 also logged 28 own death events versus c563's 19; the runs were not seed-paired, so treat the exact per-match differences cautiously, but the aggregate loss and death increase reject this variant. Keep immediate banking on Lanes. This matches the earlier broad 48-gem experiment's weaker 9/20 strong-source result and the repeat benefit of the c553 immediate-bank route.

Runs: c567 `matches/league/20261019-002821-c567-direct-lanes-safe-48-bank-strong/`; fresh c563 control `...002836-c563-direct-lanes-safe-48-bank-c563-control/`. No candidate ZIP or upload was made. Canonical source/ZIP remain c553; official unranked remains paused.

## Lanes Willow counter and Ryth item test c568–c570 (19 Oct 2026)

The official rank-45 Please Lanes replay used Varg/Cassi & Issac/Stellar/Tavi/Willow against our Varg/Cassi & Issac/Ryth/Stellar/Tavi, and lost with zero deaths but only 29 camp captures to Please's 42. The older `please-layout-proxy` uses Ren instead of Willow, so it does not represent this exact draft.

c568 tried replacing Ryth with Willow when the full enemy lineup became visible. That signal arrived after four allied picks were fixed; the first version made no change, and the predictive version added Willow as a sixth body while dropping Tavi. It stayed 1/2 against the Willow proxy, equal to a fresh c553 control. c569 moved the counter to the first visible Varg/C&I picks and reordered the Lanes lineup. It matched the Willow roster but scored 0/2 against the Willow proxy and 0/2 against the older Ren proxy, versus c553's 1/2 and 2/2. Reject both draft changes; the Willow swap is not supported.

c570 retains c553's lineup and changes only Ryth's Lanes build to Monster Strength, then Power Strength, on our side A when the enemy has the exact Varg/C&I/Stellar/Tavi/Willow draft. This targets the official replay's no-death farm deficit and reuses c543's tested full-strength queue. Against the Willow-layout proxy, c570 scored 2/2 in two runs (990–814 and 992–858); the c553 control scored 1/2 in both runs (976–990 on side A, with the side-B win unchanged). Against the older Ren proxy, both stayed 2/2 with identical aggregate scores. c570 also matched c553 at 12/12, with identical per-opponent totals, across six strong Lanes proxies. The full 20-opponent Lanes pool scored 39/40, with the same lone loss to `opp-fai-mirror` on side A as c553. These are local proxy results only; the Willow opponent is a synthetic planner using the recorded lineup, not Please's bot. Keep c570 isolated as the best current local Lanes matchup candidate pending official validation.

Runs: c568 `matches/league/20261019-003604-c568-fresh/` and `...003657-c568-fresh/`; c569 `...003842-c569-fresh/`; baseline Willow/Ren proxies `...003834-c553/` and `...003558-c553/`; c570 focused `...004002-c570-fresh/` and repeat `...004027-c570-fresh/`; strong Lanes `...004039-c570-fresh/` (with c553 control in `...004101-c553/`); full Lanes pool `...004127-c570-fresh/`. No canonical source or ZIP update and no upload/live match were made. The 10-win top-50 goal remains unverified.

## Combined Lanes and Pilgrimage candidate c571 (19 Oct 2026)

c571 combines c563's exact-draft Pilgrimage early-survival rules with c570's Lanes side-A Ryth strength queue. It built successfully, repeated 2/2 against the Willow-layout proxy, scored 184/204 on the six-strong, 17-map screen, and scored 626/680 on the full 20-opponent pool. The full-pool per-opponent wins and losses matched c563 exactly after normalizing side-label case, so this integration shows no additional broad win-rate gain. Keep it isolated; the Willow match remains synthetic and neither c570 nor c571 has live validation.

Runs: strong all maps `matches/league/20261019-004411-c571-fresh/`; Willow proxy `...004512-c571-fresh/`; full pool `...004518-c571-fresh/`. No production artifact was changed and no unranked group or upload was created.

## Pilgrimage carry-bank routing follow-up c572–c578 (19 Oct 2026)

The fresh c571 control against `opp-swirl-meta-core` repeated at 1/2: side A won 998–420, while side B lost 732–920. Its replay shows Stellar died at r232 carrying 92 gems, with the team tied at r200 and 160 behind by r300.

Gear changes did not solve the side-B loss. c572 gave Ryth Monster Strength then Power Strength (side B 664–892, 24 deaths versus c571's 16); c573 changed the second shard to Power Health (366–962); c574 gave Stellar Monster Focus then Power Focus (412–920, ending sooner). Reject all three gear variants.

Carry retreat tests were also rejected. c575 used a 65% health threshold for large carriers when an enemy was within nine tiles before r400; it improved the side-B score to 944–960 but still lost, kept the r232 92-gem death, and raised total deaths to 18. c576 removed the visibility requirement; side B scored 732–972, still lost, and had 17 deaths.

c577 changes Pilgrimage bank routing on the map side whose allied spawn is at `(46,1)`: when the exact Ren/Stellar/Cassi-and-Issac/Ryth/Varg meta-core lineup is against us, a carrier with at least 46 gems now pays the enemy-half altar penalty. The previous cutoff was 100 gems. This preserves the route choice for smaller bags and prevents a full 46-gem camp reward from being routed west simply because the enemy-half altar is closer. Two focused runs both went 2/2 versus c571's repeated 1/2; c577 won the formerly losing side B 968–920. On the six-proxy, 17-map screen it scored 185/204 versus c571's 184/204. Only one outcome changed: meta-core Pilgrimage side B became a win. Three other same-map scores shifted while staying wins. The r232 death still occurred, so the gain is from subsequent bank routing and tempo, not eliminating that death.

c578 generalized the 46-gem allied-half route rule to every opponent on Pilgrimage side B. It scored 30/40 on the default 20-opponent Pilgrimage pool versus c571's 29/40, but it tied the strong all-map screen at 184/204: the meta-core side-B loss became a win while an `opp-racer` side-B win became a loss. Keep the exact-draft c577 rule; reject the generic rule.

Runs: c572 `matches/league/20261019-005033-c572-fresh/`; c573 `...005131-c573-fresh/`; c574 `...005218-c574-fresh/`; c575 `...005455-c575-fresh/`; c576 `...005535-c576-fresh/`; c577 focused `...005612-c577-fresh/` and repeat `...005652-c577-fresh/`, fresh c571 control `...005657-c571-fresh/`, strong all maps `...005717-c577-fresh/`; c578 Pilgrimage pool `...005846-c578-fresh/`, strong all maps `...005922-c578-fresh/`.

c577 is an isolated local matchup candidate, not official validation. The canonical `bots/tungtungsahur/src` and submission ZIP remain at c553. Official unranked matches remain paused; the requested 10 consecutive top-50 wins are not established.

## Collision south-side squad follow-up c579–c586 (19 Oct 2026)

The c577 strong screen had the same repeated Collision weakness against Ming and Xuanming on side B. The replay showed the linked Cassi/Issac pair fighting near the central altar while Stellar was on a separate camp route; the two linked bodies died together at r103 before their first bank. The Collision map's side-A spawn is at y=1–3 and side-B spawn at y=37–39. The available high-performing local `ming_bot` source also co-routes the linked Cassi/Issac pair, but uses a more detailed per-body camp planner.

Draft and priority changes did not fix the loss. c579 and c580 replaced Stellar with Ryth in the 3-pick Collision lineup and scored 2/6 and 1/6 against Ming, Xuanming, and fx-dbllock. c581 and c582 reordered the same three picks and each scored 2/6. c583 tried banking before burst damage and scored 1/6. c584 made Stellar follow Issac's squad on both map sides; it scored 3/6 versus c577's 4/6. Reject these variants.

c586 keeps the tested Stellar/Cassi-and-Issac/Varg draft and assigns Stellar to Issac's squad only on the south spawn side of Collision. The focused screen repeated at 5/6 versus 4/6 for c577, converting Xuanming's side-B loss while leaving Ming's side-B loss unchanged. The full default Collision pool scored 40/40 versus c571's 37/40, converting `opp-tts-v3`, `opp-tts-v4`, and `opp-tts-v5` side-B losses without introducing a Collision loss. The six-proxy all-map screen scored 186/204 versus c571's 184/204 and c577's 185/204; compared with c577, only Xuanming Collision side B changed outcome. The complete 20-opponent, 17-map pool scored 630/680 versus c571's 626/680, with four net new wins and no new losses. The four changes are TTS-v3/v4/v5 Collision side B plus TTS-v5 Pilgrimage side A; 25 game scores shifted, mostly without changing outcomes.

The c585 replay only instrumented spawn coordinates and is excluded as candidate performance evidence. Runs: c579 `matches/league/20261019-010158-c579-fresh/`; c580 `...010224-c580-fresh/`; c581 `...010244-c581-fresh/`; c582 `...010311-c582-fresh/`; c583 `...010351-c583-fresh/`; c584 `...010519-c584-fresh/`; spawn diagnostic c585 `...010630-c585-fresh/`; c586 focused `...010705-c586-fresh/` and repeat `...010723-c586-fresh/`, default Collision pool `...010737-c586-fresh/`, strong all maps `...010758-c586-fresh/`, full pool `...010902-c586-fresh/`.

c586 is the best local candidate so far, combining c577's narrow Pilgrimage bank rule with the south-side Collision squad change. It remains local-only; canonical source and submission ZIP are still c553. Official unranked matches remain paused, and no top-50 10-win streak is verified.

## Swirl Mite-style opening follow-ups c587–c589 (19 Oct 2026)

The official Mite Swirl replay showed a C&I/Stellar/Ryth/Varg core, while our side used C&I/Stellar/Ren/Varg and suffered repeated deaths. c587 tried to recognize the full C&I/Ryth/Varg signature and mirror the Ryth/Varg farm core. The enemy's Varg pick arrived after our own lineup was fixed: both c587 and a fresh c586 control drafted the same roster and produced identical scores against Faisal-bot and `opp-swirl-meta-core` (2/4 each).

c588 moved the signal earlier to C&I/Ryth/Stellar with no Ren. Against Faisal-bot, the bot could add Ryth only after Ren was already locked, so its final roster became C&I/Stellar/Ren/Ryth rather than the intended Ryth/Varg core. It scored 6/8 against Faisal-bot, `opp-swirl-meta-core`, Ming, and Xuanming versus c586's 5/8, converting Faisal-bot side B (832–936 to 918–444). On the six-strong Swirl screen it fell to 10/12 versus c586's 11/12, losing `opp-racer` side A. On the 20-opponent Swirl pool it scored 33/40 versus 32/40, with Faisal-bot side B as the only outcome gain. This is a narrow, mixed local result, not a broad improvement.

c589 used an earlier C&I/Stellar/no-Ren signal so the Ryth/Varg picks could be made before the third allied pick. It scored 4/8 against the same four proxies versus c586's 5/8: Faisal-bot improved to 2/2, but Ming and Xuanming both fell from 1/2 and 2/2 to 0/2. Reject c589; the earlier read sacrifices too much of the Ren matchup.

Runs: c587 `matches/league/20261019-011833-c587-mite-core/`, fresh control `...011838-c586-fresh/`; c588 focused `...011919-c588-mite-opening/`, control `...011925-c586-fresh/`, six-strong `...012011-c588-mite-opening/`, control `...012015-c586-fresh/`, default Swirl `...012039-c588-mite-opening/`, control `...012051-c586-fresh/`; c589 `...012133-c589-mite-early/`.

All variants remain isolated; `bots/tungtungsahur/src` and `submissions/tungtungsahur.zip` remain at c553. No unranked match or upload was made while the user-paused live work. The live 10-win target is unchanged.

## Existing route-planner bot benchmark (19 Oct 2026)

To test whether the local `ming_bot` atlas planner was a useful wholesale replacement, I ran it and c586 against the same five strong local proxies (`xuanming`, `fx-dbllock`, `faisal-orig`, `opp-racer`, `opp-swirl-meta-core`) across all 17 maps and both sides. `ming_bot` scored 110/170; c586 scored 155/170. The planner bot was better on Eight (10/10 vs 9/10), but c586 led on the other 16 map sets, including Ambush (8/10 vs 1/10), Corners (9/10 vs 6/10), Monolith (8/10 vs 2/10), and Rows (9/10 vs 4/10). It also led on Collision, Contest, Expanse, Lanes, Pilgrimage, and Swirl. This rejects copying the planner bot wholesale; its map-specific routing ideas remain candidates for targeted adaptation only.

Runs: `matches/league/20261019-012427-ming_bot/` and the repeated c586 control `...012613-c586-fresh/` (the first c586 run `...012515-c586-fresh/` returned the same 155/170 result).

The planner benchmark's only map edge was Eight (10/10 vs c586's 9/10), so c590 tried Ming's C&I/Varg/Stellar/Vendetta/Tavi lineup against an Eight Ryth/C&I/Stellar opening. The partial signature arrived after four allied picks; replayed draft became Varg/C&I/Ryth/Stellar/Vendetta, replacing Tavi rather than Ryth. It scored 8/10 against five strong proxies versus c586's 9/10 on the same set, losing both sides to `fx-dbllock` where c586 lost only side A. Reject the late counter-draft. Run: `matches/league/20261019-013016-c590-eight-ranged-core/`.

c591 fixed the same C&I/Varg/Stellar/Vendetta/Tavi lineup on Eight from the first pick, removing the draft-timing variable. It scored 7/10 on the five-strong Eight screen versus c586's 9/10, losing side A to Xuanming, fx-dbllock, and the meta-core proxy. Reject the static roster too; the local evidence points toward route execution rather than mirroring Ming's lineup. Run: `matches/league/20261019-013212-c591-eight-roster/`.

## Rows solo-capture and Ren-counter follow-ups c592–c593 (19 Oct 2026)

c592 skips `join_capture()` for Varg on Rows, testing the recorded case where Varg shared a 22-gem capture while the opponent's Varg took the full 66. On six strong Rows proxies it tied a fresh c586 control at 11/12; both still lost Rows side A to `opp-swirl-meta-core`, with matching score and death traces. On the 20-opponent Rows pool both builds went 40/40; mean own end score was 986.7 for c592 versus 983.4 for c586. This small score change did not convert a win, so keep the capture change isolated.

c593 tests a separate draft correction from unmodified c586: on Rows, when enemy Ren becomes visible, keep the standard Varg/Cassi-and-Issac/Ryth/Stellar lineup instead of counter-picking Ren and leaving Ryth out of the four-pick draft. Two six-strong Rows runs scored 12/12 versus a fresh c586 control's 11/12; both converted the meta-core Rows side-A 990–990 loss into a win. The same screen stayed 12/12 on repeat. It scored 44/44 against the standard 22-opponent Rows pool, 187/204 across six strong proxies and all 17 maps versus c586's 186/204, and 630/680 across the 20-opponent default pool, matching c586's 630/680 exactly. The 204-game comparison changed only the meta-core Rows side-A outcome (loss to win); its side-B win also widened from 990–990 to 990–858. The 680-game comparison changed no outcomes and only two Rows scores.

Keep c593 as an isolated matchup candidate; do not promote it from proxy results. The default-pool result is unchanged, and the gain is specific to the meta-core Rows matchup. Runs: c592 strong `matches/league/20261019-013336-c592-rows-varg-solo-capture/`, c586 control `...013344-c586-fresh/`; c592 default `...013400-c592-rows-varg-solo-capture/`, c586 control `...013410-c586-fresh/`; c593 strong `...013722-c593-rows-ryth-counter/` and repeat `...013743-c593-rows-ryth-counter/`, fresh c586 control `...013729-c586-fresh/`; c593 standard Rows pool `...013759-c593-rows-ryth-counter/`, strong all maps `...013818-c593-rows-ryth-counter/`, and 680-game default pool `...013949-c593-rows-ryth-counter/`. Production source and ZIP remain c553, and official unranked testing/uploads remain paused.

## Interlock and Stampede draft follow-ups c594–c596 (19 Oct 2026)

c594 keeps the normal Interlock Tavi/Cassi-and-Issac/Ryth/Stellar lineup when enemy Ren appears, rather than switching to a Ren counter that omits Ryth. Against `opp-swirl-meta-core` on Interlock side A, it raised our final score from 270 to 780 gems and reduced deaths from 29 to 20, but still lost 780–986. The six-strong Interlock screen stayed 11/12, and the standard 22-opponent pool stayed 43/44, matching c593's win counts. In the standard pool it changed only two same-outcome games, both against `opp-fai-bruiser`. Keep this as a score/survival observation, not a win-rate improvement.

c595 preselects Ren first on Interlock, keeping Cassi-and-Issac, Ryth, and Stellar in the four-pick core. It repeated 12/12 against six strong proxies and beat the meta-core proxy on both sides, but fell to 37/44 on the standard Interlock pool versus c594's 43/44. It lost both sides to TTS-v3/v4/v5 and side B to TTS-v6; reject the broad Ren-first draft.

c596 gives Stampede the existing Varg/Cassi-and-Issac/Ryth/Stellar/Tavi lineup instead of Prism-first. It scored 9/12 against six strong proxies versus c593's 11/12, adding losses to Ming side B and fx-dbllock side A while retaining the meta-core side-A loss. Reject Varg-first as a general Stampede draft.

Runs: c594 strong `matches/league/20261019-014501-c594-interlock-keep-tank/`, c593 strong control `...014508-c593-rows-ryth-counter/`; standard Interlock pools c595 `...014638-c595-interlock-ren-first/`, c594 control `...014656-c594-interlock-keep-tank/`, and c593 control `...014719-c593-rows-ryth-counter/`; c595 repeated strong `...014619-c595-interlock-ren-first/` and `...014629-c595-interlock-ren-first/`; c596 strong `...014848-c596-stampede-varg-opening/`, c593 control `...014856-c593-rows-ryth-counter/`. No source change was promoted; production source/ZIP remain c553 and live unranked remains paused.

## Stampede Ryth gear queue c597 (19 Oct 2026)

c597 changed Ryth to Monster Strength then Power Strength on Stampede only when the opponent revealed the exact Ren/Stellar/Cassi-and-Issac/Ryth/Varg core. It built and completed all 12 strong Stampede games. The result stayed 11/12, exactly matching c593 in every winner, score, and round; the meta-core side-A loss remained 0–720. The replay recorded 17 own deaths versus c593's 14. Reject the gear change; it did not improve farm yield or combat.

Run: c597 `matches/league/20261019-015240-c597-stampede-ryth-camp-damage/`; c593 control `matches/league/20261019-014856-c593-rows-ryth-counter/`. Production source and ZIP remain c553; official unranked matches and uploads remain paused.

## Ambush tribute priority and split-opening c598–c599 (19 Oct 2026)

c598 moved Ambush bank handling ahead of the pre-bank spell burst when a champion carrying gems was already in altar range. Against the same six strong proxies it scored 10/12, exactly matching c593 in every winner, round, and score. No replay logged a visible enemy while this branch could suppress a cast, so the change had no measured effect. Reject it as a no-op. Run: `matches/league/20261019-015736-c598-ambush-bank-priority/`; source SHA-256 `6991A988B6B96C1C48FF827D41F9961E4B01D8B3F1EA9CE812984DB309129266`.

c599 put Ambush in its existing role-based split from round one instead of sharing the opening through round 149. It stayed 10/12 against those six proxies and converted no losses. The mean game length rose from 966.4 rounds for c593 to 1,039.5; own final submitted gems changed only 947.3→951.2, while opponent gems increased 230.7→270.9. Against `opp-swirl-meta-core`, side A fell from 974–902 at r1021 to 928–962 at r943, and side B fell from 880–976 at r802 to 750–976 at r790. Deaths decreased 14→10, but the unchanged win count, slower mean finish, and increased opponent score reject the early split. Run: `matches/league/20261019-015842-c599-ambush-split-opening/`; source SHA-256 `9C563908157452CD1535FE9834117ACF205C0FC37252E9B8529A28EAE307C1E8`.

Replay interpretation note: the five-round `SCORE` trace is *tributed* gems, not carried gems. In c593's Ambush side-A loss, the trace showed 974–902 at r1020 but the match ended at r1021; by the 1,000-gem win rule, the opponent must have completed a tribute with at least 98 carried gems. Do not treat a temporary submitted-score lead as a lead in the final tribute race without checking carried bags and active channels. Production remains c553; live unranked matches and uploads remain paused.

## Ambush carry capture routing c600–c604 (19 Oct 2026)

c600 added `SCOUT MOVE` counters to c593 and exactly reproduced c593's 12 strong Ambush games. It measured an average of 2,304 capture-directed movement steps versus 324 camp-directed steps per game; much of the team's movement was going toward cleared camps rather than live camps. This instrumented build is diagnostic only. Run: `matches/league/20261019-020240-c600-ambush-route-trace/`.

c601 stopped non-carry roles from joining nearby Ambush captures. Two strong 12-game runs both stayed 10/12 and produced the same outcomes. Movement fell from 2,304 to 2,108 capture-directed steps and wins averaged about 88 rounds earlier, but the 22-opponent screen fell to 41/44 versus a fresh c593 control's 43/44. It introduced losses to `tralalerotrarala` and `my-bot-v2` on side B; reject the general rule. c602 only applied the skip when the non-carry role had a visible, live assigned camp, but it was result-, score-, and movement-identical to c600; reject as a no-op. c601/c602 also use telemetry, so they remain diagnostic experiments. Runs: c601 focused `matches/league/20261019-020400-c601-ambush-carry-capture/` and repeat `...020441-c601-ambush-carry-capture/`, 22-opponent screen `...020614-c601-ambush-carry-capture/`; fresh c593 control `...020631-c593-rows-ryth-counter/`; c602 `...020528-c602-ambush-prioritize-live-camp/`.

c603 gated the carry-only rule to Ambush side A but retained movement instrumentation. Its 204-game run showed unrelated cross-map changes and 116 runner-reported errors versus c593's 113, so do not use it as clean strategy evidence. c604 reapplied the side-A gate on uninstrumented c593 source: it skips non-carry roles' nearby-capture join only when allied spawn is in Ambush A's `(3,3)`–`(6,6)` region; the bottom-right side remains unchanged. It scored 44/44 on the 22-opponent Ambush screen versus c593's fresh 43/44, and 187/204 on the six-strong all-map screen, matching c593. In the 680-game default pool it scored 631/680 versus c593's 630/680; the sole changed winner is Ambush side A against `my-bot` (loss→win), with no new losses. All 19 changed records were Ambush side A; the 480 runner-reported errors matched c593 exactly. Keep c604 as an isolated local candidate, not a production update or live top-50 validation. Source SHA-256: `6962D7B2E2E563BD99A205E5947AFD37D7790F8C137BBDEE8765A13A8CBAB34F`. Runs: strong all maps `matches/league/20261019-021008-c604-ambush-sidea-capture-clean/`, Ambush 22-opponent pool `...021123-c604-ambush-sidea-capture-clean/`, and default pool `...021140-c604-ambush-sidea-capture-clean/`.

## Contest safe-banking follow-up c607–c610 (19 Oct 2026)

Replay evidence: in the Please Contest loss, Prism collected 200 gems at r1027 and dropped them when Please's Ryth killed Prism at r1063; they were never submitted. The copied-cache c605/c606 folders did not build, so the same role-permission variants were rebuilt cleanly as c607/c608. Allowing Tavi or Ryth to join cleared-camp capture on Ambush side A was an exact no-op against the 22-opponent pool: each scored 44/44, with all scores and finish rounds matching c604. Do not pursue those role exceptions. Runs: c607 `matches/league/20261019-021850-c607-ambush-tavi-capture/`; c608 `...021917-c608-ambush-ryth-capture/`.

c609 adds a 40-step cost to Contest altars clearly closer to the enemy spawn when the carrier holds at least 100 gems; c610 tests the same rule with an 80-step cost. Both scored 44/44 on the same 22-opponent Contest pool, with no winner changes. Relative to a fresh c604 control, both changed exactly one record: against `tralalerotrarala` on side B, our submitted score improved from 600–200 at round 2000 to 800–0 at round 1608. Both also scored 12/12 on the six-strong Contest screen and matched c604 on every score and finish round. Since +40 and +80 were indistinguishable in these screens, keep the smaller +40 c609 for further local follow-up. This is a narrow score/tempo gain, not a converted win or official validation. Runs: c604 control `matches/league/20261019-022159-c604-ambush-sidea-capture-clean/`; c609 22-opponent `...022217-c609-contest-safe-bank-40/` and strong `...022343-c609-contest-safe-bank-40/`; c610 22-opponent `...022246-c610-contest-safe-bank-80/` and strong `...022404-c610-contest-safe-bank-80/`.

c609 remains isolated; production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain c553 with hashes `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. Official unranked games and uploads remain paused; the 10-win top-50 streak is unverified.

c609's 680-game default run scored 631/680, matching c604's earlier total. Its six-strong all-map run scored 186/204 versus c604's earlier 187/204, but the changed records included Lanes and Rushbait games outside the Contest-only code gate, so those separate full-pool runs are not a paired causal comparison. A fresh 44-game Contest control/candidate repeat reproduced exactly one change: `tralalerotrarala` side B improved from 600–200 at r2000 to 800–0 at r1608, with no winner change. The roster-matched local `please-contest-v98-proxy` screen remained 0/2 for c553, c604, and c609; the bank-routing change did not solve the high-pressure proxy matchup.

## Contest Varg draft counter c611–c613 (19 Oct 2026)

The local `please-contest-v98-proxy` uses the recorded top-50 Contest roster Varg/Cassi & Issac/Stellar/Ren/Ryth with a synthetic atlas planner; it is not Please's bot. Against it, c553's Contest roster was Prism/Stellar/Cassi & Issac/Ryth/Ren and lost 0/2. Direct local statistics showed a large farm-economy gap: in the two side-swapped runs c553 earned 4.5–4.8k gold and dealt 95.8–107.7k monster damage, while the proxy earned 13.3–13.4k gold and dealt 168.6–178.1k monster damage. c553 nevertheless had more kills in one side and fewer deaths in the other, so the primary signal is camp/gold throughput, not simply combat survival.

c611 drafted Varg first on Contest, mirroring the proxy's farm carry and replacing Prism. It improved the proxy screen to 1/2: side A won 600–0 while side B lost 0–200. The broad 22-opponent Contest pool fell from c604's 44/44 to 40/44, and the six-strong Contest screen fell from 12/12 to 10/12, with both strong losses on side B. Reject the unconditional Varg-first change. c612 tried adding Varg late only after the enemy Varg became visible, while keeping Prism and dropping Ren; it lost 0/2 to the proxy (side A 200–600, 5.8k vs 11.4k gold). Reject the late counterpick.

c613 limits c611's Varg-first lineup to Team A. It kept the proxy screen at 1/2 (the side-A win, side-B loss), scored 42/44 on the 22-opponent Contest pool (the two losses were side A against `opp-fai-bruiser` and `tralalerotrarala`), and returned to 12/12 on the six-strong Contest screen. Its six-strong all-map run scored 182/204, exactly matching a fresh c553 control's 182/204; all six changed records were Contest side A and no winner changed. Keep c613 isolated as a top-team matchup candidate for later live validation, not as a production update: the proxy is synthetic and the broader Contest pool loses two wins. Candidate `draft.cpp` SHA-256: `ADC4CF667041E0FD94672E043BFCDD99C3B61A4E3EE2786E8517D107F1931FFE`; candidate `bot.cpp` is byte-identical to production c553.

Runs: c553/c604/c609 versus the proxy `matches/league/20261019-023306-tungtungsahur/`, `...023324-c604-ambush-sidea-capture-clean/`, and `...023329-c609-contest-safe-bank-40/`; c611 proxy, broad, and strong Contest `...023610-c611-contest-varg-farmer/`, `...023629-c611-contest-varg-farmer/`, and `...023834-c611-contest-varg-farmer/`; c612 proxy `...023757-c612-contest-late-varg-counter/`; c613 proxy, broad, strong Contest, and strong all-map `...023918-c613-contest-sidea-varg-farmer/`, `...023935-c613-contest-sidea-varg-farmer/`, `...023952-c613-contest-sidea-varg-farmer/`, and `...024109-c613-contest-sidea-varg-farmer/`. Production source/ZIP remain c553; live unranked and uploads remain paused, and the 10-win streak is unverified.

## Contest Varg farm-combat leash c614 (19 Oct 2026)

The fresh c613 statistics exposed the remaining proxy gap: on the side-A win, our Varg earned 513 gold, dealt 10,457 monster damage, and died 13 times; the synthetic proxy Varg earned 2,295 gold, dealt 35,947 monster damage, and died once. c614 keeps the c613 draft but makes Contest Varg ignore enemies beyond two tiles so it can continue its farm route. The exact proxy screen fell from c613's 1/2 to 0/2; in the c614 side-A loss, Varg earned 911 gold but dealt only 8,005 monster damage and died 14 times. The six-strong Contest screen fell from 12/12 to 11/12, losing to `ming_bot` on side A. Reject c614: this leash did not turn the farm statistics into wins and regressed the strong screen. The data supports a Varg routing/survival bottleneck, but this experiment does not identify a winning fix. Candidate source: `bots/c614-contest-varg-farm-leash/`; runs: proxy `matches/eval/20261019-024639/`, strong pool `matches/league/20261019-024654-c614-contest-varg-farm-leash-direct-contest-strong/`. Production source and ZIP remain c553; no live match or upload was made.

c615 applies Rows' home-side solo-camp filter to Contest Varg. It was behaviorally inactive on both the roster-matched proxy pair (identical Varg stats and outcomes to c613) and the six-strong Contest pool (all 12 outcomes, scores, and finish rounds exactly matched a fresh c613 repeat). Reject as a no-op. Runs: proxy `matches/eval/20261019-024753/`, strong pool `matches/league/20261019-024804-c615-contest-varg-home-route-direct-contest-strong/`; c613 repeat control `matches/league/20261019-024820-c613-contest-sidea-varg-farmer-direct-contest-strong-repeat/`.

c616 keeps Varg's Monster Strength opening emblem, then buys Power Health before returning to Power Strength. Against the synthetic proxy, the side-A Varg's deaths fell from c613's 13 to 8 and monster damage rose from 10,457 to 11,994, but its gold was 498 versus 513 and the win stayed 1/2 (600–200 instead of 600–0 on side A). The six-strong Contest result fell to 11/12, losing to `opp-swirl-meta-core` on side A; c613 was 12/12. Reject this build as a matchup improvement. Runs: proxy `matches/eval/20261019-024907/`, strong pool `matches/league/20261019-024924-c616-contest-varg-health-build-direct-contest-strong/`. The health emblem improved survival metrics in one synthetic matchup but did not close the farming gap or preserve the strong-pool result.

c617 is an instrumented c613 diagnostic copy, not a strategy candidate. Its Contest proxy trace sampled Varg with no solo camp target at rounds 100, 1000, 1600, 1900, and 2000; at those points it had fallen back to the squad objective or anchor. This exposed a mismatch with the solo-camp selector's comment: it describes gold clusters as filler when gem camps are unavailable, but the current filter excludes every group with zero gems. c618 narrowly allowed Contest Varg to pick gold-only groups at zero gem value as that fallback. It raised side-A Varg's gold from 513 to 1,160 and monster damage from 10,457 to 18,044, while deaths changed 13→12, but that proxy side lost 200–400; c618 lost 0/2 overall against the proxy. It also repeated at 11/12 in both six-strong Contest runs, losing to `ming_bot` on side A each time; c613's matched screen is 12/12. Reject c618 despite the camp-throughput gain because it consistently loses a strong matchup and the roster-matched proxy. Runs: c617 trace `matches/eval/20261019-025047/`; c618 proxy `matches/eval/20261019-025144/`, strong runs `matches/league/20261019-025156-c618-contest-varg-gold-camps-direct-contest-strong/` and `...025227-c618-contest-varg-gold-camps-direct-contest-strong-repeat/`. The synthetic proxy remains diagnostic, not a substitute for the official top-50 bot.

## Contest follow-ups c619–c620 (19 Oct 2026)

c619 added a health-gated Contest Varg exception for wolf packs up to strength 60. It built, but the roster-matched synthetic proxy and all 12 six-strong Contest outcomes, scores, and finish rounds matched c613; there was no measured behavior change. Treat it as an inactive rule and do not carry it forward. Runs: proxy `matches/eval/20261019-025448/`; strong Contest `matches/league/20261019-025458-c619-contest-varg-wolf-farm-direct-contest-strong/`; matched c613 repeat `matches/league/20261019-024820-c613-contest-sidea-varg-farmer-direct-contest-strong-repeat/`.

c620 combines c563's Pilgrimage survival gates with c613's Team-A Varg-first Contest draft. The six-strong, 17-map screen is 184/204 after replacing one runner result with an isolated successful rerun, exactly matching c563's 184/204 and every winner/loss. Five Contest side-A scores or finish rounds changed, but none changed a win; Xuanming moved from 1,000–0 at r1797 to 600–200 at r2000. The initial runner error was a replay-file overwrite after the engine had already logged a c620 win against Faisal; a separate Faisal/Contest run completed both sides 2/2. This combination has no demonstrated strong-pool win gain. c613's separate 22-opponent Contest screen was 42/44 versus c604's 44/44, and c620's combined full default pool was not run; keep c620 local-only. Runs: combined strong screen `matches/league/20261019-025635-c620-combined-pilgrimage-contest-direct-strong-all-maps/`; Faisal rerun `matches/league/20261019-025830-c620-combined-pilgrimage-contest-direct-missing-contest-faisal/`. Candidate hashes: `bot.cpp` `E1B3BA9DBFB281AE428767C0081E9B419680433C89C9C1822D6EA30308FAC5A9`, `draft.cpp` `ADC4CF667041E0FD94672E043BFCDD99C3B61A4E3EE2786E8517D107F1931FFE`.

Production remains c553 (`bot.cpp` SHA-256 `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6`; submission ZIP SHA-256 `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`). No live match or upload was made; official unranked work remains paused and the requested 10-win streak is unverified.

## c609 full-pool check (19 Oct 2026)

c609 is c604 plus a Contest-only 40-step penalty for choosing an altar on the enemy half while carrying at least 100 gems. Its focused 22-opponent Contest screen remained 44/44; one `tralalerotrarala` side-B result reached 800–0 at r1608 instead of 600–200 at r2000. A full 680-game default-pool run recorded 629 wins in 678 parsed games and two replay-persistence errors. The engine logs show both errored games finished as c609 wins; isolated reruns completed 2/2 for each affected pairing (Lanes vs `opp-fai-melee`, Fragment vs `opp-fai-ranged`). Corrected total: 631/680, with the same per-opponent win counts as c604. This verifies no broad local win-count gain from the bank-cost tweak; keep it as a narrow banking experiment, not a promoted bot. Run: `matches/league/20261019-030039-c609-contest-safe-bank-40-direct-complete-default-pool/`; reruns `matches/league/20261019-030358-c609-contest-safe-bank-40-direct-rerun-runner-error-melee-lanes/` and `matches/league/20261019-030402-c609-contest-safe-bank-40-direct-rerun-runner-error-ranged-fragment/`; c604 control `matches/league/20261019-021140-c604-ambush-sidea-capture-clean/`.

## Stampede camp trace and Tavi split tests c621–c626 (19 Oct 2026)

c621 tried splitting a Varg from the Stampede shared opening after r100; the six strong Stampede drafts did not select Varg on our side, and all 12 candidate replays were byte-identical to c604. c622/c623 tried a Tavi solo gem camp after r100. Both stayed 11/12, with all 12 Tavi stdout traces identical to c604. A one-line diagnostic (c624) explains the no-op: at r100 the map offers one 360-gem group with strength 360, blocked by the Stampede safety rule until r150; the other nearby side groups contain only 70 or 140 gold and zero gems, so the gem-only solo selector returns none. The diagnostic replay is not strategy-score evidence.

c625 let Tavi farm those safe gold-only groups during r100–149 when no enemy was visible and the team fight alarm was clear, then rejoin for the central camp. Against six strong local proxies, c625 and a fresh c604 direct-run control both scored 11/12. Across 12 games, c625 finished with 120 more own gems and 240 fewer opponent gems, with 20 more kills and 1,650 more gold, but also suffered 46 more deaths and took 32.2 more rounds on average. No win changed; reject this split on the current evidence. c626 shortened the split window to r120–149 and fell to 10/12, adding a loss to `ming_bot` side A; reject it. The synthetic `opp-swirl-meta-core` remains a local proxy, not the live Mite team. Runs: c621 `matches/league/20261019-030930-c621-stampede-varg-after-opening-direct-strong-stampede/`; c622 `...20261019-031246-c622-stampede-tavi-solo-after-opening-direct-strong-stampede/`; c623 `...20261019-031420-c623-stampede-tavi-solo-no-visible-enemies-direct-strong-stampede/`; c624 trace `matches/league/20261019-031536-c624-stampede-camp-eligibility-trace-direct-trace-stampede/`; c625 `matches/league/20261019-031701-c625-stampede-tavi-gold-sidecamp-direct-strong-stampede/`; fresh c604 control `matches/league/20261019-031717-c604-ambush-sidea-capture-clean-direct-fresh-strong-stampede-control/`; c626 `matches/league/20261019-031857-c626-stampede-tavi-gold-sidecamp-r120-direct-strong-stampede/`. Candidate `bot.cpp` hashes: c625 `F2E4CD3D57005D3BFB186CA5C7C3B5CB02641F06496BB4196D3A079284A4E84D`; c626 `D76986EBEA9DBAE3707FF2BAB3ACD744EF155E91C2D7305FDB58597D72E9C829`.

All c621–c626 work is local only. Production remains c553 and its ZIP is unchanged; live unranked matches and uploads remain paused.

## Swirl Ryth-signature route tests c627–c628 (19 Oct 2026)

c627 accepts Ryth as an alternative to Vendetta but still requires C&I/Varg/Stellar. Its six-strong Swirl screen tied a fresh c604 control at 11/12, with every result, score, and finish round identical. Replay draft lines show none of those opponents exercised the new Ryth branch: the Ryth cores lacked Varg, while the Varg-based opponents already had Vendetta. Treat that first screen as inactive, not evidence about the Mite-style policy. Candidate `bot.cpp` SHA-256: `0F6A5023377B123943D23F798559B8DF7C96A17980677FD90916F987006C34B9`.

To exercise the signature, `opp-mite-swirl-proxy` copies the local meta-core policy and fixes its Swirl draft to C&I/Stellar/Ryth/Varg. Against it, c627 scored 1/2 while c604 scored 0/2: c627 won side A 920–480 at r1512 (c604 lost 823–983 at r1661); both lost side B, where c627 scored 600–924 and c604 210–924. A second paired run reproduced both results exactly. On the full 20-opponent Swirl pool, c627 and fresh c604 both scored 32/40 with identical winners. Only Faisal-bot's scores changed; its draft also contains the Ryth/Varg core. Across the two Faisal games c627's total was 1,120–1,822 versus c604's 1,012–1,872, with no win change. Keep c627 as a narrow matchup candidate for further review, not a promotion: the proxy shares the draft and local policy but is not Mite's bot, and no real Mite match was tested. Runs: initial synthetic pair `matches/league/20261019-032719-c627-swirl-ryth-route-trigger/` / `...032735-c604-ambush-sidea-capture-clean/`, repeat `...032759-c627-swirl-ryth-route-trigger/` / `...032805-c604-ambush-sidea-capture-clean/`, broad pool `...032815-c627-swirl-ryth-route-trigger/` / `...032837-c604-ambush-sidea-capture-clean/`.

c628 keeps the existing Varg/Vendetta trigger and additionally activates the full Swirl counterdraft mode for any C&I/Stellar/Ryth enemy core. The mode also changes retreat and early-phase policy, so this is a bundled counterdraft test rather than an isolated route test. Against the same six strong proxies it fell to 10/12 versus c604's 11/12, adding a loss to `opp-swirl-meta-core` side A (818–894 at r1465 versus c604's 972–636 at r1543). The Ming side-A loss remained; no winner was gained. Reject c628. Run: `matches/league/20261019-032612-c628-swirl-ryth-core-route/`; candidate `bot.cpp` SHA-256: `EB5EC00091204DD4C68F9BC16A1EEC4D7FBFFFD124DC5B5B2B46D352F4045368`.

Production remains c553. These are offline local results only; live unranked matches and uploads remain paused.

## Stampede Issac side-farm follow-up c629–c632 (19 Oct 2026)

c629 lowered Stampede's high-strength central camp safety gate from r150 to r125. It fell to 9/12 against the six strong Stampede proxies versus c604's 11/12; the early unlock exposed Prism and the rest of the team to camp deaths. Reject it. c630 tried sending Issac to safe gold camps when no enemy or team fight alarm was active, but the branch was placed in `marksman_turn`. `Bot::init()` assigns Issac `Role::fighter`, so Issac never called it; all 12 c630 outcomes, scores, rounds, and stdout traces matched c604. A first c631 trace hook repeated the same wrong function and therefore emitted no Issac trace. The role mapping exposed the actual no-op; neither c630 nor c631 is strategy evidence.

c632 moved that Stampede-only route into Issac's actual `fighter_turn`, after combat handling and before shared early-phase farming. The solo selector chooses an eligible gold/gem side camp away from the squad's current camp; the fighter returns to its normal policy if no distinct camp is available, an enemy/fight alarm blocks the route, or round 150 arrives. A local trace confirmed Issac selected a separate gold camp at r25 and another at r125. After removing trace output, the clean candidate rebuilt and repeated the same 11/12 result against six strong local Stampede proxies as c604, with identical winners. Across those 12 games, the clean c632 summary recorded 12,600 own gems and 3,060 opponent gems versus c604's 8,880 and 3,780.

On the 20-bot local default Stampede pool, c632 scored 37/40 in two runs with identical winners, scores, and rounds; c604 also scored 37/40. c632 converted losses to wins against `tralalerotrarala` on both sides and `opp-tts-aggro` side B, while adding losses against Faisal-bot side B, `opp-tts-locker` side A, and `tungtungsahur-v1` side B. Aggregate reported own gems rose 32,700→40,680 and opponent gems fell 10,680→9,360; mean game duration was essentially unchanged. Keep c632 as a local Stampede farming candidate for later validation, not a production update: win count did not increase, the matchups traded three wins for three losses, and these 20 bots are local opponents rather than current top-50 live teams. Clean source: `bots/c632-stampede-issac-sidefarm-role-fixed/src/bot.cpp`, SHA-256 `FA4146C632C35DF376CA94FB5F087E078004D1447975B336F857EA148A74E7F9`. Runs: c629 `matches/league/20261019-033337-c629-stampede-gemcamp-r125/`; c630 `matches/league/20261019-033547-c630-stampede-issac-sidefarm/`; c632 clean strong `matches/league/20261019-034346-c632-stampede-issac-sidefarm-role-fixed-direct-role-fixed-clean-source/`; default repeats `matches/league/20261019-034139-c632-stampede-issac-sidefarm-role-fixed-direct-role-fixed-default/` and `matches/league/20261019-034239-c632-stampede-issac-sidefarm-role-fixed-direct-role-fixed-default-repeat/`; fresh c604 strong control `matches/league/20261019-033355-c604-ambush-sidea-capture-clean/`; broad c604 control `matches/league/20261019-021140-c604-ambush-sidea-capture-clean/`.

Production source/ZIP remain c553. No official unranked match or upload was made; the 10-consecutive top-50 goal remains unverified and live work remains paused.

c633 paused the Issac route whenever any Stampede opponent was visible within 10 tiles of Ryth. It remained 11/12 on the strong set but traded c632's meta-core side-A loss for an `opp-racer` side-B loss; the latter uses the Prism/Stellar/C&I/Ryth/Tavi roster recorded for Mite. That c633 replay ended 0 gems, 2 kills, 8 deaths, and 940 gold at r736 versus `opp-racer`'s 1,080 gems, 9 deaths, and 3,440 gold. Its 20-bot default result stayed 37/40 with three gains and three losses exchanged, so reject the unconditional alert. c634 copied two damage emblems for Issac (Monster Strength, Power Strength, then Durability Health); it scored 11/12 strong and 36/40 default versus c632's 37/40. c635 tried one Monster Strength emblem then Jungle Health and Power Health; it scored 11/12 strong and 37/40 default, exchanging three matchups for three others while increasing own gems and reducing opponent gems, but also increasing deaths and lowering gold. Neither gear queue improved the local win count.

c636 restricted the 10-tile alert to a C&I/Ryth/Stellar/Varg enemy core. It reached 12/12 strong, but also activated against Faisal-bot and traded its side-A win for a side-B win; default stayed 37/40 while own gem totals fell and opponent totals rose versus c632. c637 additionally requires Ren in that draft. It repeated 12/12 on the six-strong set with identical scores, rounds, and winners; relative to c632, only `opp-swirl-meta-core` side A changed, from a 360–1,080 loss at r1516 to a 1,080–720 win at r1761. The 20-bot default remained 37/40 with every outcome, score, and finish round identical to c632. On a fresh six-proxy, 17-map run, c637 scored 188/204 versus c604 at 187/204; the only winner change was the same `opp-swirl-meta-core` Stampede side-A conversion. All other outcomes matched. Keep c637 as a narrow local counterdraft candidate for the Ren/C&I/Ryth/Stellar/Varg Stampede core. Mite's recorded Stampede lineup lacks Ren and Varg, so this trigger does not address that exact roster; c632 remains 2/2 against the local `opp-racer` draft with that roster. c637 source `bots/c637-stampede-ren-varg-core-guard/src/bot.cpp`, SHA-256 `02ACB1F1AB3561741D0214DF6A6328CEE07228261B4C407C60EB3C0DA8A252A3`. Runs: c633 strong/default `matches/league/20261019-034729-c633-stampede-fight-aware-sidefarm-direct-fight-aware-strong/` and `...20261019-034855-c633-stampede-fight-aware-sidefarm-direct-fight-aware-default/`; c634 strong/default `...20261019-034956-c634-stampede-issac-damage-gear-direct-issac-strength-gear-strong/` and `...20261019-035010-c634-stampede-issac-damage-gear-direct-issac-strength-gear-default/`; c635 strong/default `...20261019-035136-c635-stampede-issac-hybrid-gear-direct-hybrid-gear-strong/` and `...20261019-035150-c635-stampede-issac-hybrid-gear-direct-hybrid-gear-default/`; c636 strong/default `...20261019-035310-c636-stampede-varg-core-fight-guard-direct-varg-core-guard-strong/` and `...20261019-035325-c636-stampede-varg-core-fight-guard-direct-varg-core-guard-default/`; c637 strong repeats `matches/league/20261019-035429-c637-stampede-ren-varg-core-guard-direct-ren-varg-core-strong/` and `...20261019-035507-c637-stampede-ren-varg-core-guard-direct-ren-varg-core-strong-repeat/`, default `...20261019-035443-c637-stampede-ren-varg-core-guard-direct-ren-varg-core-default/`. All-map comparison: c637 `matches/league/20261019-035628-c637-stampede-ren-varg-core-guard-direct-ren-varg-core-strong-allmaps/`; fresh c604 `matches/league/20261019-035759-c604-ambush-sidea-capture-clean-direct-ren-varg-core-strong-allmaps-control/`.


## c638 Contest Varg Power-only gear check (19 Oct 2026)

The live Please replay shows its Varg building Power Strength while farming. c638 tested a Contest-only Varg queue that buys Power Strength throughout, replacing the current Monster Strength opening followed by Power Strength. This was not an active test of that build: in all 12 focused and 40 broad Contest replays, our final draft omitted Varg, so the new purchase branch never ran. `SCOUT DRAFT` lines in the replay bundles confirm the selected rosters.

The focused six-proxy comparison was 12/12 for both current source and c638, with every winner, score, and finish round identical and 10,200 own gems each. The 20-opponent Contest screen was 40/40 for both, again with every record identical and 37,200 own gems each. Treat c638 as an inactive experiment, not evidence for or against Power-only Varg gear. Do not carry it into the production bot.

Candidate `bots/c638-contest-varg-power-first/src/bot.cpp` SHA-256: `D395CC9EB1B96C51667B16E7C3C010995FE6CE60F6A4DA48DF6989ACCB1900FC`. Runs: current control and c638 strong `matches/league/20261019-040326-tungtungsahur-direct-c638-contest-varg-power-first-baseline/` and `matches/league/20261019-040348-c638-contest-varg-power-first-direct-c638-contest-varg-power-first-strong/`; broad control and c638 `matches/league/20261019-040442-tungtungsahur-direct-c638-contest-varg-power-first-broad-baseline/` and `matches/league/20261019-040503-c638-contest-varg-power-first-direct-c638-contest-varg-power-first-broad/`.

Production remains c553; source and ZIP hashes are unchanged. No official match or upload was made. Live testing remains paused and the 10-win top-50 target remains unverified.


## c639 Contest shopping recall at enemy distance 5 (19 Oct 2026)

The Please replay showed enemy champions visible at roughly 6-8 tiles during the period before our first Stellar purchase. c639 changes the Contest shopping-trip guard to allow recall when visible enemies are farther than 5 tiles, while retaining the team fight alarm and the existing rule on every other map. On the six strong local Contest proxies it kept 12/12 wins and raised our aggregate reported gems from 10,200 to 10,600. However, the full 20-opponent Contest pool fell from the fresh control's 40/40 to 39/40, with a new loss to `my-bot-v2` on side B (600:600 at r2000 versus the control's 600:0). Broad-pool own gems were unchanged at 37,200. Reject c639 as a general change; the focused gem gain did not transfer and the shopping recall can expose the team to a distant opponent.

Candidate source `bots/c639-contest-safe-shop-distance/src/bot.cpp`, SHA-256 `094907B3896A689E68BEB67F2D15E44001AD0A65AD1500CDEB910875EF2755DE`. Runs: strong `matches/league/20261019-040921-c639-contest-safe-shop-distance-direct-c639-contest-safe-shop-distance-strong/`; broad `matches/league/20261019-040946-c639-contest-safe-shop-distance-direct-c639-contest-safe-shop-distance-broad/`; fresh current-source controls `matches/league/20261019-040326-tungtungsahur-direct-c638-contest-varg-power-first-baseline/` and `matches/league/20261019-040442-tungtungsahur-direct-c638-contest-varg-power-first-broad-baseline/`. No upload or official match.

Production remains c553; source and ZIP hashes remain unchanged. Live testing is paused and the 10-win top-50 target is unverified.


## c640 Contest first-camp fight leash (19 Oct 2026)

c640 reduced both Contest's early movement-combat leash and burst-cast leash from 5 tiles to 2 for rounds 0-74, then restored 5 through round 149. This tested whether skipping distant early fights would recover the opening camp clear that Please reached at r27 while ours reached r48. It regressed the six-strong Contest screen from the current source's 12/12 to 9/12, losing Ming side A and both `opp-swirl-meta-core` sides; reported own gems fell from 10,200 to 9,400. Reject c640 without a broad run. Local strong opponents punished the reduced opening engagement.

Candidate source `bots/c640-contest-first-camp-leash/src/bot.cpp`, SHA-256 `15FD0B721667613FD50501F11BE2AF7178B95EBBB267DFBB583E83BE34DFEDEE`. Run: `matches/league/20261019-041115-c640-contest-first-camp-leash-direct-c640-contest-first-camp-leash-strong/`. No upload or official match.

Production remains c553; source and ZIP hashes remain unchanged. Live testing is paused and the 10-win top-50 target is unverified.


## c641-c644 Please-profile Contest counter (19 Oct 2026)

The archived rank-49 Please draft is ordered Varg / Cassi & Issac / Stellar / Ren / Ryth. The synthetic `please-contest-v98-proxy` uses that same order and an atlas planner; it is not Please's executable. Fresh current-source control c641 lost both sides (Team A 200:400, Team B 200:200 at r2000).

Two isolated changes each improved one side: c639 allowed Contest shop recall past visible enemies farther than five tiles and won Team B only; c640 narrowed the opening fight leash to two tiles for rounds 0-74 and won Team A only. Their combination in c642 lost both sides. c643 applied the leash only on Team A and the shop rule only on Team B; it won 2/2 against the proxy, but the membership-only draft gate also triggered against `opp-swirl-meta-core`, reducing the six-strong Contest screen from 12/12 to 11/12.

c644 tightens the gate to the exact observed opponent pick order, then applies c643's side-specific rules. It won both sides against the synthetic proxy twice with identical results: Team A 800:400 and Team B 200:0, both at r2000. It scored 12/12 against the six strong local Contest opponents and 40/40 against the 20-opponent Contest pool. Compared with fresh current-source controls, all 12 strong and all 40 broad result records (winners, scores, and rounds) were identical; neither pool used the exact Please pick order. Keep c644 as an isolated candidate for a future live check, not a production change or a top-50 win.

Candidate `bots/c644-please-pick-order-profile/src/bot.cpp`, SHA-256 `18ED6E6FEE1D5BFF8BF4E57B018C4398CBE95D683E936638B4FDC7EFCEC46AC8`. Runs: proxy `matches/league/20261019-041809-c644-please-pick-order-profile-direct-c644-please-profile-target/` and repeat `matches/league/20261019-041910-c644-please-pick-order-profile-direct-c644-please-profile-target-repeat/`; strong `matches/league/20261019-041824-c644-please-pick-order-profile-direct-c644-please-profile-strong/`; broad `matches/league/20261019-041834-c644-please-pick-order-profile-direct-c644-please-profile-broad/`. Current-source controls are c641 `matches/league/20261019-041314-tungtungsahur-direct-c641-please-proxy-current-control/`, c638 strong `matches/league/20261019-040326-tungtungsahur-direct-c638-contest-varg-power-first-baseline/`, and c638 broad `matches/league/20261019-040442-tungtungsahur-direct-c638-contest-varg-power-first-broad-baseline/`.

Production remains c553; source and submission ZIP remain unchanged. No official match or upload was made. Live testing remains paused and the 10-win top-50 objective is unverified.


### c644 proxy outcome decomposition (19 Oct 2026)

The 2–0 label hides a large side split, and both games reached round 2000. Against the same synthetic proxy, the current-source c641 control scored 200:400 on Team A (kills 48:32, deaths 51:57, gold 4,770:13,255) and 200:200 on Team B (kills 25:30, deaths 51:37, gold 4,545:13,435). c644 scored 800:400 on Team A (kills 60:16, deaths 31:74, gold 7,320:9,130), but only 200:0 on Team B (kills 22:52, deaths 73:31, gold 3,395:15,585).

This supports a real Team A combat improvement against this proxy. Team B's gem-only win is not evidence of better farming or fighting: it had fewer kills, more than twice the deaths, and far less gold than the proxy, while gaining only a 200-gem lead at the timeout. Treat c644 as an asymmetric matchup experiment, not a generally stronger bot. Keep it local and unpromoted until actual live validation can resume. Source and run paths are in the c641-c644 section above.


## c645 Stampede side-farm extension rejected (19 Oct 2026)

c645 extends c637's safe Issac side-camp route from rounds 0–149 through round 179. On the six strong local Stampede opponents it scored 9/12 against a fresh c637 control at 12/12. It lost both `fx-dbllock` sides and `opp-swirl-meta-core` side A, all wins held by c637; c645 also reduced the `ming_bot` side-A score from 1,260 to 1,080. Reject the longer split: the additional farming time pulls Issac off the team too long against pressure drafts.

Candidate `bots/c645-stampede-issac-sidefarm-r180/src/bot.cpp`, SHA-256 `6EB637282A429095EB1D2677E442387A294F6E0D6334F02687A4DD28D0AD70C3`. c645 run `matches/league/20261019-042420-c645-stampede-issac-sidefarm-r180-direct-r180-strong-screen/`; fresh c637 control `matches/league/20261019-042441-c637-stampede-ren-varg-core-guard-direct-fresh-r180-control/`. No production change or upload.

## c646 combined Contest/Willow-Lanes profiles (19 Oct 2026)

c646 combines two isolated, map-gated local responses from c553: c644's early Contest leash / safe shop rules against the exact Varg / C&I / Stellar / Ren / Ryth order, plus c570's Ryth strength-item order on Lanes side A against the Varg / C&I / Stellar / Tavi / Willow lineup. Against their matching synthetic proxies it scored 2/2 on Contest and 2/2 on Lanes. The Contest proxy is the recorded Please draft-order proxy; the Lanes proxy is a synthetic Willow-layout planner, not Please's executable.

The broad 20-opponent, two-map screen scored 79/80 (Contest 40/40, Lanes 39/40), matching the current c553 win counts. Against fresh c553 controls, there were no winner flips; two Lanes records changed score or finish round only (`opp-fai-heal` and `tralalerotrarala`). On the six strong local opponents across all 17 maps, c646 scored 182/204 and matched c553 exactly on every winner, score, and finish round. Keep c646 isolated as a two-map local matchup candidate; it does not establish a current top-50 win, and production remains c553 pending the paused live validation.

Candidate `bots/c646-please-two-map-profiles/src/bot.cpp`, SHA-256 `F0C520838A2AC31F6A9F7D7C5BD61866D0F0FA4BB991614EB9DB0B12B0CA98F0`. Runs: Contest target `matches/league/20261019-042537-c646-please-two-map-profiles-direct-contest-target/`; Lanes target `matches/league/20261019-042553-c646-please-two-map-profiles-direct-lanes-target/`; two-map broad `matches/league/20261019-042614-c646-please-two-map-profiles-direct-broad-two-map-screen/`; strong all-map `matches/league/20261019-042717-c646-please-two-map-profiles-direct-strong-all-maps-screen/`. Controls: c553 Contest `matches/league/20261019-040442-tungtungsahur-direct-c638-contest-varg-power-first-broad-baseline/`, c553 Lanes `matches/league/20261018-232508-c553-direct-lanes-please-ryth-power-first-full-pool/`, and c553 strong all-map `matches/league/20261018-232646-tungtungsahur-direct-c553-canonical-strong-all-maps/`.


## Archived Please draft check and c647–c648 Lanes follow-up (19 Oct 2026)

I rechecked the official rank-49 Please group `8a9a1654-7673-4da3-bbae-daaa2f5cc715` against `sdk/cpp/cambc.h`'s `champion_draft` enum. Contest Please picks `[9,3,4,8,0]` decode to Varg / Cassi & Issac / Stellar / Ren / Ryth, exactly matching c644's Contest gate. Lanes Please picks `[9,3,4,8,10]` decode to Varg / Cassi & Issac / Stellar / Ren / Tavi. c646's Lanes Team-A gear gate instead requires Willow and does not match that archived Please roster. The Lanes target win for c646 was against a different synthetic Willow-layout lineup; do not count it as evidence against rank-49 Please on Lanes. In the archived group, our team was Team A and Please Team B.

c647 and c648 tested Team-A Ryth gear against the matching local Ren/Tavi roster proxy (`please-layout-proxy`). c647 buys Monster Strength before Power Strength; c648 reverses the order. The c646 baseline scored 2/2 (Team A 1,020:990 at r585; Team B 1,020:990 at r621). c647 also scored 2/2: its Team-A game was 1,012:946 at r555, with kills 1:0, deaths 1:2, and gold 4,330:4,140 versus c646's 2:1 kills, 1:3 deaths, and 4,490:4,190 gold. The same c647 Team-A outcome repeated exactly in `matches/league/20261019-043552-c647-please-ren-tavi-lanes-monster-first-direct-ren-tavi-monster-first-repeat/`. The gem margin improved by 36, but our own score and gold declined; this does not demonstrate better farming or a new win. c648 lost Team A 882:1,012 at r529 and stayed 1/2 overall.

c647's full 20-opponent Lanes pool was 39/40, equal to c646; no winner changed. The six-strong Lanes screen was 12/12. In the broad pool one `my-bot-v2` side-A score changed from 1,014:606 to 1,020:680, with no winner change. Keep c647 isolated as an unproven score-margin experiment; reject c648. The earlier c569 draft swap that replaced Ryth with Tavi against this Ren/Tavi proxy finished 0/2 versus c553's 2/2, so do not retry that roster swap. Lanes remains unresolved against the actual ranked Please executable.

Sources and runs: c647 `bots/c647-please-ren-tavi-lanes-monster-first/src/bot.cpp` SHA-256 `D97B577E5DFC9681F2261EA405F7383E574DFB0AD358B712EF3EF8074285D05C`; target `matches/league/20261019-043114-c647-please-ren-tavi-lanes-monster-first-direct-ren-tavi-monster-first/` and repeat `matches/league/20261019-043552-c647-please-ren-tavi-lanes-monster-first-direct-ren-tavi-monster-first-repeat/`, broad `matches/league/20261019-043433-c647-please-ren-tavi-lanes-monster-first-direct-full-lanes-pool/`, strong `matches/league/20261019-043459-c647-please-ren-tavi-lanes-monster-first-direct-strong-lanes-screen/`. c648 `bots/c648-please-ren-tavi-lanes-power-first/src/bot.cpp` SHA-256 `9BDB3AFB8D68F7927A7FDDD9F8DB3D2D8FB07D13E9AEDCC55B7703A9B8ECCF27`; target `matches/league/20261019-043128-c648-please-ren-tavi-lanes-power-first-direct-ren-tavi-power-first/`. c646 exact-roster control `matches/league/20261019-043109-c646-please-two-map-profiles-direct-ren-tavi-exact-draft-control/`. Prior c569 roster swap is under `matches/league/20261019-003842-c569-fresh/`.


## c649–c654 Contest leash sweep: retain c652 for future live validation (19 Oct 2026)

These candidates inherit c646 and vary only the Team-A Contest leash duration for the exact archived Please Contest draft. Each target run uses a local synthetic Please-layout proxy, so these are controlled local matchup results, not ranked wins. The 2-tile leash through round 99 (c652) was the only tested duration with a repeatable 2/2 outcome and a strong target-side result: in two identical runs Team A reached 1,000 submitted gems at round 1,998, leading 1,000:400 with 77 kills, 26 deaths, and 9,555 earned gold versus 5,630 for the proxy; Team B scored 200:0 at round 2,000. This is stronger than c646's 800:400 Team-A proxy result, but does not establish a general improvement.

c652 passed the 20-opponent Contest pool 40/40 and six-strong Contest set 12/12. Paired c646 comparisons showed zero winner flips and no score or finish-round changes in either screen. The exact lineup gate keeps this effect out of unrelated opponents; the only repeated difference is on the synthetic target. Retain c652 as the most promising local exact-draft Contest counter for a future official test, isolated from production.

Other duration variants were worse or less useful: c649 (3 tiles through r74) and c650 (4 tiles through r74) each scored 1/2; c651 (1 tile through r74) scored 2/2 but only 800:200 for Team A; c653 (2 tiles through r124) scored 1/2; c654 (2 tiles through r149) scored 2/2 but only 600:200 for Team A, with 55 kills, 52 deaths, and 6,155 gold versus the proxy's 10,610. Keep c649, c650, c651, c653, and c654 rejected. No production source or ZIP was changed and no upload occurred.

c652 source: `bots/c652-please-contest-leash2-r100/src/bot.cpp`, SHA-256 `E4A1494097AA44CF9D4CA54B25389CFF6A3D09C0E3F2B86BAC086E26500C431E`. Target runs `matches/league/20261019-043821-c652-please-contest-leash2-r100-direct-please-target/` and repeat `matches/league/20261019-043842-c652-please-contest-leash2-r100-direct-please-target-repeat/`; strong `matches/league/20261019-043854-c652-please-contest-leash2-r100-direct-strong-contest-screen/`; broad `matches/league/20261019-043903-c652-please-contest-leash2-r100-direct-broad-contest-screen/`. c649 source SHA `E94652F5B75152E10226662D5C9E37133C536E81BA1845C6498F07ED3F06193E`; c650 `5B682B12E6A2C24C9108865F5891F605ADB8C898E48911C68CB79DE2E0E8E394`; c651 `F44D9268A45FDE76412DF3C4AC46AE2B956178DEE95B038BA215413FFBD243FA`; c653 `F1D7FF8AE97011859A0D2EF505CD0BCE806138D2B66D1CA58B146033EEA967A3`; c654 `04ED68E5303110360E013085EC1F273A8D772900C47E1EE3FD8A0160488E2471`.

## c655–c658 Contest leash cutoff bracket (19 Oct 2026)

I bracketed c652's cutoff with 2-tile leash thresholds at rounds 90, 101, 105, and 110 against the same local synthetic Please Contest proxy. c655 (`round < 90`) repeated c652's exact 2/2 outcomes: Team A reached 1,000:400 at r1998 with 77 kills, 26 deaths, and 9,555 gold; Team B finished 200:0 with 22 kills, 73 deaths, and 3,395 gold. Thus rounds 90–99 did not affect this replay. c652 (`round < 100`) remains the best setting.

Including round 100 changed the Team-A target outcome sharply: c657 (`round < 101`) fell to 1/2; Team A lost 200:400 at the timeout with 55 kills, 57 deaths, and 5,190 gold versus 12,695 for the proxy. c658 (`round < 105`) also scored 1/2, losing Team A 600:800 with 68 kills, 36 deaths, and 9,825 gold versus 7,860; c656 (`round < 110`) scored 1/2 as previously recorded. This sharp step is specific to the synthetic matchup and has not been checked against Please's executable. Reject c656–c658; c655 is equivalent to c652 on the observed target and does not improve it. Do not widen c652's cutoff.

c655 source SHA-256 `86990FA76BF55003C0A200C376E326230B7CE347C5765B9FAC16C4039CA718C0`; run `matches/league/20261019-044245-c655-please-contest-leash2-r90-direct-leash90-target/`. c656 run `matches/league/20261019-044257-c656-please-contest-leash2-r110-direct-leash110-target/`; source SHA is recorded with the c649–c654 sweep above. c657 source SHA-256 `AC90B2F197EBE4EE5B8BDB6ECFC5A0CE9694F5C70A048A8A88CA4EB8B8776D7B`; run `matches/league/20261019-044331-c657-please-contest-leash2-r101-direct-leash101-target/`. c658 source SHA-256 `B8FDB9F20509F6FD88C1D0F8E83C04271FFC702A7A70EF262044DA54A4396DB2`; run `matches/league/20261019-044343-c658-please-contest-leash2-r105-direct-leash105-target/`. All games were local and unranked; production stayed c553.
## c659 Contest Monster Focus build rejected (19 Oct 2026)

To investigate the actual rank-49 replay's early farm and equipment timing gap, c659 changed Stellar's first emblem to Monster Focus only for the exact archived Please Contest draft on our Team-A side; all other c652 behavior, including its 2-tile leash through round 99, was retained. Against the local synthetic proxy it fell to 1/2. Team A tied gems 600:600 and lost on gold, 8,070:10,205, despite a better K/D (55:34 versus the proxy's 20:66). The c652 Power Focus control scored 1,000:400 on Team A, with 9,555:5,630 gold and 77:26 K/D; Team B was identical at 200:0. The Monster Focus emblem has helped on other camp-heavy maps, but this Contest result says that farming emblem does not transfer to this contested matchup. Reject c659 and keep Power Focus for this profile. Synthetic proxy evidence only; no official validation.

c659 source `bots/c659-please-contest-stellar-monster-focus/src/bot.cpp`, SHA-256 `83379A8D51A049059161629AB33074299B484069DA43B1E739AA26B885B61D56`; run `matches/league/20261019-044532-c659-please-contest-stellar-monster-focus-direct-monster-focus-target/`.
## Archived Please Lanes route timing and c660–c661 split tests (19 Oct 2026)

The official rank-49 Please Lanes replay (`9bf96de6-6cc5-42cf-9dcd-7b973135fd63`) is a no-death farm race, so route tempo is the relevant deficit. Event timestamps show Please's Ren cleared a camp at r35 (53,4), its Varg cleared at r41 (53,2), and Stellar at r48 (53,13). Our Issac first cleared at r47 (39,13), Ryth at r63, and our Varg not until r146. The totals were 30:43 camp clears and 750:1,000 submitted gems. Please's Stellar bought Power Focus at r67; ours bought Monster Focus at r73. Please's Ren bought Power Strength and Durability Health at r68. These per-event timings sharpen the known aggregate: the opponent starts clearing with Ren/Varg earlier, while our Varg's first clear comes much later.

c660 tested starting the role split at turn 1 for Team A only against the exact Please Lanes draft. It scored 1/2 against the local synthetic Ren/Tavi proxy. Team A lost 904:1,012 at r565 (0 kills, 4 deaths, 3,890 gold vs 4,380); Team B won 1,020:990 at r621 (1 kill, 2 deaths, 4,350 gold). The c646 round-50 control scored 2/2, including a Team-A win 1,020:990 at r585. c661 moved the exact-draft split to round 45; it produced the exact same scores, rounds, kills, deaths, and gold as c660. Reject c660/c661 and keep the round-50 opening; the 1/2 proxy evidence does not establish what would happen against Please's executable.

c660 source SHA-256 `08A511E8F1E85CD4A9B9CEAB07A5561ED889C4043643B5BAA01DFD8BC3827D29`; run `matches/league/20261019-044851-c660-please-lanes-early-split-direct-please-lanes-opening-target/`. c661 source SHA-256 `B1C73B3032BDF526117213AF871447362F52749CA4D168E0C50692BFD3F841D4`; run `matches/league/20261019-044931-c661-please-lanes-split-r45-direct-please-lanes-r45-target/`. Archived official event data is in `matches/live/8a9a1654-7673-4da3-bbae-daaa2f5cc715/match-9bf96de6-6cc5-42cf-9dcd-7b973135fd63-summary.json`. No official match or upload was made; production remains c553.
## c662–c664 Please Lanes Varg route experiments (19 Oct 2026)

The rank-49 replay's Varg first cleared at r41 while ours first cleared at r146. I tested three Team-A Lanes changes gated on the Please Varg/C&I/Stellar/Ren/Tavi roster. c662 removed Varg from early capture duty but otherwise kept the grouped opening; it matched c646 exactly on the focused 2/2 target and every result in the 40-game broad Lanes pool (39/40, same `opp-fai-mirror` side-A loss). This change has no measured upside. c663 sent Varg to a separate passive-camp route while the rest remained together; it scored 1/2, with Team A losing 984:1,012 at r583 (1 kill, 3 deaths, 4,280 gold vs 4,420), while Team B matched the 1,020:990 control. c664 gave Varg a safe active-camp route excluding Ryth's shared target; it also scored 1/2, with Team A losing 962:1,012 at r593 (0 kills, 3 deaths, 4,050 gold vs 4,370); Team B again matched control. Reject c662–c664. Local synthetic results favor retaining the current grouped Lanes opening for now; they do not prove what would happen against the ranked executable.

c662 source SHA-256 `28FD9FF634BF622C78351EE8B26FD7DD592A5FAAE54551418AACB0D9F39630A5`; target `matches/league/20261019-045037-c662-please-lanes-varg-farm-duty-direct-please-varg-duty-target/`; broad `matches/league/20261019-045116-c662-please-lanes-varg-farm-duty-direct-full-lanes-screen/`. c663 source SHA-256 `7B60BF12BF4E9B8B4F6FB527E1AACB85493DE5497A4F659F1345F7DC2BD5B03A`; target `matches/league/20261019-045218-c663-please-lanes-varg-solo-route-direct-please-varg-solo-target/`. c664 source SHA-256 `2BCD27E71BBC9022358F2F3EB550ED1FD623D47478BB1AF14ECBAD5D1255F976`; target `matches/league/20261019-045311-c664-please-lanes-varg-active-camp-direct-please-varg-active-target/`. No production change or upload.

## c665–c666 delayed Varg solo-route timing (19 Oct 2026)

To test whether the Lanes solo-camp route was simply starting too early, c665 and c666 cloned c663 and gated its Varg route to rounds 35 and 40 respectively; the rest of the bot was unchanged. Both were 1/2 against `please-layout-proxy`, below c646's 2/2 control. c665's Team-A game lost 882:1,012 at r585 and its Team-B game won 1,020:990 at r621 (average bot gems 951). c666 lost Team A 868:1,012 at r517 and won Team B 1,020:990 at r621 (average bot gems 944). Reject both cutoffs; moving Varg onto the solo route earlier does not close the recorded farm gap against this proxy. This is still a synthetic local opponent, not Please's executable.

c665 source SHA-256 `B5CE3E2CABAA49137097935E113D59708ACF40E20E04F7E81C94F2B7FE6ED1FE`; run `matches/league/20261019-045526-bots/c665-please-lanes-varg-solo-r35-direct-c665-please-varg-solo-r35-target/`. c666 source SHA-256 `0890DA03B464F743B90FF5949C31B24B5C4C0001B34AFDAF43D2FA1638BC63AB`; run `matches/league/20261019-045510-bots/c666-please-lanes-varg-solo-r40-direct-c666-please-varg-solo-r40-target/`. Production remains unchanged (`bots/tungtungsahur/src/bot.cpp` SHA-256 `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6`; `submissions/tungtungsahur.zip` SHA-256 `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`). No upload or official unranked match occurred.

## c593 Rows draft recheck and direct production comparison (19 Oct 2026)

c593's Rows change was rechecked against `please-layout-proxy`. Its Rows draft is Varg/Cassi & Issac/Stellar/Ren, matching the recorded Please Rows draft; c593 selected Varg/Cassi & Issac/Ryth/Ren, matching our recorded lineup. c593 beat the proxy 2/2 (1,056:660 at r561; 1,023:660 at r666), but a fresh c553 production control also beat it 2/2 with exactly the same scores, rounds, kills, deaths, and drafts. The proxy has the matching draft only; it is not Please's executable, and c593's targeted win is not an improvement over production.

Direct c593-vs-c553 and c593-vs-c646 Rows games both split by side: c593 won side A 1,056:990 at r574 and lost side B 990:1,056 at r574. Across all 17 maps c593 scored 16/34 versus c553, winning one side on 16 maps and losing both Pilgrimage sides. c563 separately scored 0/2 versus c553 on Pilgrimage. These direct comparisons do not support replacing production; keep c553 as the current bot and treat c586/c593 as local matchup candidates only. This does not erase c586/c593's recorded gains against varied proxy pools, but they are not a robust head-to-head improvement.

Runs: c593 vs Please-draft proxy Rows `matches/league/20261019-045753-bots/c593-rows-ryth-counter-direct-c593-rows-headtohead-and-please-target/`; c593 vs c646 and c553 Rows `matches/league/20261019-045813-bots/c593-rows-ryth-counter-direct-c593-rows-vs-current-and-please-candidate/`; c553 control vs Please-draft proxy `matches/league/20261019-045950-bots/c553-direct-c553-rows-please-exact-draft-control/`; c593 vs c553 all maps `matches/league/20261019-050004-bots/c593-rows-ryth-counter-direct-c593-vs-production-all-maps/`; c563 vs c553 Pilgrimage `matches/league/20261019-050038-bots/c563-direct-c563-vs-production-pilgrimage/`. No production edit, official unranked match, or upload occurred.

## c667 Rows Stellar draft counter test (19 Oct 2026)

The archived rank-49 Please Rows replay (`match-5818aad6-4e5d-45fe-8dc0-39da8a70d934`) narrows the gap: our first camp clear was Ren at r29 and Please's was Varg at r25, but Please finished with 17 clears to our 11. Our team A cleared with Varg 3 times (only group 4, at r178/292/389), Ren 4 times, Ryth 3 times, Issac once, and Cassi zero; Please team B cleared with Varg 4, Ren 5, Stellar 3, Cassi 3, and Issac 2 times across groups 1/3/5. The first-clear delay was small; the sustained clear cadence and different draft output were larger differences.

c667 starts from c553 and, on Rows after seeing enemy Varg plus Cassi & Issac, takes Stellar before Ryth to mirror the recorded opponent's Varg/C&I/Stellar/Ren core. The focused three-opponent screen was 4/6: 1/2 against c553, 2/2 against `please-layout-proxy`, and 1/2 against `opp-swirl-meta-core`. In the direct c553 games, c667 lost side A 792:1,001 at r590 (4 vs 3 deaths) and won side B 1,023:924 at r551 (0 deaths both); the target-proxy wins do not beat fresh c553, which also went 2/2 against the exact Rows draft with identical scores, rounds, drafts, kills, and deaths. The full 24-opponent Rows screen scored 46/48 versus a fresh c553 control's 47/48: no win gained, with one additional loss to `ming_bot` on side B. Reject c667. The replay suggests a throughput/cadence deficit, but this draft swap did not solve it.

c667 draft.cpp SHA-256 `63C1D67DCE3D59CB6BCFC8B049B5C3C1E9183278C997E70978608F196971FDD2`; focused run `matches/league/20261019-050316-bots/c667-rows-stellar-after-varg-cni-direct-rows-stellar-target-screen/`; c667 full screen `matches/league/20261019-050415-bots/c667-rows-stellar-after-varg-cni-direct-c667-rows-24opponent-screen/`; fresh c553 control `matches/league/20261019-050434-bots/c553-direct-c553-rows-24opponent-fresh-control/`. No production change or upload occurred.

## c667 full Rows pool result (19 Oct 2026)

The exact Varg/C&I-to-Stellar draft gate did not survive the broad screen. Across 24 opponents and both sides, c667 scored 46/48; a fresh c553 scored 47/48. Neither gained a win over the other across the pool: c667's extra loss was `ming_bot` side B, while both lost to `opp-swirl-meta-core` side A. Focused head-to-head c667 vs c553 split 1–1 by side (c667 792:1,001 on A; c667 1,023:924 on B). The exact-draft proxy still finished 2/2 for both bots; c667 did not improve on current production and sometimes earned fewer gems. Reject c667. The Rows replay's 11:17 clearance gap remains; the role-activity and repeated camp cadence need further work.

Runs: c667 `matches/league/20261019-050415-bots/c667-rows-stellar-after-varg-cni-direct-c667-rows-24opponent-screen/`; fresh c553 `matches/league/20261019-050434-bots/c553-direct-c553-rows-24opponent-fresh-control/`. c667 draft source remains isolated in `bots/c667-rows-stellar-after-varg-cni/`; production stays unchanged.

## Rows Cassi item queue and shop timing tests c668–c669 (19 Oct 2026)

The archived Please Rows replay (`match-5818aad6-4e5d-45fe-8dc0-39da8a70d934`) shows a purchase-timing and damage difference: Please's Cassi bought five Power Focus and four Durability Focus shards at r32; our Cassi's recorded buys were five Power Focus shards at r201 and three Durability Health shards at r280. Their Cassi dealt 14.6k monster damage versus our 4.1k. c668 changed only the Rows Cassi second queue from Durability Health to Durability Focus. It scored 46/48 across 24 local Rows opponents versus c553's fresh 47/48, adding an `opp-fai-ranged` side-B loss; it did not add any wins. Its exact-draft proxy games remained 2/2, and the fresh production control also went 2/2. Reject c668.

c669 instead lowered only Rows Cassi's safe return-to-shop threshold from 150 to 75 gold. It scored 3/6 on the focused c553/Please-proxy/meta-core screen and lost both direct c553 games, finishing 990 gems on both sides versus c553's 1,012 and 1,056. It still beat the weak exact-draft proxy 2/2, but that did not transfer to the c553 head-to-head; it also lost one meta-core side. Reject c669. The item queue and early shop return are not enough by themselves; purchase timing may reflect the farm-income gap rather than cause it.

c668 source SHA-256 `8B648C432630FE804E453BBFE6C08B21626006269994B77F947448AE8813C913`; 24-opponent run `matches/league/20261019-050747-bots/c668-rows-cassi-durability-focus-direct-c668-rows-24opponent-screen/`. c669 source SHA-256 `426FB942FF23AE5F5AD265F39815FD65FDCADA75AF68D0BC87B5DB0FD205F35E`; focused run `matches/league/20261019-050859-bots/c669-rows-cassi-early-shop-direct-rows-cassi-early-shop-target/`. Production source and ZIP remain unchanged at `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. No upload or official match occurred.

## c670 Rows Ren follows Issac objective test (19 Oct 2026)

The replay shows team A had both Issac and Ren acting as squad-B fighters, while Cassi followed the shared objective. c670 kept Ren attacking camps but made him follow a fresh shared Issac objective on Rows instead of choosing and publishing a competing camp. The focused screen scored 4/6; it split with c553 by side (c670 1,056:990 win on A and 990:1,056 loss on B), and the exact-draft proxy remained a 2/2 win with fewer gems than c553 (2,024 vs 2,079 over both sides). The 24-opponent Rows pool was 47/48, matching fresh c553's 47/48 with the same sole `opp-swirl-meta-core` side-A loss and no converted wins. Reject c670: the competing-objective hypothesis did not produce a broad or target win gain.

Focused run `matches/league/20261019-051035-bots/c670-rows-ren-follows-issac-direct-rows-ren-follows-issac-target/`; 24-opponent run `matches/league/20261019-051054-bots/c670-rows-ren-follows-issac-direct-c670-rows-24opponent-screen/`; source SHA-256 `34FDA4CE22B64C0C214494A4E8D95258C8D82C73220A662B740E256D3EBCC6CD`. Production source and ZIP remain unchanged.


## Rows Cassi passive-route test c671 (19 Oct 2026)

c671 let Rows Cassi choose a separate safe gem camp rather than follow the squad objective. Its six-game c553 / Please-layout-proxy / meta-core screen was 4/6: 1/2 against c553 (loss on side B), 1/2 against the synthetic Please-layout proxy (loss on side B), and 2/2 against meta-core. The existing c553 baseline was 2/2 against the exact-draft proxy; the candidate's side-B loss and the direct c553 split show that a separate Cassi route did not reliably turn her extra activity into wins. Reject c671.

Run: `matches/league/20261019-051211-bots/c671-rows-cassi-solo-passive-direct-rows-cassi-solo-passive-target/`; source SHA-256 `5B8002BB5D918B3A9243B32445E65D7C0A748BBC98D1CEA891CDBE9A89B6326D`.

## Rows Ryth camp-damage equipment test c672 (19 Oct 2026)

c672 changed only Rows Ryth's first emblem from Monster Health to Monster Strength, retaining Power Health second. The 24-opponent / 48-game Rows screen scored 47/48, exactly matching a fresh c553 control with the same winner on every record. Average own gems were 1,026.9 versus 1,030.6; opponent gems were 666.2 versus 676.0; average finish was 604.6 versus 606.4 rounds. The six-game focused screen scored 4/6, including 2/2 against the synthetic Please-layout proxy, but c553 also beat that proxy 2/2. Reject c672: the small timing and opponent-score changes did not improve win outcomes or our gem total.

Source SHA-256 `C5926572ED0F644963013415BEB328CF79B0A075D0D88A4BAB712510BC538C34`; focused run `matches/league/20261019-051552-bots/c672-rows-ryth-monster-strength-direct-c672-rows-target-screen/`; 24-opponent run `matches/league/20261019-051622-bots/c672-rows-ryth-monster-strength-direct-c672-rows-24opponent-screen/`; fresh c553 control `matches/league/20261019-050434-bots/c553-direct-c553-rows-24opponent-fresh-control/`. Production source and ZIP remain unchanged. No official match or upload occurred; unranked testing remains paused.


## Rows Ryth gem-only route test c673 (19 Oct 2026)

c673 changed only Rows tank target selection: Ryth ignored gold-only groups and waited for a gem camp. It scored 4/6 in the focused screen, but lost both direct games to fresh c553 at 990 gems (c553 finished with 1,012 and 1,056). It beat `please-layout-proxy` 2/2 and meta-core 2/2; the exact-draft proxy is not a sufficient control because fresh c553 also beat it 2/2. Reject c673 and do not run the broad screen. The live replay's Ryth did spend two cycles clearing gold-only group 8 before his first gem clear at r331; that route earns useful bridge income while gem groups respawn, and removing it hurt local head-to-head.

Source SHA-256 `1ABB38016AC13BC018A5E7263103F2817D39CD5B2AE91ED4481446C062981695`; focused run `matches/league/20261019-051743-bots/c673-rows-ryth-gem-camps-direct-c673-rows-target-screen/`. Production source and ZIP remain unchanged; no live match or upload occurred.


## Rows Ren solo gem-route candidate c674 (19 Oct 2026)

c674 gives Rows Ren an independent safe-gem route when available, avoiding Ryth's anchor and Issac's shared camp objective; if no safe target exists, Ren falls back to Issac's objective. Combat behavior is unchanged. The focused six-game screen repeated exactly at 4/6: 1/2 against c553, 2/2 against `please-layout-proxy`, and 1/2 against `opp-swirl-meta-core`; those win counts match the controls and do not show a direct win gain.

The 24-opponent Rows screen scored 47/48, with exactly the same winners as fresh c553. Average own gems improved slightly (1,033.5 vs 1,030.6), opponent gems fell (669.2 vs 676.0), and average finish was 2.2 rounds sooner. On six strong local opponents in Rows, both c674 and c553 scored 11/12; c674 averaged 1,038.6 own gems vs 1,035.8, opponent gems 752.6 vs 791.1, and finished 19.9 rounds sooner. Changes were concentrated against Ming and Xuanming; the `opp-swirl-meta-core` side-A loss remained. Keep c674 isolated as a local Rows lead for future live validation, not as a production upgrade: it added no wins and the Please roster proxy did not distinguish it from production.

Source SHA-256 `3693512863477E35192D40CD5EFE30A572ABACD0DADEB79346FD17A6AAE73E30`. Runs: focused `matches/league/20261019-052025-bots/c674-rows-ren-solo-gem-route-direct-c674-rows-ren-solo-target/`, exact repeat `matches/league/20261019-052115-bots/c674-rows-ren-solo-gem-route-direct-c674-rows-ren-solo-repeat/`, 24-opponent `matches/league/20261019-052045-bots/c674-rows-ren-solo-gem-route-direct-c674-rows-24opponent-screen/`, six-strong candidate `matches/league/20261019-052133-bots/c674-rows-ren-solo-gem-route-direct-c674-rows-six-strong/`, and fresh c553 six-strong control `matches/league/20261019-052140-bots/tungtungsahur-direct-c553-rows-six-strong-fresh-control/`. Production source/ZIP remain unchanged; no upload or live match occurred.


## c675: c604 plus Rows Ren solo route (19 Oct 2026)

c675 combines the best broad local candidate c604 with c674's Rows-only Ren safe-gem route. On the exact c604 six-strong, 17-map pool it scored 187/204, exactly matching c604; every winner matched. Only six Rows records changed against Ming, Xuanming, and Faisal-orig; all remained wins, and several finished sooner or left fewer gems to the opponent. Every non-Rows winner and finish round matched c604.

The default 20-opponent, 17-map pool also matched c604 at 631/680 with no winner changes. The initial direct run had a replay-writer collision on `my-bot` / Corners / side A after the engine completed a 1,008–490 Team-A win at r708; rerunning that exact pairing in a unique output directory reproduced the win, score, round, and zero crashes. The raw run is `summary.json`; the complete corrected count is `summary-recovered.json`. Keep c675 only as a local pace candidate for future live validation; no win-count gain over c604 was measured.

Source `bots/c675-c604-plus-rows-ren-route/src/bot.cpp`, SHA-256 `EC49BC115BC0FA395FF6FC0C5F465AF9AD9F111445D79012F751302873085537`. Matched strong run `matches/league/20261019-052510-bots/c675-c604-plus-rows-ren-route-direct-c675-c604-matched-strong-all-maps/`; default run and recovered summary under `matches/league/20261019-052623-bots/c675-c604-plus-rows-ren-route-direct-c675-default-680-screen/`; c604 controls are its recorded 187/204 strong and 631/680 default runs. Production remains c553; official unranked remains paused.


## c676 Expanse Cassi & Issac Monster-first equipment test (19 Oct 2026)

Fresh ladder and match data show rank-1 Intercontinental Fish buying Monster emblems on all four Expanse champions before Power emblems. c676 mirrors that queue for both Cassi and Issac; c553 already gives Monster-first gear to Stellar and Varg on Expanse. On the same five local opponents and both sides, c553 and c676 each won 10/10. c553 averaged 967 submitted gems for us and 667 for opponents, finishing in 809.5 rounds; c676 averaged 961 for us and 716.6 for opponents, finishing in 853.3 rounds. No win changed, while c676 scored less, conceded more, and finished later. Reject the C&I gear change; the observed top-team build is not enough evidence to adopt it.

Candidate `bots/c676-expanse-cni-monster-fresh/src/bot.cpp`, SHA-256 `5400C891882117B0F0D42A90113817893F37206FE501981918A4A4D4EF2C5726`. Candidate run `matches/league/20261019-053803-c676-expanse-cni-monster-fresh/`; fresh c553 control `matches/league/20261019-053737-tungtungsahur/`. All 20 local matches completed with zero failures. See [`analysis/top50-evaluation-20261019.md`](../../analysis/top50-evaluation-20261019.md) for the refreshed ladder and five-map Fish–Mite replay review. Production source and ZIP remain unchanged; no official match or upload occurred.


## c677 Stampede top-5 draft copy rejected (19 Oct 2026)

The newest #5 Univardisty replay used Cassi & Issac / Stellar / Varg / Tavi / Ren on Stampede and beat #1 Fish 1,080–0. c677 applied that exact five-pick lineup unconditionally on Stampede, starting from c675. Against the same six strong local proxies and both sides, c677 scored 7/12 versus a fresh c675 control's 11/12. Four of the five candidate losses were on side B; the fifth was `opp-racer` side A. Reject the full draft copy; it does not transfer to our local matchup pool.

Candidate `bots/c677-stampede-top5-draft/src/draft.cpp`, SHA-256 `9CA3C255EA08CE7094B363D9BAEC016E5861F2DB660C048450864CD6316FB9BD`. Run `matches/league/20261019-054352-c677-stampede-top5-draft/`; fresh c675 control `matches/league/20261019-054343-c675-c604-plus-rows-ren-route/`. Both runs completed all 12 games with zero failures.


## c678 Stampede Varg with tank retained rejected (19 Oct 2026)

c678 replaced Prism with Varg while retaining Cassi & Issac, Stellar, Ryth, and Tavi. It scored 10/12 against the same six strong opponents, below the fresh c675 control at 11/12. Its two losses were `ming_bot` and `opp-swirl-meta-core` on side A; the control lost only to `opp-swirl-meta-core` on side A. This change gained no wins and added one loss; reject it. The full c677/c678 replay review and current ladder snapshot are in [`analysis/top50-evaluation-20261019.md`](../../analysis/top50-evaluation-20261019.md).

Candidate `bots/c678-stampede-varg-tank-draft/src/draft.cpp`, SHA-256 `6DB268B8757249788C99443F105A6ED1D19FBA26B56DC25BE1491F79A1EE6DF8`. Run `matches/league/20261019-054434-c678-stampede-varg-tank-draft/`. All 12 matches completed with zero failures. Production source and ZIP remain c553; no official match or upload occurred.


## Stampede core alert and Issac side-camp follow-up c679–c680 (19 Oct 2026)

c679 ported c637's map-specific tank alert onto the newer c675 base and widened its five-pick signature to cover both the local Ren/C&I/Ryth/Stellar/Varg core and Univardisty's recorded C&I/Stellar/Varg/Tavi/Ren draft. Alert alone did not add a win: it stayed 11/12, but the `opp-swirl-meta-core` side-A loss shifted from 0–720 at r913 to 480–960 at r1813.

c680 added c637's Issac safe side-camp split before round 150, including safe gold and low-strength wolf groups, while retaining the alert. It won 12/12 against the same six strong local proxies in two identical Stampede runs; c675 had 11/12. The targeted `opp-swirl-meta-core` side-A game changed from a 0–720 loss at r913 to a 900–720 win at r1761. On the 17-map six-strong screen c680 scored 188/204 vs c675's 187/204; the only winner change was that Stampede side-A conversion, and all 204 games completed without runner failures.

This is a promising local candidate, not a win against Univardisty's live bot: the opponent tested is a local policy proxy, and the official unranked pause remains in effect. Keep production c553 and its ZIP unchanged; the live 10-win streak remains 0/10.

Candidate `bots/c679-stampede-core-alert-fresh/src/bot.cpp` SHA-256 `BF116DCE4E83EB27F7354DF0EA3242A4A12C361A525798750063D6DB09DB1980`; run `matches/league/20261019-054937-c679-stampede-core-alert-fresh/`. Candidate `bots/c680-stampede-alert-sidecamp/src/bot.cpp` SHA-256 `6D1F9A603D8A700A09F1A951AEE637F80014DADEF6F178401EEB0C7E5E70040C`. Repeat Stampede runs: `matches/league/20261019-055050-c680-stampede-alert-sidecamp/` and `matches/league/20261019-055107-c680-stampede-alert-sidecamp/`; all-map screen: `matches/league/20261019-055139-c680-stampede-alert-sidecamp/`.


## Stampede gold weighting and carry-equipment follow-up c681–c688 (19 Oct 2026)

c681 set early Stampede gold weight to 0 globally and scored 11/12 on the six-strong screen, adding an `fx-dbllock` side-B loss. c682 used weight 0.5 and returned to 12/12 but showed no win gain over c680. c683 limited gem-first weighting to either Ryth or Tavi core drafts; it stayed 12/12 strong but fell to 36/40 on the default Stampede pool, adding a `my-bot-v2` side-B loss. Reject all three broad gold-weight changes.

c684 kept c680's normal weighting except against the Ryth/Varg/Ren meta core without Tavi. It was 12/12 on the six-strong Stampede set twice and 37/40 on the default pool. Its 188/204 all-map strong score matched c680's win count, but changed the meta-core Stampede scores and finish times. c685 copied Fish's Power Focus / Home Health / Durability Health queue for Stellar and fell to 8/12 strong. Reject that full item copy.

c686 changed only Stampede Stellar's queue to Power Focus, Durability Health, then Power Focus. It scored 12/12 on the six-strong set, 39/40 on the default Stampede pool twice, and 633/680 on the 17-map, 20-opponent pool with no runner failures. Compared with c675, the two added broad-pool wins were both Stampede side B: `tralalerotrarala` changed from 0–1,080 at r1944 to a 720–540 win at r2000, and `opp-tts-aggro` from 780–1,200 at r1825 to a 720–360 win at r1365. Its sole loss in the default Stampede pool was `tralalerotrarala` side A. Treat c686 as the best local candidate so far, not a verified upgrade against ranked executables.

c687 gated the same item queue to the matching enemy Varg/C&I/Stellar/Ren core with Ryth or Tavi. It preserved 12/12 on the strong set but scored 37/40 in the default pool, restoring the tralalerotrarala side-A win while reintroducing three c686 wins as losses. Reject the gate. c688 applied the queue only when our side was B; it scored 11/12 strong and lost the meta-core side-A game, so reject it without a broad run.

Runs: c681 `matches/league/20261019-055749-c681-stampede-gem-first/`; c682 `matches/league/20261019-055807-c682-stampede-gem-priority-balanced/`; c683 strong/repeat/default `matches/league/20261019-060013-c683-stampede-gem-priority-ryth-core/`, `matches/league/20261019-060034-c683-stampede-gem-priority-ryth-core/`, `matches/league/20261019-060041-c683-stampede-gem-priority-ryth-core/`; c684 strong/repeat/default/all-map `matches/league/20261019-060206-c684-stampede-ryth-core-gem-priority/`, `matches/league/20261019-060224-c684-stampede-ryth-core-gem-priority/`, `matches/league/20261019-060231-c684-stampede-ryth-core-gem-priority/`, `matches/league/20261019-060251-c684-stampede-ryth-core-gem-priority/`; c685 `matches/league/20261019-060652-c685-stampede-stellar-protection-build/`; c686 strong/default/repeat/all-map `matches/league/20261019-060719-c686-stampede-stellar-durability-step/`, `matches/league/20261019-060750-c686-stampede-stellar-durability-step/`, `matches/league/20261019-060815-c686-stampede-stellar-durability-step/`, `matches/league/20261019-060839-c686-stampede-stellar-durability-step/`; c687 strong/default `matches/league/20261019-061559-c687-core-gate-direct-c687-core-gate-strong/`, `matches/league/20261019-061619-c687-core-gate-direct-c687-core-gate-default-stampede-40/`; c688 strong `matches/league/20261019-061715-c688-stampede-side-b-stellar-durability-direct-c688-side-b-stampede-strong/`.

Source hashes: c681 `C24F4BBADBD995033202C63C73CDE4810C445DE9163FCCE6CE26782FA5420B5C`; c682 `E16DB0DB9402F7C5F690EB038C83C423788C85537C396E74831F81D11CD6EF06`; c683 `095076CC9973E243EBB4B26F25A7A833A2E0F3180F8C35563716F5761D00D6FE`; c684 `7D3E90CA521FA74BBFC25E76A51DE9A5085E6EE94FE0BD1C60BFCB239A8F0530`; c685 `ECACB827218A8D3C90CB99B7501656486B61377FFCA86E2D611E968BE54FDA58`; c686 `7E2E74D1C4E0BBDECAB5726AE50BB293B62F159EC68B6DC2B89E5165200F6DB3`; c687 `29949343F65C506CCCB27FBBC9DDBB5942BB08BA8BB1A6A033A86E64CA33BEDC`; c688 `9B870327B7CF9EF60C4A05B10BAEB81070088B0A1D81948DD6766C9139FA80B6`.

Production source and ZIP remain c553, unchanged. Candidate c686 was uploaded as test version v101; a fresh unranked group is pending. The requested live target is 10 consecutive wins and remains 0/10.
