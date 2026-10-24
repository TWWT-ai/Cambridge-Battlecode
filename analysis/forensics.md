# Forensics: 5 platform losses to the top player

All numbers come from `python analysis/forensics.py` (sections `platform mapid local decomp pace ming v4diag`)
unless stated otherwise. Inputs:

> **Version note (17 Oct 2026):** this report reconstructs the older build used in the platform matches. Its
> references to what the “current bot” does describe that historical build, not necessarily today’s source. The
> double-lock fix is now present in `bots/tungtungsahur/src/bot.cpp`: `enemy_lock_at()` enumerates enemy locks
> and the deposit path uses it. The respawn-squat guard is also present in the current camp readiness code.
> Keep the remaining replay observations as historical evidence until a fresh current-source replay confirms them.

- `matches/platform-logs/<id>/team-a.stdout`: our SCORE trace (`SCORE round ours theirs`, every 5 rounds) plus
  `bot error:` lines. Nothing else was logged. A "tribute event" below is a change in a team's total between two
  samples, so one event can add up several champions' tributes.
- `matches/forensics/run1/`: opp-tts-v2 and opp-tts-v4 (the platform-era code) as team A against ming_bot,
  Faisal-bot and starter-cpp on all 10 official maps (60 games, from the earlier run).
- `matches/forensics/v4diag/` (new): `bots/fx-v4diag` = opp-tts-v4 plus a per-champion DIAG trace (deaths, gem
  changes, status every 10 rounds, visible altar locks) as team A against ming_bot, Faisal-bot and opp-tts-locker.
  13 games.
- `matches/forensics/run3`, `run4`, `run5`, `run6` (earlier run): fx-diag (the current bot plus the same trace),
  fx-dbllock, fx-leaderfix and the current tungtungsahur against ming_bot, Faisal-bot and starter-cpp.
- `matches/forensics/lockfix/` (new): `bots/fx-lockfix` (the current bot plus a lock fix) and the current
  tungtungsahur against fx-dbllock. 12 games.
- `matches/league/20261015-085651-tungtungsahur/`: ming_bot against the current tungtungsahur, 20 games.
- `analysis/map-dumps/*.txt`: camp groups and team size per map. `analysis/plan_results.txt`: results from the
  econ-race simulator.

## Summary

1. **Maps.** The five matches are probably five different maps: 069a8cb7 = corners, 1ab06080 = packs,
   2be0e2c1 = interlock, 51e36018 = lanes, e8446c17 = expanse. Expanse is certain: our platform trace is
   identical, event for event, to a local opp-tts-v4 vs starter-cpp game (19 of 19 tribute events, same rounds).
   The same match also shows that the platform build was **opp-tts-v4**. Lanes is also certain: the first 8
   events match exactly. Interlock and packs are near-certain: every one of the 44 events can be built from that
   map's camp yields, and on packs all 25 events are exactly 44 or 48. Corners is likely, at about 80%.
2. **The top player banks after almost every capture.** 78% (75 of 96) of its tribute events equal exactly
   one camp group's gems (22, 24, 36, 44, 48 or 72). On corners and packs the figure is 40 of 41. Its median bag is 48.
   Two or more tributes landing in the same 5-round window happen in 0% (packs) to 37% (interlock, expanse) of
   windows. Our losses do not explain its gains: no gain lines up with a drop in our progress. The only amounts
   that are not a sum of at most 4 camp yields are a final +188 on lanes, which looks like a coordinated last
   deposit (800 to 988).
3. **Pace.** Its first tribute comes at r35-r75, no earlier than ours (r40-r50 on 4 of the 5 maps). Its first
   100 rounds are ordinary: 66-214 gems, and on interlock and lanes we were ahead at r100. After that it runs a
   steady 2.1-3.9 gems per round, reaching 500 at r205-r295 and 1000 at about r340-r480. On lanes, expanse and
   corners its finish rounds sit within about 0-35 rounds of the simulator's "every champion solo-farms" plan
   (358 / 381 / 372 against about 340 / 380 / 405). The current tungtungsahur needs 430-480 rounds on lanes and
   expanse even against starter-cpp. **We lose the race on economy before any fighting happens.**
4. **How it suppressed us.** It depends on the map:
   - **Corners (96 gems in 400 rounds).** By r70 it had tributed 22 + 4×48. That is all four central gem pairs
     next to the central altar, including the two that are closer to us. From r215 to r385 it captured 13 gem
     pairs worth 48 in 170 rounds, which needs all four groups. Meanwhile our squad leaders kept walking to two
     elk+gem groups (5300 hp, 120 damage per turn) that they cannot clear. In that diagnostic replay, Ryth
     targets (45,59) on every status line from r30 to r210; that build had 1 capture by r200. This is not the
     current main's pace: its latest corners games against ming_bot scored 308 (side A) and 258 (side B) by r200.
     It won 1/2, so the map remains contested, but the old no-capture loop is not reproduced.
   - **Interlock (346).** From r405 to r470 four of our bodies failed every turn with "Target must be a
     visible enemy or neutral camp". This was the **double-lock bug**. When both teams had a lock on one altar,
     `cambc::vision::altar_lock_at` returned *our* lock (sdk/cpp/cambc.h:4706), and that build attacked its own
     lock. The historical reproduction produced 7,002 failed turns and a 2000-round collision game. The fix in
     `bots/fx-lockfix` brought failures to 0 in all 6 test games; the current main now uses the same enemy-only
     lookup in `enemy_lock_at()` and the deposit path. The archived platform trace itself still reflects the old
     build. Separately, after r185 the top player took over our 72-gem gem cluster: it made 7 captures worth 72,
     while one cluster can supply about 5.
   - **Packs (180).** It took both central groups worth 48 a total of 11 times, while we got them once. We made
     only 3 captures in 425 rounds on a map where our three 2-wolf groups are 6-22 tiles from spawn. One of our
     champions was stunned at r310 (the "Champion cannot act" error). The SCORE data cannot separate deaths from
     zoning.
   - **Lanes and expanse.** It did not touch us. On expanse our trace equals the starter-cpp game. On lanes only
     our squads' elk captures (36s) disappeared, while our solo gem farmer was never interrupted. It simply
     farmed faster: 988 by r330 and 972 by r355.
5. **ming_bot is a good proxy only on corners.** There, ming's pace against the old bot (686 at r300, 874 at
   r400) matches the top player (680, 968). On expanse, interlock, lanes and packs the top player reaches 500
   about 45-430 rounds earlier than ming. ming vs v4 on packs: 128 gems in 745 rounds; top player: 968 by r475.
   Beating ming is not evidence of beating the top player.

## 1. Map identification (Q4)

Method: compare our increments with the camp yields of each map (`analysis/map-dumps`), and our platform events
with our own deterministic farming traces from the platform-era code on every map
(`matches/forensics/run1`, 6 games per map).

| match | best guess | confidence | decisive evidence |
|---|---|---|---|
| e8446c17 | **expanse** (3 picks) | ~100% | 19 of 19 of our events identical in round and amount to `opp-tts-v4-vs-starter-cpp-expanse` (r40:+48 r60:+48 r70:+48 r100:+48 r130:+48 r160:+22 r170:+48 ... r375:+48). opp-tts-v2 differs from the 3rd event (r75), so the platform ran **v4**. Next best map scores 15.6 against 49.9. |
| 51e36018 | **lanes** (5 picks) | ~99% | First 8 events identical to v2 and v4 vs starter-cpp (24s at r50/65/75/85/95/110, +60 at r130). Only lanes and collect give our bot 24-only tributes; on collect our first events are r35:+24 r45:+24 r50:+48. |
| 2be0e2c1 | **interlock** (4 picks) | ~95% | Every event on both sides is 22, 36 or 72, or a sum of them (94 = 72+22, 58 = 36+22). That is exactly interlock's set (W 22, E 36, 3-gem cluster 72). Our first +72 at r45 matches 5 of the 6 local interlock games. Up to 20 errors per 5 rounds means 4 bodies frozen per round, which fits a 4-pick draft (5 bodies counting Cassi and Issac separately). |
| 1ab06080 | **packs** (3 picks) | ~90% | All 25 events (ours and theirs) are exactly 44 or 48. Packs has only two gem values: 2-wolf groups (44) and 2-gem/2-gold groups (48). On expanse, the only other map with both values, our bot always tributes +48 at r40 (6 of 6 local games); here our events are r50:+48 r115:+44. |
| 069a8cb7 | **corners** (5 picks) | ~80% | Their 20 events are 22, 48, 96 (2×48 or the elk+gem group) and 36; 19 of 20 are a single corners group. They tributed 214 = 22 + 4×48 by r70, which fits the four central 48-gem pairs next to the central altar (35,34). Our only events are +48 at r170 and r185. Old v4 vs ming on corners also stays at 0 until r210. Collect is the alternative, but our bot tributes 24s there from r35; expanse is ruled out by its fixed r40 opening. |

Map-ID scores (forensics.py `mapid`: 2·prefix + 3·oursOK + 3·theirOK + 2·set + 6·exact1 − Δfirst/50):
069a8cb7 corners 12.9 > expanse 10.9 > collect 10.8; 1ab06080 packs 13.8 > corners 12.8 > expanse 12.3 (a single
shared +48 inflates corners; exact1, the share of events equal to one whole group, is 1.00 for packs and 0.48 for
corners); 2be0e2c1 interlock 14.3 > collect 12.1; 51e36018 lanes 28.3 > collect 12.8; e8446c17 expanse 49.9 >
corners 15.6.

**Platform build:** v4's bot.cpp is byte-identical to v3's. v4 differs only in the draft (Stellar before Tavi),
and the exact expanse match (3 picks: Ryth, Cassi&Issac, Stellar) confirms v4.

## 2. Bank sizes, stolen gems and parallel tributes (Q1)

Camp yields per map, whole group: corners 22/36/48/72/96; packs 44/48; interlock 22/36/72; lanes 22/24/36;
expanse 22/36/44/48/108.

| match / map | their events | single whole group | median | mean | events made of 2+ groups | odd amounts |
|---|---|---|---|---|---|---|
| 069a8cb7 corners | 20 | 19 (95%) | 48 | 48.4 | 1 (84 = 48+36) | none |
| 1ab06080 packs | 21 | 21 (100%) | 48 | 46.1 | 0 | none |
| 2be0e2c1 interlock | 19 | 12 (63%) | 44 | 50.7 | 7 (44, 94×4, 58×2) | none |
| 51e36018 lanes | 20 | 13 (65%) | 24 | 49.4 | 7 (48, 108×2, 84, 72, 58, 188) | **+188 at r330** (not a sum of ≤4 groups) |
| e8446c17 expanse | 16 | 10 (63%) | 48 | 60.8 | 6 (96, 92×2, 106, 70, 140) | none |

- **Banking threshold:** one capture per trip. On corners and packs every bag is one group: 48 for the central
  gem pairs at corners (1 tile from the central altar), 44 or 48 on packs. On the two big maps (lanes 90×30,
  expanse 80×80) about a third of the events are 2-3 captures (92-140), which suggests a bag of about 2 captures
  when the altar is far away. The +188 on lanes (800 to 988, with 1000 needed) at r330, after +108 at r315,
  looks like several champions arriving together for a final deposit.
- **Parallel tributes:** at most 2-3 champions tribute in the same window. On packs (3 picks) it never happens
  in 21 events. With mean gaps of 14.5-23.6 rounds between events, its champions bank on staggered cycles rather
  than as a group.
- **Stolen gems:** no evidence. Our bags (24, 44, 48, 72) look the same as camp yields, so a coincidence test is
  the only option. No gain of theirs comes with a drop in our progress: on lanes and expanse we kept tributing
  inside ±10 rounds of every large gain. The capacity checks below fully explain their totals by farming. On packs
  and interlock, stealing cannot be ruled out, because a stolen 44/48/72 looks exactly like a capture.

## 3. Timing and pace (Q2)

| match | map | side | 1st trib | 0-100 | 100-200 | 200-300 | 300-end | end | total | gems/round from 1st | events | mean gap | gap CV | r@500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 069a8cb7 | corners | top | 50 | 214 | 94 | 372 | 288 | 400 | 968 | 2.73 | 20 | 17.6 | 0.81 | 235 |
| 069a8cb7 | corners | us | 170 | 0 | 96 | 0 | 0 | 400 | 96 | 0.41 | 2 | | | - |
| 1ab06080 | packs | top | 35 | 136 | 232 | 136 | 464 | 475 | 968 | 2.18 | 21 | 22.0 | 0.51 | 275 |
| 1ab06080 | packs | us | 50 | 48 | 44 | 44 | 44 | 475 | 180 | 0.42 | 4 | 95.0 | 0.60 | - |
| 2be0e2c1 | interlock | top | 35 | 66 | 188 | 268 | 442 | 470 | 964 | 2.19 | 19 | 23.6 | 0.85 | 295 |
| 2be0e2c1 | interlock | us | 45 | 166 | 144 | 36 | 0 | 470 | 346 | 0.80 | 6 | 43.0 | 0.58 | - |
| 51e36018 | lanes | top | 55 | 96 | 396 | 176 | 320 | 335 | 988 | 3.47 | 20 | 14.5 | 0.77 | 205 |
| 51e36018 | lanes | us | 50 | 120 | 228 | 216 | 84 | 335 | 648 | 2.23 | 25 | 11.7 | 0.34 | 270 |
| e8446c17 | expanse | top | 75 | 210 | 188 | 316 | 258 | 375 | 972 | 3.19 | 16 | 18.7 | 0.53 | 225 |
| e8446c17 | expanse | us | 40 | 192 | 118 | 238 | 190 | 375 | 738 | 2.17 | 19 | 18.6 | 0.58 | 265 |

(The 300-end column covers different lengths: the games end at r335-r475.)

- **First tribute:** r35-r75 for them, r40-r50 for us (r170 on corners). The race is not lost in the opening.
  At r100 we led on interlock (166 to 66) and lanes (120 to 96, a +24 lead), and we were close on expanse
  (192 to 210).
- **Pace:** from r100 on, the top player sustains 2.2-3.9 gems per round. The steady-state stretches are
  "factory-like": a stream of single-group events, mean gap 14-24 rounds, CV 0.5-0.85. The pace rises over the
  game (interlock 66 / 188 / 268 / 442 per 100 rounds), which suggests item scaling or more camps coming under
  its control. There is one lull: corners r70-r215, only 94 gems, while both teams fought over the center. Our 96
  arrived inside that window.
- **Finish (1000):** about r340 (lanes), r380 (expanse), r405 (corners), r475 (interlock), r480 (packs).
  - Current tungtungsahur **vs starter-cpp** (no opposition; run6 A/B): lanes 435/430, expanse 465/480, packs
    530/540, interlock 445/455, corners 360/410. Even uncontested, we are 50-125 rounds slower on 3 of these 5
    maps.
  - Simulator (`analysis/plan_results.txt`, half map, no enemy): "all-solo" plan lanes 358, expanse 381,
    corners 372, interlock 478. These match the top player within about 0-35 rounds. The "tts-like" plan
    (2 squads, bank every capture, Chebyshev choice) gives 506 / 403 / 414 / 540.

## 4. How it suppressed us (Q3)

### Corners (069a8cb7): center denial plus our leaders looping on camps they cannot clear

- Platform: their 214 by r70 is 22 + 48 + 96 + 48 = one wolf + four 48-gem pairs. The central groups (34,32),
  (36,32), (34,36), (36,36) are 19-21 steps from either spawn and 1 tile from the central altar (35,34)
  (map_layout.py corners).
- From r215 to r385 they made 12 single +48 tributes and one +84 (48+36): 13 pair captures in 170 rounds. One
  group cycles in about 55-60 rounds (respawn 50 + kill + 5-round capture), so 2 groups give about 6 captures in
  that span. **13 captures need all 4 central groups.** Their 3.9 gems per round in that stretch equals the
  4-group capacity of 4×48/50 = 3.84.
- Our side, from the diagnostic replays (`fx-v4diag-vs-ming_bot-corners`, ming also grabs the center: 24/48/48/48
  by r70):
  - Ryth's squad targets (45,59), the enemy-side elk+gem group (5300 hp, 120 damage per turn incoming, 24 steps
    from B and 32 from us), on every status line from r30 to r210.
  - Issac's squad targets (25,59), a group of the same type. Neither group is ever captured.
  - The solo back-liners go to the center, meet 3-6 enemies, and die: Cassi&Issac at r77, Stellar at r101.
  - 1 capture by r200, first tribute r210.
  - Against opp-tts-locker: 8 deaths by r200, first tribute r290, game lost 792-912.
- **The current bot is the same.** `fx-diag-vs-ming_bot-corners` (run3) has 0 gems at r200 and a first tribute
  at r210. Ryth targets (45,59) on 26 of 30 status lines and Issac (25,59) on 24 of 30 up to r300. Even against
  starter-cpp, Ryth targets (45,59) on 28 of 30 lines. All the gems come from the center and back-liners.
- Gems lost on death were small (48 vs ming on corners). The loss is missing captures, not stolen bags.

### Interlock (2be0e2c1): lost the camp after r185, then the double-lock paralysis

- **r0-r185, we led** 310 to 254: 4 captures of our 72-gem cluster at (10,18).
- **After r185** we never captured a 72 again. They made 7 captures worth 72 between r160 and r450 (+72 or +94).
  One such cluster cycles in about 60-65 rounds, so their own cluster supplies at most about 5. They took ours
  at least twice. We gained only +36 at r260 between r185 and r400.
- **r403-r470:** 241 lines of "engine error 42: Target must be a visible enemy or neutral camp", up to 20 per
  5 rounds, so 4 bodies failed every turn.
  - Cause: the bot places its own locks on contested altars (bot.cpp:664-680, `place_lock`). The top player
    then locked the same altar.
  - `bank()` sees `enemy_locks.is_set(altar)` and calls `attack_lock(cambc::vision::altar_lock_at(altar))`
    (bot.cpp:951 / :977).
  - The SDK says *"Prefer the allied lock if both teams have a lock on this altar"* (sdk/cpp/cambc.h:4706). We
    attack our own lock, which fails every turn, and the enemy lock stays.
  - Every champion that has to bank walks to that altar and freezes there while holding its gems.
- **Reproduced locally (earlier run3, fx-diag vs fx-dbllock; fx-dbllock places locks onto altars the enemy has
  locked):**
  - collision: r2000, 706-198, 7,002 failed lock attacks, 3,504 "LOCKED lock_at_is_ally=1" lines.
  - monolith: 1,192 failed lock attacks.
- **Still in the current bot** (lockfix batch):
  - current tts vs fx-dbllock: collision A r2000, 706, 7,002 errors; monolith A 1,192 errors; interlock B
    r2000, 786-514, 4,537 errors; monolith B 2,438 errors.
- **Fix verified:** `bots/fx-lockfix` looks up the enemy lock with `cambc::vision::altar_locks(team::enemy)`.
  - **0 errors in all 6 games.**
  - collision A wins at r1120 with 998 (was r2000 and 706).
  - monolith B wins at r715 (was r990).
  - interlock B wins at r1015 with 930 (was r2000 and 786).
  - Win count 3/6 against 4/6 for the current bot, because the mirror opponent fx-dbllock itself has the bug and
    froze less once we stopped feeding it double locks. Against the top player, which does not freeze, only our
    own freeze matters.

### Packs (1ab06080): both central groups and our wolves lost

- They captured the central 48-gem groups (2 gem clusters + 2 gold clusters) 11 times. One group cycles in
  about 65 rounds, so one group allows about 6, and **they took both**. We got one, at r50.
- We tributed 3 times in 425 rounds (r115, r290, r335, all +44). Our 2-wolf groups at (8,2), (16,2) and (24,3)
  are 6/14/22 steps from our spawn. Locally the old bot captured 8-13 times by r200 (v4diag vs ming and Faisal),
  so on the platform our champions were dead, zoned or fighting most of the game.
- One "Champion cannot act" at r310 means a champion was crowd-controlled during its turn, so the top player
  brings stuns.
- The SCORE trace cannot separate kills (a stolen bag looks like 44/48) from zoning.

### Lanes (51e36018) and expanse (e8446c17): no suppression, just a faster farm

- **Expanse:** our 19 events equal the starter-cpp game, so the top player never touched our champions, camps or
  altars. It won 972 to 738 by r375 through economy alone.
- **Lanes:**
  - Our solo gem farmer delivered the same 24-gem stream as against starter-cpp, about every 10-15 rounds.
  - The squads' elk captures (+36 at r180/r255/r265 vs starter-cpp) are missing. Our first 36 came at r325, so
    the squads were zoned out of the middle (elk at x=39).
  - At r335 we had 648, against 768 in the starter game.

### Hypotheses checked

| hypothesis | verdict |
|---|---|
| They kill our champions repeatedly and steal bags | **Weak.** No odd-valued or coincident gains. Local deaths cost 0-144 gems per game. Possible on packs, but not provable. |
| They take camps near our spawn or our side | **Yes, on contested central gem groups:** corners (4 of 4 central pairs), packs (both central groups), interlock (our 72-gem cluster after r185). Not on big maps. |
| They lock our altar | **Yes, at least once** (interlock). Interacting with our own lock, it froze our whole team (the bug above). |
| Our old bot was buggy | **Yes in the logged build:** the double-lock freeze is fixed in current source; the corners leader loop is not reproduced by the latest main replay (258–308 gems at r200), though the bot still went 1/2 on corners vs ming_bot. |
| They simply farm faster | **Yes, on all 5 maps.** This alone decides lanes and expanse. |

## 5. Is ming_bot a reasonable proxy? (Q5)

ming's tributed total in our SCORE traces (forensics.py `ming`), compared with the top player:

| map | ming @300 (range over 3-4 games) | ming r@500 | top player @300 | top r@500 | proxy? |
|---|---|---|---|---|---|
| corners | 428-686 | 240-365 (one game never) | 680 | 235 | **yes** (ming vs v2: 686 / 874 at r300 / r400) |
| expanse | 432-502 | 270-380 | 714 | 225 | no, top is about 1.5× faster |
| interlock | 72-224 | 600-725 | 522 | 295 | no |
| lanes | 288-526 | 275-380 | 668 | 205 | no |
| packs | 60-444 | 355 to never | 504 | 275 | no (ming vs v4: 128 gems in 745 rounds) |

ming beats us mainly through fights and locks, and its econ pace is ordinary. The top player beats us on pace.
Local evaluation should therefore add a race metric: rounds to 1000 against a passive opponent (zz-idle or
starter-cpp), with a target of about **r340 lanes, r380 expanse, r400 corners, r475 interlock, r480 packs.**
League win counts against ming or Faisal will not show whether we can beat the top player.

## 6. Inferred strategy of the top player, and weaknesses (Q6)

**Likely strategy:**

- Most champions farm on their own or in pairs. Each camp group gets one champion: the event stream is single
  groups, never 2-3 split shares (no 24s from 48-gem pairs, no 11/18/33).
- Bank after every capture at the nearest altar (bag about 44-48; about 2 captures on big maps).
- Greedy targeting of the highest gems-per-round groups, which puts gem clusters next to altars first.
- **Contest the central, symmetric gem groups** (corners center pairs, packs central groups, interlock gem
  clusters), taking the ones on our side as well.
- Uses altar locks and crowd control.
- Does not bother with us on big maps.
- Its end rounds match the econ simulator's "all-solo, bank-each-capture" plan within about 0-35 rounds on
  lanes, expanse and corners, so it plays close to the econ optimum for half the map.

**Weaknesses we can use:**

1. **Slow opening:** 66-214 gems by r100. We were ahead at r100 on interlock and lanes. A fast, safe start plus
   holding the shared center groups early would put it behind.
2. **Predictable tributes:** about 16-21 tributes per game of about 48 gems, at the altar nearest the farm
   (corners: always (35,34); packs and interlock: the central altars). A 48-gem tribute takes 5 turns. Our peel
   (stun) delays a tribute, and a kill steals 48+. A lock that we place first on *their* farm altar forces
   3 hits per lock, and each re-lock costs them a tribute restart.
3. **No harassment on big maps:** on lanes and expanse it lets us farm untouched. A faster farm alone wins there.
4. **The central groups are its main income on symmetric maps.** Denying even half of them (corners: 2 of 4
   pairs) cuts its rate there from about 3.9 to about 2 gems per round.

## 7. Recommendations (ranked by expected impact)

| # | change | where | evidence / expected impact | effort |
|---|---|---|---|---|
| 1 | **DONE: fix the double-lock freeze.** The main now selects the enemy lock by position rather than calling `altar_lock_at`. | `bots/tungtungsahur/src/bot.cpp`: `enemy_lock_at()` and the deposit path | The old build froze 4 bodies for the last 65 rounds of 2be0e2c1; the fix had 0 failures in all 6 `fx-lockfix` test games. Current-source match coverage against this exact double-lock setup should still be refreshed. | done |
| 2 | **Faster pure econ on big maps:** more solo farming (each body takes its own group, ideally a gem cluster next to an altar), bank each capture, and on lanes chain 2-3 adjacent 24-gem clusters per trip. Judge by rounds to 1000 against zz-idle or starter, not by league wins. Experiment #3 in PLAN.md rejected solo farming on a weak, fight-heavy league, which is the wrong metric for this opponent. | role logic in bot.cpp (squad leaders' `choose_camp`, `farm_nearby_cluster` radius / solo rule) | Top player lanes about r340 and expanse about r380, against our 430-480 uncontested. The simulator's all-solo plan reaches 358 / 381, and the tts-like plan 506 / 403. That is a 90-125 round gap, decisive on 2 of 5 platform maps. | medium |
| 3 | **Recheck target choice on corners and lanes** using current-source traces before changing the planner. | `choose_camp` and squad target selection | The old diagnostic showed leaders repeating an uncleareable target. Latest main corners games score 258–308 by r200 and finish 1/2 vs ming_bot, so the old no-capture behavior is gone; a side-specific loss remains. The old `fx-leaderfix` improved corners but regressed rows, elkring and packs. | medium |
| 4 | **Contest and hold central gem groups and their altar** on corners, packs and interlock with a full squad, not solo back-liners. Place our lock on the altar the opponent farms at (corners (35,34)). | squad target choice and `place_lock` (bot.cpp:664) | The top player's corners income was about 3.9 gems per round from the 4 central pairs. On packs it got the central groups 11 times to our 1, and on interlock it took our cluster after r185. Our solo back-liners died there (Cassi&Issac at r77, Stellar at r101 on corners vs ming). | medium-high |
| 5 | **Survive small maps (packs):** 3 picks on a 31×31 map, where we made 3 captures in 425 rounds. Keep the 3 bodies together, fight only with numbers, and retreat or bank before engaging. Treat a stun as a signal to disengage. | role and fight logic for 3-pick maps | Packs loss 180-968. Locally against ming and Faisal the same code captured 8-13 times by r200, so the top player's fighting is the difference. Needs a stronger sparring partner (opp-tts-aggro or locker) to test. | medium |
| 6 | **Exploit its tributes:** peel stuns already exist. Add a lock on the altar where an enemy is tributing, or will tribute, when we are next to it (experiment #24 had no effect against the league; the top player tributes about 20 times per game at predictable altars). | `peel()` / `place_lock()` | Small but cheap. Each successful cancellation costs it 5+ turns plus 3 lock hits. | low |
| 7 | **Evaluation:** add a "race" gate (rounds to 1000 against zz-idle per map) with the targets above, and a lock-heavy opponent (fx-dbllock or opp-tts-locker) to the league. | tools/league.py usage | ming and Faisal are not proxies on 4 of 5 maps (section 5). | low |

## Reproduce

```
python analysis/forensics.py                       # platform, mapid, local, decomp, pace, ming
python analysis/forensics.py v4diag                # fx-v4diag diagnostics
./cambc.exe build bots/fx-v4diag && ./cambc.exe run-batch matches/forensics/v4diag/manifest.txt --jobs 6 --color never
./cambc.exe build bots/fx-lockfix && ./cambc.exe run-batch matches/forensics/lockfix/manifest.txt --jobs 6 --color never
python analysis/map_layout.py corners packs interlock lanes expanse
```

New bots: `bots/fx-v4diag` (opp-tts-v4 plus a DIAG trace and the round in error lines) and `bots/fx-lockfix`
(the current tungtungsahur plus the enemy-lock lookup). bots/tungtungsahur was not modified.
